import pygame as pg
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from player import Player
from geometry import Block, Geobject
from maps import Map
from map_editor import editor_update, editor_draw
import map_editor as me
from visuals import sync_animations_cycles
import SoundsManagement as sm
from visuals import img, load_folder

class App:
    def __init__(self):
        self.name = 'default'

    def update(self):
        vr.info_txt = f'App : {self.name}'

    def pre_update(self):
        vr.game_window.fill('black')

    def post_update(self):
        u.Text("fps : " + str(round(vr.fps, 1)), (10, vr.win_height - 18), 12, 'orange')
        u.Text("info : " + str(vr.info_txt), (10, vr.win_height - 48), 14, 'orange')

    def ended(self):
        return False

class Transition(App):
    def __init__(self, app, duration=0.5):
        super().__init__()
        self.name = 'Transition'

        self.t_start = vr.t
        self.duration = duration

        self.half_nb_frames = cf.fps * self.duration // 2
        self.frames_counter = 0
        self.state = 'rising'

        self.mask = pg.Surface(vr.window_size, masks='black')
        self.mask.convert_alpha()

        vr.in_transition = True
        vr.transition = self
        vr.apps['others'].append(self)
        self.next_app = app

    def update(self):
        if self.state != 'ended':

            if self.state == 'rising':
                self.frames_counter += 1
            elif self.state == 'falling':
                self.frames_counter += -1

            if self.frames_counter >= self.half_nb_frames and self.state == 'rising': self.state = 'falling'
            elif self.frames_counter <= 0 and self.state == 'falling': self.state = 'rising'

            if self.middle():
                vr.apps['main'] = self.next_app
                vr.apps['main'].pre_update()

            self.mask.set_alpha(200 * self.frames_counter / self.half_nb_frames)
            vr.game_window.blit(self.mask, (0, 0))

    def pre_update(self):
        if vr.t - self.t_start > self.duration:
            self.state = 'ended'
            vr.in_transition = False

    def post_update(self):
        pass

    def ended(self):
        return self.state == 'ended'
    def middle(self):
        return self.frames_counter == self.half_nb_frames

class Game(App):
    def __init__(self):
        super().__init__()
        self.name = 'Game'

        vr.world_area_obj = Geobject((0, 0), ((cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.world_size[1] - cf.worldborder[1]), (cf.worldborder[0], cf.world_size[1] - cf.worldborder[1])))

        vr.player = Player()
        vr.map = Map()
        vr.map.load_map()

        sm.PlayMusic('ingame')

    def update(self):
        cursor_world_coord = t.Vadd(vr.cursor, vr.camera_coord)

        vr.map.update()

        for ambient_obj in vr.map.ambient_elts:
            ambient_obj.draw()
            if not ambient_obj.alive: vr.map.old_ambient_elts.append(ambient_obj)

        me.editor_selected_obj = None
        for obj in vr.map.geobjects:
            if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
                obj.update()
                obj.draw()
            if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(
                    cursor_world_coord) and obj.get_size() == (me.size_selected, me.size_selected):
                me.editor_selected_obj = obj

        for obj in vr.map.creatures:
            if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
                obj.update()
                obj.draw()
                if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(
                        cursor_world_coord) and obj.get_size() == (me.size_selected, me.size_selected):
                    me.editor_selected_obj = obj

        vr.player.update()
        vr.player.draw()

        if cf.editor_mode:
            editor_update()
            editor_draw()
        if vr.inputs['E'] and me.wait_for_key(): cf.editor_mode = False if cf.editor_mode else True

    def pre_update(self):
        if vr.inputs['ESC']:
            Transition(Menu(), duration=0.5)
            return

        if vr.inputs['R']:
            vr.map.reload_map()
            vr.player.__init__()
            time.sleep(0.1)
            print("Map Reloaded.")

        u.blur_background()
        u.draw_worldborder()
        pg.draw.line(vr.game_window, 'black', u.adapt_to_view((0, cf.world_size[1] - cf.worldborder[1])),
                     u.adapt_to_view((cf.world_size[0], cf.world_size[1] - cf.worldborder[1])), 20)

    def post_update(self):
        u.Text("fps : " + str(round(vr.fps, 1)), (10, vr.win_height - 18), 12, 'orange')
        if cf.editor_mode: u.Text("info : " + str(vr.info_txt), (10, vr.win_height - 48), 14, 'orange')
        pg.display.update()

class Menu(App):
    def __init__(self):
        super().__init__()
        self.name = 'Menu'

        self.movie = VideoCapture(u.path('rsc/videos/background_menu.mp4'))
        self.movie_shape = self.movie.read()[1].shape[1::-1]

        self.title = img(u.path('rsc/misc/lightspeed_title.png'), resize=(vr.win_width * 0.8, vr.win_height * 0.25), full_path=True)

    def update(self):

        success, img = self.movie.read()
        if img is None:
            self.movie.set(CAP_PROP_POS_FRAMES, 0)
            success, img = self.movie.read()
        frame = pg.image.frombuffer(img.tobytes(), self.movie_shape, "BGR")
        frame = frame.convert_alpha()
        frame.set_alpha(100)

        vr.game_window.blit(pg.transform.scale(frame, vr.window_size), (0, 0))
        vr.game_window.blit(self.title, (vr.win_width * 0.12, vr.win_height * 0.13))
        u.Text('Arthur1459', (vr.win_width * 0.13 + vr.win_width * 0.75 * 0.37, vr.win_height * 0.13 + vr.win_height * 0.25 * 1.1), 48, 'white', font_type='robot')

        u.Text('[ PLAY SPACE ]', (vr.win_width * 0.25, vr.win_height * 0.75), 32, 'red', font_type='robot')
        u.Text('[ SETTINGS C ]', (vr.win_width * 0.6, vr.win_height * 0.75), 32, 'red', font_type='robot')

    def pre_update(self):
        if vr.inputs['SPACE']: Transition(Game(), duration=0.5)
        if vr.inputs['C']: Transition(Settings(), duration=0.5)
        if vr.inputs['ESC']: vr.running = False

    def post_update(self):
        pass

class Settings(App):
    def __init__(self):
        super().__init__()
        self.name = 'settings'

    def update(self):
        u.Text('Settings', (vr.win_width * 0.13, vr.win_height * 0.13), 48, 'white', font_type='robot')

    def pre_update(self):
        vr.game_window.fill('black')
        if vr.inputs['ESC']: Transition(Menu(), duration=0.5)

    def post_update(self):
        pass