import vars as vr
import config as cf
import tools as t
import utils as u
from visuals import player_visuals
from ambient import Particle

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

        self.grapple = GrappleHook()

        self.actions_timers = {'jump': 0, 'respawn': 0, 'grapple': 0}
        self.actions_counter = {'jump': 0, 'double_jump': 1, 'side_jump': 0}
        self.player_power_acc = 0

        self.detectors = {'body': Detector(self.get_center(), (0, 0)),
                          'body_right': Detector(self.get_center(), (0.3 * self.sizex, 0)),
                          'body_left': Detector(self.get_center(), (-0.3 * self.sizex, 0)),
                          'right': Detector(self.get_center(), (0.6 * self.sizex, 0)),
                          'left': Detector(self.get_center(), (-0.6 * self.sizex, 0)),
                          'head': Detector(self.get_center(), (0, -0.6 * self.sizey)),
                          'walk_right': Detector(self.get_center(), (0.4 * self.sizex, 0.3 * self.sizey)),
                          'walk_left': Detector(self.get_center(), (-0.4 * self.sizex, 0.3 * self.sizey)),
                          'knees': Detector(self.get_center(), (0, 0.5 * self.sizey)),
                          'foot': Detector(self.get_center(), (0, 0.55 * self.sizey))}
        self.all_detection = self.get_all_detection()

    def update(self):
        for detector in self.detectors:
            self.detectors[detector].update(self.get_center())
        self.all_detection = self.get_all_detection()

        # Action reload
        if vr.t - self.actions_timers['jump'] > cf.player_jump_reload and 'jump_ready' not in self.tags:
            self.tags.add('jump_ready')

        # User inputs
        self.control_player()

        # Update Speed wanted
        self.acc = t.Vadd(self.acc, (0, u.distance_to_acc_per_updt(vr.gravity)))
        self.speed = t.Vcl(1, t.VxV(self.speed, (cf.player_ground_friction if 'on_ground' in self.tags else cf.player_air_friction, cf.player_air_friction)), vr.dt_update, self.acc)

        # Special Detector detection
        if 'dead' not in self.tags and self.is_killed():
            self.tags.add('dead')
            self.actions_timers['respawn'] = vr.t
            self.damage_taken_effect()

        if 'dead' not in self.tags:
            # Control collide
            if 'solid' in self.detectors['right'].detection:
                if self.speed[0] > 0:
                    self.speed[0] = 0
            if 'solid' in self.detectors['left'].detection:
                if self.speed[0] < 0:
                    self.speed[0] = 0

            if 'solid' in self.detectors['foot'].detection:
                self.tags.add('on_ground')
                if self.speed[1] > 0:
                    self.speed[1] = 0
            else:
                if 'on_ground' in self.tags: self.tags.remove('on_ground')
            if 'solid' in self.detectors['head'].detection:
                if self.speed[1] < 0:
                    self.speed[1] = 0.1 * abs(self.speed[1])
                    if 'jumping' in self.tags: self.tags.remove('jumping')

            if 'solid' in self.detectors['body_right'].detection:
                self.speed[0] += -1 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
            if 'solid' in self.detectors['body_left'].detection:
                self.speed[0] += 1 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
            if 'solid' in self.detectors['walk_right'].detection and 'solid' not in self.detectors['right'].detection:
                self.speed[0] += 0.2 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
                self.speed[1] += -1 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
            if 'solid' in self.detectors['walk_left'].detection and 'solid' not in self.detectors['left'].detection:
                self.speed[0] += -0.2 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
                self.speed[1] += -1 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
            if 'solid' in self.detectors['knees'].detection:
                self.speed[1] += -1 * u.distance_to_speed_per_updt(cf.anti_glitch_power)
            if 'solid' in self.detectors['body'].detection:
                self.speed[1] += -2 * u.distance_to_speed_per_updt(cf.anti_glitch_power)

            # Speed Zero if small
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
            vr.camera_coord = t.Vcl(1, vr.camera_coord, 1 * vr.dt_update, camera_speed)

        #---

        # Update Visual
        self.update_visual()

        # Reset vars
        self.acc = [0, 0]
        return

    def update_visual(self):

        if 'dead' in self.tags:
            new_states = 'dead'
        elif self.speed[1] < 0:
            if self.speed[0] >= 0:
                new_states = 'jump_right'
            else:
                new_states = 'jump_left'
        elif 'on_ground' in self.tags and self.speed[0] != 0.:
            if t.s(self.speed[0]) == t.s(self.acc[0]):
                new_states = 'run_right' if self.speed[0] > 0 else 'run_left'
            elif abs(self.speed[0]) > u.distance_to_speed_per_updt(cf.player_speed_start):
                new_states = 'slide_right' if self.speed[0] > 0 else 'slide_left'
            else:
                new_states = 'stand'
        elif self.speed[1] > 0:
            new_states = 'fall'
        else:
            new_states = 'stand'

        speed_factor = max(0.3, 8 * t.norm(self.speed) / u.distance_to_speed_per_updt(self.sizex))

        if u.proba((speed_factor**2) * 10) and 'dead' not in self.tags:
            anchor = t.Vadd(t.Vadd(vr.camera_coord, self.coord), (self.sizex/2 + t.rndInt(-0.2 * self.sizex, 0.2 * self.sizex), self.sizey/2 + t.rndInt(- 0.4 * self.sizey, 0.4 * self.sizey)))
            vr.map.ambient_elts.append(Particle('default', anchor, size=self.sizex, speed=self.speed, gravity=True))

        if new_states != self.states:
            self.states = new_states
            self.visual, self.visual_index, self.visual_time, self.visual_duration = self.visuals[self.states]['frames'][0], 0, 0, self.visuals[self.states]['duration']
        if vr.t - self.visual_time > self.visual_duration / speed_factor:
            self.visual_index = (self.visual_index + 1) % len(self.visuals[self.states]['frames'])
            self.visual_time = vr.t
            self.visual = self.visuals[self.states]['frames'][self.visual_index]

    def control_player(self):

        if vr.fly_mode:
            if vr.inputs['RIGHT']: self.speed[0] = 1 * u.distance_to_speed_per_updt(10)
            elif vr.inputs['LEFT']: self.speed[0] = -1 * u.distance_to_speed_per_updt(10)
            if vr.inputs['DOWN']: self.speed[1] = 1 * u.distance_to_speed_per_updt(10)
            elif vr.inputs['UP']: self.speed[1] = -1 * u.distance_to_speed_per_updt(10)
            return

        if vr.inputs['SPACE']:
            self.launch_grapple()
        else:
            self.retract_grapple()
        self.grapple.update(self.get_center())
        if self.grapple.state == 'caught':
            self.acc = t.Vadd(self.acc, t.Vmul(t.Vdir(self.get_center(), self.grapple.target_anchor), u.distance_to_acc_per_updt(cf.player_grapple_force)))
            self.tags.add('can_double_jump')
            return

        in_the_air = 'on_ground' not in self.tags
        max_acc = u.distance_to_acc_per_updt(cf.player_max_acc)
        if vr.inputs['RIGHT'] and 'solid' not in self.detectors['right'].detection:
            if self.speed[0] < 0:
                self.player_power_acc = u.distance_to_acc_per_updt(cf.player_acc_break_ground)
            else:
                self.player_power_acc = max(min(max_acc, self.player_power_acc + cf.player_power_acc_increment), u.distance_to_acc_per_updt(cf.player_acc_minimal_ground))
                self.speed[0] = max(self.speed[0], 1 * u.distance_to_speed_per_updt(cf.player_speed_start) if not in_the_air else 0)
            self.acc[0] = min(max_acc, self.player_power_acc) if vr.player.speed[1] == 0. else min(self.player_power_acc * cf.player_air_control, max_acc)
        elif vr.inputs['LEFT'] and 'solid' not in self.detectors['left'].detection:
            if self.speed[0] > 0:
                self.player_power_acc = u.distance_to_acc_per_updt(cf.player_acc_break_ground)
            else:
                self.player_power_acc = max(min(max_acc, self.player_power_acc + cf.player_power_acc_increment), u.distance_to_acc_per_updt(cf.player_acc_minimal_ground))
                self.speed[0] = min(self.speed[0], -1 * u.distance_to_speed_per_updt(cf.player_speed_start) if not in_the_air else 0)
            self.acc[0] += -1 * min(max_acc, self.player_power_acc) if vr.player.speed[1] == 0. else -1 * min(self.player_power_acc * cf.player_air_control, max_acc)
        else:
            self.player_power_acc = 0

        jump_speed = u.distance_to_speed_per_updt(cf.player_jump_power)
        side_jump_speed = u.distance_to_speed_per_updt(cf.player_side_jump_power)
        if vr.inputs['DOWN']:
            self.acc[1] += u.distance_to_acc_per_updt(cf.player_down_acc)
        elif vr.inputs['UP']:
            if not in_the_air and 'jump_ready' in self.tags or 'can_double_jump' in self.tags:
                self.remove_tag('jump_ready')
                self.actions_timers['jump'] = vr.t
                self.actions_counter['jump'] = 0
                if 'can_double_jump' in self.tags:
                    self.tags.add('double_jumping')
                    self.speed[1] = min(-1 * jump_speed * cf.player_double_jump_power, self.speed[1])
                    self.remove_tag('can_double_jump')
                    if vr.inputs['RIGHT'] and self.speed[0] < 0: self.speed[0] = u.distance_to_speed_per_updt(cf.player_double_jump_speed_turn)
                    if vr.inputs['LEFT'] and self.speed[0] > 0: self.speed[0] = -1 * u.distance_to_speed_per_updt(cf.player_double_jump_speed_turn)
                else:
                    self.tags.add('jumping')
                    self.speed[1] = min(-1 * jump_speed, self.speed[1]) # Normal Jump
            elif in_the_air:
                self.actions_counter['side_jump'] = 0
                if 'can_side_jump' in self.tags and 'solid' in self.detectors['right'].detection:
                    self.speed[0] = -1 * max(u.distance_to_speed_per_updt(cf.player_side_jump_speed_turn) , abs(self.speed[0]))
                    self.speed[1] = min(-1 * side_jump_speed, self.speed[1])
                    self.actions_counter['side_jump'] = 0
                    self.remove_tag('can_side_jump')
                    self.actions_counter['double_jump'] = 1
                    self.remove_tag('can_double_jump')
                if 'can_side_jump' in self.tags and 'solid' in self.detectors['left'].detection:
                    self.speed[0] = 1 * max(u.distance_to_speed_per_updt(cf.player_side_jump_speed_turn) , abs(self.speed[0]))
                    self.speed[1] = min(-1 * side_jump_speed, self.speed[1])
                    self.actions_counter['side_jump'] = 0
                    self.remove_tag('can_side_jump')
                    self.actions_counter['double_jump'] = 1
                    self.remove_tag('can_double_jump')
            if 'jumping' in self.tags:
                if self.actions_counter['jump'] < cf.player_jump_max_counter:
                    self.speed[1] = min(-1 * jump_speed, self.speed[1])
                    self.actions_counter['jump'] += 1
                else:
                    self.remove_tag('jumping')
            elif 'double_jumping' in self.tags:
                if self.actions_counter['jump'] < cf.player_jump_max_counter:
                    self.speed[1] = min(-1 * jump_speed * cf.player_double_jump_power, self.speed[1])
                    self.actions_counter['jump'] += 1
                else:
                    self.remove_tag('double_jumping')

        else:
            if in_the_air:
                if self.actions_counter['double_jump'] == 1:
                    self.tags.add('can_double_jump')
                    self.actions_counter['double_jump'] = 0
                if self.actions_counter['side_jump'] == 0:
                    self.tags.add('can_side_jump')
                    self.actions_counter['side_jump'] = 1
            elif not in_the_air:
                self.actions_counter['double_jump'] = 1
                self.remove_tag('can_double_jump')
                self.remove_tag('can_side_jump')
            self.remove_tag('jumping')
            self.remove_tag('double_jumping')

    def launch_grapple(self):
        if vr.t - self.actions_timers['grapple'] > cf.player_grapple_reload and 'grappling' not in self.tags:
            self.actions_timers['grapple'] = vr.t
            self.tags.add('grappling')
            direction = [0, 0]
            if vr.inputs['UP']:
                direction[1] = -1
            elif vr.inputs['DOWN']:
                direction[1] = 1
            if vr.inputs['RIGHT']:
                direction[0] = 1
            elif vr.inputs['LEFT']:
                direction[0] = -1
            if direction == [0, 0]: direction = [0, -1]
            self.grapple.launch(direction)
        return

    def retract_grapple(self):
        self.grapple.retract()
        self.remove_tag('grappling')

    def is_killed(self):
        return (not all((self.all_detection.isdisjoint({'spike'}), self.detectors['body'].detection.isdisjoint({'bat'})))) and (not vr.fly_mode)

    def respawn(self):
        self.decentralise = [0, 0]
        self.coord = t.Vadd(t.Vdiff(vr.middle, self.get_half_size()), self.decentralise)
        self.speed = [0, 0]
        self.acc = [0, 0]
        self.tags = set()
        self.states = 'stand'
        self.actions_timers = {'jump': 0, 'respawn': 0, 'grapple': 0}
        self.actions_counter = {'jump': 0, 'double_jump': 1, 'side_jump': 0}
        self.player_power_acc = 0

    def damage_taken_effect(self):
        for i in range(100):
            anchor = t.Vadd(t.Vadd(self.coord, vr.camera_coord), (
            self.sizex / 2 + t.rndInt(-0.2 * self.sizex, 0.2 * self.sizex),
            self.sizey / 2 + t.rndInt(- 0.4 * self.sizey, 0.4 * self.sizey)))
            max_speed = u.distance_to_speed_per_updt(15)
            speed = (t.rndInt(-max_speed, max_speed), t.rndInt(-max_speed, max_speed))
            vr.map.ambient_elts.append(Particle('fire', anchor, size=4, speed=speed, gravity=True))

    def remove_tag(self, tag):
        if tag in self.tags: self.tags.remove(tag)
    def get_size(self):
        return self.sizex, self.sizey
    def get_half_size(self):
        return self.sizex/2, self.sizey/2
    def get_center(self):
        return t.Vadd(self.coord, self.get_half_size())
    def get_world_anchor_centered(self):
        return t.Vadd(vr.camera_coord, self.get_center())
    def get_all_detection(self):
        detection = set()
        for detector in self.detectors:
            detection = detection.union(self.detectors[detector].detection)
        return detection

    def draw(self):
        vr.window.blit(self.visual, self.coord)

        if self.grapple.state in ('launched', 'caught'):
            pg.draw.line(vr.window, (120, 90, 10), self.get_center(), self.grapple.target_anchor, 3)
            vr.window.blit(self.visuals['grapple']['frames'][0], self.grapple.get_top_left())
            #pg.draw.rect(vr.window, (180, 150, 50), [self.grapple.target_anchor[0] - 4, self.grapple.target_anchor[1] - 4, 8, 8], 3)

