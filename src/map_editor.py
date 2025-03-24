import vars as vr
import config as cf
import tools as t
import utils as u
import geometry as geo
import maps
import pygame as pg

click_minimal_duration = 0.1
wait_key = vr.t

toggle_placement = False
blocks, blocks_index = ['block', 'spike'], 0
block_type_to_place = 'block'
medium_block_types = {'default', 'block'}
small_block_types = {'spike'}
large_block_types = set()
size_selected = cf.block_default_size

toggle_grid_magnet = True

target_anchor = vr.cursor
editor_selected_obj = None

def editor_update():
    global toggle_placement, toggle_grid_magnet
    global block_type_to_place, medium_block_types, small_block_types, large_block_types
    global target_anchor, editor_selected_obj, size_selected
    global blocks, blocks_index

    if vr.inputs['G'] and wait_for_key():
        block_type_to_place = blocks[blocks_index]
        blocks_index = (blocks_index + 1) % len(blocks)

    if toggle_grid_magnet:
        if block_type_to_place in medium_block_types:
            size_selected = cf.block_default_size
        elif block_type_to_place in small_block_types:
            size_selected = cf.block_default_size // 2
        elif block_type_to_place in large_block_types :
            size_selected = cf.block_default_size * 2

        x, y = t.Vadd(vr.camera_coord, vr.cursor)
        target_anchor = (x // size_selected) * size_selected, (y // size_selected) * size_selected

    if vr.inputs['B'] and wait_for_key():
        toggle_placement = False if toggle_placement else True

    if toggle_placement:
        vr.info_txt = block_type_to_place
        if vr.inputs['CLICK'] and wait_for_key():
            if editor_selected_obj is not None and editor_selected_obj.size == (size_selected, size_selected):
                vr.map.remove(editor_selected_obj)
            else:
                anchor = target_anchor if toggle_grid_magnet else t.Vadd(vr.camera_coord, t.Vcl(1, vr.cursor, -0.5, (size_selected, size_selected)))
                if block_type_to_place == 'block':
                    vr.map.add_block(anchor, (size_selected, size_selected), update=True)
                elif block_type_to_place == 'spike':
                    vr.map.add('spike', (anchor, (size_selected, size_selected)), update=True)
                elif block_type_to_place == 'default':
                    pass
                else:
                    print("# Error : unknown type block -> ", block_type_to_place)

    if vr.inputs['S'] and wait_for_key(dt=0.2):
        vr.map.save_map()
        print("Map Saved.")

    if vr.inputs['F'] and wait_for_key():
        vr.fly_mode = False if vr.fly_mode else True
        vr.gravity = 0 if vr.fly_mode else cf.gravity

    return

def editor_draw():
    global toggle_placement, size_selected

    if editor_selected_obj is not None:
        coord = u.adapt_to_view(editor_selected_obj.world_anchor)
        pg.draw.rect(vr.window, 'yellow', (coord[0], coord[1], editor_selected_obj.sizex(), editor_selected_obj.sizey()), 3)

    if toggle_placement:
        topleft = u.adapt_to_view(target_anchor) if toggle_grid_magnet else t.Vcl(1, vr.cursor, -0.5, (size_selected, size_selected))
        pg.draw.rect(vr.window, 'red', (topleft[0], topleft[1], size_selected, size_selected), 2)

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
