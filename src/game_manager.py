import pygame as pg
from cv2 import VideoCapture, CAP_PROP_POS_FRAMES
import tools as t
import utils as u
import vars as vr
import config as cf
import sound_config as scf
import time
from glob import glob

from player import Player
from geometry import Block, Geobject
from maps import Map, Particle
from map_editor import editor_update, editor_draw
import map_editor as me
import SoundsManagement as sm
from visuals import img, load_folder
import gui

class App:
    def __init__(self):
        self.name = 'default'

    def update(self):
        pass

    def pre_update(self):
        pass

    def post_update(self):
        pass

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

class Gui(App):
    def __init__(self):
        super().__init__()
        self.name = 'gui'
        self.gui_elements = {'fps': gui.Displayer((vr.win_width * 0.023, vr.win_height * 0.985), (75, 15), round(vr.fps, 1), shiftx=0.2, shifty=0.08, text_size=12)}

    def update(self):
        if cf.show_fps: self.gui_elements['fps'].update(vr.fps, rounding=1, unit='fps')

    def post_update(self):
        if cf.show_fps: self.gui_elements['fps'].draw()

class Game(App):
    def __init__(self, level=None):
        super().__init__()
        self.name = 'Game'
        self.level = level if level is not None else 'Playground'
        self.level_completed = False

        vr.world_area_obj = Geobject((0, 0), ((cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.world_size[1] - cf.worldborder[1]), (cf.worldborder[0], cf.world_size[1] - cf.worldborder[1])))

        vr.player = Player()
        vr.map = Map()
        vr.map.load_map(name=self.level)

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
                if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(cursor_world_coord) and obj.get_type() in me.types_classification[me.current_targeted_type]:
                    me.editor_selected_obj = obj

        for obj in vr.map.creatures:
            if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
                obj.update()
                obj.draw()
                if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(cursor_world_coord) and obj.get_type() in me.types_classification[me.current_targeted_type]:
                    me.editor_selected_obj = obj

        vr.map.draw_misc()

        if not self.level_completed:
            if vr.map.completed:
                sm.PlayEffect('level_completed')
                Transition(LevelSelection())
                self.level_completed = True
        else:
            vr.player.draw()
            return

        vr.player.update()
        vr.player.draw()

        editor_update()
        if me.toggle_editor:
            editor_draw()

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
        if me.toggle_editor: u.draw_worldborder()

    def post_update(self):
        pg.display.update()

class Menu(App):
    def __init__(self):
        super().__init__()
        self.name = 'Menu'

        self.movie = VideoCapture(u.path('rsc/videos/background_menu.mp4'))
        self.movie_shape = self.movie.read()[1].shape[1::-1]

        self.title = img(u.path('rsc/misc/lightspeed_title.png'), resize=(vr.win_width * 0.8, vr.win_height * 0.25), full_path=True)

        self.gui_elements = {'quit': gui.PressButton((vr.win_width * 0.028, vr.win_height * 0.025), (60, 25), 'Quit', text_size=16, shiftx=0.22, shifty=0.12, callback=self.quit_callback, font='robot'),
                             'play': gui.PressButton((vr.win_width * 0.5, vr.win_height * 0.5), (250, 85), '[ PLAY ]', text_size=56, shiftx=0.14, shifty=0.15, callback=self.play_callback, transparent=True, framed=True, font='robot', color='red'),
                             'settings': gui.PressButton((vr.win_width * 0.5, vr.win_height * 0.65), (200, 50), '[ SETTINGS ]', text_size=32, shiftx=0.1, shifty=0.15, callback=self.settings_callback, transparent=True, framed=True, font='robot', color='red')}

        sm.PlayMusic('menu')
        sm.PlayEffect('back_menu')

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
        u.Text('By Arthur1459', (vr.win_width * 0.44, vr.win_height * 0.95), 24, 'white', font_type='robot')

        #u.Text('[ PLAY SPACE ]', (vr.win_width * 0.25, vr.win_height * 0.75), 32, 'red', font_type='robot')
        #u.Text('[ SETTINGS C ]', (vr.win_width * 0.6, vr.win_height * 0.75), 32, 'red', font_type='robot')

        for elt_name in self.gui_elements:
            self.gui_elements[elt_name].update()
            self.gui_elements[elt_name].draw()

    def pre_update(self):
        vr.game_window.fill('black')
        if vr.inputs['SPACE']: self.play_callback()
        if vr.inputs['C']: self.settings_callback()
        if vr.inputs['ESC']: self.quit_callback()

    def post_update(self):
        pass

    def play_callback(self, *args):
        Transition(LevelSelection(worlds=(1, 4)), duration=0.5)
    def settings_callback(self, *args):
        Transition(Settings(), duration=0.5)
    def quit_callback(self, *args):
        print("\n##### Game Stopped #####\n")
        vr.running = False

