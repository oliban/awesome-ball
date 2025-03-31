# stick_hockey_penguin.py
# -*- coding: utf-8 -*-
import pygame
import sys
import math
import random
import os
from datetime import datetime

# --- Get Timestamp ---
GENERATION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Constants ---
SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600; FPS = 60
WHITE = (255, 255, 255); BLACK = (0, 0, 0);
# Theme Colors
ICE_BLUE = (210, 240, 255); RINK_WHITE = (245, 245, 255); PUCK_COLOR = (20, 20, 30)
TEAM1_COLOR = (0, 0, 200); TEAM1_ACCENT = (200, 200, 255) # Blue Team (P1)
TEAM2_COLOR = (200, 0, 0); TEAM2_ACCENT = (255, 200, 200) # Red Team (P2)
PENGUIN_BODY_COLOR = (30, 30, 40); PENGUIN_BELLY_COLOR = (240, 240, 240); PENGUIN_BEAK_FEET_COLOR = (255, 165, 0)

GRASS_GREEN = (34, 139, 34); YELLOW = (255, 255, 0); TEXT_COLOR = (10, 10, 50)
ARROW_RED = (255, 50, 50); STAR_YELLOW = (255, 255, 100); STAR_ORANGE = (255, 180, 0)
RED = (255, 0, 0)
DEBUG_BLUE = (0, 0, 255)
GOAL_POST_COLOR = (200, 20, 20); GOAL_NET_COLOR = (180, 180, 190) # Red Posts
GOAL_EXPLOSION_COLORS = [WHITE, YELLOW, STAR_YELLOW, (255, 215, 0)]
NOSE_COLOR = (50, 50, 50) # Still used for default players
SCOREBOARD_BG_COLOR = (50, 50, 80, 180)
SCOREBOARD_BORDER_COLOR = (200, 200, 220)
SCOREBOARD_TEXT_FLASH_COLOR = YELLOW
SCREEN_FLASH_COLOR = (255, 255, 255, 100)
SCREEN_FLASH_DURATION = 0.15
DEBUG_HIT_ANGLES = False

# Physics
GRAVITY = 0.5; BASE_PLAYER_SPEED = 4.5; BASE_JUMP_POWER = -11
PLAYER_FRICTION = 0.95
BASE_HIT_FORCE_X = 18; BASE_HIT_FORCE_Y = -1
HIT_FORCE_LEVEL = 1.5
HEADBUTT_UP_FORCE = 15.0; HEADBUTT_VY_MULTIPLIER = 1.2
HEADBUTT_PLAYER_VX_FACTOR = 0.6; HEADBUTT_POS_X_FACTOR = 0.15
HEAD_BOUNCE_MULTIPLIER = 3.0
PUCK_FRICTION = 0.998; PUCK_BOUNCE = 0.6; GROUND_Y = SCREEN_HEIGHT - 50

# Collision Specific
PLAYER_BODY_BOUNCE = 0.65; PLAYER_VEL_TRANSFER = 0.25
MIN_BODY_BOUNCE_VEL = 1.5; PLAYER_BODY_COLLISION_FRAMES = 4
HEAD_PLATFORM_RADIUS_BUFFER = 5

# Hit Collision Tweak
HIT_RADIUS_NORMAL = 16; HIT_RADIUS_FALLING_BONUS = 6
PUCK_FALLING_VELOCITY_THRESHOLD = 5

# Goal Constants (Hockey Style)
GOAL_MARGIN_X = 15
GOAL_WIDTH = 100
GOAL_HEIGHT = 80
GOAL_POST_THICKNESS = 8
GOAL_Y_POS = GROUND_Y - GOAL_HEIGHT
GOAL_LINE_X_LEFT = GOAL_MARGIN_X; GOAL_LINE_X_RIGHT = SCREEN_WIDTH - GOAL_MARGIN_X

# Animation Constants
WALK_CYCLE_SPEED = 0.25; BODY_WOBBLE_AMOUNT = 0
RUN_UPPER_ARM_SWING = math.pi / 6.0; RUN_UPPER_ARM_WOBBLE_AMP = 0; RUN_UPPER_ARM_WOBBLE_SPEED = 0
RUN_FOREARM_SWING = math.pi / 5.0; RUN_FOREARM_WOBBLE_AMP = 0; RUN_FOREARM_WOBBLE_SPEED = 0
RUN_FOREARM_OFFSET_FACTOR = 0.1; JUMP_UPPER_ARM_BASE = -math.pi * 0.1; JUMP_UPPER_ARM_WOBBLE_AMP = 0
JUMP_UPPER_ARM_WOBBLE_SPEED = 0; JUMP_UPPER_ARM_VY_FACTOR = 0.01; JUMP_FOREARM_BASE = math.pi * 0.1
JUMP_FOREARM_WOBBLE_AMP = 0; JUMP_FOREARM_WOBBLE_SPEED = 0
LEG_THIGH_SWING = math.pi / 7.0; LEG_SHIN_BEND_WALK = math.pi / 8.0; LEG_SHIN_BEND_SHIFT = math.pi / 2.5
HIT_THIGH_WINDUP_ANGLE = -math.pi / 4.5; HIT_THIGH_FOLLOW_ANGLE = math.pi * 0.7
HIT_SHIN_WINDUP_ANGLE = math.pi * 0.75; HIT_SHIN_IMPACT_ANGLE = -math.pi * 0.05
HIT_SHIN_FOLLOW_ANGLE = math.pi * 0.5
JUMP_THIGH_TUCK = math.pi * 0.1; JUMP_SHIN_TUCK = math.pi * 0.2
TUMBLE_DURATION = 2.5

# --- Particle Constants ---
PARTICLE_LIFESPAN = 1.0; PARTICLE_SPEED = 150; PARTICLE_COUNT = 12; PARTICLE_SIZE = 6
GOAL_PARTICLE_COUNT = 30; GOAL_PARTICLE_SPEED_MIN = 200
GOAL_PARTICLE_SPEED_MAX = 350; GOAL_PARTICLE_LIFESPAN = 1.2
SMOKE_PARTICLE_COLOR = [(180, 180, 180), (150, 150, 150), (120, 120, 120)]
SMOKE_PARTICLE_LIFESPAN = 0.4
SMOKE_PARTICLE_SPEED = 40
SMOKE_PARTICLE_SIZE = 5
SMOKE_EMISSION_RATE = 2

# --- Debug Mode ---
debug_mode = False
DEBUG_BG_COLOR = (220, 180, 255)
DEBUG_MATCH_POINT_LIMIT = 1

# --- Game State Constants ---
MATCH_POINT_LIMIT = 5
GAME_WIN_LIMIT = 5
MATCH_OVER_DURATION = 3.0
GOAL_MESSAGE_DURATION = 1.5

# --- Power-up Constants ---
POWERUP_TYPES = ["FLIGHT", "ROCKET_LAUNCHER", "BIG_PLAYER", "SUPER_JUMP",
                 "BALL_FREEZE", "SPEED_BOOST", "GOAL_SHIELD", "SHRINK_OPPONENT",
                 "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD", "GOAL_ENLARGER", "PENGUIN"]
POWERUP_SPAWN_INTERVAL_MIN = 15.0
POWERUP_SPAWN_INTERVAL_MAX = 30.0
POWERUP_DESCEND_SPEED = 100
POWERUP_DRIFT_SPEED = 25
POWERUP_BOX_SIZE = (30, 25)
POWERUP_CHUTE_COLOR = (255, 165, 0)
POWERUP_CHUTE_ALT_COLOR = (240, 240, 240)
POWERUP_BOX_COLOR = (210, 180, 140)
POWERUP_FLIGHT_DURATION = 15.0
POWERUP_BIG_PLAYER_DURATION = 20.0
POWERUP_BIG_PLAYER_SCALE = 1.75
POWERUP_SHRINK_PLAYER_DURATION = 30.0
POWERUP_SHRINK_PLAYER_SCALE = 0.6
POWERUP_SUPER_JUMP_DURATION = 15.0
POWERUP_SUPER_JUMP_MULTIPLIER = 1.8
POWERUP_BALL_FREEZE_DURATION = 10.0
POWERUP_SPEED_BOOST_DURATION = 10.0
POWERUP_SPEED_BOOST_MULTIPLIER = 1.6
POWERUP_GOAL_SHIELD_DURATION = 10.0
POWERUP_GOAL_SHIELD_COLOR = (0, 220, 255)
POWERUP_GOAL_SHIELD_WIDTH = 12
POWERUP_GOAL_SHIELD_PULSE_SPEED = 4.0
POWERUP_GOAL_SHIELD_MIN_ALPHA = 160
POWERUP_GOAL_SHIELD_MAX_ALPHA = 240
BIG_PLAYER_KICK_MULTIPLIER = 2.0
POWERUP_LOW_GRAVITY_DURATION = 15.0
POWERUP_LOW_GRAVITY_FACTOR = 0.4
POWERUP_REVERSE_CONTROLS_DURATION = 12.0
POWERUP_ENORMOUS_HEAD_DURATION = 15.0
POWERUP_ENORMOUS_HEAD_SCALE = 7.0
POWERUP_GOAL_ENLARGER_DURATION = 15.0
POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE = 40
POWERUP_PENGUIN_DURATION = 20.0
PENGUIN_FRICTION_FACTOR = 0.99


# --- Rocket Launcher Constants ---
ROCKET_SPEED = 600
ROCKET_SIZE = (18, 6)
ROCKET_COLOR = (100, 100, 110)
ROCKET_BLAST_RADIUS_FACTOR = 2.5
ROCKET_EXPLOSION_DURATION = 0.4
ROCKET_EXPLOSION_FORCE = 95.0
ROCKET_PLAYER_UPWARD_BOOST = 20.0
ROCKET_BALL_UPWARD_BOOST = 5.0
ROCKET_EXPLOSION_COLOR = (255, 100, 0, 180)
GUN_COLOR = (70, 80, 90)
GUN_SIZE = (25, 8)
GUN_ANIM_SPEED = 3.0
GUN_ANIM_MAGNITUDE = 0.3
LASER_COLOR_HEX = "#C70E20"
LASER_ALPHA = 220
LASER_COLOR = pygame.Color(LASER_COLOR_HEX)
LASER_COLOR.a = LASER_ALPHA
LASER_LENGTH = 200
LASER_WIDTH = 1

# --- Player Tumbling Constants ---
PLAYER_TUMBLE_ROT_SPEED_MIN = 10.0
PLAYER_TUMBLE_ROT_SPEED_MAX = 20.0
PLAYER_TUMBLE_DAMPING = 0.98

# --- Custom Event Types ---
SOUND_FINISHED_EVENT = pygame.USEREVENT + 1

# --- Helper Functions ---
# ... (draw helpers unchanged) ...
def draw_polygon_shape(surface, color, center, size, sides, angle=0, width=0):
    points = []
    for i in range(sides): offset_angle = math.pi / sides if sides % 2 == 0 else math.pi / 2.0; theta = offset_angle + (2.0 * math.pi * i / sides) + angle; x = center[0] + size * math.cos(theta); y = center[1] + size * math.sin(theta); points.append((int(x), int(y)))
    pygame.draw.polygon(surface, color, points, width)
def draw_pentagon(surface, color, center, size, angle=0, width=0): draw_polygon_shape(surface, color, center, size, 5, angle, width)
def draw_hexagon(surface, color, center, size, angle=0, width=0): draw_polygon_shape(surface, color, center, size, 6, angle, width)
def normalize(v): mag_sq = v[0]**2 + v[1]**2; mag = math.sqrt(mag_sq) if mag_sq > 0 else 0; return (v[0]/mag, v[1]/mag) if mag > 0 else (0,0)
def draw_rotated_rectangle(surface, color, rect_center, width, height, angle_rad):
    half_w, half_h = width / 2, height / 2; corners = [(-half_w, -half_h), ( half_w, -half_h), ( half_w,  half_h), (-half_w,  half_h)]
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad); rotated_corners = []
    for x, y in corners: x_rot = x * cos_a - y * sin_a; y_rot = x * sin_a + y * cos_a; rotated_corners.append((rect_center[0] + x_rot, rect_center[1] + y_rot))
    pygame.draw.polygon(surface, color, rotated_corners, 0); pygame.draw.polygon(surface, BLACK, rotated_corners, 1)
def draw_hockey_goal(surface, center_x, goal_y, goal_width, goal_height, thickness, post_color, net_color):
    half_width = goal_width // 2
    left_post = (center_x - half_width, goal_y)
    right_post = (center_x + half_width, goal_y)
    bottom_left = (center_x - half_width, goal_y + goal_height)
    bottom_right = (center_x + half_width, goal_y + goal_height)
    top_bar_y = goal_y
    pygame.draw.line(surface, post_color, left_post, bottom_left, thickness)
    pygame.draw.line(surface, post_color, right_post, bottom_right, thickness)
    pygame.draw.line(surface, post_color, left_post, right_post, thickness)
    num_net_lines = 8
    for i in range(1, num_net_lines):
        x = left_post[0] + i * (goal_width / num_net_lines)
        pygame.draw.line(surface, net_color, (int(x), top_bar_y), (int(x), bottom_left[1]), 1)
    pygame.draw.line(surface, net_color, bottom_left, bottom_right, 1)
def draw_scoreboard(surface, p1_score, p2_score, p1_games, p2_games, score_font, name_font, game_score_font, is_goal_active):
    name_text = "Team Blue vs. Team Red"; score_text = f"{p1_score} - {p2_score}"; game_score_text = f"({p1_games}-{p2_games})"
    score_text_color = SCOREBOARD_TEXT_FLASH_COLOR if is_goal_active else TEXT_COLOR
    score_surf = score_font.render(score_text, True, score_text_color); score_rect = score_surf.get_rect()
    name_surf = name_font.render(name_text, True, TEXT_COLOR); name_rect = name_surf.get_rect()
    game_score_surf = game_score_font.render(game_score_text, True, TEXT_COLOR); game_score_rect = game_score_surf.get_rect()
    panel_padding_x = 20; panel_padding_y = 10; text_spacing = 2
    panel_width = max(name_rect.width, score_rect.width, game_score_rect.width) + panel_padding_x * 2
    panel_height = (name_rect.height + text_spacing + score_rect.height + text_spacing + game_score_rect.height + panel_padding_y * 2)
    panel_rect = pygame.Rect(0, 0, panel_width, panel_height); panel_rect.centerx = SCREEN_WIDTH // 2; panel_rect.top = 5
    name_rect.centerx = panel_rect.centerx; name_rect.top = panel_rect.top + panel_padding_y
    score_rect.centerx = panel_rect.centerx; score_rect.top = name_rect.bottom + text_spacing
    game_score_rect.centerx = panel_rect.centerx; game_score_rect.top = score_rect.bottom + text_spacing
    panel_surf = pygame.Surface(panel_rect.size, pygame.SRCALPHA); panel_surf.fill(SCOREBOARD_BG_COLOR)
    pygame.draw.rect(panel_surf, SCOREBOARD_BORDER_COLOR, panel_surf.get_rect(), 2); surface.blit(panel_surf, panel_rect.topleft)
    surface.blit(name_surf, name_rect); surface.blit(score_surf, score_rect); surface.blit(game_score_surf, game_score_rect)
def draw_game_scores(surface, scores_list, font):
    start_x = 10; start_y = 10; current_y = start_y
    for score_tuple in reversed(scores_list):
        p1s, p2s = score_tuple; winner_name_str = ""
        current_limit = DEBUG_MATCH_POINT_LIMIT if debug_mode else MATCH_POINT_LIMIT
        if p1s >= current_limit and p1s > p2s: winner_name_str = " (Blue)"
        elif p2s >= current_limit and p2s > p1s: winner_name_str = " (Red)"
        elif p1s == p2s and p1s >= current_limit: winner_name_str = " (Draw)"
        score_str = f"{p1s} - {p2s}{winner_name_str}"; score_surf = font.render(score_str, True, TEXT_COLOR)
        score_rect = score_surf.get_rect(topleft=(start_x, current_y)); surface.blit(score_surf, score_rect)
        current_y += score_rect.height + 1
