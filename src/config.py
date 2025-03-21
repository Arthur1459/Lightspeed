# Game configuration (Must be non-mutable)

game_name = "Game Name"
version = 1.0

fullscreen = False
fps = 60
fps_treshold = 0.5

world_size = (50_000, 5_000)
view_size = (1_200, 800)
worldborder = (600, 400)

fly_mode = False

camera_follow_speed_tresh = 10
gravity = 1
anti_glitch_power = 1
max_blur = 90
back_base_color = [50, 20, 30]

# Player
player_size = (55, 80)
player_speed_start = 5
player_acc_break_ground = 0.1
player_acc_minimal_ground = 0.5
player_power_acc_increment = 50
player_max_acc = 2.5
player_jump_reload = 0.1
player_jump_max_counter = 10
player_jump_power = 16
player_double_jump_speed_turn = 1
player_side_jump_speed_turn = 2
player_down_acc = 1
player_air_control = 0.4
player_ground_friction = 0.85
player_air_friction = 0.95
