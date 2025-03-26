# Game configuration (Must be non-mutable)

game_name = "Game Name"
version = 1.0

fullscreen = False
fps = 60
fps_treshold = 0.5

world_size = (20_000, 5_000)
view_size = (1_200, 800)
worldborder = (600, 400)

# Modes
fly_mode = False
editor_mode = True
controller_threshold = 0.1

# World
gravity = 1.5

# Camera
camera_follow_speed_tresh = 10
start_camera_coord = (worldborder[0], world_size[1] - worldborder[1] - view_size[1])

# Map
max_blur = 90
back_base_color = [50, 20, 30]
block_default_size = 100

# Player
respawn_time = 1.
anti_glitch_power = 1
player_size = (50, 70)
player_speed_start = 8
player_acc_break_ground = 0.1
player_acc_minimal_ground = 0.4
player_power_acc_increment = 50
player_max_acc = 2.5
player_jump_reload = 0.1
player_jump_max_counter = 10
player_jump_power = 18
player_double_jump_power = 0.6
player_double_jump_speed_turn = 1.
player_side_jump_speed_turn = 10
player_side_jump_power = 2
player_down_acc = 1
player_air_control = 0.6
player_ground_friction = 0.85
player_air_friction = 0.95
player_grapple_reload = 0.5
player_grapple_speed = 1
player_grapple_max_length, player_grapple_min_length = 350, 100
player_grapple_force = 1.8
player_grapple_size = (12, 12)

# Creatures
bat = {'action_radius': 200, 'moving_radius': 50, 'size': 75, 'speed_default': 0.5, 'speed_attack': 2, 'come_back_speed': 0.5}

