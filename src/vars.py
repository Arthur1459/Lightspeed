# Global variables used by the game
import config as cf

window_size = cf.window_default_size
win_width, win_height = window_size[0], window_size[1]
middle = (win_width // 2, win_height // 2)

window = None
clock = None

running = False

# In game
inputs = {}
fps = cf.fps
dt, t = 1/fps, 0

cursor = (0, 0)
info_txt = ""
id = 0

player = None