def draw_trophy(surface, winner_name, title_font, name_font):
    cup_color = (255, 215, 0); base_color = (139, 69, 19); engraved_color = BLACK
    trophy_center_x = SCREEN_WIDTH // 2; trophy_base_y = SCREEN_HEIGHT // 2 + 180
    cup_width = 80; cup_height = 100; base_width = 140; base_height = 40
    handle_width = 20; handle_height = 60
    base_rect = pygame.Rect(0, 0, base_width, base_height); base_rect.midbottom = (trophy_center_x, trophy_base_y); pygame.draw.rect(surface, base_color, base_rect); pygame.draw.rect(surface, BLACK, base_rect, 1)
    stem_top_y = base_rect.top; stem_bottom_y = stem_top_y - 40; pygame.draw.line(surface, cup_color, (trophy_center_x, stem_top_y), (trophy_center_x, stem_bottom_y), 10)
    cup_rect = pygame.Rect(0, 0, cup_width, cup_height); cup_rect.midbottom = (trophy_center_x, stem_bottom_y); pygame.draw.ellipse(surface, cup_color, cup_rect); pygame.draw.ellipse(surface, BLACK, cup_rect, 1)
    handle_left_rect = pygame.Rect(cup_rect.left - handle_width, cup_rect.top + 10, handle_width, handle_height); handle_right_rect = pygame.Rect(cup_rect.right, cup_rect.top + 10, handle_width, handle_height)
    pygame.draw.rect(surface, cup_color, handle_left_rect); pygame.draw.rect(surface, BLACK, handle_left_rect, 1)
    pygame.draw.rect(surface, cup_color, handle_right_rect); pygame.draw.rect(surface, BLACK, handle_right_rect, 1)
    name_surf = name_font.render(winner_name, True, engraved_color); name_rect = name_surf.get_rect(center=base_rect.center); surface.blit(name_surf, name_rect)
    title_text = "GAME WINNER!"; title_surf = title_font.render(title_text, True, YELLOW)
    title_rect = title_surf.get_rect(center=(trophy_center_x, trophy_base_y - 220 - 100))
    bg_rect = title_rect.inflate(40, 20); bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA); bg_surf.fill((0, 0, 100, 200)); surface.blit(bg_surf, bg_rect.topleft)
    surface.blit(title_surf, title_rect)
    rematch_font = name_font; rematch_text = "Press R for Rematch"; rematch_surf = rematch_font.render(rematch_text, True, WHITE)
    rematch_rect = rematch_surf.get_rect(centerx=trophy_center_x, top=15)
    surface.blit(rematch_surf, rematch_rect)
def draw_offscreen_arrow(s, puck, p_pos):
    ar_sz = 15; pad = 25; is_off = False; tx, ty = puck.x, puck.y; ax = max(pad, min(puck.x, SCREEN_WIDTH - pad)); ay = max(pad, min(puck.y, SCREEN_HEIGHT - pad))
    if puck.x < 0 or puck.x > SCREEN_WIDTH: ax = pad if puck.x < 0 else SCREEN_WIDTH - pad; is_off = True
    if puck.y < 0 or puck.y > SCREEN_HEIGHT: ay = pad if puck.y < 0 else SCREEN_HEIGHT - pad; is_off = True
    if not is_off: return
    ang = math.atan2(ty - ay, tx - ax); p1 = (ar_sz, 0); p2 = (-ar_sz / 2, -ar_sz / 2); p3 = (-ar_sz / 2, ar_sz / 2)
    cos_a, sin_a = math.cos(ang), math.sin(ang); p1r = (p1[0] * cos_a - p1[1] * sin_a, p1[0] * sin_a + p1[1] * cos_a); p2r = (p2[0] * cos_a - p2[1] * sin_a, p2[0] * sin_a + p2[1] * cos_a); p3r = (p3[0] * cos_a - p3[1] * sin_a, p3[0] * sin_a + p3[1] * cos_a)
    pts = [(ax + p1r[0], ay + p1r[1]), (ax + p2r[0], ay + p2r[1]), (ax + p3r[0], ay + p3r[1])]; pygame.draw.polygon(s, ARROW_RED, [(int(p[0]), int(p[1])) for p in pts])

# --- Class Definitions ---
class Particle: # ... (no change) ...
    def __init__(self, x, y, colors=[STAR_YELLOW, STAR_ORANGE, WHITE], speed_min=PARTICLE_SPEED * 0.5, speed_max=PARTICLE_SPEED * 1.5, lifespan=PARTICLE_LIFESPAN, size=PARTICLE_SIZE, p_type='star', angle_override=None):
        self.x = x; self.y = y; self.p_type = p_type
        if angle_override is not None: angle = angle_override
        else: angle = random.uniform(0, 2 * math.pi)
        if self.p_type == 'smoke':
            self.color = random.choice(SMOKE_PARTICLE_COLOR); self.lifespan = random.uniform(SMOKE_PARTICLE_LIFESPAN * 0.7, SMOKE_PARTICLE_LIFESPAN * 1.3); speed = random.uniform(SMOKE_PARTICLE_SPEED * 0.5, SMOKE_PARTICLE_SPEED * 1.5); self.size = random.uniform(SMOKE_PARTICLE_SIZE * 0.8, SMOKE_PARTICLE_SIZE * 1.2)
        else:
            self.color = random.choice(colors); self.lifespan = random.uniform(lifespan * 0.8, lifespan * 1.2); speed = random.uniform(speed_min, speed_max); self.size = random.uniform(size * 0.8, size * 1.2)
        self.vx = math.cos(angle) * speed; self.vy = math.sin(angle) * speed; self.start_life = self.lifespan;
    def update(self, dt):
        self.x += self.vx * dt; self.y += self.vy * dt;
        if self.p_type == 'smoke': self.vy += GRAVITY * 10 * dt; self.vx *= 0.95; self.vy *= 0.98
        else: self.vy += GRAVITY * 20 * dt
        self.lifespan -= dt;
        if self.start_life > 0: life_ratio = max(0, self.lifespan / self.start_life); current_size_base = SMOKE_PARTICLE_SIZE if self.p_type == 'smoke' else PARTICLE_SIZE; self.size = current_size_base * life_ratio
        else: self.size = 0
        return self.lifespan > 0 and self.size > 0.5
    def draw(self, screen):
        if self.size > 0:
            if self.p_type == 'smoke':
                 alpha = int(200 * max(0, (self.lifespan / self.start_life))); color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha); temp_surf = pygame.Surface((int(self.size), int(self.size)), pygame.SRCALPHA); pygame.draw.circle(temp_surf, color_with_alpha, (int(self.size/2), int(self.size/2)), int(self.size/2)); screen.blit(temp_surf, (int(self.x - self.size/2), int(self.y - self.size/2)))
            else: pygame.draw.rect(screen, self.color, (int(self.x - self.size/2), int(self.y - self.size/2), int(self.size), int(self.size)))

class ParachutePowerup: # ... (no change) ...
    def __init__(self):
        self.x = -100; self.y = -100; self.vy = POWERUP_DESCEND_SPEED; self.vx = 0
        self.width, self.height = POWERUP_BOX_SIZE; self.active = False
        self.chute_radius = 35; self.powerup_type = None
        self.id = random.randint(1, 1000000)
    def spawn(self):
        self.active = True; self.powerup_type = random.choice(POWERUP_TYPES)
        self.x = random.randint(GOAL_MARGIN_X + 50, SCREEN_WIDTH - GOAL_MARGIN_X - 50); self.y = -self.chute_radius * 2
        self.vx = random.uniform(-POWERUP_DRIFT_SPEED, POWERUP_DRIFT_SPEED); print(f"Powerup spawned: {self.powerup_type} at ({self.x:.0f}, {self.y:.0f})")
    def update(self, dt):
        if not self.active: return False
        self.y += self.vy * dt; self.x += self.vx * dt
        if self.x - self.width/2 < 0 or self.x + self.width/2 > SCREEN_WIDTH: self.vx *= -0.8
        if self.y - self.chute_radius > SCREEN_HEIGHT: self.active = False
        return self.active
    def get_box_rect(self):
        return pygame.Rect(self.x - self.width / 2, self.y, self.width, self.height)
    def check_collision(self, player):
        if not self.active: return None
        if player.is_tumbling: return None
        player_rect = player.get_body_rect(); powerup_box_rect = self.get_box_rect()
        if player_rect.colliderect(powerup_box_rect):
            print(f"Powerup collected: {self.powerup_type}")
            play_sound(loaded_sounds['combo'])
            return self.powerup_type
        return None
    def draw(self, screen):
        if not self.active: return
        box_rect = self.get_box_rect(); pygame.draw.rect(screen, POWERUP_BOX_COLOR, box_rect); pygame.draw.rect(screen, BLACK, box_rect, 1)
        chute_center_x = int(self.x); chute_top_y = int(self.y - self.chute_radius)
        chute_rect = pygame.Rect(0, 0, self.chute_radius * 2, self.chute_radius * 1.5); chute_rect.center = (chute_center_x, chute_top_y)
        num_panels = 6; angle_step = math.pi / num_panels
        for i in range(num_panels):
            angle1 = math.pi + i * angle_step; angle2 = math.pi + (i + 1) * angle_step
            color = POWERUP_CHUTE_ALT_COLOR if i % 2 == 0 else POWERUP_CHUTE_COLOR
            p1 = (chute_center_x, chute_top_y); p2 = (chute_center_x + self.chute_radius * math.cos(angle1), chute_top_y + self.chute_radius * 0.75 * math.sin(angle1)); p3 = (chute_center_x + self.chute_radius * math.cos(angle2), chute_top_y + self.chute_radius * 0.75 * math.sin(angle2))
            try: pygame.draw.polygon(screen, color, [p1, p2, p3])
            except ValueError: pass
        pygame.draw.ellipse(screen, BLACK, chute_rect, 1)
        string_points = [(box_rect.left + 3, box_rect.top), (box_rect.right - 3, box_rect.top), (box_rect.centerx, box_rect.top)]; chute_bottom_center = (chute_center_x, chute_top_y + int(self.chute_radius * 0.75))
        for point in string_points: pygame.draw.line(screen, BLACK, point, chute_bottom_center, 1)

class Rocket: # Removed reflect shield check
    def __init__(self, x, y, vx, vy, owner_player):
        self.x = x; self.y = y; self.vx = vx; self.vy = vy
        self.width, self.height = ROCKET_SIZE
        self.owner = owner_player; self.active = True
        self.angle = math.atan2(vy, vx)
        self.smoke_timer = 0
        self.last_pos = (x, y)
    def update(self, dt, players, puck): # Renamed ball -> puck
        global particles
        if not self.active: return False
        self.last_pos = (self.x, self.y)
        self.x += self.vx * dt; self.y += self.vy * dt
        self.angle = math.atan2(self.vy, self.vx)
        self.smoke_timer -= dt
        if self.smoke_timer <= 0:
            num_smoke = 1
            for _ in range(num_smoke):
                offset_dist = -(self.width / 2 + 3); smoke_x = self.x + math.cos(self.angle) * offset_dist; smoke_y = self.y + math.sin(self.angle) * offset_dist
                spread_angle = self.angle + math.pi + random.uniform(-0.5, 0.5); particles.append(Particle(smoke_x, smoke_y, p_type='smoke', angle_override=spread_angle))
            self.smoke_timer = 1 / (FPS * (SMOKE_EMISSION_RATE/10.0))
        exploded = False
        if self.x < -self.width or self.x > SCREEN_WIDTH + self.width or self.y < -self.height or self.y > SCREEN_HEIGHT + self.height:
            self.active = False; return False
        if self.y + self.height / 2 > GROUND_Y:
            self.y = GROUND_Y - self.height / 2; exploded = True
        rocket_rect = self.get_rect(); rocket_center_x, rocket_center_y = self.x, self.y
        for p in players:
            if p == self.owner: continue
            # Removed Reflect Shield check
            if p.get_body_rect().colliderect(rocket_rect): exploded = True; break
            if not exploded:
                head_pos, head_radius = p.get_head_position_radius()
                dist_sq_head = (rocket_center_x - head_pos[0])**2 + (rocket_center_y - head_pos[1])**2
                if dist_sq_head < (head_radius + max(self.width, self.height) / 2)**2: exploded = True; break
        if not exploded:
            puck_rect = pygame.Rect(puck.x - puck.radius, puck.y - puck.radius, puck.radius * 2, puck.radius * 2) # Use puck
            if puck_rect.colliderect(rocket_rect): exploded = True
        if exploded:
            self.active = False; create_explosion(self.x, self.y, puck.radius * ROCKET_BLAST_RADIUS_FACTOR, players, puck) # Use puck
            return True
        return False
    def get_rect(self):
        return pygame.Rect(self.x - max(self.width, self.height)/2, self.y - max(self.width, self.height)/2, max(self.width, self.height), max(self.width, self.height))
    def draw(self, screen):
        if not self.active: return
        draw_rotated_rectangle(screen, ROCKET_COLOR, (self.x, self.y), self.width, self.height, self.angle)

