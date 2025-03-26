import pygame as pg
from math import cos, sin, pi, tan
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

def init():

    pg.init()
    pg.display.set_caption(cf.game_name)

    # screen initialisation
    if not cf.fullscreen:
        vr.window = pg.display.set_mode(vr.window_size)
    else:
        vr.window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        vr.window_size = vr.window.get_size()

    vr.clock = pg.time.Clock()

    vr.mask_background = pg.surface.Surface(vr.window_size)
    vr.mask_background.fill(cf.back_base_color)
    vr.mask_background.convert_alpha()

    vr.world_area_obj = Geobject((0, 0), ((cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.worldborder[1]), (cf.world_size[0] - cf.worldborder[0], cf.world_size[1] - cf.worldborder[1]), (cf.worldborder[0], cf.world_size[1] - cf.worldborder[1])))

    for name, animation in sync_animations_cycles:
        vr.animation_cycles[name]['t'] = vr.t
        vr.animation_cycles[name]['dt_threshold'] = animation['duration']
        vr.animation_cycles[name]['index'] = 0
        vr.animation_cycles[name]['max_index'] = len(animation['frames'])

    vr.player = Player()
    vr.map = Map()
    vr.map.load_map()

    sm.PlayMusic('ingame')

    return

def main():
    init()

    vr.running = True

    frames_fps, t_fps = 0, time.time() - 1

    while vr.running:

        vr.clock.tick(cf.fps)

        vr.t = time.time()
        frames_fps += 1
        vr.fps = frames_fps/(vr.t - t_fps)
        vr.dt_update = 1 / vr.fps if vr.fps != 0 else 0.1
        if frames_fps > 1000:
            frames_fps, t_fps = 0, time.time()

        vr.inputs['CLICK'] = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                vr.running = False
            elif event.type == pg.JOYDEVICEADDED:
                vr.controller = pg.joystick.Joystick(event.device_index)
                print(f"Joystick connected. (id : {vr.controller.get_instance_id()})")
            elif event.type == pg.MOUSEBUTTONDOWN:
                vr.inputs['CLICK'], vr.inputs['CLICK_PRESSED'] = True, True
                print("Cursor clicked at : ", pg.mouse.get_pos())
            elif event.type == pg.MOUSEBUTTONUP:
                vr.inputs['CLICK_PRESSED'] = False

        # Main Loop #
        u.getInputs()
        pre_update()
        if vr.fps > cf.fps * cf.fps_treshold:
            update()
        post_update()
        # --------- #

    return

def update():
    vr.cursor = pg.mouse.get_pos()
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
        if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(cursor_world_coord) and obj.get_size() == (me.size_selected, me.size_selected):
            me.editor_selected_obj = obj

    for obj in vr.map.creatures:
        if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
            obj.update()
            obj.draw()
            if t.distance(obj.world_anchor, cursor_world_coord) < obj.radius and obj.intersect(cursor_world_coord) and obj.get_size() == (me.size_selected, me.size_selected):
                me.editor_selected_obj = obj

    vr.player.update()
    vr.player.draw()

    if cf.editor_mode:
        editor_update()
        editor_draw()

    test_at_update()
    return

def test_at_update():
    return

def pre_update():
    if vr.inputs['R']:
        vr.map.reload_map()
        vr.player.__init__()
        time.sleep(0.1)
        print("Map Reloaded.")

    u.blur_background()
    u.draw_worldborder()
    pg.draw.line(vr.window, 'black', u.adapt_to_view((0, cf.world_size[1] - cf.worldborder[1])), u.adapt_to_view((cf.world_size[0], cf.world_size[1] - cf.worldborder[1])), 20)
    return

def post_update():
    u.Text("fps : " + str(round(vr.fps, 1)), (10, vr.win_height - 24), 14, 'orange')
    u.Text("info : " + str(vr.info_txt), (10, vr.win_height - 48), 14, 'orange')
    pg.display.update()
    return

if __name__ == "__main__":
    main()
