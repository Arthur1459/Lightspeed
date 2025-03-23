import vars as vr
import config as cf
import tools as t
import utils as u
import geometry as geo
import maps
import pygame as pg

click_minimal_duration = 0.1
wait_key = vr.t

toggle_block = False
toggle_grid_magnet = True

target_anchor = vr.cursor
editor_selected_obj = None

def editor_update():
    global toggle_block, toggle_grid_magnet, target_anchor

    if toggle_grid_magnet:
        x, y = t.Vadd(vr.camera_coord, vr.cursor)
        target_anchor = (x // cf.block_default_size) * cf.block_default_size, (y // cf.block_default_size) * cf.block_default_size

    if vr.inputs['B'] and wait_for_key():
        toggle_block = False if toggle_block else True

    if toggle_block and vr.inputs['CLICK'] and wait_for_key():
        if editor_selected_obj is not None:
            vr.map.remove(editor_selected_obj)
        else:
            anchor = target_anchor if toggle_grid_magnet else t.Vadd(vr.camera_coord, t.Vcl(1, vr.cursor, -0.5, (cf.block_default_size, cf.block_default_size)))
            vr.map.add_block(anchor, (cf.block_default_size, cf.block_default_size), update=True)

    if vr.inputs['S'] and wait_for_key():
        vr.map.save_map()
        print("Map Saved.")

    return

def editor_draw():
    global toggle_block

    if editor_selected_obj is not None:
        coord = u.adapt_to_view(editor_selected_obj.world_anchor)
        pg.draw.rect(vr.window, 'yellow', (coord[0], coord[1], editor_selected_obj.sizex(), editor_selected_obj.sizey()), 3)

    if toggle_block:
        topleft = u.adapt_to_view(target_anchor) if toggle_grid_magnet else t.Vcl(1, vr.cursor, -0.5, (cf.block_default_size, cf.block_default_size))
        pg.draw.rect(vr.window, 'red', (topleft[0], topleft[1], cf.block_default_size, cf.block_default_size), 2)

    return

def wait_for_key(dt=click_minimal_duration, reset=True):
    global wait_key
    if vr.t - wait_key > dt:
        if reset:
            wait_key = vr.t
        return True
    else:
        return False

def reset_key():
    global wait_key
    wait_key = vr.t
