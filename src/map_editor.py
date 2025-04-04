import vars as vr
import config as cf
import tools as t
import utils as u
import geometry as geo
import maps
import pygame as pg

click_minimal_duration = 0.1
wait_key = vr.t

toggle_editor = False
blocks, blocks_index = ['block', 'spike', 'bat'], 0
map_classification = {'geobject': 'geobject', 'block': 'geobject', 'spike': 'geobject', 'creature': 'creature', 'bat': 'creature'}
current_block_type_to_place = 'block'

medium_block_types = {'default', 'block'}
small_block_types = {'spike', 'bat'}
large_block_types = set()

types_classification = {'large': large_block_types, 'medium': medium_block_types, 'small': small_block_types}
types_sizes = {'large': cf.block_default_size * 2,
               'medium': cf.block_default_size * 1,
               'small': cf.block_default_size * 0.5}

current_targeted_type = 'medium'

toggle_grid_magnet = True

target_anchor = vr.cursor
editor_selected_obj = None

def editor_update():
    global toggle_editor, toggle_grid_magnet
    global current_block_type_to_place, medium_block_types, small_block_types, large_block_types, map_classification
    global target_anchor, editor_selected_obj, current_targeted_type
    global blocks, blocks_index

    if vr.inputs['E'] and wait_for_key() and cf.allow_editor_mode:
        toggle_editor = False if toggle_editor else True
    if not toggle_editor: return

    if vr.inputs['G'] and wait_for_key():
        current_block_type_to_place = blocks[blocks_index]
        blocks_index = (blocks_index + 1) % len(blocks)

    if toggle_grid_magnet:
        if current_block_type_to_place in medium_block_types:
            current_targeted_type = 'medium'
        elif current_block_type_to_place in small_block_types:
            current_targeted_type = 'small'
        elif current_block_type_to_place in large_block_types :
            current_targeted_type = 'large'

        x, y = t.Vadd(vr.camera_coord, vr.cursor)
        size_selected = types_sizes[current_targeted_type]
        target_anchor = (x // size_selected) * size_selected, (y // size_selected) * size_selected

    vr.info_txt = current_block_type_to_place
    if vr.inputs['CLICK'] and wait_for_key():
        if editor_selected_obj is not None:
            vr.map.remove(editor_selected_obj, obj_classification=map_classification[editor_selected_obj.get_type()])
        else:
            anchor = target_anchor if toggle_grid_magnet else t.Vadd(vr.camera_coord, t.Vcl(1, vr.cursor, -0.5, (size_selected, size_selected)))
            if current_block_type_to_place == 'block':
                vr.map.add_block(anchor, (size_selected, size_selected), update=True)
            elif current_block_type_to_place == 'spike':
                vr.map.add_geobject('spike', (anchor, (size_selected, size_selected)), update=True)
            elif current_block_type_to_place == 'bat':
                vr.map.add_creature('bat', anchor, update=True)
            elif current_block_type_to_place == 'default':
                pass
            else:
                print("# Error : unknown type block -> ", current_block_type_to_place)

    if vr.inputs['S'] and wait_for_key(dt=0.2):
        vr.map.save_map()
        print("Map Saved.")

    if vr.inputs['F'] and wait_for_key():
        vr.fly_mode = False if vr.fly_mode else True
        vr.gravity = 0 if vr.fly_mode else cf.gravity

    return

def editor_draw():
    global target_anchor
    global toggle_editor, toggle_grid_magnet
    global types_sizes, current_targeted_type

    if toggle_editor:
        if editor_selected_obj is not None:
            coord = u.adapt_to_view(editor_selected_obj.world_anchor)
            pg.draw.rect(vr.game_window, 'yellow', (coord[0], coord[1], editor_selected_obj.sizex(), editor_selected_obj.sizey()), 3)

        topleft = u.adapt_to_view(target_anchor) if toggle_grid_magnet else t.Vcl(1, vr.cursor, -0.5, (types_sizes[current_targeted_type], types_sizes[current_targeted_type]))
        pg.draw.rect(vr.game_window, 'red', (topleft[0], topleft[1], types_sizes[current_targeted_type], types_sizes[current_targeted_type]), 2)

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
