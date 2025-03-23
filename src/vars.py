# Global variables used by the game
import config as cf

window_size = cf.view_size
win_width, win_height = window_size[0], window_size[1]
win_half_width, win_half_height = win_width/2, win_height/2
middle = (win_width // 2, win_height // 2)
camera_radius = ((win_width**2 + win_height**2)**0.5)/2

window = None
clock = None

running = False

# In game
inputs = {}
fps = cf.fps
dt_update, t = 1 / fps, 0

cursor = (0, 0)
info_txt = ""
id = 0

camera_coord = cf.start_camera_coord
mask_background = None
world_area_obj = None

player = None
map = None


