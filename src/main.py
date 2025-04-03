import torch.nn.init
import torch.onnx.symbolic_opset9

from game_manager import *
from visuals import img
from utils import path

def init():

    pg.init()
    pg.display.set_caption(cf.game_name)
    pg.display.set_icon(img(path('rsc/misc/logo.png'), full_path=True))

    # Game surface initialisation
    vr.game_window = pg.Surface(cf.view_size)

    # screen initialisation
    if not cf.fullscreen:
        vr.displayed_window = pg.display.set_mode(vr.window_size)
    else:
        vr.displayed_window = pg.display.set_mode(vr.window_size, pg.RESIZABLE)

    vr.clock = pg.time.Clock()

    vr.mask_background = pg.surface.Surface(vr.window_size)
    vr.mask_background.fill(cf.back_base_color)
    vr.mask_background.convert_alpha()

    for name, animation in sync_animations_cycles:
        vr.animation_cycles[name]['t'] = vr.t
        vr.animation_cycles[name]['dt_threshold'] = animation['duration']
        vr.animation_cycles[name]['index'] = 0
        vr.animation_cycles[name]['max_index'] = len(animation['frames'])

    vr.app = Menu()
    vr.apps['main'] = vr.app

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

    vr.apps['main'].update()
    for app in vr.apps['others']:
        app.update()

    test_at_update()
    return
def test_at_update():
    return

def pre_update():
    vr.apps['main'].pre_update()

    apps_ended = []
    for app in vr.apps['others']:
        app.pre_update()
        if app.ended():
            apps_ended.append(app)

    for app_ended in apps_ended:
        vr.apps['others'].remove(app_ended)

    return

def post_update():
    vr.apps['main'].post_update()
    for app in vr.apps['others']:
        app.post_update()

    vr.displayed_window.blit(pg.transform.scale(vr.game_window, vr.displayed_window.get_size()), (0, 0))
    pg.display.update()
    return

if __name__ == "__main__":
    main()