class Settings(App):
    def __init__(self):
        super().__init__()
        self.name = 'settings'

        self.gui_elements = {'menu': gui.PressButton((vr.win_width * 0.045, vr.win_height * 0.03), (100, 30), 'menu', shiftx=0.25, shifty=0.15, callback=self.back_callback),
                             'toggle_fps': gui.SwitchButton((vr.win_width * 0.25, vr.win_height * 0.3), (40, 40), 'Show FPS', switch_on=cf.show_fps, text_size=24, shiftx=1.3, shifty=0.15, callback=self.fps_callback),
                             'editor_mode': gui.SwitchButton((vr.win_width * 0.25, vr.win_height * 0.4), (40, 40), 'Editor Mode', switch_on=me.toggle_editor, text_size=24, shiftx=1.3, shifty=0.15, callback=self.editor_callback),
                             'fly_mode': gui.SwitchButton((vr.win_width * 0.25, vr.win_height * 0.5), (40, 40), 'Fly Mode', switch_on=vr.fly_mode, text_size=24, shiftx=1.3, shifty=0.15, callback=self.fly_callback),
                             'toggle_music': gui.SwitchButton((vr.win_width * 0.5, vr.win_height * 0.3), (40, 40), 'Music', switch_on=scf.sound_musics_mode, text_size=24, shiftx=1.3, shifty=0.15, callback=self.music_callback),
                             'music_volume': gui.SlidingValue((vr.win_width * 0.5, vr.win_height * 0.4), (40, 40), value=scf.music_volume, val_unit="%", value_size=14, val_shiftx=0.13, val_shifty=0.3, msg='Volume Music', text_size=24, shiftx=1.3, shifty=0.15, callback=self.music_volume_callback),
                             'toggle_sfx': gui.SwitchButton((vr.win_width * 0.5, vr.win_height * 0.5), (40, 40), 'Sound Effects', switch_on=scf.sound_effects_mode,  text_size=24, shiftx=1.3, shifty=0.15, callback=self.sfx_callback),
                             'sfx_volume': gui.SlidingValue((vr.win_width * 0.5, vr.win_height * 0.6), (40, 40), value=scf.sfx_volume, val_unit="%", value_size=14, val_shiftx=0.13, val_shifty=0.3, msg='SFX Music', text_size=24, shiftx=1.3, shifty=0.15, callback=self.sfx_volume_callback)
                             }

    def update(self):

        for elt_name in self.gui_elements:
            self.gui_elements[elt_name].update()
            self.gui_elements[elt_name].draw()

        u.Text('Settings', (vr.win_width * 0.13, vr.win_height * 0.13), 48, 'white', font_type='robot')

    def pre_update(self):
        vr.game_window.fill('black')
        if vr.inputs['ESC']: Transition(Menu(), duration=0.5)

    def back_callback(self, *args):
        Transition(Menu(), duration=0.5)
    def fps_callback(self, button_state):
        cf.show_fps = button_state
    def music_callback(self, button_state):
        scf.sound_musics_mode = button_state
        if scf.sound_musics_mode:
            sm.PlayMusic(sm.current_playlist)
        else:
            sm.StopMusic()
    def sfx_callback(self, button_state):
        scf.sound_effects_mode = button_state
    def editor_callback(self, button_state):
        me.toggle_editor = button_state
    def fly_callback(self, button_state):
        u.toggle_fly_mode(set_on=button_state)
    def music_volume_callback(self, volume):
        scf.music_volume = volume
        sm.updateVolume(scf.music_volume)
    def sfx_volume_callback(self, volume):
        scf.sfx_volume = volume

    def post_update(self):
        pass