class Explosion: # ... (no change) ...
    def __init__(self, x, y, max_radius):
        self.x = x; self.y = y; self.max_radius = max_radius
        self.duration = ROCKET_EXPLOSION_DURATION; self.timer = self.duration
        self.active = True; self.current_radius = 0
    def update(self, dt):
        if not self.active: return False
        self.timer -= dt
        if self.timer <= 0: self.active = False; return False
        progress = 1.0 - (self.timer / self.duration)
        self.current_radius = self.max_radius * math.sin(progress * math.pi)
        return True
    def draw(self, screen):
        if not self.active or self.current_radius <= 0: return
        temp_surf = pygame.Surface((self.current_radius * 2, self.current_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surf, ROCKET_EXPLOSION_COLOR, (self.current_radius, self.current_radius), int(self.current_radius))
        screen.blit(temp_surf, (int(self.x - self.current_radius), int(self.y - self.current_radius)))

def create_explosion(x, y, radius, players, puck): # Renamed ball -> puck, added min bump
    global active_explosions
    print(f"Explosion created at ({x:.0f}, {y:.0f}) with radius {radius:.0f}")
    play_sound(loaded_sounds['wall_hit'])
    MIN_ROCKET_BUMP_SPEED = 2.0

    for p in players:
        dist_sq = (p.x - x)**2 + (p.y - y)**2
        if dist_sq < radius**2 and dist_sq > 0:
            dist = math.sqrt(dist_sq); force_magnitude = ROCKET_EXPLOSION_FORCE * (1.0 - (dist / radius))
            push_vec_x = (p.x - x) / dist; push_vec_y = (p.y - y) / dist
            explode_vx = push_vec_x * force_magnitude
            explode_vy = push_vec_y * force_magnitude * 0.8 - ROCKET_PLAYER_UPWARD_BOOST
            bump_vx = push_vec_x * MIN_ROCKET_BUMP_SPEED
            bump_vy = push_vec_y * MIN_ROCKET_BUMP_SPEED * 0.5
            p.vx += explode_vx + bump_vx
            p.vy += explode_vy + bump_vy
            p.is_jumping = True
            p.on_other_player_head = False
            p.start_tumble()
    dist_sq = (puck.x - x)**2 + (puck.y - y)**2
    if dist_sq < radius**2 and dist_sq > 0:
        dist = math.sqrt(dist_sq); force_magnitude = ROCKET_EXPLOSION_FORCE * (1.0 - (dist / radius))
        push_vec_x = (puck.x - x) / dist; push_vec_y = (puck.y - y) / dist
        puck.apply_force(push_vec_x * force_magnitude, push_vec_y * force_magnitude - ROCKET_BALL_UPWARD_BOOST, hitter='explosion')
    active_explosions.append(Explosion(x, y, radius))

class StickMan:
    def __init__(self, x, y, facing=1):
        self.x = x; self.y = y; self.base_y = y; self.width = 20; self.height = 80; self.vx = 0; self.vy = 0; self.is_jumping = False; self.is_kicking = False; self.kick_timer = 0; self.kick_duration = 18; self.walk_cycle_timer = 0.0;
        self.base_head_radius = 12; self.base_torso_length = 36; self.base_limb_width = 10; self.base_upper_arm_length = 12; self.base_forearm_length = 12; self.base_thigh_length = 14; self.base_shin_length = 14; self.base_nose_length = self.base_head_radius * 0.5; self.base_nose_width = self.base_head_radius * 0.3
        self.head_radius = self.base_head_radius; self.torso_length = self.base_torso_length; self.limb_width = self.base_limb_width; self.upper_arm_length = self.base_upper_arm_length; self.forearm_length = self.base_forearm_length; self.thigh_length = self.base_thigh_length; self.shin_length = self.base_shin_length; self.current_nose_length = self.base_nose_length; self.current_nose_width = self.base_nose_width
        self.l_upper_arm_angle = 0; self.r_upper_arm_angle = 0; self.l_forearm_angle = 0; self.r_forearm_angle = 0; self.l_thigh_angle = 0; self.r_thigh_angle = 0; self.l_shin_angle = 0; self.r_shin_angle = 0; self.head_pos = (0, 0); self.neck_pos = (0, 0); self.hip_pos = (0, 0); self.shoulder_pos = (0, 0); self.l_elbow_pos = (0, 0); self.r_elbow_pos = (0, 0); self.l_hand_pos = (0, 0); self.r_hand_pos = (0, 0); self.l_knee_pos = (0, 0); self.r_knee_pos = (0, 0); self.l_foot_pos = (0, 0); self.r_foot_pos = (0, 0); self.body_rect = pygame.Rect(0,0,0,0); self.facing_direction = facing; self.on_other_player_head = False
        self.wing_color = (173, 216, 230); self.wing_outline_color = (50, 50, 100); self.wing_rest_angle_offset = math.pi * 0.1 + (math.pi / 6); self.l_wing_base_angle = math.pi + self.wing_rest_angle_offset; self.r_wing_base_angle = -self.wing_rest_angle_offset; self.l_wing_upper_angle = self.l_wing_base_angle - 0.4; self.l_wing_lower_angle = self.l_wing_base_angle + 0.6; self.r_wing_upper_angle = self.r_wing_base_angle + 0.4; self.r_wing_lower_angle = self.r_wing_base_angle - 0.6; self.wing_flap_timer = 0.0; self.wing_flap_duration = 0.2; self.wing_flapping = False; self.wing_flap_magnitude = math.pi * 0.4; self.wing_upper_lobe_size = (30, 22); self.wing_lower_lobe_size = (28, 25)
        self.eye_color = BLACK
        self.team_color = TEAM1_COLOR; self.team_accent = TEAM1_ACCENT # Defaults, set after init
        self.torso_colors = [self.team_color, self.team_accent, self.team_color]; self.arm_colors = [self.team_accent, self.team_color]; self.leg_colors = [self.team_color, self.team_accent]
        self.cap_color = self.team_accent; self.cap_brim_color = BLACK
        self.active_powerups = {}
        self.is_flying = False; self.is_big = False; self.is_shrunk = False; self.is_enormous_head = False; self.is_penguin = False
        self.jump_power = BASE_JUMP_POWER; self.player_speed = BASE_PLAYER_SPEED; self.is_controls_reversed = False
        self.head_pulse_timer = 0.0
        self.gun_anim_timer = random.uniform(0, 2 * math.pi); self.gun_angle_offset = 0.0; self.gun_tip_pos = (0, 0)
        self.is_tumbling = False; self.tumble_timer = 0.0; self.rotation_angle = 0.0; self.rotation_velocity = 0.0

    def start_tumble(self):
        if not self.is_tumbling:
             self.is_tumbling = True; self.tumble_timer = TUMBLE_DURATION
             self.rotation_velocity = random.uniform(PLAYER_TUMBLE_ROT_SPEED_MIN, PLAYER_TUMBLE_ROT_SPEED_MAX) * random.choice([-1, 1])
             self.is_kicking = False; self.kick_timer = 0

    def apply_powerup(self, powerup_type, other_player=None): # Updated powerup logic
        current_val = self.active_powerups.get(powerup_type, 0)
        if powerup_type == "FLIGHT":
            self.active_powerups["FLIGHT"] = POWERUP_FLIGHT_DURATION; self.is_flying = True; print(f"Flight activated/refreshed: {POWERUP_FLIGHT_DURATION:.1f}s")
        elif powerup_type == "ROCKET_LAUNCHER":
            new_ammo = current_val + 3; self.active_powerups["ROCKET_LAUNCHER"] = new_ammo; print(f"Rocket Launcher ammo: {new_ammo}")
        elif powerup_type == "BIG_PLAYER":
            self.active_powerups["BIG_PLAYER"] = POWERUP_BIG_PLAYER_DURATION; self.is_big = True
            if "SHRUNK" in self.active_powerups: del self.active_powerups["SHRUNK"]; self.is_shrunk = False
            if "ENORMOUS_HEAD" in self.active_powerups: del self.active_powerups["ENORMOUS_HEAD"]; self.is_enormous_head = False
            self.calculate_current_sizes(); print(f"Big Player activated/refreshed: {POWERUP_BIG_PLAYER_DURATION:.1f}s")
        elif powerup_type == "SUPER_JUMP":
            self.active_powerups["SUPER_JUMP"] = POWERUP_SUPER_JUMP_DURATION
            self.jump_power = BASE_JUMP_POWER * POWERUP_SUPER_JUMP_MULTIPLIER; print(f"Super Jump activated/refreshed: {POWERUP_SUPER_JUMP_DURATION:.1f}s")
        elif powerup_type == "SPEED_BOOST":
            self.active_powerups["SPEED_BOOST"] = POWERUP_SPEED_BOOST_DURATION
            self.player_speed = BASE_PLAYER_SPEED * POWERUP_SPEED_BOOST_MULTIPLIER; print(f"Speed Boost activated/refreshed: {POWERUP_SPEED_BOOST_DURATION:.1f}s")
        elif powerup_type == "SHRINK_OPPONENT":
            if other_player: other_player.apply_shrink()
        elif powerup_type == "GOAL_SHIELD":
             if self is player1: global p1_shield_active, p1_shield_timer; p1_shield_timer += POWERUP_GOAL_SHIELD_DURATION; p1_shield_active = True; print(f"P1 Shield extended: {p1_shield_timer:.1f}s")
             elif self is player2: global p2_shield_active, p2_shield_timer; p2_shield_timer += POWERUP_GOAL_SHIELD_DURATION; p2_shield_active = True; print(f"P2 Shield extended: {p2_shield_timer:.1f}s")
        elif powerup_type == "BALL_FREEZE":
             global ball_freeze_timer
             ball_freeze_timer += POWERUP_BALL_FREEZE_DURATION
             puck.is_frozen = True; puck.freeze_effect_timer = 0; print(f"Puck Freeze extended: {ball_freeze_timer:.1f}s")
             puck.vx = 0; puck.vy = 0
        elif powerup_type == "LOW_GRAVITY":
             self.active_powerups["LOW_GRAVITY"] = POWERUP_LOW_GRAVITY_DURATION; print(f"Low Gravity activated: {POWERUP_LOW_GRAVITY_DURATION:.1f}s")
        elif powerup_type == "REVERSE_CONTROLS":
             if other_player: other_player.apply_reverse_controls()
        elif powerup_type == "ENORMOUS_HEAD":
             self.active_powerups["ENORMOUS_HEAD"] = POWERUP_ENORMOUS_HEAD_DURATION; self.is_enormous_head = True
             if "SHRUNK" in self.active_powerups: del self.active_powerups["SHRUNK"]; self.is_shrunk = False
             self.calculate_current_sizes(); print(f"Enormous Head activated: {POWERUP_ENORMOUS_HEAD_DURATION:.1f}s")
        elif powerup_type == "GOAL_ENLARGER":
             if self is player1: global p2_goal_enlarged_timer; p2_goal_enlarged_timer = POWERUP_GOAL_ENLARGER_DURATION; print("P2 Goal Enlarged!")
             elif self is player2: global p1_goal_enlarged_timer; p1_goal_enlarged_timer = POWERUP_GOAL_ENLARGER_DURATION; print("P1 Goal Enlarged!")
        elif powerup_type == "PENGUIN":
             self.active_powerups["PENGUIN"] = POWERUP_PENGUIN_DURATION; self.is_penguin = True; print(f"Penguin Mode! {POWERUP_PENGUIN_DURATION:.1f}s")

    def apply_shrink(self):
         self.active_powerups["SHRUNK"] = POWERUP_SHRINK_PLAYER_DURATION; self.is_shrunk = True
         if "BIG_PLAYER" in self.active_powerups: del self.active_powerups["BIG_PLAYER"]; self.is_big = False
         if "ENORMOUS_HEAD" in self.active_powerups: del self.active_powerups["ENORMOUS_HEAD"]; self.is_enormous_head = False
         self.calculate_current_sizes()
         print(f"Player shrunk for {POWERUP_SHRINK_PLAYER_DURATION}s")
    def apply_reverse_controls(self):
        print(f"Player {1 if self.facing_direction==1 else 2} controls reversed!")
        self.active_powerups["REVERSE_CONTROLS"] = POWERUP_REVERSE_CONTROLS_DURATION
        self.is_controls_reversed = True
    def apply_force_push(self, opponent, ball): pass
    def calculate_current_sizes(self):
        body_scale = 1.0
        if self.is_big: body_scale = POWERUP_BIG_PLAYER_SCALE
        elif self.is_shrunk: body_scale = POWERUP_SHRINK_PLAYER_SCALE
        self.torso_length = self.base_torso_length * body_scale
        self.limb_width = self.base_limb_width * (1.0 + (body_scale - 1.0) * 0.5)
        self.upper_arm_length = self.base_upper_arm_length * body_scale; self.forearm_length = self.base_forearm_length * body_scale
        self.thigh_length = self.base_thigh_length * body_scale; self.shin_length = self.base_shin_length * body_scale

        head_scale = body_scale
        if self.is_enormous_head:
            pulse_factor = (math.sin(self.head_pulse_timer) + 1) / 2
            pulse_amount = 0.15
            effective_head_scale = POWERUP_ENORMOUS_HEAD_SCALE * (1.0 - pulse_amount + pulse_factor * pulse_amount * 2)
            head_scale = effective_head_scale
        self.head_radius = self.base_head_radius * head_scale
        self.current_nose_length = self.base_nose_length * head_scale
        self.current_nose_width = self.base_nose_width * head_scale
    def move(self, direction):
        if self.is_tumbling: return
        move_direction = direction
        if self.is_controls_reversed: move_direction *= -1
        if not self.is_kicking: self.vx = move_direction * self.player_speed
        if direction != 0 and not self.is_penguin: self.facing_direction = direction
    def stop_move(self):
        if self.is_tumbling: return
        if not self.is_penguin: self.vx = 0
    def jump(self):
        if self.is_tumbling: return
        can_jump_now = False
        if "FLIGHT" in self.active_powerups:
            if not self.is_kicking: can_jump_now = True
        else:
            if (not self.is_jumping or self.on_other_player_head) and not self.is_kicking: can_jump_now = True
        if can_jump_now:
            was_on_head = self.on_other_player_head; play_sound(loaded_sounds['jump']);
            if was_on_head: play_sound(loaded_sounds['combo'])
            self.is_jumping = True; self.on_other_player_head = False
            self.vy = self.jump_power; self.walk_cycle_timer = 0
            if "FLIGHT" in self.active_powerups: self.start_wing_flap()
    def start_hit(self): # Renamed
        if self.is_tumbling: return
        if not self.is_kicking:
            if "ROCKET_LAUNCHER" in self.active_powerups: self.fire_rocket()
            else: self.is_kicking = True; self.kick_timer = 0; self.vx = 0
    def fire_rocket(self): # Renamed from fire_kick
        global active_rockets
        if "ROCKET_LAUNCHER" not in self.active_powerups: return
        ammo = self.active_powerups["ROCKET_LAUNCHER"]
        if ammo <= 0: return
        print(f"Player {1 if self.facing_direction == 1 else 2} firing rocket! ({ammo-1} left)")
        play_sound(loaded_sounds['kick'])
        base_angle = 0 if self.facing_direction == 1 else math.pi; laser_world_angle = base_angle + self.gun_angle_offset
        start_x, start_y = self.gun_tip_pos
        rocket_vx = ROCKET_SPEED * math.cos(laser_world_angle); rocket_vy = ROCKET_SPEED * math.sin(laser_world_angle)
        active_rockets.append(Rocket(start_x, start_y, rocket_vx, rocket_vy, self))
        ammo -= 1
        if ammo <= 0: del self.active_powerups["ROCKET_LAUNCHER"]
        else: self.active_powerups["ROCKET_LAUNCHER"] = ammo
    def start_wing_flap(self): # ... (no change) ...
         if not self.wing_flapping: self.wing_flapping = True; self.wing_flap_timer = self.wing_flap_duration
    def randomize_nose(self): # ... (no change) ...
        random_factor = random.uniform(1.0, 5.0); self.current_nose_length = self.base_nose_length * random_factor; self.current_nose_width = self.base_nose_width * random_factor; self.current_nose_width = min(self.current_nose_width, self.current_nose_length * 0.8)
    def update(self, dt, other_player):
        if self.is_tumbling:
            self.tumble_timer -= dt
            if self.tumble_timer <= 0: self.is_tumbling = False; self.tumble_timer = 0.0; self.rotation_angle = 0.0; self.rotation_velocity = 0.0; print(f"Player {1 if self is player1 else 2} finished tumble.")
            else: self.rotation_angle += self.rotation_velocity * dt; self.rotation_velocity *= (PLAYER_TUMBLE_DAMPING ** (dt * 60))
        expired_powerups = []
        for p_type, value in list(self.active_powerups.items()):
            if p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD", "PENGUIN"]:
                new_timer = value - dt
                if new_timer <= 0:
                    expired_powerups.append(p_type)
                    if p_type == "FLIGHT": self.is_flying = False; print("Flight ended")
                    elif p_type == "BIG_PLAYER": self.is_big = False; self.calculate_current_sizes(); print("Big Player ended")
                    elif p_type == "SHRUNK": self.is_shrunk = False; self.calculate_current_sizes(); print("Shrink ended")
                    elif p_type == "SUPER_JUMP": self.jump_power = BASE_JUMP_POWER; print("Super Jump ended")
                    elif p_type == "SPEED_BOOST": self.player_speed = BASE_PLAYER_SPEED; print("Speed Boost ended")
                    elif p_type == "LOW_GRAVITY": print("Low Gravity ended")
                    elif p_type == "REVERSE_CONTROLS": self.is_controls_reversed = False; print("Controls Restored")
                    elif p_type == "ENORMOUS_HEAD": self.is_enormous_head = False; self.calculate_current_sizes(); print("Enormous Head ended")
                    elif p_type == "PENGUIN": self.is_penguin = False; print("Penguin mode ended")
                else:
                    self.active_powerups[p_type] = new_timer
        for p_type in expired_powerups:
            if p_type in self.active_powerups: del self.active_powerups[p_type]
        if "ROCKET_LAUNCHER" in self.active_powerups: self.gun_anim_timer += dt * GUN_ANIM_SPEED; self.gun_angle_offset = math.sin(self.gun_anim_timer) * GUN_ANIM_MAGNITUDE
        if self.is_enormous_head: self.head_pulse_timer += dt * 5.0; self.calculate_current_sizes()

        current_gravity = GRAVITY * POWERUP_LOW_GRAVITY_FACTOR if "LOW_GRAVITY" in self.active_powerups else GRAVITY
        current_friction = PENGUIN_FRICTION_FACTOR if self.is_penguin else PLAYER_FRICTION

        was_airborne = self.is_jumping or (not self.on_other_player_head and self.y < self.base_y); time_ms = pygame.time.get_ticks()
        was_on_head = self.on_other_player_head; landed_on_head_this_frame = False; landed_on_ground_this_frame = False
        platform_y = self.base_y; other_head_pos, other_head_radius = other_player.get_head_position_radius()
        head_top_y = other_head_pos[1] - other_head_radius; dist_x_head = self.x - other_head_pos[0]
        is_aligned_for_head = abs(dist_x_head) < (other_head_radius + self.head_radius + HEAD_PLATFORM_RADIUS_BUFFER)
        if not was_on_head: self.vy += current_gravity
        elif was_on_head and not is_aligned_for_head: self.on_other_player_head = False; self.is_jumping = True; self.vy += current_gravity
        elif was_on_head and is_aligned_for_head: self.y = head_top_y; self.vy = 0
        next_y = self.y + self.vy
        if self.vy >= 0:
            can_land_on_head_now = (is_aligned_for_head and next_y >= head_top_y and self.y < head_top_y + 5)
            if can_land_on_head_now:
                self.y = head_top_y; self.vy = 0; self.is_jumping = False; self.on_other_player_head = True; landed_on_head_this_frame = True
                if self.is_tumbling: self.vy *= -0.3
                if other_player.is_enormous_head: print("Bounce on enormous head!"); self.vy = BASE_JUMP_POWER * HEAD_BOUNCE_MULTIPLIER
            elif not landed_on_head_this_frame and next_y >= self.base_y:
                self.y = self.base_y; self.vy = 0; self.is_jumping = False; self.on_other_player_head = False; landed_on_ground_this_frame = True
                if self.is_tumbling: self.rotation_velocity *= 0.8; self.vx *= 0.8
            else: self.y = next_y;
            if self.y < self.base_y and not landed_on_head_this_frame: self.on_other_player_head = False
        else: self.y = next_y; self.on_other_player_head = False
        if self.y > self.base_y and not self.on_other_player_head: self.y = self.base_y;
        if self.vy > 0 and self.y == self.base_y: self.vy = 0; self.is_jumping = False;
        is_now_grounded = landed_on_ground_this_frame or landed_on_head_this_frame
        if was_airborne and is_now_grounded and not self.is_tumbling: play_sound(loaded_sounds['land'])

        intended_vx = self.vx
        if not self.is_kicking:
            effective_vx = intended_vx
            if self.on_other_player_head: effective_vx += other_player.vx
            if self.is_tumbling and not self.on_other_player_head and self.y < self.base_y:
                 self.vx *= 0.99; effective_vx = self.vx
            self.x += effective_vx
            self.x = max(self.limb_width / 2, min(self.x, SCREEN_WIDTH - self.limb_width / 2))

        if not self.is_kicking and is_now_grounded and self.vx != 0:
             if (self.vx > 0 and intended_vx <= 0) or (self.vx < 0 and intended_vx >= 0) or self.is_penguin:
                 self.vx *= current_friction

        if "FLIGHT" in self.active_powerups:
            rest_l_base = math.pi * 0.8; rest_r_base = math.pi * 0.2; flap_down_l_base = rest_l_base + self.wing_flap_magnitude; flap_down_r_base = rest_r_base - self.wing_flap_magnitude
            if self.wing_flapping:
                self.wing_flap_timer -= dt
                if self.wing_flap_timer <= 0: self.wing_flapping = False; self.wing_flap_timer = 0.0; self.l_wing_base_angle = rest_l_base; self.r_wing_base_angle = rest_r_base
                else: progress = 1.0 - (self.wing_flap_timer / self.wing_flap_duration); flap_phase = math.sin(progress * math.pi); self.l_wing_base_angle = rest_l_base + (flap_down_l_base - rest_l_base) * flap_phase; self.r_wing_base_angle = rest_r_base + (flap_down_r_base - rest_r_base) * flap_phase
            else: lerp_speed = 6.0 * dt; self.l_wing_base_angle += (rest_l_base - self.l_wing_base_angle) * lerp_speed; self.r_wing_base_angle += (rest_r_base - self.r_wing_base_angle) * lerp_speed
            self.l_wing_upper_angle = self.l_wing_base_angle - 0.4; self.l_wing_lower_angle = self.l_wing_base_angle + 0.6; self.r_wing_upper_angle = self.r_wing_base_angle + 0.4; self.r_wing_lower_angle = self.r_wing_base_angle - 0.6
        if not self.is_tumbling and not self.is_penguin:
            is_walking = abs(intended_vx) > 0 and not self.is_jumping and not self.is_kicking and not self.on_other_player_head
            if is_walking: self.walk_cycle_timer += WALK_CYCLE_SPEED
            elif not self.is_jumping and not self.is_kicking: self.walk_cycle_timer *= 0.9
            if abs(self.walk_cycle_timer) < 0.1: self.walk_cycle_timer = 0
            if self.is_kicking:
                 self.walk_cycle_timer = 0; self.kick_timer += 1; progress = min(self.kick_timer / self.kick_duration, 1.0); windup_end = 0.20; impact_start = 0.25; impact_end = 0.50; follow_end = 1.0
                 if progress < windup_end: thigh_prog_angle = HIT_THIGH_WINDUP_ANGLE * (progress / windup_end)
                 elif progress < impact_end: impact_progress = (progress - windup_end) / (impact_end - windup_end); thigh_prog_angle = HIT_THIGH_WINDUP_ANGLE + (HIT_THIGH_FOLLOW_ANGLE - HIT_THIGH_WINDUP_ANGLE) * impact_progress
                 else: follow_progress = (progress - impact_end) / (follow_end - impact_end); ease_out_factor = 1.0 - follow_progress**1.5; thigh_prog_angle = HIT_THIGH_FOLLOW_ANGLE * ease_out_factor
                 if progress < impact_start: shin_prog_angle = HIT_SHIN_WINDUP_ANGLE * (progress / impact_start)
                 elif progress < impact_end: impact_progress = (progress - impact_start) / (impact_end - impact_start); ease_in_factor = impact_progress ** 2; shin_prog_angle = HIT_SHIN_WINDUP_ANGLE + (HIT_SHIN_IMPACT_ANGLE - HIT_SHIN_WINDUP_ANGLE) * ease_in_factor
                 else: follow_progress = (progress - impact_end) / (follow_end - impact_end); shin_prog_angle = HIT_SHIN_IMPACT_ANGLE + (HIT_SHIN_FOLLOW_ANGLE - HIT_SHIN_IMPACT_ANGLE) * follow_progress
                 kick_direction_multiplier = self.facing_direction
                 if kick_direction_multiplier == 1: self.r_thigh_angle = thigh_prog_angle; self.r_shin_angle = shin_prog_angle; self.l_thigh_angle = -thigh_prog_angle * 0.3; self.l_shin_angle = 0.3
                 else: self.l_thigh_angle = thigh_prog_angle * kick_direction_multiplier; self.l_shin_angle = shin_prog_angle; self.r_thigh_angle = -thigh_prog_angle * 0.3 * kick_direction_multiplier; self.r_shin_angle = 0.3
                 base_thigh_abs = abs(thigh_prog_angle); self.l_upper_arm_angle = -base_thigh_abs * 0.15 if self.facing_direction == 1 else base_thigh_abs * 0.12; self.r_upper_arm_angle = base_thigh_abs * 0.12 if self.facing_direction == 1 else -base_thigh_abs * 0.15
                 self.l_forearm_angle = 0.2; self.r_forearm_angle = 0.2
                 if self.kick_timer >= self.kick_duration: self.is_kicking = False; self.kick_timer = 0;
            else:
                 if is_walking: walk_sin = math.sin(self.walk_cycle_timer); self.l_upper_arm_angle = RUN_UPPER_ARM_SWING * walk_sin * self.facing_direction; self.r_upper_arm_angle = -RUN_UPPER_ARM_SWING * walk_sin * self.facing_direction; self.l_forearm_angle = RUN_FOREARM_SWING * math.sin(self.walk_cycle_timer - RUN_FOREARM_OFFSET_FACTOR) * self.facing_direction; self.r_forearm_angle = -RUN_FOREARM_SWING * math.sin(self.walk_cycle_timer - RUN_FOREARM_OFFSET_FACTOR) * self.facing_direction; self.l_thigh_angle = -LEG_THIGH_SWING * walk_sin * self.facing_direction; self.r_thigh_angle = LEG_THIGH_SWING * walk_sin * self.facing_direction; shin_bend = LEG_SHIN_BEND_WALK * max(0, math.sin(self.walk_cycle_timer + LEG_SHIN_BEND_SHIFT)); self.l_shin_angle = shin_bend if self.l_thigh_angle * self.facing_direction < 0 else 0.1; self.r_shin_angle = shin_bend if self.r_thigh_angle * self.facing_direction < 0 else 0.1
                 elif self.is_jumping and not self.on_other_player_head: base_up_angle = JUMP_UPPER_ARM_BASE - self.vy * JUMP_UPPER_ARM_VY_FACTOR; self.l_upper_arm_angle = base_up_angle; self.r_upper_arm_angle = base_up_angle; base_fore_angle = JUMP_FOREARM_BASE; self.l_forearm_angle = base_fore_angle; self.r_forearm_angle = base_fore_angle; jump_progress = max(0, min(1, 1 - (self.y / self.base_y))); thigh_tuck = JUMP_THIGH_TUCK * jump_progress; shin_tuck = JUMP_SHIN_TUCK * jump_progress; self.l_thigh_angle = thigh_tuck; self.r_thigh_angle = thigh_tuck; self.l_shin_angle = shin_tuck; self.r_shin_angle = shin_tuck
                 else: self.l_upper_arm_angle = 0; self.r_upper_arm_angle = 0; self.l_forearm_angle = 0; self.r_forearm_angle = 0; self.l_thigh_angle = 0; self.r_thigh_angle = 0; self.l_shin_angle = 0; self.r_shin_angle = 0
        elif self.is_tumbling:
            tumble_speed = self.rotation_velocity * 1.5; current_time_ms = pygame.time.get_ticks()
            self.l_upper_arm_angle = math.sin(current_time_ms * 0.01 + 1) * 0.8 + tumble_speed * 0.05
            self.r_upper_arm_angle = math.sin(current_time_ms * 0.01 + 2) * 0.8 - tumble_speed * 0.05
            self.l_forearm_angle = math.sin(current_time_ms * 0.015 + 3) * 1.2
            self.r_forearm_angle = math.sin(current_time_ms * 0.015 + 4) * 1.2
            self.l_thigh_angle = math.sin(current_time_ms * 0.01 + 5) * 0.6 - tumble_speed * 0.04
            self.r_thigh_angle = math.sin(current_time_ms * 0.01 + 6) * 0.6 + tumble_speed * 0.04
            self.l_shin_angle = math.sin(current_time_ms * 0.015 + 7) * 1.0
            self.r_shin_angle = math.sin(current_time_ms * 0.015 + 0) * 1.0
        else: # Penguin state (not tumbling)
            self.l_upper_arm_angle = math.pi * 0.05; self.r_upper_arm_angle = -math.pi * 0.05
            self.l_forearm_angle = math.pi * 0.1; self.r_forearm_angle = -math.pi * 0.1
            self.l_thigh_angle = 0; self.r_thigh_angle = 0
            self.l_shin_angle = 0; self.r_shin_angle = 0

        # --- Calculate Joint Positions ---
        current_y = self.y; current_x = self.x
        total_leg_visual_height = self.thigh_length + self.shin_length
        self.hip_pos = (current_x, current_y - total_leg_visual_height)
        upper_body_x = current_x
        self.neck_pos = (upper_body_x, self.hip_pos[1] - self.torso_length)
        self.head_pos = (upper_body_x, self.neck_pos[1] - self.head_radius)
        self.shoulder_pos = self.neck_pos
        l_elbow_x = self.shoulder_pos[0] + self.upper_arm_length * math.sin(self.l_upper_arm_angle); l_elbow_y = self.shoulder_pos[1] + self.upper_arm_length * math.cos(self.l_upper_arm_angle); self.l_elbow_pos = (l_elbow_x, l_elbow_y); l_hand_angle_world = self.l_upper_arm_angle + self.l_forearm_angle; l_hand_x = self.l_elbow_pos[0] + self.forearm_length * math.sin(l_hand_angle_world); l_hand_y = self.l_elbow_pos[1] + self.forearm_length * math.cos(l_hand_angle_world); self.l_hand_pos = (l_hand_x, l_hand_y);
        r_elbow_x = self.shoulder_pos[0] + self.upper_arm_length * math.sin(self.r_upper_arm_angle); r_elbow_y = self.shoulder_pos[1] + self.upper_arm_length * math.cos(self.r_upper_arm_angle); self.r_elbow_pos = (r_elbow_x, r_elbow_y); r_hand_angle_world = self.r_upper_arm_angle + self.r_forearm_angle; r_hand_x = self.r_elbow_pos[0] + self.forearm_length * math.sin(r_hand_angle_world); r_hand_y = self.r_elbow_pos[1] + self.forearm_length * math.cos(r_hand_angle_world); self.r_hand_pos = (r_hand_x, r_hand_y);
        l_knee_x = self.hip_pos[0] + self.thigh_length * math.sin(self.l_thigh_angle); l_knee_y = self.hip_pos[1] + self.thigh_length * math.cos(self.l_thigh_angle); self.l_knee_pos = (l_knee_x, l_knee_y); l_foot_angle_world = self.l_thigh_angle + self.l_shin_angle; l_foot_x = self.l_knee_pos[0] + self.shin_length * math.sin(l_foot_angle_world); l_foot_y = self.l_knee_pos[1] + self.shin_length * math.cos(l_foot_angle_world); self.l_foot_pos = (l_foot_x, l_foot_y);
        r_knee_x = self.hip_pos[0] + self.thigh_length * math.sin(self.r_thigh_angle); r_knee_y = self.hip_pos[1] + self.thigh_length * math.cos(self.r_thigh_angle); self.r_knee_pos = (r_knee_x, r_knee_y); r_foot_angle_world = self.r_thigh_angle + self.r_shin_angle; r_foot_x = self.r_knee_pos[0] + self.shin_length * math.sin(r_foot_angle_world); r_foot_y = self.r_knee_pos[1] + self.shin_length * math.cos(r_foot_angle_world)
        self.l_foot_pos = (l_foot_x, l_foot_y); self.r_foot_pos = (r_foot_x, r_foot_y)

        # --- Update Body Rect ---
        body_width = self.limb_width * 1.5
        self.body_rect.width = int(body_width)
        self.body_rect.height = max(1, int(self.hip_pos[1] - self.neck_pos[1]))
        self.body_rect.centerx = int(self.hip_pos[0])
        self.body_rect.top = int(self.neck_pos[1])

    def get_hit_impact_point(self): # Renamed
        impact_start = 0.25; impact_end = 0.6
        if self.is_kicking:
            if self.kick_duration <= 0: return None
            progress = self.kick_timer / self.kick_duration
            if impact_start < progress < impact_end: return self.r_foot_pos if self.facing_direction == 1 else self.l_foot_pos
        return None
    def get_head_position_radius(self): return self.head_pos, self.head_radius
    def get_body_rect(self): return self.body_rect
    def draw(self, screen):
        if self.is_penguin:
            body_scale = self.head_radius / self.base_head_radius
            body_width = 25 * body_scale; body_height = 55 * body_scale
            body_center_x = int(self.x); body_bottom_y = int(self.y)
            body_rect = pygame.Rect(0, 0, body_width, body_height); body_rect.midbottom = (body_center_x, body_bottom_y)
            belly_width = body_width * 0.7; belly_height = body_height * 0.8
            belly_rect = pygame.Rect(0, 0, belly_width, belly_height); belly_rect.center = body_rect.center; belly_rect.top += body_height * 0.1
            foot_width = body_width * 0.4; foot_height = 10 * body_scale
            left_foot_rect = pygame.Rect(0, 0, foot_width, foot_height); left_foot_rect.midtop = (body_rect.centerx - body_width * 0.25, body_rect.bottom - foot_height * 0.5)
            right_foot_rect = pygame.Rect(0, 0, foot_width, foot_height); right_foot_rect.midtop = (body_rect.centerx + body_width * 0.25, body_rect.bottom - foot_height * 0.5)
            beak_width = self.head_radius * 0.6 ; beak_height = self.head_radius * 0.4
            beak_center_y = body_rect.top + self.head_radius * 0.8
            beak_x = body_rect.centerx + (self.head_radius * 0.4) * self.facing_direction
            beak_tip_x = beak_x + beak_width * self.facing_direction
            beak_points = [(beak_x, beak_center_y - beak_height / 2), (beak_tip_x, beak_center_y), (beak_x, beak_center_y + beak_height / 2)]
            flipper_width = 10 * body_scale; flipper_height = body_height * 0.4
            flipper_angle = math.pi / 8 * math.sin(self.walk_cycle_timer * 4) # Waddle flap based on walk timer
            left_flipper_center = (body_rect.left - flipper_width/3 , body_rect.centery)
            right_flipper_center = (body_rect.right + flipper_width/3, body_rect.centery)

            if self.is_tumbling and self.rotation_angle != 0:
                 bounds = body_rect.inflate(flipper_width*2, foot_height*2)
                 penguin_surf = pygame.Surface(bounds.size, pygame.SRCALPHA)
                 offset_x = -bounds.left; offset_y = -bounds.top
                 body_rect_off = body_rect.move(offset_x, offset_y); belly_rect_off = belly_rect.move(offset_x, offset_y); left_foot_rect_off = left_foot_rect.move(offset_x, offset_y); right_foot_rect_off = right_foot_rect.move(offset_x, offset_y)
                 beak_points_off = [(p[0] + offset_x, p[1] + offset_y) for p in beak_points]; left_flipper_center_off = (left_flipper_center[0] + offset_x, left_flipper_center[1] + offset_y); right_flipper_center_off = (right_flipper_center[0] + offset_x, right_flipper_center[1] + offset_y)
                 pygame.draw.ellipse(penguin_surf, PENGUIN_BODY_COLOR, body_rect_off); pygame.draw.ellipse(penguin_surf, PENGUIN_BELLY_COLOR, belly_rect_off); pygame.draw.ellipse(penguin_surf, PENGUIN_BEAK_FEET_COLOR, left_foot_rect_off); pygame.draw.ellipse(penguin_surf, PENGUIN_BEAK_FEET_COLOR, right_foot_rect_off); pygame.draw.polygon(penguin_surf, PENGUIN_BEAK_FEET_COLOR, beak_points_off)
                 draw_rotated_rectangle(penguin_surf, PENGUIN_BODY_COLOR, left_flipper_center_off, flipper_width, flipper_height, -math.pi/2 -flipper_angle); draw_rotated_rectangle(penguin_surf, PENGUIN_BODY_COLOR, right_flipper_center_off, flipper_width, flipper_height, math.pi/2 + flipper_angle)
                 pygame.draw.ellipse(penguin_surf, BLACK, body_rect_off, 1)
                 rotated_penguin = pygame.transform.rotate(penguin_surf, -math.degrees(self.rotation_angle))
                 blit_rect = rotated_penguin.get_rect(center=(body_center_x, body_rect.centery))
                 screen.blit(rotated_penguin, blit_rect.topleft)
            else:
                 pygame.draw.ellipse(screen, PENGUIN_BODY_COLOR, body_rect); pygame.draw.ellipse(screen, PENGUIN_BELLY_COLOR, belly_rect); pygame.draw.ellipse(screen, PENGUIN_BEAK_FEET_COLOR, left_foot_rect); pygame.draw.ellipse(screen, PENGUIN_BEAK_FEET_COLOR, right_foot_rect); pygame.draw.polygon(screen, PENGUIN_BEAK_FEET_COLOR, beak_points)
                 draw_rotated_rectangle(screen, PENGUIN_BODY_COLOR, left_flipper_center, flipper_width, flipper_height, -math.pi/2 -flipper_angle); draw_rotated_rectangle(screen, PENGUIN_BODY_COLOR, right_flipper_center, flipper_width, flipper_height, math.pi/2 + flipper_angle)
                 pygame.draw.ellipse(screen, BLACK, body_rect, 1)
        else: # --- Normal Stickman Drawing ---
            all_points = [self.head_pos, self.neck_pos, self.hip_pos, self.shoulder_pos, self.l_elbow_pos, self.r_elbow_pos, self.l_hand_pos, self.r_hand_pos, self.l_knee_pos, self.r_knee_pos, self.l_foot_pos, self.r_foot_pos]
            if "ROCKET_LAUNCHER" in self.active_powerups: all_points.append(self.gun_tip_pos)
            min_x = min(p[0] for p in all_points) - self.head_radius - self.limb_width; max_x = max(p[0] for p in all_points) + self.head_radius + self.limb_width
            min_y = min(p[1] for p in all_points) - self.head_radius - self.limb_width; max_y = max(p[1] for p in all_points) + self.head_radius + self.limb_width
            if "FLIGHT" in self.active_powerups:
                 min_x = min(min_x, self.shoulder_pos[0] - self.wing_upper_lobe_size[0] - 10); max_x = max(max_x, self.shoulder_pos[0] + self.wing_upper_lobe_size[0] + 10)
                 min_y = min(min_y, self.shoulder_pos[1] - self.wing_upper_lobe_size[1] - 10); max_y = max(max_y, self.hip_pos[1] + self.wing_lower_lobe_size[1] + 10)
            surf_width = max(1, int(max_x - min_x)); surf_height = max(1, int(max_y - min_y))
            temp_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
            offset_x = -min_x; offset_y = -min_y
            def offset_pos(pos): return (pos[0] + offset_x, pos[1] + offset_y)
            head_center_int = offset_pos(self.head_pos)
            cap_height = self.head_radius * 0.8; cap_width = self.head_radius * 1.8; cap_rect = pygame.Rect(0, 0, cap_width, cap_height); cap_rect.center = (head_center_int[0], head_center_int[1] - self.head_radius * 0.5); pygame.draw.ellipse(temp_surf, self.cap_color, cap_rect)
            brim_width = self.head_radius * 1.2; brim_height = self.head_radius * 0.4; brim_x = head_center_int[0] + (self.head_radius * 0.5) * self.facing_direction; brim_y = cap_rect.centery + cap_height * 0.1; brim_rect = pygame.Rect(0, 0, brim_width, brim_height); brim_rect.center = (brim_x, brim_y); pygame.draw.rect(temp_surf, self.cap_brim_color, brim_rect)
            pygame.draw.circle(temp_surf, RINK_WHITE, head_center_int, int(self.head_radius), 0)
            eye_offset_x = self.head_radius * 0.35 * self.facing_direction; eye_offset_y = -self.head_radius * 0.1; eye_radius = int(max(1, 3 * (self.head_radius / self.base_head_radius)))
            eye_pos_x = int(head_center_int[0] + eye_offset_x); eye_y = int(head_center_int[1] + eye_offset_y)
            pygame.draw.circle(temp_surf, self.eye_color, (eye_pos_x, eye_y - eye_radius // 2 - 1), eye_radius); pygame.draw.circle(temp_surf, self.eye_color, (eye_pos_x, eye_y + eye_radius // 2 + 1), eye_radius)
            nose_tip_x = head_center_int[0] + (self.head_radius * 0.5 + self.current_nose_length) * self.facing_direction; nose_tip_y = head_center_int[1] + self.head_radius * 0.1
            nose_base_x = head_center_int[0] + (self.head_radius * 0.3) * self.facing_direction; nose_base_y1 = nose_tip_y - self.current_nose_width / 2; nose_base_y2 = nose_tip_y + self.current_nose_width / 2
            nose_points = [(int(nose_base_x), int(nose_base_y1)), (int(nose_tip_x), int(nose_tip_y)), (int(nose_base_x), int(nose_base_y2))]; pygame.draw.polygon(temp_surf, NOSE_COLOR, nose_points)
            pygame.draw.circle(temp_surf, BLACK, head_center_int, int(self.head_radius), 1)
            torso_start_pos = offset_pos(self.neck_pos); torso_segment_height = self.torso_length / 3; current_torso_y = torso_start_pos[1]
            for i in range(3): rect_center_x = torso_start_pos[0]; rect_center_y = current_torso_y + torso_segment_height / 2; draw_rotated_rectangle(temp_surf, self.team_color if i % 2 == 0 else self.team_accent, (rect_center_x, rect_center_y), self.limb_width, torso_segment_height, 0); current_torso_y += torso_segment_height
            def draw_limb_segment_offset(start_pos, end_pos, length, color, limb_w):
                o_start = offset_pos(start_pos); o_end = offset_pos(end_pos); center_x = (o_start[0] + o_end[0]) / 2; center_y = (o_start[1] + o_end[1]) / 2
                dx = o_end[0] - o_start[0]; dy = o_end[1] - o_start[1]; draw_length = math.hypot(dx, dy);
                if draw_length < 1: draw_length = 1
                angle = math.atan2(dy, dx); draw_rotated_rectangle(temp_surf, color, (center_x, center_y), draw_length, limb_w, angle + math.pi/2)
            draw_limb_segment_offset(self.shoulder_pos, self.l_elbow_pos, self.upper_arm_length, self.team_accent, self.limb_width); draw_limb_segment_offset(self.l_elbow_pos, self.l_hand_pos, self.forearm_length, self.team_color, self.limb_width)
            draw_limb_segment_offset(self.shoulder_pos, self.r_elbow_pos, self.upper_arm_length, self.team_accent, self.limb_width); draw_limb_segment_offset(self.r_elbow_pos, self.r_hand_pos, self.forearm_length, self.team_color, self.limb_width)
            draw_limb_segment_offset(self.hip_pos, self.l_knee_pos, self.thigh_length, self.team_color, self.limb_width); draw_limb_segment_offset(self.l_knee_pos, self.l_foot_pos, self.shin_length, self.team_accent, self.limb_width)
            draw_limb_segment_offset(self.hip_pos, self.r_knee_pos, self.thigh_length, self.team_color, self.limb_width); draw_limb_segment_offset(self.r_knee_pos, self.r_foot_pos, self.shin_length, self.team_accent, self.limb_width)
            if "FLIGHT" in self.active_powerups:
                 o_shoulder_pos = offset_pos(self.shoulder_pos); o_hip_pos = offset_pos(self.hip_pos)
                 upper_attach_x = o_shoulder_pos[0]; upper_attach_y = o_shoulder_pos[1] + 5; lower_attach_x = o_hip_pos[0]; lower_attach_y = o_hip_pos[1] - 5
                 upper_length = self.wing_upper_lobe_size[0]; upper_width = self.wing_upper_lobe_size[1]; lower_length = self.wing_lower_lobe_size[0]; lower_width = self.wing_lower_lobe_size[1]
                 def create_wing_poly_offset(attach_point, angle, length, width):
                    cos_a = math.cos(angle); sin_a = math.sin(angle); cos_w = math.cos(angle + math.pi/2); sin_w = math.sin(angle + math.pi/2)
                    p1 = attach_point; p2 = (attach_point[0] + length * 0.6 * cos_a + width * 0.5 * cos_w, attach_point[1] + length * 0.6 * sin_a + width * 0.5 * sin_w)
                    p3 = (attach_point[0] + length * cos_a, attach_point[1] + length * sin_a); p4 = (attach_point[0] + length * 0.6 * cos_a - width * 0.5 * cos_w, attach_point[1] + length * 0.6 * sin_a - width * 0.5 * sin_w)
                    p5 = (attach_point[0] + length*0.2 * cos_a - width*0.2 * cos_w, attach_point[1] + length*0.2 * sin_a - width*0.2 * sin_w)
                    return [(int(p[0]), int(p[1])) for p in [p1, p2, p3, p4, p5]]
                 l_attach_upper = (upper_attach_x - 4, upper_attach_y); l_attach_lower = (lower_attach_x - 4, lower_attach_y); l_upper_poly = create_wing_poly_offset(l_attach_upper, self.l_wing_upper_angle, upper_length, upper_width)
                 l_lower_poly = create_wing_poly_offset(l_attach_lower, self.l_wing_lower_angle, lower_length, lower_width); pygame.draw.polygon(temp_surf, self.wing_color, l_upper_poly); pygame.draw.polygon(temp_surf, self.wing_outline_color, l_upper_poly, 1)
                 pygame.draw.polygon(temp_surf, self.wing_color, l_lower_poly); pygame.draw.polygon(temp_surf, self.wing_outline_color, l_lower_poly, 1); r_attach_upper = (upper_attach_x + 4, upper_attach_y); r_attach_lower = (lower_attach_x + 4, lower_attach_y)
                 r_upper_poly = create_wing_poly_offset(r_attach_upper, self.r_wing_upper_angle, upper_length, upper_width); r_lower_poly = create_wing_poly_offset(r_attach_lower, self.r_wing_lower_angle, lower_length, lower_width)
                 pygame.draw.polygon(temp_surf, self.wing_color, r_upper_poly); pygame.draw.polygon(temp_surf, self.wing_outline_color, r_upper_poly, 1); pygame.draw.polygon(temp_surf, self.wing_color, r_lower_poly); pygame.draw.polygon(temp_surf, self.wing_outline_color, r_lower_poly, 1)
            if "ROCKET_LAUNCHER" in self.active_powerups:
                o_shoulder_pos = offset_pos(self.shoulder_pos)
                gun_attach_x = o_shoulder_pos[0] + 5 * self.facing_direction; gun_attach_y = o_shoulder_pos[1] + 10
                base_angle = 0 if self.facing_direction == 1 else math.pi; gun_world_angle = base_angle + self.gun_angle_offset
                gun_center_x = gun_attach_x + (GUN_SIZE[0] / 2) * math.cos(gun_world_angle); gun_center_y = gun_attach_y + (GUN_SIZE[0] / 2) * math.sin(gun_world_angle)
                draw_rotated_rectangle(temp_surf, GUN_COLOR, (gun_center_x, gun_center_y), GUN_SIZE[0], GUN_SIZE[1], gun_world_angle)
                world_gun_attach_x = self.shoulder_pos[0] + 5 * self.facing_direction; world_gun_attach_y = self.shoulder_pos[1] + 10
                world_gun_center_x = world_gun_attach_x + (GUN_SIZE[0] / 2) * math.cos(gun_world_angle); world_gun_center_y = world_gun_attach_y + (GUN_SIZE[0] / 2) * math.sin(gun_world_angle)
                tip_offset = GUN_SIZE[0] / 2; self.gun_tip_pos = (world_gun_center_x + tip_offset * math.cos(gun_world_angle), world_gun_center_y + tip_offset * math.sin(gun_world_angle))
            if self.is_tumbling and self.rotation_angle != 0:
                rotated_surf = pygame.transform.rotate(temp_surf, -math.degrees(self.rotation_angle))
                blit_rect = rotated_surf.get_rect(center = offset_pos(self.hip_pos))
                screen.blit(rotated_surf, (blit_rect.left - offset_x, blit_rect.top - offset_y))
            else:
                screen.blit(temp_surf, (min_x, min_y))
            # Draw laser outside the rotated surface logic
            if "ROCKET_LAUNCHER" in self.active_powerups:
                base_angle = 0 if self.facing_direction == 1 else math.pi
                laser_world_angle = base_angle + self.gun_angle_offset
                laser_end_x = self.gun_tip_pos[0] + LASER_LENGTH * math.cos(laser_world_angle); laser_end_y = self.gun_tip_pos[1] + LASER_LENGTH * math.sin(laser_world_angle)
                try: pygame.draw.aaline(screen, LASER_COLOR, self.gun_tip_pos, (laser_end_x, laser_end_y))
                except ValueError: pass
            if self.is_controls_reversed:
                q_font = pygame.font.Font(None, int(24 * (self.head_radius / self.base_head_radius)))
                q_surf = q_font.render("?", True, RED)
                q_rect = q_surf.get_rect(centerx=int(self.head_pos[0]), bottom=int(self.head_pos[1] - self.head_radius - 5)); screen.blit(q_surf, q_rect)


# --- Puck Class --- Renamed from Ball
class Puck: # Renamed, updated friction/bounce, draw as circle
    def __init__(self, x, y, radius):
        self.x = x; self.y = y; self.radius = radius; self.vx = 0; self.vy = 0;
        self.last_hit_by = None # Rotation removed for puck
        self.is_frozen = False; self.freeze_effect_timer = 0.0
    def apply_force(self, force_x, force_y, hitter='player'):
        if self.is_frozen: return
        self.vx += force_x; self.vy += force_y; self.last_hit_by = hitter
    def update(self, dt):
        if self.freeze_effect_timer > 0: self.freeze_effect_timer -= dt
        if self.is_frozen: return False

        self.vy += GRAVITY;
        self.vx *= PUCK_FRICTION;
        self.vy *= PUCK_FRICTION;
        self.x += self.vx; self.y += self.vy
        hit_ground = False; hit_wall_this_frame = False; hit_shield_this_frame = False

        current_goal_height_p1 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        current_goal_y_p1 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        current_goal_height_p2 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        current_goal_y_p2 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)

        if p1_shield_active:
            shield_rect = pygame.Rect(GOAL_LINE_X_LEFT - POWERUP_GOAL_SHIELD_WIDTH // 2, current_goal_y_p1, POWERUP_GOAL_SHIELD_WIDTH, current_goal_height_p1) # Adjusted position
            if self.get_rect().colliderect(shield_rect):
                if self.vx < 0: self.x = shield_rect.right + self.radius; self.vx *= -PUCK_BOUNCE; hit_shield_this_frame = True
        if p2_shield_active:
            shield_rect = pygame.Rect(GOAL_LINE_X_RIGHT + GOAL_WIDTH // 2, current_goal_y_p2, POWERUP_GOAL_SHIELD_WIDTH, current_goal_height_p2) # Adjusted position
            if self.get_rect().colliderect(shield_rect):
                if self.vx > 0: self.x = shield_rect.left - self.radius; self.vx *= -PUCK_BOUNCE; hit_shield_this_frame = True
        if hit_shield_this_frame: play_sound(loaded_sounds['wall_hit'])

        if self.x + self.radius >= SCREEN_WIDTH: self.x = SCREEN_WIDTH - self.radius; self.vx *= -PUCK_BOUNCE; hit_wall_this_frame = True
        elif self.x - self.radius <= 0: self.x = self.radius; self.vx *= -PUCK_BOUNCE; hit_wall_this_frame = True
        if hit_wall_this_frame and not hit_shield_this_frame: play_sound(loaded_sounds['wall_hit'])

        if self.y + self.radius >= GROUND_Y:
            if self.vy >= 0:
                impact_vy = abs(self.vy); self.y = GROUND_Y - self.radius; self.vy *= -PUCK_BOUNCE;
                if abs(self.vy) < 1: self.vy = 0
                if impact_vy > 1.5: play_sound(loaded_sounds['ball_bounce'])
                hit_ground = True
        if abs(self.vx) < 0.1 and self.is_on_ground(): self.vx = 0
        return hit_ground
    def is_on_ground(self): return self.y + self.radius >= GROUND_Y - 0.5
    def get_rect(self): return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)
    def draw(self, screen):
        center_tuple = (int(self.x), int(self.y));
        pygame.draw.circle(screen, PUCK_COLOR, center_tuple, self.radius)
        pygame.draw.circle(screen, BLACK, center_tuple, self.radius, 1)
        if self.is_frozen or self.freeze_effect_timer > 0:
            alpha = 220
            if self.freeze_effect_timer > 0 and not self.is_frozen: alpha = int(220 * (self.freeze_effect_timer / (POWERUP_BALL_FREEZE_DURATION * 0.1)))
            freeze_color = (173, 216, 230, max(0, min(255, alpha)))
            shield_radius = self.radius + 3
            temp_surf = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, freeze_color, (shield_radius, shield_radius), shield_radius)
            pygame.draw.circle(temp_surf, (230, 240, 255, alpha // 2), (shield_radius, shield_radius), shield_radius, 1)
            screen.blit(temp_surf, (int(self.x - shield_radius), int(self.y - shield_radius)))


# --- Game Setup ---
pygame.init(); pygame.mixer.pre_init(44100, -16, 2, 512); pygame.mixer.init()
announcement_channel = pygame.mixer.Channel(0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)); pygame.display.set_caption("Stick Hockey!");
clock = pygame.time.Clock()

# --- Sound Loading ---
# ... (sound loading unchanged) ...
def load_sounds(sound_dir="sounds"):
    sounds = {}
    sound_files = {"kick": ["kick_ball1.wav", "kick_ball2.wav"], "jump": ["jump1.wav"], "land": ["land1.wav"],"wall_hit": ["wall_hit1.wav"], "player_bump": ["player_bump1.wav"], "headbutt": ["headbutt1.wav"], "body_hit": ["body_hit1.wav"], "combo": ["combo_sparkle1.wav", "combo_sparkle2.wav", "combo_sparkle3.wav", "combo_sparkle4.wav"], "ball_bounce": ["ball_bounce1.wav"], "nils_wins": ["nils_wins.wav"], "harry_wins": ["harry_wins.wav"], "nils_ahead": ["nils_ahead.wav"], "harry_ahead": ["harry_ahead.wav"], "super_jackpot": ["super_jackpot.wav"]}
    for name, filenames in sound_files.items():
        sounds[name] = []
        for filename in filenames:
            path = os.path.join(sound_dir, filename)
            try: sound = pygame.mixer.Sound(path); sounds[name].append(sound); print(f"Loaded sound: {path}")
            except pygame.error as e: print(f"Warning: Could not load sound '{path}': {e}")
    sounds['numbers'] = {}
    for i in range(0, 6):
        filename = f"{i}.wav"; path = os.path.join(sound_dir, filename)
        try: sound = pygame.mixer.Sound(path); sounds['numbers'][i] = sound; print(f"Loaded sound: {path} as number {i}")
        except pygame.error as e: print(f"Warning: Could not load number sound '{path}': {e}"); sounds['numbers'][i] = None
    for player_num in [1, 2]:
        goal_key = f"goal_p{player_num}"; sounds[goal_key] = []; i = 1
        while True:
            filename = f"player{player_num}_goal{i}.wav"; path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                try: sound = pygame.mixer.Sound(path); sounds[goal_key].append(sound); print(f"Loaded sound: {path}"); i += 1
                except pygame.error as e: print(f"Warning: Could not load sound '{path}': {e}"); break
            else: break
        if not sounds[goal_key]: print(f"Warning: No goal sounds found for Player {player_num}")
    required_keys = ["goal_p1", "goal_p2", "kick", "jump", "land", "wall_hit", "player_bump", "headbutt", "body_hit", "combo", "ball_bounce", "nils_wins", "harry_wins", "nils_ahead", "harry_ahead", "super_jackpot"]
    for key in required_keys:
        if key not in sounds: sounds[key] = []
    if 'numbers' not in sounds: sounds['numbers'] = {}
    return sounds
# --- Sound Playing Helpers ---
def play_sound(sound_list): # ... (no change) ...
    if sound_list:
        sound_to_play = random.choice(sound_list)
        ch = pygame.mixer.find_channel(True)
        if ch: ch.play(sound_to_play)
def queue_sound(sound_list): # ... (no change) ...
    global announcement_queue
    if sound_list:
        sound_to_play = random.choice(sound_list)
        if sound_to_play: announcement_queue.append(sound_to_play)
def queue_specific_sound(sound_obj): # ... (no change) ...
    global announcement_queue
    if sound_obj: announcement_queue.append(sound_obj)
def play_next_announcement(): # ... (no change) ...
    global announcement_queue, announcement_channel
    if announcement_queue and not announcement_channel.get_busy():
        next_sound = announcement_queue.pop(0)
        if next_sound:
            announcement_channel.play(next_sound)
            announcement_channel.set_endevent(SOUND_FINISHED_EVENT)
        else: pygame.event.post(pygame.event.Event(SOUND_FINISHED_EVENT))
loaded_sounds = load_sounds()

# --- Player/Ball/Font/Powerup Setup ---
active_powerups = []
player1 = StickMan(SCREEN_WIDTH // 4, GROUND_Y, facing=1); player2 = StickMan(SCREEN_WIDTH * 3 // 4, GROUND_Y, facing=-1)
player1.team_color = TEAM1_COLOR; player1.team_accent = TEAM1_ACCENT
player1.torso_colors = [player1.team_color, player1.team_accent, player1.team_color]; player1.arm_colors = [player1.team_accent, player1.team_color]; player1.leg_colors = [player1.team_color, player1.team_accent]; player1.cap_color = player1.team_accent
player2.team_color = TEAM2_COLOR; player2.team_accent = TEAM2_ACCENT
player2.torso_colors = [player2.team_color, player2.team_accent, player2.team_color]; player2.arm_colors = [player2.team_accent, player2.team_color]; player2.leg_colors = [player2.team_color, player2.team_accent]; player2.cap_color = player2.team_color
player_list = [player1, player2]
puck = Puck(SCREEN_WIDTH // 2, GROUND_Y - 20, 10)
font_large = pygame.font.Font(None, 50); font_medium = pygame.font.Font(None, 36); font_small = pygame.font.Font(None, 28)
font_timestamp = pygame.font.Font(None, 20); font_goal = pygame.font.Font(None, 80)
winner_images = {}
try:
    winner_images[1] = pygame.image.load("nils_wins.png").convert_alpha()
    winner_images[2] = pygame.image.load("harry_wins.png").convert_alpha()
    print("Loaded winner images.")
except pygame.error as e:
    print(f"Warning: Could not load winner images: {e}")
    winner_images[1] = None; winner_images[2] = None

# --- Score & State Variables ---
player1_score = 0; player2_score = 0; p1_games_won = 0; p2_games_won = 0
game_scores = []; match_active = True; match_over_timer = 0.0; game_over = False
match_winner = None; overall_winner = None; match_end_sound_played = False
game_over_sound_played = False
announcement_queue = []
goal_message_timer = 0; screen_flash_timer = 0
puck_was_on_ground = True; particles = []; p1_can_headbutt = True; p2_can_headbutt = True
p1_body_collision_timer = 0; p2_body_collision_timer = 0; current_hit_count = 0
powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
active_rockets = []; active_explosions = []
ball_freeze_timer = 0.0
p1_shield_active = False; p1_shield_timer = 0.0
p2_shield_active = False; p2_shield_timer = 0.0
jackpot_triggered_this_match = False
p1_goal_enlarged_timer = 0.0
p2_goal_enlarged_timer = 0.0


# --- Reset/Start Functions ---
def reset_positions(): # Keeps powerups active, resets player state only
    global puck_was_on_ground, current_hit_count, p1_can_headbutt, p2_can_headbutt, p1_body_collision_timer, p2_body_collision_timer, active_rockets, active_explosions
    puck.x = SCREEN_WIDTH // 2; puck.y = SCREEN_HEIGHT // 3; puck.vx = 0; puck.vy = 0;
    if puck.is_frozen: puck.freeze_effect_timer = POWERUP_BALL_FREEZE_DURATION * 0.1
    player1.x = SCREEN_WIDTH // 4; player1.y = GROUND_Y; player1.vx = 0; player1.vy = 0; player1.is_kicking = False; player1.on_other_player_head = False; player1.facing_direction = 1; player1.is_jumping = False; player1.is_tumbling = False; player1.rotation_angle = 0; player1.rotation_velocity = 0; player1.is_controls_reversed = False; player1.is_penguin = False
    player2.x = SCREEN_WIDTH * 3 // 4; player2.y = GROUND_Y; player2.vx = 0; player2.vy = 0; player2.is_kicking = False; player2.on_other_player_head = False; player2.facing_direction = -1; player2.is_jumping = False; player2.is_tumbling = False; player2.rotation_angle = 0; player2.rotation_velocity = 0; player2.is_controls_reversed = False; player2.is_penguin = False
    # Reset sizes which might have been changed by powerups
    player1.calculate_current_sizes(); player2.calculate_current_sizes()
    current_hit_count = 0; puck_was_on_ground = False; p1_can_headbutt = True; p2_can_headbutt = True; p1_body_collision_timer = 0; p2_body_collision_timer = 0;
    active_rockets = []; active_explosions = []
def start_new_match(): # Full reset for new match
    global player1_score, player2_score, match_active, match_winner, match_over_timer, match_end_sound_played, announcement_queue, powerup_spawn_timer, active_powerups, ball_freeze_timer, p1_shield_active, p1_shield_timer, p2_shield_active, p2_shield_timer, jackpot_triggered_this_match, p1_goal_enlarged_timer, p2_goal_enlarged_timer
    player1_score = 0; player2_score = 0; match_active = True; match_winner = None; match_over_timer = 0.0; match_end_sound_played = False
    announcement_queue = []; reset_positions()
    player1.active_powerups = {}; player1.is_flying = False; player1.is_big = False; player1.is_shrunk = False; player1.is_enormous_head = False; player1.is_penguin=False; player1.jump_power = BASE_JUMP_POWER; player1.player_speed = BASE_PLAYER_SPEED; player1.calculate_current_sizes()
    player2.active_powerups = {}; player2.is_flying = False; player2.is_big = False; player2.is_shrunk = False; player2.is_enormous_head = False; player2.is_penguin=False; player2.jump_power = BASE_JUMP_POWER; player2.player_speed = BASE_PLAYER_SPEED; player2.calculate_current_sizes()
    active_powerups = []
    ball_freeze_timer = 0.0; puck.is_frozen = False; puck.freeze_effect_timer = 0.0
    p1_shield_active = False; p1_shield_timer = 0.0; p2_shield_active = False; p2_shield_timer = 0.0
    p1_goal_enlarged_timer = 0.0; p2_goal_enlarged_timer = 0.0
    player1.randomize_nose(); player2.randomize_nose()
    powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
    jackpot_triggered_this_match = False
    print("Starting new match.")
def start_new_game(): # Full reset
    global p1_games_won, p2_games_won, game_scores, game_over, overall_winner, announcement_queue, game_over_sound_played, active_powerups
    p1_games_won = 0; p2_games_won = 0; game_scores = []; game_over = False; overall_winner = None; game_over_sound_played = False
    active_powerups = []
    announcement_queue = []; start_new_match(); print("Starting new game.")

# --- Collision Handling Function (Player-Puck) ---
# ... (unchanged) ...
def handle_player_puck_collisions(player, puck, can_headbutt, body_collision_timer, is_puck_airborne):
    global current_hit_count
    hit_performed = False; headbutt_performed = False; score_increase = False; hit_pt = None
    local_hit_point = player.get_hit_impact_point()
    if local_hit_point:
        dist_x = local_hit_point[0] - puck.x; dist_y = local_hit_point[1] - puck.y; dist_sq = dist_x**2 + dist_y**2
        eff_hit_rad = HIT_RADIUS_NORMAL + (HIT_RADIUS_FALLING_BONUS if puck.vy > PUCK_FALLING_VELOCITY_THRESHOLD else 0)
        scale_factor = player.head_radius / player.base_head_radius if player.is_penguin else (player.torso_length / player.base_torso_length)
        if dist_sq < (puck.radius + eff_hit_rad * scale_factor)**2:
             if player.kick_duration <= 0: progress = 1.0
             else: progress = player.kick_timer / player.kick_duration
             if 0.25 < progress < 0.6:
                 hit_x = BASE_HIT_FORCE_X * HIT_FORCE_LEVEL * player.facing_direction; hit_y = BASE_HIT_FORCE_Y * HIT_FORCE_LEVEL
                 if player.vy < 0: hit_y += player.vy * 0.4
                 puck.apply_force(hit_x, hit_y, hitter=player); hit_performed = True; hit_pt = local_hit_point; play_sound(loaded_sounds['kick']);
                 if is_puck_airborne: current_hit_count += 1; score_increase = True
    head_pos, head_radius = player.get_head_position_radius(); dist_x_head = puck.x - head_pos[0]; dist_y_head = puck.y - head_pos[1]
    dist_head_sq = dist_x_head**2 + dist_y_head**2; headbutt_cooldown_just_applied = False
    if dist_head_sq < (puck.radius + head_radius)**2:
        if can_headbutt:
            force_y = -HEADBUTT_UP_FORCE;
            if player.vy < 0: force_y -= abs(player.vy) * HEADBUTT_VY_MULTIPLIER
            if player.is_enormous_head: force_y *= HEAD_BOUNCE_MULTIPLIER; print("Puck bounce off enormous head!")
            force_x = player.vx * HEADBUTT_PLAYER_VX_FACTOR - dist_x_head * HEADBUTT_POS_X_FACTOR
            puck.apply_force(force_x, force_y, hitter=player); headbutt_cooldown_just_applied = True; headbutt_performed = True; play_sound(loaded_sounds['headbutt']);
            if is_puck_airborne: current_hit_count += 1; score_increase = True
    new_can_headbutt = can_headbutt
    if headbutt_cooldown_just_applied: new_can_headbutt = False
    elif not new_can_headbutt and dist_head_sq > (puck.radius + head_radius + 15)**2: new_can_headbutt = True
    new_body_collision_timer = body_collision_timer
    if not hit_performed and not headbutt_performed and body_collision_timer == 0:
        player_rect = player.get_body_rect(); closest_x = max(player_rect.left, min(puck.x, player_rect.right)); closest_y = max(player_rect.top, min(puck.y, player_rect.bottom))
        delta_x = puck.x - closest_x; delta_y = puck.y - closest_y; dist_sq_body = delta_x**2 + delta_y**2
        if dist_sq_body < puck.radius**2:
             collision_occurred = False
             if dist_sq_body > 0:
                 distance = math.sqrt(dist_sq_body); overlap = puck.radius - distance; collision_normal_x = delta_x / distance; collision_normal_y = delta_y / distance
                 push_amount = overlap + 0.2; puck.x += collision_normal_x * push_amount; puck.y += collision_normal_y * push_amount
                 rel_vx = puck.vx - player.vx; rel_vy = puck.vy - player.vy; vel_along_normal = rel_vx * collision_normal_x + rel_vy * collision_normal_y
                 if vel_along_normal < 0:
                     impulse_scalar = -(1 + PLAYER_BODY_BOUNCE) * vel_along_normal; bounce_vx = impulse_scalar * collision_normal_x; bounce_vy = impulse_scalar * collision_normal_y
                     bounce_vx += player.vx * PLAYER_VEL_TRANSFER; bounce_vy += player.vy * PLAYER_VEL_TRANSFER
                     new_vel_mag_sq = bounce_vx**2 + bounce_vy**2
                     if new_vel_mag_sq < MIN_BODY_BOUNCE_VEL**2:
                         if new_vel_mag_sq > 0: scale = MIN_BODY_BOUNCE_VEL / math.sqrt(new_vel_mag_sq); bounce_vx *= scale; bounce_vy *= scale
                         else: bounce_vx = collision_normal_x * MIN_BODY_BOUNCE_VEL; bounce_vy = collision_normal_y * MIN_BODY_BOUNCE_VEL
                     puck.vx = bounce_vx; puck.vy = bounce_vy; new_body_collision_timer = PLAYER_BODY_COLLISION_FRAMES; collision_occurred = True
             elif dist_sq_body == 0:
                  puck.y = player_rect.top - puck.radius - 0.1
                  if puck.vy > 0: puck.vy *= -PLAYER_BODY_BOUNCE
                  new_body_collision_timer = PLAYER_BODY_COLLISION_FRAMES; collision_occurred = True
             if collision_occurred: play_sound(loaded_sounds['body_hit'])
    return score_increase, new_can_headbutt, new_body_collision_timer, hit_pt

# --- Start First Game ---
start_new_game()

# --- Main Game Loop ---
running = True
while running:
    dt = clock.tick(FPS) / 1000.0; dt = min(dt, 0.1)

    # --- Global Input & Event Processing ---
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        if event.type == SOUND_FINISHED_EVENT: play_next_announcement()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_7: debug_mode = not debug_mode; print(f"Debug Mode {'ACT' if debug_mode else 'DEACT'}IVATED")
            elif event.key == pygame.K_6:
                if match_active:
                    print("DEBUG: Forcing powerup spawn."); new_powerup = ParachutePowerup(); new_powerup.spawn(); active_powerups.append(new_powerup); powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
                else: print("DEBUG: Match inactive, cannot force spawn.")
            elif game_over and event.key == pygame.K_r: start_new_game()
            elif match_active:
                if not player1.is_tumbling:
                    if event.key == pygame.K_a: player1.move(-1)
                    elif event.key == pygame.K_d: player1.move(1)
                    elif event.key == pygame.K_w: player1.jump()
                    elif event.key == pygame.K_s: player1.start_hit() # Renamed
                if not player2.is_tumbling:
                    if event.key == pygame.K_LEFT: player2.move(-1)
                    elif event.key == pygame.K_RIGHT: player2.move(1)
                    elif event.key == pygame.K_UP: player2.jump()
                    elif event.key == pygame.K_DOWN: player2.start_hit() # Renamed
        if event.type == pygame.KEYUP:
             if match_active:
                if not player1.is_tumbling:
                    if event.key == pygame.K_a and player1.vx < 0: player1.stop_move()
                    elif event.key == pygame.K_d and player1.vx > 0: player1.stop_move()
                if not player2.is_tumbling:
                    if event.key == pygame.K_LEFT and player2.vx < 0: player2.stop_move()
                    elif event.key == pygame.K_RIGHT and player2.vx > 0: player2.stop_move()

    # --- Handle Game Over State ---
    if game_over:
        if not game_over_sound_played:
            announcement_queue = [];
            winner_sound_key = 'nils_wins' if overall_winner == 1 else 'harry_wins'
            queue_sound(loaded_sounds.get(winner_sound_key, []))
            play_next_announcement(); game_over_sound_played = True
        bg_color = DEBUG_BG_COLOR if debug_mode else ICE_BLUE
        screen.fill(bg_color); pygame.draw.rect(screen, RINK_WHITE, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        winner_name = "Team Blue" if overall_winner == 1 else "Team Red";
        draw_trophy(screen, winner_name, font_goal, font_large)
        winner_image = winner_images.get(overall_winner)
        if winner_image:
            image_rect = winner_image.get_rect(); trophy_center_x = SCREEN_WIDTH // 2; base_width = 140; padding = 50
            image_center_x = trophy_center_x + base_width // 2 + image_rect.width // 2 + padding
            image_center_y = SCREEN_HEIGHT // 2 + 180 - 40 - 100 // 2
            image_rect.center = (image_center_x, image_center_y)
            image_rect.right = min(image_rect.right, SCREEN_WIDTH - 10)
            screen.blit(winner_image, image_rect)
        draw_game_scores(screen, game_scores, font_small); pygame.display.flip(); continue

    # --- Handle Match Over State ---
    if match_over_timer > 0:
        match_over_timer -= dt
        if match_over_timer <= 0 and not game_over: start_new_match()

    # --- Process Announcement Sound Queue ---
    play_next_announcement()

    # --- Power-up Spawning (with Jackpot) ---
    if match_active: # ... (unchanged) ...
        powerup_spawn_timer -= dt
        if powerup_spawn_timer <= 0:
            if not jackpot_triggered_this_match and random.randint(1, 6) == 1:
                print("!!! SUPER JACKPOT !!!"); play_sound(loaded_sounds.get('super_jackpot', []))
                jackpot_triggered_this_match = True
                for _ in range(8):
                    new_powerup = ParachutePowerup(); new_powerup.spawn(); active_powerups.append(new_powerup)
            else:
                new_powerup = ParachutePowerup(); new_powerup.spawn(); active_powerups.append(new_powerup)
            powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)

    # --- Update Global Powerup Timers ---
    if ball_freeze_timer > 0: # ... (unchanged) ...
        ball_freeze_timer -= dt
        if ball_freeze_timer <= 0:
            puck.is_frozen = False; puck.freeze_effect_timer = POWERUP_BALL_FREEZE_DURATION * 0.1 ; print("Puck un-frozen")
    if p1_shield_timer > 0: # ... (unchanged) ...
        p1_shield_timer -= dt
        if p1_shield_timer <= 0: p1_shield_active = False; print("P1 Shield down")
    if p2_shield_timer > 0: # ... (unchanged) ...
        p2_shield_timer -= dt
        if p2_shield_timer <= 0: p2_shield_active = False; print("P2 Shield down")
    if p1_goal_enlarged_timer > 0: # ... (unchanged) ...
        p1_goal_enlarged_timer -= dt
        if p1_goal_enlarged_timer <= 0: print("P1 Goal Normal Size")
    if p2_goal_enlarged_timer > 0: # ... (unchanged) ...
        p2_goal_enlarged_timer -= dt
        if p2_goal_enlarged_timer <= 0: print("P2 Goal Normal Size")


    # --- Updates (Only if match active) ---
    if match_active:
        if p1_body_collision_timer > 0: p1_body_collision_timer -= 1
        if p2_body_collision_timer > 0: p2_body_collision_timer -= 1
        if goal_message_timer > 0: goal_message_timer -= dt
        if screen_flash_timer > 0: screen_flash_timer -= dt

        player1.update(dt, player2); player2.update(dt, player1)
        puck_hit_ground_this_frame = puck.update(dt)

        active_powerups = [p for p in active_powerups if p.update(dt)]
        particles = [p for p in particles if p.update(dt)]
        active_rockets = [r for r in active_rockets if r.active and not r.update(dt, player_list, puck)]
        active_explosions = [e for e in active_explosions if e.update(dt)]

        # --- Power-up Collection ---
        collected_powerups_indices = [] # ... (Includes spawning 2 on freeze) ...
        for i, pup in enumerate(active_powerups):
            collected_this_pup = False
            if not collected_this_pup and not player1.is_tumbling:
                collected_type_p1 = pup.check_collision(player1)
                if collected_type_p1:
                    player1.apply_powerup(collected_type_p1, other_player=player2)
                    collected_powerups_indices.append(i); collected_this_pup = True
                    if collected_type_p1 == "BALL_FREEZE":
                         print("Ball Freeze collected - Spawning 2 more powerups!")
                         new_powerup1 = ParachutePowerup(); new_powerup1.spawn(); active_powerups.append(new_powerup1)
                         new_powerup2 = ParachutePowerup(); new_powerup2.spawn(); active_powerups.append(new_powerup2)
                         powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)

            if not collected_this_pup and not player2.is_tumbling:
                collected_type_p2 = pup.check_collision(player2)
                if collected_type_p2:
                    player2.apply_powerup(collected_type_p2, other_player=player1)
                    collected_powerups_indices.append(i)
                    if collected_type_p2 == "BALL_FREEZE":
                         print("Ball Freeze collected - Spawning 2 more powerups!")
                         new_powerup1 = ParachutePowerup(); new_powerup1.spawn(); active_powerups.append(new_powerup1)
                         new_powerup2 = ParachutePowerup(); new_powerup2.spawn(); active_powerups.append(new_powerup2)
                         powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)

        if collected_powerups_indices:
             active_powerups = [pup for idx, pup in enumerate(active_powerups) if idx not in collected_powerups_indices]


        # --- Player Collisions ---
        # ... (player-player collision unchanged) ...
        p1_rect = player1.get_body_rect(); p2_rect = player2.get_body_rect()
        if p1_rect.colliderect(p2_rect):
            p1_is_on_p2 = player1.on_other_player_head; p2_is_on_p1 = player2.on_other_player_head
            if p1_is_on_p2 and abs(player1.y - (player2.head_pos[1] - player2.head_radius)) > 10: p1_is_on_p2 = False
            if p2_is_on_p1 and abs(player2.y - (player1.head_pos[1] - player1.head_radius)) > 10: p2_is_on_p1 = False
            if not p1_is_on_p2 and not p2_is_on_p1:
                dx = player2.x - player1.x; overlap_x = (p1_rect.width / 2 + p2_rect.width / 2) - abs(dx)
                if overlap_x > 0:
                    play_sound(loaded_sounds['player_bump']); push = overlap_x / 2 + 0.1
                    if dx >= 0: player1.x -= push; player2.x += push;
                    if player1.vx > 0: player1.vx = 0
                    if player2.vx < 0: player2.vx = 0
                    else: player1.x += push; player2.x -= push;
                    if player1.vx < 0: player1.vx = 0
                    if player2.vx > 0: player2.vx = 0
        hit_push_amount = puck.radius * 1.5; hit_push_vx_base = 5
        p1_hit_point = player1.get_hit_impact_point()
        if p1_hit_point and p2_rect.collidepoint(p1_hit_point) and not player2.is_tumbling:
            print("P1 hit P2")
            hit_multiplier = BIG_PLAYER_KICK_MULTIPLIER if player1.is_big else 1.0
            hit_push_vx = hit_push_vx_base * hit_multiplier
            player2.x += hit_push_amount * player1.facing_direction * hit_multiplier
            player2.vx += hit_push_vx * player1.facing_direction
            player2.vy -= 3 * hit_multiplier; player2.is_jumping = True
            play_sound(loaded_sounds['body_hit'])
        p2_hit_point = player2.get_hit_impact_point()
        if p2_hit_point and p1_rect.collidepoint(p2_hit_point) and not player1.is_tumbling:
            print("P2 hit P1")
            hit_multiplier = BIG_PLAYER_KICK_MULTIPLIER if player2.is_big else 1.0
            hit_push_vx = hit_push_vx_base * hit_multiplier
            player1.x += hit_push_amount * player2.facing_direction * hit_multiplier
            player1.vx += hit_push_vx * player2.facing_direction
            player1.vy -= 3 * hit_multiplier; player1.is_jumping = True
            play_sound(loaded_sounds['body_hit'])
        player1.x = max(player1.limb_width / 2, min(player1.x, SCREEN_WIDTH - player1.limb_width / 2))
        player2.x = max(player2.limb_width / 2, min(player2.x, SCREEN_WIDTH - player2.limb_width / 2))

        # Combo Reset
        is_puck_airborne = not puck.is_on_ground()
        if not is_puck_airborne and puck_hit_ground_this_frame and not puck_was_on_ground: current_hit_count = 0
        puck_was_on_ground = not is_puck_airborne

        # Player-Puck Collisions (only if not tumbling)
        p1_hit, p1_can_headbutt, p1_body_collision_timer, p1_hit_pt = handle_player_puck_collisions(player1, puck, p1_can_headbutt, p1_body_collision_timer, is_puck_airborne)
        p2_hit, p2_can_headbutt, p2_body_collision_timer, p2_hit_pt = handle_player_puck_collisions(player2, puck, p2_can_headbutt, p2_body_collision_timer, is_puck_airborne)
        score_increased_this_frame = p1_hit or p2_hit
        last_hit_point = p1_hit_pt if p1_hit_pt else p2_hit_pt

        # Combo Trigger
        if score_increased_this_frame and last_hit_point and current_hit_count > 0 and current_hit_count % 5 == 0:
            play_sound(loaded_sounds['combo'])
            num_kick_particles = PARTICLE_COUNT // 2
            for _ in range(num_kick_particles): particle_x = last_hit_point[0] + random.uniform(-5, 5); particle_y = last_hit_point[1] + random.uniform(-5, 5); particles.append(Particle(particle_x, particle_y))


    # --- Goal Detection & Effects ---
    goal_scored_this_frame = False; scorer = 0
    goal_height_p1 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
    goal_y_p1 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
    goal_height_p2 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
    goal_y_p2 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)

    if match_active and not puck.is_frozen:
        if puck.x + puck.radius >= GOAL_LINE_X_RIGHT and puck.y > goal_y_p2 and not p2_shield_active:
            player1_score += 1; scorer = 1; goal_message_timer = GOAL_MESSAGE_DURATION; goal_scored_this_frame = True; goal_pos_x = SCREEN_WIDTH; print(f"GOAL! Player 1 Score: {player1_score}"); screen_flash_timer = SCREEN_FLASH_DURATION
        elif puck.x - puck.radius <= GOAL_LINE_X_LEFT and puck.y > goal_y_p1 and not p1_shield_active:
            player2_score += 1; scorer = 2; goal_message_timer = GOAL_MESSAGE_DURATION; goal_scored_this_frame = True; goal_pos_x = 0; print(f"GOAL! Player 2 Score: {player2_score}"); screen_flash_timer = SCREEN_FLASH_DURATION

    if goal_scored_this_frame: # ... (unchanged goal handling) ...
        if scorer == 1: play_sound(loaded_sounds['goal_p1']);
        if player1_score > 0 and player1_score % 5 == 0: play_sound(loaded_sounds['combo'])
        elif scorer == 2: play_sound(loaded_sounds['goal_p2']);
        if player2_score > 0 and player2_score % 5 == 0: play_sound(loaded_sounds['combo'])
        goal_center_y = GOAL_Y_POS + GOAL_HEIGHT / 2
        for _ in range(GOAL_PARTICLE_COUNT): particles.append(Particle(goal_pos_x, goal_center_y, colors=GOAL_EXPLOSION_COLORS, speed_min=GOAL_PARTICLE_SPEED_MIN, speed_max=GOAL_PARTICLE_SPEED_MAX, lifespan=GOAL_PARTICLE_LIFESPAN))
        current_match_limit = DEBUG_MATCH_POINT_LIMIT if debug_mode else MATCH_POINT_LIMIT
        winner_found_this_match = False
        if player1_score >= current_match_limit: match_winner = 1; winner_found_this_match = True; print(f"Player 1 wins the match! (Limit: {current_match_limit})")
        elif player2_score >= current_match_limit: match_winner = 2; winner_found_this_match = True; print(f"Player 2 wins the match! (Limit: {current_match_limit})")
        if winner_found_this_match:
            match_active = False; match_over_timer = MATCH_OVER_DURATION; match_end_sound_played = False
            if match_winner == 1: p1_games_won += 1
            elif match_winner == 2: p2_games_won += 1
            game_scores.insert(0, (player1_score, player2_score));
            if len(game_scores) > 9: game_scores.pop()
            print(f"Games Won: P1={p1_games_won}, P2={p2_games_won}")
            if not (p1_games_won >= GAME_WIN_LIMIT or p2_games_won >= GAME_WIN_LIMIT):
                announcement_queue = []; p1_games = p1_games_won; p2_games = p2_games_won
                if p1_games > p2_games: queue_sound(loaded_sounds['nils_ahead']); queue_specific_sound(loaded_sounds['numbers'].get(p1_games)); queue_specific_sound(loaded_sounds['numbers'].get(p2_games))
                elif p2_games > p1_games: queue_sound(loaded_sounds['harry_ahead']); queue_specific_sound(loaded_sounds['numbers'].get(p2_games)); queue_specific_sound(loaded_sounds['numbers'].get(p1_games))
                else: queue_specific_sound(loaded_sounds['numbers'].get(p1_games)); queue_specific_sound(loaded_sounds['numbers'].get(p2_games))
                play_next_announcement()
            if p1_games_won >= GAME_WIN_LIMIT: overall_winner = 1; game_over = True; print("PLAYER 1 WINS THE GAME!")
            elif p2_games_won >= GAME_WIN_LIMIT: overall_winner = 2; game_over = True; print("PLAYER 2 WINS THE GAME!")
        reset_positions(); continue


    # --- Drawing ---
    bg_color = ICE_BLUE
    if debug_mode: bg_color = DEBUG_BG_COLOR
    screen.fill(bg_color)
    pygame.draw.rect(screen, RINK_WHITE, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))

    # Draw Hockey Goals
    draw_hockey_goal(screen, GOAL_LINE_X_LEFT, GOAL_Y_POS, GOAL_WIDTH, GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0), GOAL_POST_THICKNESS, GOAL_POST_COLOR, GOAL_NET_COLOR)
    draw_hockey_goal(screen, GOAL_LINE_X_RIGHT, GOAL_Y_POS, GOAL_WIDTH, GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0), GOAL_POST_THICKNESS, GOAL_POST_COLOR, GOAL_NET_COLOR)

    # Draw Goal Shields with Pulse
    current_time = pygame.time.get_ticks() / 1000.0
    pulse = (math.sin(current_time * POWERUP_GOAL_SHIELD_PULSE_SPEED) + 1) / 2
    shield_alpha = int(POWERUP_GOAL_SHIELD_MIN_ALPHA + pulse * (POWERUP_GOAL_SHIELD_MAX_ALPHA - POWERUP_GOAL_SHIELD_MIN_ALPHA))
    shield_color_with_alpha = (POWERUP_GOAL_SHIELD_COLOR[0], POWERUP_GOAL_SHIELD_COLOR[1], POWERUP_GOAL_SHIELD_COLOR[2], shield_alpha)
    if p1_shield_active:
        shield_height = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        shield_y = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        shield_rect = pygame.Rect(GOAL_LINE_X_LEFT - GOAL_WIDTH // 2 - POWERUP_GOAL_SHIELD_WIDTH, shield_y, POWERUP_GOAL_SHIELD_WIDTH, shield_height)
        shield_surf = pygame.Surface(shield_rect.size, pygame.SRCALPHA); shield_surf.fill(shield_color_with_alpha)
        screen.blit(shield_surf, shield_rect.topleft); pygame.draw.rect(screen, WHITE, shield_rect, 1)
    if p2_shield_active:
        shield_height = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        shield_y = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        shield_rect = pygame.Rect(GOAL_LINE_X_RIGHT + GOAL_WIDTH // 2, shield_y, POWERUP_GOAL_SHIELD_WIDTH, shield_height)
        shield_surf = pygame.Surface(shield_rect.size, pygame.SRCALPHA); shield_surf.fill(shield_color_with_alpha)
        screen.blit(shield_surf, shield_rect.topleft); pygame.draw.rect(screen, WHITE, shield_rect, 1)

    if screen_flash_timer > 0: flash_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA); flash_alpha = int(255 * (screen_flash_timer / SCREEN_FLASH_DURATION)); flash_surf.fill((SCREEN_FLASH_COLOR[0], SCREEN_FLASH_COLOR[1], SCREEN_FLASH_COLOR[2], flash_alpha)); screen.blit(flash_surf, (0,0))

    # Draw Game Elements
    for p in particles: p.draw(screen)
    for pup in active_powerups: pup.draw(screen)
    for r in active_rockets: r.draw(screen)
    player1.draw(screen); player2.draw(screen)
    puck.draw(screen) # Renamed
    for e in active_explosions: e.draw(screen)
    draw_offscreen_arrow(screen, puck, None) # Renamed

    # --- Draw UI ---
    # ... (UI drawing unchanged) ...
    draw_scoreboard(screen, player1_score, player2_score, p1_games_won, p2_games_won, font_large, font_medium, font_small, goal_message_timer > 0 or match_over_timer > 0)
    draw_game_scores(screen, game_scores, font_small)
    if goal_message_timer > 0 and match_active:
        goal_text_surf = font_goal.render("GOAL!", True, RED); bg_rect = goal_text_rect.inflate(20, 10); bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA); bg_surf.fill((RINK_WHITE[0], RINK_WHITE[1], RINK_WHITE[2], 180)); screen.blit(bg_surf, bg_rect.topleft); screen.blit(goal_text_surf, goal_text_rect)
    if match_over_timer > 0 and not game_over:
        winner_name = "Team Blue" if match_winner == 1 else "Team Red"; match_win_text = f"{winner_name} Wins the Match!"; match_win_surf = font_large.render(match_win_text, True, YELLOW); match_win_rect = match_win_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        next_match_surf = font_medium.render("Next Match Starting...", True, WHITE); next_match_rect = next_match_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        bg_rect = match_win_rect.union(next_match_rect).inflate(40, 20); bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA); bg_surf.fill((0, 0, 100, 200)); screen.blit(bg_surf, bg_rect.topleft)
        screen.blit(match_win_surf, match_win_rect); screen.blit(next_match_surf, next_match_rect)

    if match_active:
        cooldown_radius = 5; indicator_offset_y = - player1.head_radius - cooldown_radius - 2
        if not p1_can_headbutt: cooldown_color = (255, 0, 0, 180); head_x, head_y = player1.head_pos; indicator_x = int(head_x); indicator_y = int(head_y + indicator_offset_y); temp_surf = pygame.Surface((cooldown_radius*2, cooldown_radius*2), pygame.SRCALPHA); pygame.draw.circle(temp_surf, cooldown_color, (cooldown_radius, cooldown_radius), cooldown_radius); screen.blit(temp_surf, (indicator_x - cooldown_radius, indicator_y - cooldown_radius))
        if not p2_can_headbutt: cooldown_color = (0, 0, 255, 180); head_x, head_y = player2.head_pos; indicator_x = int(head_x); indicator_y = int(head_y + indicator_offset_y); temp_surf = pygame.Surface((cooldown_radius*2, cooldown_radius*2), pygame.SRCALPHA); pygame.draw.circle(temp_surf, cooldown_color, (cooldown_radius, cooldown_radius), cooldown_radius); screen.blit(temp_surf, (indicator_x - cooldown_radius, indicator_y - cooldown_radius))

        powerup_font = font_small; line_height = powerup_font.get_height() + 2
        powerup_colors = { "FLIGHT": (0,100,200), "ROCKET_LAUNCHER": (200, 50, 50), "BIG_PLAYER": (50, 180, 50),
                           "SUPER_JUMP": (200, 200, 50), "SPEED_BOOST": (255, 150, 0), "GOAL_SHIELD": (100, 180, 255),
                           "SHRUNK": (150, 100, 200), "LOW_GRAVITY": (180, 180, 255), "REVERSE_CONTROLS": (255, 100, 100),
                           "ENORMOUS_HEAD": (255, 100, 200), "GOAL_ENLARGER": (50, 200, 150), "PENGUIN": (100, 100, 120)}
        powerup_texts = { "FLIGHT": "Flight: {:.1f}", "ROCKET_LAUNCHER": "ROCKET(x{})", "BIG_PLAYER": "BIG: {:.1f}",
                          "SUPER_JUMP": "JUMP: {:.1f}", "SPEED_BOOST": "SPEED: {:.1f}", "GOAL_SHIELD": "SHIELD: {:.1f}",
                          "SHRUNK": "Shrunk: {:.1f}", "LOW_GRAVITY": "LOW-G: {:.1f}", "REVERSE_CONTROLS": "REVERSED: {:.1f}",
                          "ENORMOUS_HEAD": "BIG HEAD: {:.1f}", "GOAL_ENLARGER": "GOAL+: {:.1f}", "PENGUIN": "PENGUIN: {:.1f}"}

        # Player 1 UI
        p1_ui_y = SCREEN_HEIGHT - 30
        for p_type in sorted(player1.active_powerups.keys()):
            val = player1.active_powerups[p_type]; text_template = powerup_texts.get(p_type, p_type); text = ""
            if p_type == "ROCKET_LAUNCHER": text = text_template.format(val)
            elif p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD", "PENGUIN"]: text = text_template.format(val)
            else: text = text_template
            color = powerup_colors.get(p_type, WHITE); surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomleft=(10, p1_ui_y)); screen.blit(surf, rect)
            p1_ui_y -= line_height
        if p1_shield_active:
            text = powerup_texts.get("GOAL_SHIELD", "SHIELD: {:.1f}").format(p1_shield_timer); color = powerup_colors.get("GOAL_SHIELD", WHITE)
            surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomleft=(10, p1_ui_y)); screen.blit(surf, rect)
            p1_ui_y -= line_height
        if p1_goal_enlarged_timer > 0:
            text = powerup_texts.get("GOAL_ENLARGER", "GOAL+: {:.1f}").format(p1_goal_enlarged_timer); color = powerup_colors.get("GOAL_ENLARGER", WHITE)
            surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomleft=(10, p1_ui_y)); screen.blit(surf, rect)
            p1_ui_y -= line_height

        # Player 2 UI
        p2_ui_y = SCREEN_HEIGHT - 30
        for p_type in sorted(player2.active_powerups.keys()):
            val = player2.active_powerups[p_type]; text_template = powerup_texts.get(p_type, p_type); text = ""
            if p_type == "ROCKET_LAUNCHER": text = text_template.format(val)
            elif p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD", "PENGUIN"]: text = text_template.format(val)
            else: text = text_template
            color = powerup_colors.get(p_type, WHITE); surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomright=(SCREEN_WIDTH - 10, p2_ui_y)); screen.blit(surf, rect)
            p2_ui_y -= line_height
        if p2_shield_active:
            text = powerup_texts.get("GOAL_SHIELD", "SHIELD: {:.1f}").format(p2_shield_timer); color = powerup_colors.get("GOAL_SHIELD", WHITE)
            surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomright=(SCREEN_WIDTH - 10, p2_ui_y)); screen.blit(surf, rect)
            p2_ui_y -= line_height
        if p2_goal_enlarged_timer > 0:
            text = powerup_texts.get("GOAL_ENLARGER", "GOAL+: {:.1f}").format(p2_goal_enlarged_timer); color = powerup_colors.get("GOAL_ENLARGER", WHITE)
            surf = powerup_font.render(text, True, color); rect = surf.get_rect(bottomright=(SCREEN_WIDTH - 10, p2_ui_y)); screen.blit(surf, rect)
            p2_ui_y -= line_height

        # Global Effect Indicators
        if puck.is_frozen:
            freeze_text = "PUCK FROZEN: {:.1f}".format(ball_freeze_timer); freeze_surf = powerup_font.render(freeze_text, True, (180, 220, 255)); freeze_rect = freeze_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)); screen.blit(freeze_surf, freeze_rect)


    if debug_mode:
        timestamp_surf = font_timestamp.render(GENERATION_TIMESTAMP, True, TEXT_COLOR); timestamp_rect = timestamp_surf.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)); screen.blit(timestamp_surf, timestamp_rect)

    pygame.display.flip()

# Cleanup
pygame.quit(); sys.exit()
