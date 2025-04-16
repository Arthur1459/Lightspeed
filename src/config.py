# Game configuration (Must be non-mutable)

game_name = "Lightspeed"
version = "beta 1.0"

fullscreen = True
fps = 60
fps_treshold = 0.5

world_size = (20_000, 5_000)
view_size = (1_280, 720)

worldborder = (view_size[0]//2, view_size[1]//2)

# Settings
fly_mode = False
controller_threshold = 0.1
show_fps = True

# World
nb_worlds = 4
gravity = 1.4

# Camera
camera_follow_speed_tresh = 10
start_camera_coord = (worldborder[0], world_size[1] - worldborder[1] - view_size[1])

# Map
min_blur = 90
back_base_color = [50, 20, 30]
block_default_size = 100

# Player
respawn_time = 1.
anti_glitch_power = 1
fly_speed = 12
player_size = (50, 70)
player_speed_start_ground = 8
player_speed_start_air = 4
player_acc_break = 0.25
player_acc_minimal_ground = 0.5
player_power_acc_increment = 50
player_max_acc = 2.5
player_jump_reload = 0.1
player_jump_max_counter = 12
player_jump_power = 14
player_double_jump_factor = 0.25
player_double_jump_speed_turn = 1
player_side_jump_speed_turn = 12
player_side_jump_power = 1
player_down_acc = 1
player_air_control = 0.9
player_air_control_speed_threshold = 16
player_ground_friction = 0.8
player_air_friction = 0.95
player_grapple_reload = 0.25
player_grapple_speed = 1
player_grapple_max_length, player_grapple_min_length = 250, 100
player_grapple_force = 10
player_grapple_size = (12, 12)
player_balancing_power = 2500
draw_player_detectors = False

# Creatures
bat = {'action_radius': 200, 'moving_radius': 50, 'size': 50, 'speed_default': 0.5, 'speed_attack': 2, 'come_back_speed': 0.5}
zombietree = {'action_radius': 300, 'moving_radius': 50, 'size': (75, 100), 'speed_default': 0.5, 'speed_attack': 3, 'come_back_speed': 0.5}

