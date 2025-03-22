import pygame as pg
from math import cos, sin, pi, tan
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from player import Player
from geometry import Geobject

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

    return

def main():
    init()

    # TEST
    vr.player = Player()
    vr.geobjects.append(Geobject())
    # END TEST

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

        for event in pg.event.get():
            if event.type == pg.QUIT:
                vr.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                print("Cursor : ", pg.mouse.get_pos())

        # Main Loop #
        pre_update()
        if vr.fps > cf.fps * cf.fps_treshold:
            u.getInputs()
            update()
        post_update()
        # --------- #

    return

def update():
    vr.cursor = pg.mouse.get_pos()

    test_update()

    u.draw_worldborder()
    return

def test_update():

    for obj in vr.geobjects:
        if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
            obj.update()
            obj.draw()

    max_acc = u.distance_to_acc_per_updt(10)
    jump_speed = u.distance_to_speed_per_updt(5)
    if vr.inputs['RIGHT']:
        vr.player_power_acc = max(min(max_acc, vr.player_power_acc + 50), 4000)
        vr.player.acc[0] = min(max_acc, vr.player_power_acc) if vr.player.speed[1] == 0. else min(vr.player_power_acc * 0.4, max_acc)
    elif vr.inputs['LEFT']:
        vr.player_power_acc = max(min(max_acc, vr.player_power_acc + 50), 4000)
        vr.player.acc[0] += -1 * min(max_acc, vr.player_power_acc) if vr.player.speed[1] == 0. else -1 * min(vr.player_power_acc * 0.4, max_acc)
    else:
        vr.player_power_acc = 0

    if vr.inputs['DOWN']:
        vr.player.acc[1] += max_acc
    elif vr.inputs['UP'] and vr.player.speed[1] == 0.:
        vr.player.speed[1] += - 8 * jump_speed

    vr.info_txt = vr.player.acc

    vr.player.update()
    vr.player.draw()

    return

def pre_update():
    vr.window.fill((50, 20, 30))
    return

def post_update():
    u.Text("fps : " + str(round(vr.fps, 1)), (10, vr.win_height - 24), 14, 'orange')
    u.Text("info : " + str(vr.info_txt), (10, vr.win_height - 48), 14, 'orange')
    pg.display.update()
    return

if __name__ == "__main__":
    main()
