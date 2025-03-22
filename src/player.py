import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import player_visuals

import pygame as pg

class Player:
    def __init__(self):
        self.id = u.getNewId()

        self.sizex, self.sizey = cf.player_size

        self.decentralise = [0, 0]
        self.coord = t.Vadd(t.Vdiff(vr.middle, self.get_half_size()), self.decentralise)

        self.speed = [0, 0]
        self.acc = [0, 0]

        self.tags = set()

        self.states = 'stand'
        self.visuals = player_visuals
        self.visual, self.visual_index, self.visual_time, self.visual_duration = self.visuals[self.states]['frames'][0], 0, 0, self.visuals[self.states]['duration']

        self.actions_timers = {'jump': 0}

    def update(self):

        self.acc = t.Vadd(self.acc, (0, u.distance_to_acc_per_updt(2)))
        self.speed = t.Vcl(1, t.VxV(self.speed, (0.8 if self.speed[1] == 0. else 0.9, 0.9)), vr.dt_update, self.acc)

        dx_left, dx_right, dy_up, dy_down = u.distance_to_borders(t.Vadd(t.Vadd(vr.camera_coord, vr.middle), self.decentralise), border=t.Vadd(cf.worldborder, self.get_half_size()))

        # Tags
        if dy_down < 4:
            self.tags.add('on_ground')
        elif 'on_ground' in self.tags:
            self.tags.remove('on_ground')
        if vr.t - self.actions_timers['jump'] > cf.player_jump_reload:
            self.tags.add('jump_ready')

        # Speed reset on border
        if (dx_left < 3 and self.speed[0] < 0) or (dx_right < 3 and self.speed[0] > 0):
            self.speed[0] = 0
        if (dy_up < 4 and self.speed[1] < 0) or (dy_down < 4 and self.speed[1] > 0):
            self.speed[1] = 0

        # Speed Zero while small
        if abs(self.speed[0]) < u.distance_to_speed_per_updt(0.2): self.speed[0] = 0
        if abs(self.speed[1]) < u.distance_to_speed_per_updt(0.2): self.speed[1] = 0

        # Coord decentralised in window
        self.coord = t.Vadd(t.Vdiff(vr.middle, self.get_half_size()), self.decentralise)

        #--- Camera update
        camera_speed = [0, 0]
        border_distances = (-self.decentralise[0] + self.sizex/2, 2 * cf.worldborder[0] + 2 * self.decentralise[0], -self.decentralise[1] + self.sizey/2, 2 * cf.worldborder[1] + 2 * self.decentralise[1])

        future_decentralise = t.Vcl(1, self.decentralise, vr.dt_update, self.speed)
        self.decentralise = t.VmaxControl(future_decentralise, self.sizex)
        speed_remaining = (u.distance_to_speed_per_updt(future_decentralise[0] - self.decentralise[0]), u.distance_to_speed_per_updt(future_decentralise[1] - self.decentralise[1]))

        if abs(self.speed[0]) * vr.dt_update < cf.camera_follow_speed_tresh:
            camera_speed[0] += 0.05 * u.distance_to_speed_per_updt(self.decentralise[0]) + speed_remaining[0]
            self.decentralise[0] += -1 * vr.dt_update * (camera_speed[0] - speed_remaining[0])
        if u.distance_to_speed_per_updt(abs(self.speed[1])) < cf.camera_follow_speed_tresh:
            camera_speed[1] += 0.05 * u.distance_to_speed_per_updt(self.decentralise[1]) + speed_remaining[1]
            self.decentralise[1] += -1 * vr.dt_update * (camera_speed[1] - speed_remaining[1])

        if abs(self.decentralise[0]) == self.sizex:
            camera_speed[0] += self.speed[0]
        if abs(self.decentralise[1]) == self.sizex:
            camera_speed[1] += self.speed[1]
        new_camera_pos = t.Vcl(1, vr.camera_coord, 1 * vr.dt_update, camera_speed)

        vr.camera_coord = u.keep_in_border(new_camera_pos, delta=border_distances)
        #---

        # Update Visual
        self.update_visual()

        # Reset vars
        self.acc = [0, 0]
        return

    def update_visual(self):

        if self.speed[1] < 0:
            if self.speed[0] >= 0:
                new_states = 'jump_right'
            else:
                new_states = 'jump_left'
        elif self.speed[1] == 0. and self.speed[0] != 0.:
            if t.s(self.speed[0]) == t.s(self.acc[0]):
                new_states = 'run_right' if self.speed[0] > 0 else 'run_left'
            else:
                new_states = 'slide_right' if self.speed[0] > 0 else 'slide_left'
        elif self.speed[1] > 0:
            new_states = 'fall'
        else:
            new_states = 'stand'

        speed_factor = max(0.3, 8 * t.norm(self.speed) / u.distance_to_speed_per_updt(self.sizex))

        if new_states != self.states:
            self.states = new_states
            self.visual, self.visual_index, self.visual_time, self.visual_duration = self.visuals[self.states]['frames'][0], 0, 0, self.visuals[self.states]['duration']
        if vr.t - self.visual_time > self.visual_duration / speed_factor:
            self.visual_index = (self.visual_index + 1) % len(self.visuals[self.states]['frames'])
            self.visual_time = vr.t
            self.visual = self.visuals[self.states]['frames'][self.visual_index]

    def get_size(self):
        return self.sizex, self.sizey
    def get_half_size(self):
        return self.sizex/2, self.sizey/2

    def draw(self):
        vr.window.blit(self.visual, self.coord)