class LevelSelection(App):
    def __init__(self, worlds=(1, 4)):
        super().__init__()
        self.name = 'level selection'

        self.gui_elements = {'menu': gui.PressButton((vr.win_width * 0.045, vr.win_height * 0.03), (100, 30), 'menu', shiftx=0.25, shifty=0.15, callback=self.back_callback),
                             'Playground': gui.PressButton((vr.win_width * 0.81, vr.win_height * 0.155), (200, 45), 'Playground', text_size=30, font='robot', transparent=True, framed=True, shiftx=0.1, shifty=0.17, callback=self.play_callback, callback_args=('Playground',))}

        self.levels = self.init_levels_list(worlds)

        self.ambient_elts = []
        self.old_ambient_elts = []

        sm.PlayMusic('menu')

        self.mask = pg.Surface(vr.game_window.get_size(), masks='black').convert_alpha()
        self.mask.set_alpha(50)

    def update(self):
        if vr.inputs['ESC']: Transition(Menu(), duration=0.5)

        for elt_name in self.gui_elements:
            self.gui_elements[elt_name].update()
            self.gui_elements[elt_name].draw()

        u.Text('Levels', (vr.win_width * 0.12, vr.win_height * 0.12), 48, 'white', font_type='robot')

        for world_num in self.levels:
            u.Text(f'World {world_num}', (vr.win_width * 0.152 + (world_num - 1) * vr.win_width * 0.18, vr.win_height * 0.22), 48, 'white', font_type='robot')

    def pre_update(self):
        vr.game_window.blit(self.mask, (0, 0))
        self.update_and_draw_particle()
        pg.draw.rect(vr.game_window, (110, 110, 110), (vr.win_width * 0.1, vr.win_height * 0.1, vr.win_width * 0.8, vr.win_height * 0.8), 10)
        pg.draw.line(vr.game_window, (110, 110, 110), (vr.win_width * 0.102, vr.win_height * 0.2), (vr.win_width * 0.898, vr.win_height * 0.2), 10)

        return

    def post_update(self):
        return

    def init_levels_list(self, worlds):
        button_width, button_height = vr.win_width * 0.18, vr.win_height * 0.08

        levels = {world_num: [levelpath.split('rsc/maps/')[1].replace('.pkl', '') for levelpath in sorted(glob(u.path(f"rsc/maps/world_{world_num}/*.pkl")))] for world_num in range(worlds[0], worlds[1]+1)}

        for world in levels:
            for l, level_path in enumerate(levels[world]):
                self.gui_elements[f"W{world}L{l+1}"] = gui.PressButton((vr.win_width * 0.215 + (world - 1) * button_width, vr.win_height * 0.34 + l * button_height), (200, 45), f'level {l+1}', text_size=30, font='robot',
                                                                       transparent=True, framed=True, shiftx=0.1, shifty=0.17, callback=self.play_callback, callback_args=(level_path,))
        return levels

    def update_and_draw_particle(self):
        for ambient_elt in self.old_ambient_elts:
            if ambient_elt in self.ambient_elts: self.ambient_elts.remove(ambient_elt)
        self.old_ambient_elts = []

        void_particle_max_speed = u.distance_to_speed_per_updt(0.2)
        rnd_anchor = t.Vadd(vr.camera_coord, (t.rndInt(0, vr.win_width), t.rndInt(0, vr.win_height)))
        self.ambient_elts.append(Particle('void', rnd_anchor, persistence=2., size=4, speed=(t.rndInt(-1 * void_particle_max_speed, 1 * void_particle_max_speed), t.rndInt(-1 * void_particle_max_speed, 1 * void_particle_max_speed))))

        for ambient_obj in self.ambient_elts:
            ambient_obj.draw()
            if not ambient_obj.alive: self.old_ambient_elts.append(ambient_obj)

    def play_callback(self, *args):
        level = args[0] if len(args) > 0 else 'default'
        Transition(Game(level=level), duration=0.5)
    def back_callback(self, *args):
        Transition(Menu(), duration=0.5)