class GrappleHook:
    def __init__(self):
        self.target_anchor = vr.middle
        self.length = 0
        self.direction = (0, 0)
        self.state = 'stored'

        self.detector = Detector(self.target_anchor, (0, 0))

    def launch(self, direction):
        self.direction = direction
        self.state = 'launched'
    def retract(self):
        self.length = 0
        self.state = 'stored'
        self.target_anchor = vr.middle
    def get_top_left(self):
        return t.Vcl(1, self.target_anchor, -0.5, cf.player_grapple_size)
    def update(self, player_coord):

        if self.state == 'launched':
            self.length = min(self.length + u.distance_to_speed_per_updt(cf.player_grapple_speed), cf.player_grapple_max_length)
            self.target_anchor = t.Vcl(1, player_coord, self.length, self.direction)
            self.detector.update(self.target_anchor)
        elif self.state == 'caught':
            self.target_anchor = u.adapt_to_view(self.detector.absolute_coord)
            self.length = t.distance(player_coord, self.target_anchor)

        if self.state == 'launched':
            if 'solid' in self.detector.detection:
                self.state = 'caught'

        if self.length == cf.player_grapple_max_length:
            self.retract()

class Detector:
    def __init__(self, anchor, relative_coord):
        self.id = u.getNewId()
        self.win_anchor = anchor
        self.relative_coord = relative_coord
        self.absolute_coord = t.Vadd(vr.camera_coord, t.Vadd(self.win_anchor, self.relative_coord))

        self.detection = set()

    def update(self, anchor):
        self.win_anchor = anchor
        self.absolute_coord = t.Vadd(vr.camera_coord, t.Vadd(self.win_anchor, self.relative_coord))

        self.detection = set()
        if not vr.world_area_obj.intersect(self.absolute_coord):
            self.detection.add('solid')
        for obj in vr.map.geobjects + vr.map.creatures:
            if t.distance(self.absolute_coord, obj.world_anchor) < obj.radius and obj.intersect(self.absolute_coord):
                self.detection = self.detection.union(obj.tags)

    def draw(self):
        pg.draw.circle(vr.window, 'white' if len(self.detection) == 0 else 'red', u.adapt_to_view(self.absolute_coord), 4)
