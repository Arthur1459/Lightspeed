import pygame as pg
from math import cos, sin, pi, tan
import tools as t
import utils as u
import vars as vr
import config as cf
import time

from player import Player
from geometry import Block, Geobject

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

    return

def main():
    init()

    # TEST
    vr.player = Player()
    nx, ny = cf.world_size[0]//200, cf.world_size[1]//200
    for i in range(500):
        vr.geobjects.append(Block(anchori=(t.rndInt(1, nx - 1) * 200, t.rndInt(1, ny - 1) * 200), size=(200, 200)))
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
        u.getInputs()
        pre_update()
        if vr.fps > cf.fps * cf.fps_treshold:
            update()
        post_update()
        # --------- #

    return

def update():
    vr.cursor = pg.mouse.get_pos()

    for obj in vr.geobjects:
        if t.distance(obj.world_anchor, u.get_view_center_coord()) < obj.radius + vr.camera_radius:
            obj.update()
            obj.draw()

    vr.player.update()
    vr.player.draw()

    test_update()
    return

def test_update():

    return

def pre_update():
    speed_factor = t.norm(vr.player.speed)/1000
    color = cf.back_base_color[:]
    color[0] = min(250, cf.back_base_color[0] * max(0.5, speed_factor))
    vr.mask_background.fill(color)
    vr.mask_background.set_alpha(max(cf.max_blur, min(255, int(255 * (1 - speed_factor)))))
    vr.window.blit(vr.mask_background, (0, 0))

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
