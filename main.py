# stickkick_powerup.py
# -*- coding: utf-8 -*-
import pygame
import sys
import math
import random
import os
import time
from datetime import datetime

# --- Get Timestamp ---
GENERATION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Constants ---
SCREEN_WIDTH = 800; SCREEN_HEIGHT = 600; FPS = 60
WHITE = (255, 255, 255); BLACK = (0, 0, 0); SKY_BLUE = (135, 206, 235)
P1_COLOR_MAIN = (220, 220, 220); P1_COLOR_ACCENT = (30, 30, 30)
ITALY_GREEN = (0, 146, 70); ITALY_WHITE = (241, 242, 241); ITALY_RED = (206, 43, 55)
P2_COLOR_MAIN = ITALY_GREEN; P2_COLOR_ACCENT = ITALY_RED; P2_COLOR_WHITE = ITALY_WHITE
GRASS_GREEN = (34, 139, 34); YELLOW = (255, 255, 0); TEXT_COLOR = (10, 10, 50)
ARROW_RED = (255, 50, 50); STAR_YELLOW = (255, 255, 100); STAR_ORANGE = (255, 180, 0)
RED = (255, 0, 0)
DEBUG_BLUE = (0, 0, 255)
GOAL_COLOR = (220, 220, 220); GOAL_NET_COLOR = (180, 180, 190)
GOAL_EXPLOSION_COLORS = [WHITE, YELLOW, STAR_YELLOW, (255, 215, 0)]
NOSE_COLOR = (50, 50, 50)
SCOREBOARD_BG_COLOR = (50, 50, 80, 180)
SCOREBOARD_BORDER_COLOR = (200, 200, 220)
SCOREBOARD_TEXT_FLASH_COLOR = YELLOW
SCREEN_FLASH_COLOR = (255, 255, 255, 100)
SCREEN_FLASH_DURATION = 0.15
DEBUG_KICK_ANGLES = False


# Physics
GRAVITY = 0.5; BASE_PLAYER_SPEED = 4; BASE_JUMP_POWER = -11
BASE_KICK_FORCE_X = 15; BASE_KICK_FORCE_Y = -2
KICK_FORCE_LEVEL = 1.5
HEADBUTT_UP_FORCE = 15.0; HEADBUTT_VY_MULTIPLIER = 1.2
HEADBUTT_PLAYER_VX_FACTOR = 0.6; HEADBUTT_POS_X_FACTOR = 0.15
BALL_FRICTION = 0.99; BALL_BOUNCE = 0.7; GROUND_Y = SCREEN_HEIGHT - 50

# --- Time of Day Constants ---
TIMES_OF_DAY = ["Day", "Evening", "Night", "Morning"]
TIME_OF_DAY_COLORS = {
    "Day": SKY_BLUE,
    "Evening": (180, 140, 190), # Purplish
    "Night": (20, 20, 60),      # Dark blue
    "Morning": (255, 180, 140)   # Orangey pink
}
STAR_COUNT = 50
STARS = [(random.randint(0, SCREEN_WIDTH), random.randint(0, int(GROUND_Y * 0.8))) for _ in range(STAR_COUNT)] # Now GROUND_Y can be used

# Collision Specific
PLAYER_BODY_BOUNCE = 0.65; PLAYER_VEL_TRANSFER = 0.25
MIN_BODY_BOUNCE_VEL = 1.5; PLAYER_BODY_COLLISION_FRAMES = 4
HEAD_PLATFORM_RADIUS_BUFFER = 5

# Kick Collision Tweak
KICK_RADIUS_NORMAL = 16; KICK_RADIUS_FALLING_BONUS = 6
BALL_FALLING_VELOCITY_THRESHOLD = 5

# Goal Constants
GOAL_MARGIN_X = 40
GOAL_HEIGHT = 135; GOAL_POST_THICKNESS = 3; GOAL_Y_POS = GROUND_Y - GOAL_HEIGHT
GOAL_DEPTH_X = 30; GOAL_DEPTH_Y = -15
GOAL_LINE_X_LEFT = GOAL_MARGIN_X; GOAL_LINE_X_RIGHT = SCREEN_WIDTH - GOAL_MARGIN_X

# Animation Constants
WALK_CYCLE_SPEED = 0.25; BODY_WOBBLE_AMOUNT = 0
RUN_UPPER_ARM_SWING = math.pi / 6.0; RUN_UPPER_ARM_WOBBLE_AMP = 0; RUN_UPPER_ARM_WOBBLE_SPEED = 0
RUN_FOREARM_SWING = math.pi / 5.0; RUN_FOREARM_WOBBLE_AMP = 0; RUN_FOREARM_WOBBLE_SPEED = 0
RUN_FOREARM_OFFSET_FACTOR = 0.1; JUMP_UPPER_ARM_BASE = -math.pi * 0.1; JUMP_UPPER_ARM_WOBBLE_AMP = 0
JUMP_UPPER_ARM_WOBBLE_SPEED = 0; JUMP_UPPER_ARM_VY_FACTOR = 0.01; JUMP_FOREARM_BASE = math.pi * 0.1
JUMP_FOREARM_WOBBLE_AMP = 0; JUMP_FOREARM_WOBBLE_SPEED = 0
LEG_THIGH_SWING = math.pi / 7.0; LEG_SHIN_BEND_WALK = math.pi / 8.0; LEG_SHIN_BEND_SHIFT = math.pi / 2.5
KICK_THIGH_WINDUP_ANGLE = -math.pi / 4.5; KICK_THIGH_FOLLOW_ANGLE = math.pi * 0.7
KICK_SHIN_WINDUP_ANGLE = math.pi * 0.75; KICK_SHIN_IMPACT_ANGLE = -math.pi * 0.05
KICK_SHIN_FOLLOW_ANGLE = math.pi * 0.5
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

# --- Weather Effect Constants ---
WEATHER_TYPES = ["SUNNY", "RAINY", "WINDY", "SNOWY", "FOGGY", "GOTHENBURG_WEATHER"]
WEATHER_EFFECTS = {
    "SUNNY": {"gravity": 1.0, "background_color": (135, 206, 235)},  # Normal conditions
    "RAINY": {"gravity": 1.05, "background_color": (100, 149, 180)},  # Wet conditions
    "WINDY": {"wind_force_range": (10.0, 25.0), "background_color": (175, 196, 215)}, # Wind pushes objects (random force)
    "SNOWY": {"gravity": 0.9, "background_color": (220, 230, 240)},  # Lower gravity
    "FOGGY": {"gravity": 1.0, "background_color": (200, 200, 200)},  # Reduced visibility
    "GOTHENBURG_WEATHER": {"gravity": 1.1, "background_color": (90, 110, 130), "wind_force": 22.0, "wind_angle": math.pi * 0.85} # Heavy rain, strong side/up wind
}
WEATHER_PARTICLE_COUNT = {
    "SUNNY": 5,
    "RAINY": 40,
    "WINDY": 15,
    "SNOWY": 20,
    "FOGGY": 0,
    "GOTHENBURG_WEATHER": 70 # Heavy rain
}
WEATHER_WIND_DIRECTION = 1  # 1 = right, -1 = left (for WINDY weather)
WEATHER_WIND_CHANGE_TIMER = 0  # Timer for wind direction changes
CURRENT_WIND_FORCE = 0 # Current randomized wind force for WINDY weather

# --- Weather Messages --- (Added)
WEATHER_MESSAGES = {
    "SUNNY": [
        "What a lovely sunny day!",
        "Perfect weather for some kickabout!",
        "Don't forget sunscreen! Oh wait..."
    ],
    "RAINY": [
        "Looks like rain...",
        "A bit damp today, isn't it?",
        "It's raining cats and dogs! (Not literally)"
    ],
    "WINDY": [
        "Hold onto your hats, it's windy!",
        "The wind is really picking up!",
        "Whoosh! That's the sound of the wind."
    ],
    "SNOWY": [
        "Snow is falling... gently?",
        "Time for a snowball fight? No, football!",
        "Brr! It's a bit chilly and snowy."
    ],
    "FOGGY": [
        "Visibility is low due to fog.",
        "Can you even see the ball?",
        "Foggy conditions ahead!"
    ],
    "GOTHENBURG_WEATHER": [
        "Ah, classic Gothenburg weather!",
        "Rain, wind... just another Tuesday.",
        "Heavy showers and strong winds! Typical."
    ]
}
WEATHER_MESSAGE_DURATION = 5.5 # Seconds to display message (Increased from 2.5)

# --- Game State Constants ---
MATCH_POINT_LIMIT = 5
GAME_WIN_LIMIT = 5
MATCH_OVER_DURATION = 3.0
GOAL_MESSAGE_DURATION = 1.5

# --- Power-up Constants ---
POWERUP_TYPES = ["FLIGHT", "ROCKET_LAUNCHER", "BIG_PLAYER", "SUPER_JUMP",
                 "BALL_FREEZE", "SPEED_BOOST", "GOAL_SHIELD", "SHRINK_OPPONENT",
                 "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD", "GOAL_ENLARGER", "SWORD"] # <<< Removed old, added new
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
POWERUP_BALL_FREEZE_DURATION = 10.0 # Reduced duration
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
POWERUP_ENORMOUS_HEAD_SCALE = 7.0 # <<< Changed scale
POWERUP_GOAL_ENLARGER_DURATION = 15.0
POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE = 40
POWERUP_SWORD_DURATION = 30.0  # Changed from 15.0 to 30.0 seconds
# Removed FORCE_PUSH_RADIUS, FORCE_PUSH_FORCE, REFLECT_SHIELD_DURATION, REFLECT_SHIELD_COLOR


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
def draw_goal_isometric(surface, goal_line_x, goal_y, goal_height, depth_x, depth_y, thickness, post_color, net_color, enlarged_height=0):
    effective_goal_height = goal_height + enlarged_height
    effective_goal_y = goal_y - enlarged_height
    
    # Calculate goal dimensions - make a rectangular box
    goal_width = abs(depth_x) * 2.0  # Wider goal
    goal_depth = abs(depth_x) * 1.2   # Deeper goal
    
    # Determine direction for proper isometric display
    depth_dir = 1 if depth_x > 0 else -1
    
    # Calculate key points for the goal frame
    # Front face points
    front_left_top = (goal_line_x - goal_width/2, effective_goal_y)
    front_right_top = (goal_line_x + goal_width/2, effective_goal_y)
    front_left_bottom = (goal_line_x - goal_width/2, effective_goal_y + effective_goal_height)
    front_right_bottom = (goal_line_x + goal_width/2, effective_goal_y + effective_goal_height)
    
    # Back face points (with depth)
    back_left_top = (front_left_top[0] + depth_dir * goal_depth, front_left_top[1] + depth_y/3)
    back_right_top = (front_right_top[0] + depth_dir * goal_depth, front_right_top[1] + depth_y/3)
    back_left_bottom = (front_left_bottom[0] + depth_dir * goal_depth, front_left_bottom[1])  # Keep bottom level
    back_right_bottom = (front_right_bottom[0] + depth_dir * goal_depth, front_right_bottom[1])  # Keep bottom level
    
    # Convert all points to integers for drawing
    flt = (int(front_left_top[0]), int(front_left_top[1]))
    frt = (int(front_right_top[0]), int(front_right_top[1]))
    flb = (int(front_left_bottom[0]), int(front_left_bottom[1]))
    frb = (int(front_right_bottom[0]), int(front_right_bottom[1]))
    
    blt = (int(back_left_top[0]), int(back_left_top[1]))
    brt = (int(back_right_top[0]), int(back_right_top[1]))
    blb = (int(back_left_bottom[0]), int(back_left_bottom[1]))
    brb = (int(back_right_bottom[0]), int(back_right_bottom[1]))
    
    # Draw goal frame (white posts and crossbar) - thicker
    post_thickness = thickness + 4  # Increased thickness
    crossbar_thickness = thickness + 5  # Thicker crossbar
    crossbar_height = 8  # Height of the crossbar (vertical thickness)
    
    # Draw the crossbar with height (multiple horizontal lines to create thickness)
    for i in range(crossbar_height):
        # Calculate vertical offset for each line of the crossbar
        y_offset = i - crossbar_height//2
        
        # Front crossbar with thickness
        pygame.draw.line(
            surface, post_color, 
            (flt[0], flt[1] + y_offset), 
            (frt[0], frt[1] + y_offset), 
            crossbar_thickness - abs(y_offset)  # Thinner at edges to create rounded effect
        )
        
        # Back crossbar with thickness
        pygame.draw.line(
            surface, post_color, 
            (blt[0], blt[1] + y_offset), 
            (brt[0], brt[1] + y_offset), 
            (crossbar_thickness - 1) - abs(y_offset)  # Slightly thinner in back
        )
        
        # Left connector with thickness
        pygame.draw.line(
            surface, post_color, 
            (flt[0], flt[1] + y_offset), 
            (blt[0], blt[1] + y_offset), 
            (crossbar_thickness - 1) - abs(y_offset)
        )
        
        # Right connector with thickness
        pygame.draw.line(
            surface, post_color, 
            (frt[0], frt[1] + y_offset), 
            (brt[0], brt[1] + y_offset), 
            (crossbar_thickness - 1) - abs(y_offset)
        )
    
    # Draw vertical posts
    pygame.draw.line(surface, post_color, flt, flb, post_thickness)  # Left post
    pygame.draw.line(surface, post_color, frt, frb, post_thickness)  # Right post
    pygame.draw.line(surface, post_color, blt, blb, post_thickness - 1)  # Back left post
    pygame.draw.line(surface, post_color, brt, brb, post_thickness - 1)  # Back right post
    
    # Draw net with grid pattern (only above ground)
    net_color_with_alpha = (net_color[0], net_color[1], net_color[2], 180)  # Add some transparency
    
    # Create temporary surface for drawing the net with alpha
    net_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Vertical net lines on side panels (left and right)
    num_vertical = 8
    for i in range(1, num_vertical):
        ratio = i / num_vertical
        
        # Left side panel
        left_top = (flt[0] + (blt[0] - flt[0]) * ratio, flt[1] + (blt[1] - flt[1]) * ratio)
        left_bottom = (flb[0] + (blb[0] - flb[0]) * ratio, flb[1])
        pygame.draw.line(net_surf, net_color_with_alpha, left_top, left_bottom, 1)
        
        # Right side panel
        right_top = (frt[0] + (brt[0] - frt[0]) * ratio, frt[1] + (brt[1] - frt[1]) * ratio)
        right_bottom = (frb[0] + (brb[0] - frb[0]) * ratio, frb[1])
        pygame.draw.line(net_surf, net_color_with_alpha, right_top, right_bottom, 1)
    
    # Horizontal net lines on side panels
    num_horizontal = 10
    for i in range(1, num_horizontal):
        ratio = i / num_horizontal
        
        # Left side panel
        left_front = (flt[0], flt[1] + (flb[1] - flt[1]) * ratio)
        left_back = (blt[0], blt[1] + (blb[1] - blt[1]) * ratio)
        pygame.draw.line(net_surf, net_color_with_alpha, left_front, left_back, 1)
        
        # Right side panel
        right_front = (frt[0], frt[1] + (frb[1] - frt[1]) * ratio)
        right_back = (brt[0], brt[1] + (brb[1] - brt[1]) * ratio)
        pygame.draw.line(net_surf, net_color_with_alpha, right_front, right_back, 1)
    
    # Top panel - horizontal lines across depth
    for i in range(1, num_vertical):
        ratio = i / num_vertical
        top_left = (flt[0] + (blt[0] - flt[0]) * ratio, flt[1] + (blt[1] - flt[1]) * ratio)
        top_right = (frt[0] + (brt[0] - frt[0]) * ratio, frt[1] + (brt[1] - frt[1]) * ratio)
        pygame.draw.line(net_surf, net_color_with_alpha, top_left, top_right, 1)
    
    # Top panel - horizontal lines across width
    for i in range(1, num_horizontal):
        ratio = i / num_horizontal
        top_left = (flt[0] + (frt[0] - flt[0]) * ratio, flt[1])
        top_back = (blt[0] + (brt[0] - blt[0]) * ratio, blt[1])
        pygame.draw.line(net_surf, net_color_with_alpha, top_left, top_back, 1)
    
    # Back panel - vertical lines
    for i in range(1, num_horizontal):
        ratio = i / num_horizontal
        back_top = (blt[0] + (brt[0] - blt[0]) * ratio, blt[1])
        back_bottom = (blb[0] + (brb[0] - blb[0]) * ratio, blb[1])
        pygame.draw.line(net_surf, net_color_with_alpha, back_top, back_bottom, 1)
    
    # Back panel - horizontal lines
    for i in range(1, num_vertical):
        ratio = i / num_vertical
        back_left = (blt[0], blt[1] + (blb[1] - blt[1]) * ratio)
        back_right = (brt[0], brt[1] + (brb[1] - brt[1]) * ratio)
        pygame.draw.line(net_surf, net_color_with_alpha, back_left, back_right, 1)
    
    # Draw the net surface onto the main surface
    surface.blit(net_surf, (0, 0))
def draw_scoreboard(surface, p1_score, p2_score, p1_games, p2_games, score_font, name_font, game_score_font, is_goal_active):
    name_text = "Nils vs. Harry"; score_text = f"{p1_score} - {p2_score}"; game_score_text = f"({p1_games}-{p2_games})"
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
        if p1s >= current_limit and p1s > p2s: winner_name_str = " (Nils)"
        elif p2s >= current_limit and p2s > p1s: winner_name_str = " (Harry)"
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
    title_rect = title_surf.get_rect(center=(trophy_center_x, trophy_base_y - 220 - 100)) # Adjusted Y
    bg_rect = title_rect.inflate(40, 20); bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA); bg_surf.fill((0, 0, 100, 200)); surface.blit(bg_surf, bg_rect.topleft)
    surface.blit(title_surf, title_rect)
    rematch_font = name_font; rematch_text = "Press R for Rematch"; rematch_surf = rematch_font.render(rematch_text, True, WHITE)
    rematch_rect = rematch_surf.get_rect(centerx=trophy_center_x, top=15) # Positioned near top
    surface.blit(rematch_surf, rematch_rect)
def draw_offscreen_arrow(s, ball, p_pos):
    ar_sz = 15; pad = 25; is_off = False; tx, ty = ball.x, ball.y; ax = max(pad, min(ball.x, SCREEN_WIDTH - pad)); ay = max(pad, min(ball.y, SCREEN_HEIGHT - pad))
    if ball.x < 0 or ball.x > SCREEN_WIDTH: ax = pad if ball.x < 0 else SCREEN_WIDTH - pad; is_off = True
    if ball.y < 0 or ball.y > SCREEN_HEIGHT: ay = pad if ball.y < 0 else SCREEN_HEIGHT - pad; is_off = True
    if not is_off: return
    ang = math.atan2(ty - ay, tx - ax); p1 = (ar_sz, 0); p2 = (-ar_sz / 2, -ar_sz / 2); p3 = (-ar_sz / 2, ar_sz / 2)
    cos_a, sin_a = math.cos(ang), math.sin(ang); p1r = (p1[0] * cos_a - p1[1] * sin_a, p1[0] * sin_a + p1[1] * cos_a); p2r = (p2[0] * cos_a - p2[1] * sin_a, p2[0] * sin_a + p2[1] * cos_a); p3r = (p3[0] * cos_a - p3[1] * sin_a, p3[0] * sin_a + p3[1] * cos_a)
    pts = [(ax + p1r[0], ay + p1r[1]), (ax + p2r[0], ay + p2r[1]), (ax + p3r[0], ay + p3r[1])]; pygame.draw.polygon(s, ARROW_RED, [(int(p[0]), int(p[1])) for p in pts])

# Function to linearly interpolate between two colors
def lerp_color(color1, color2, factor):
    factor = max(0.0, min(1.0, factor)) # Clamp factor between 0 and 1
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)

# Function to draw a simple moon
def draw_moon(surface, position, size, color):
    pygame.draw.circle(surface, color, position, size)
    # Optional: Add a darker circle offset for a crescent effect
    dark_color = (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50))
    offset_x = size // 3
    offset_y = -size // 4
    pygame.draw.circle(surface, dark_color, (position[0] + offset_x, position[1] + offset_y), size)

# --- SWORD Powerup Constants --- (Moved here)
POWERUP_SWORD_DURATION = 30.0  # Increased from 15.0 to 30.0
SWORD_COLOR = (192, 192, 192) # Silver
SWORD_HILT_COLOR = (139, 69, 19) # Brown
SWORD_LENGTH_FACTOR = 1.8 # Relative to torso length
SWORD_WIDTH_FACTOR = 0.2 # Relative to limb width
SWORD_HIT_FORCE = 10  # Decreased from original value to reduce ball power
SWORD_PLAYER_HIT_FORCE = 500.0 # Horizontal force on player
SWORD_PLAYER_UPWARD_BOOST = 250.0 # Upward force on player

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
    def update(self, dt, players, ball):
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
            # Removed Reflect Shield Check
            if p.get_body_rect().colliderect(rocket_rect): exploded = True; break
            if not exploded:
                head_pos, head_radius = p.get_head_position_radius()
                dist_sq_head = (rocket_center_x - head_pos[0])**2 + (rocket_center_y - head_pos[1])**2
                if dist_sq_head < (head_radius + max(self.width, self.height) / 2)**2: exploded = True; break
        if not exploded:
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
            if ball_rect.colliderect(rocket_rect): exploded = True
        if exploded:
            self.active = False; create_explosion(self.x, self.y, ball.radius * ROCKET_BLAST_RADIUS_FACTOR, players, ball)
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

def create_explosion(x, y, radius, players, ball): # Added minimum bump
    global active_explosions
    print(f"Explosion created at ({x:.0f}, {y:.0f}) with radius {radius:.0f}")
    play_sound(loaded_sounds['wall_hit'])
    MIN_ROCKET_BUMP_SPEED = 2.0 # Minimum speed away from blast

    for p in players:
        dist_sq = (p.x - x)**2 + (p.y - y)**2
        if dist_sq < radius**2 and dist_sq > 0:
            dist = math.sqrt(dist_sq); force_magnitude = ROCKET_EXPLOSION_FORCE * (1.0 - (dist / radius))
            push_vec_x = (p.x - x) / dist; push_vec_y = (p.y - y) / dist
            explode_vx = push_vec_x * force_magnitude
            explode_vy = push_vec_y * force_magnitude * 0.8 - ROCKET_PLAYER_UPWARD_BOOST
            bump_vx = push_vec_x * MIN_ROCKET_BUMP_SPEED
            bump_vy = push_vec_y * MIN_ROCKET_BUMP_SPEED * 0.5
            p.vx += explode_vx + bump_vx # <<< Combine forces
            p.vy += explode_vy + bump_vy # <<< Combine forces
            p.is_jumping = True
            p.on_other_player_head = False
            p.start_tumble()
    dist_sq = (ball.x - x)**2 + (ball.y - y)**2
    if dist_sq < radius**2 and dist_sq > 0:
        dist = math.sqrt(dist_sq); force_magnitude = ROCKET_EXPLOSION_FORCE * (1.0 - (dist / radius))
        push_vec_x = (ball.x - x) / dist; push_vec_y = (ball.y - y) / dist
        ball.apply_force(push_vec_x * force_magnitude, push_vec_y * force_magnitude - ROCKET_BALL_UPWARD_BOOST, hitter='explosion')
    active_explosions.append(Explosion(x, y, radius))

class WeatherParticle:
    def __init__(self, weather_type, screen_width, screen_height):
        self.weather_type = weather_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
        
    def reset(self):
        if self.weather_type == "SUNNY":
            # Sun rays
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(0, self.screen_height // 3)
            self.size = random.randint(2, 5)
            self.speed = random.uniform(10, 30)
            self.color = (255, 255, 200, random.randint(50, 150))
            self.lifespan = random.uniform(2.0, 5.0)
            self.angle = random.uniform(0, 2 * math.pi)
            
        elif self.weather_type == "RAINY":
            # Rain drops
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(-50, 0)
            self.size = random.randint(1, 2)
            self.length = random.randint(5, 15)
            self.speed = random.uniform(200, 400)
            self.color = (120, 160, 255, random.randint(150, 220))
            self.lifespan = None  # Will reset when off-screen
            
        elif self.weather_type == "WINDY":
            self.size = random.uniform(2.0, 4.0)
            self.color = (200, 200, 255, random.randint(100, 180))
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(0, self.screen_height * 0.9)
            # Ändra från negativ till positiv riktning så att partiklarna följer samma riktning som spelarpåverkan
            self.speed = random.uniform(100, 200) * WEATHER_WIND_DIRECTION  # Följ wind direction utan inversion
            self.lifespan = None  # Will reset when off-screen
            self.angle = 0
            self.rotation_speed = random.uniform(-5, 5)
            self.vertical_speed = random.uniform(-20, 20)  # Lägg till vertikal hastighet
            
        elif self.weather_type == "SNOWY":
            # Snowflakes
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(-50, 0)
            self.size = random.randint(2, 4)
            self.speed = random.uniform(30, 80)
            self.horizontal_drift = random.uniform(-20, 20)
            self.color = (255, 255, 255, random.randint(180, 250))
            self.lifespan = None  # Will reset when off-screen
            
        elif self.weather_type == "FOGGY":
            # Fog patches (not used much since we'll use a global fog overlay)
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(0, self.screen_height)
            self.size = random.randint(30, 80)
            self.speed = random.uniform(5, 15)
            self.color = (255, 255, 255, random.randint(5, 20))
            self.lifespan = random.uniform(3.0, 8.0)
            
        elif self.weather_type == "GOTHENBURG_WEATHER":
            # Gothenburg rain drops (heavy, sideways)
            self.x = random.randint(-50, self.screen_width + 50)
            self.y = random.randint(-50, self.screen_height + 50)
            self.size = random.randint(2, 3)
            self.length = random.randint(10, 20)
            self.speed = random.uniform(300, 500)
            self.color = (100, 120, 180, random.randint(180, 240))
            self.lifespan = None
            # Get the fixed wind angle from WEATHER_EFFECTS
            self.angle = WEATHER_EFFECTS["GOTHENBURG_WEATHER"].get("wind_angle", math.pi) + random.uniform(-0.1, 0.1)
            
            
    def update(self, dt):
        if self.lifespan is not None:
            self.lifespan -= dt
            if self.lifespan <= 0:
                self.reset()
                return
        
        if self.weather_type == "SUNNY":
            # Sun rays move outward from a point
            self.x += math.cos(self.angle) * self.speed * dt
            self.y += math.sin(self.angle) * self.speed * dt
            
            # If off-screen, reset
            if (self.x < -10 or self.x > self.screen_width + 10 or 
                self.y < -10 or self.y > self.screen_height + 10):
                self.reset()
                
        elif self.weather_type == "RAINY":
            # Rain falls straight down (slightly angled)
            self.x -= 20 * dt  # Slight angle
            self.y += self.speed * dt
            
            # If off-screen, reset to top
            if self.y > self.screen_height:
                self.reset()
                
        elif self.weather_type == "WINDY":
            # Wind blows objects sideways with some up/down movement
            self.x += self.speed * dt
            self.y += self.vertical_speed * dt
            self.angle += self.rotation_speed * dt
            
            # Occasionally change vertical direction
            if random.random() < 0.02:
                self.vertical_speed = random.uniform(-20, 20)
                
            # If off-screen, reset
            if ((WEATHER_WIND_DIRECTION < 0 and self.x > self.screen_width + 50) or
                (WEATHER_WIND_DIRECTION > 0 and self.x < -50) or
                self.y < -50 or self.y > self.screen_height + 50):
                self.reset()
                
        elif self.weather_type == "SNOWY":
            # Snow falls down with some horizontal drift
            self.y += self.speed * dt
            self.x += self.horizontal_drift * dt
            
            # Occasionally change horizontal drift
            if random.random() < 0.05:
                self.horizontal_drift = random.uniform(-20, 20)
                
            # If off-screen, reset to top
            if self.y > self.screen_height or self.x < -10 or self.x > self.screen_width + 10:
                self.reset()
                
        elif self.weather_type == "FOGGY":
            # Fog drifts slowly
            self.x += self.speed * dt
            
            # If off-screen, reset
            if self.x > self.screen_width + self.size:
                self.reset()
                
        elif self.weather_type == "GOTHENBURG_WEATHER":
            # Move rain drops along the fixed wind angle
            self.x += self.speed * math.cos(self.angle) * dt
            self.y += self.speed * math.sin(self.angle) * dt
            
            # Reset if far off-screen
            if (self.x < -100 or self.x > self.screen_width + 100 or
                self.y < -100 or self.y > self.screen_height + 100):
                self.reset()
    
    def draw(self, screen):
        if self.weather_type == "SUNNY":
            # Draw sun ray as a small circle
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))
            
        elif self.weather_type == "RAINY" or self.weather_type == "GOTHENBURG_WEATHER": # Draw rain/gothenburg rain
            # Draw rain drop as a line along its angle
            start_x = int(self.x)
            start_y = int(self.y)
            # Use angle for direction (gothenburg has a specific angle, rain is mostly vertical)
            draw_angle = math.pi/2 + 0.1 if self.weather_type == "RAINY" else self.angle
            end_x = int(start_x + self.length * math.cos(draw_angle))
            end_y = int(start_y + self.length * math.sin(draw_angle))
            
            pygame.draw.line(screen, self.color, (start_x, start_y), (end_x, end_y), self.size)
            
        elif self.weather_type == "WINDY":
            # Draw wind debris as rotating rectangles
            rect_surf = pygame.Surface((self.size * 3, self.size), pygame.SRCALPHA)
            pygame.draw.rect(rect_surf, self.color, (0, 0, self.size * 3, self.size))
            rotated = pygame.transform.rotate(rect_surf, self.angle * 57.3)  # Convert to degrees
            screen.blit(rotated, (int(self.x - rotated.get_width() // 2),
                                int(self.y - rotated.get_height() // 2)))
                                
        elif self.weather_type == "SNOWY":
            # Draw snowflake as a small circle
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class StickMan: # Updated powerup dict/handling
    # Add team_color and team_accent to the arguments, with defaults
    def __init__(self, x, y, facing=1, team_color=WHITE, team_accent=BLACK):
        self.x = x; self.y = y; self.base_y = y; self.width = 20; self.height = 80; self.vx = 0; self.vy = 0; self.is_jumping = False; self.is_kicking = False; self.kick_timer = 0; self.kick_duration = 18; self.walk_cycle_timer = 0.0;

        # --- Assign Team Colors FIRST ---
        # Assign the passed arguments to the instance attributes
        self.team_color = team_color
        self.team_accent = team_accent
        self.eye_color = BLACK # Assign eye color here too

        # --- Base size attributes ---
        self.base_head_radius = 12; self.base_torso_length = 36; self.base_limb_width = 10; self.base_upper_arm_length = 12; self.base_forearm_length = 12; self.base_thigh_length = 14; self.base_shin_length = 14; self.base_nose_length = self.base_head_radius * 0.5; self.base_nose_width = self.base_head_radius * 0.3
        # --- Current size attributes (initially same as base) ---
        self.head_radius = self.base_head_radius; self.torso_length = self.base_torso_length; self.limb_width = self.base_limb_width; self.upper_arm_length = self.base_upper_arm_length; self.forearm_length = self.base_forearm_length; self.thigh_length = self.base_thigh_length; self.shin_length = self.base_shin_length; self.current_nose_length = self.base_nose_length; self.current_nose_width = self.base_nose_width

        # --- Use Team Colors ---
        # This block now correctly uses the assigned self.team_color and self.team_accent
        self.torso_colors = [self.team_color, self.team_accent, self.team_color]
        self.arm_colors = [self.team_accent, self.team_color]
        self.leg_colors = [self.team_color, self.team_accent]
        self.cap_color = self.team_accent # Use accent for cap
        self.cap_brim_color = BLACK

        # --- Animation & State Attributes ---
        self.l_upper_arm_angle = 0; self.r_upper_arm_angle = 0; self.l_forearm_angle = 0; self.r_forearm_angle = 0; self.l_thigh_angle = 0; self.r_thigh_angle = 0; self.l_shin_angle = 0; self.r_shin_angle = 0; self.head_pos = (0, 0); self.neck_pos = (0, 0); self.hip_pos = (0, 0); self.shoulder_pos = (0, 0); self.l_elbow_pos = (0, 0); self.r_elbow_pos = (0, 0); self.l_hand_pos = (0, 0); self.r_hand_pos = (0, 0); self.l_knee_pos = (0, 0); self.r_knee_pos = (0, 0); self.l_foot_pos = (0, 0); self.r_foot_pos = (0, 0); self.body_rect = pygame.Rect(0,0,0,0); self.facing_direction = facing; self.on_other_player_head = False
        
        # --- Crossbar Standing Variables ---
        self.on_left_crossbar = False
        self.on_right_crossbar = False

        # --- Wing Attributes (if applicable) ---
        self.wing_color = (173, 216, 230); self.wing_outline_color = (50, 50, 100); self.wing_rest_angle_offset = math.pi * 0.1 + (math.pi / 6); self.l_wing_base_angle = math.pi + self.wing_rest_angle_offset; self.r_wing_base_angle = -self.wing_rest_angle_offset; self.l_wing_upper_angle = self.l_wing_base_angle - 0.4; self.l_wing_lower_angle = self.l_wing_base_angle + 0.6; self.r_wing_upper_angle = self.r_wing_base_angle + 0.4; self.r_wing_lower_angle = self.r_wing_base_angle - 0.6; self.wing_flap_timer = 0.0; self.wing_flap_duration = 0.2; self.wing_flapping = False; self.wing_flap_magnitude = math.pi * 0.4; self.wing_upper_lobe_size = (30, 22); self.wing_lower_lobe_size = (28, 25)

        # --- Sword Attributes ---
        self.is_sword = False
        self.sword_angle = 0

        # --- Powerups and State ---
        self.active_powerups = {} # Updated powerup dict/handling
        self.is_flying = False; self.is_big = False; self.is_shrunk = False; self.is_enormous_head = False; self.is_penguin = False # Added penguin state
        self.jump_power = BASE_JUMP_POWER; self.player_speed = BASE_PLAYER_SPEED; self.is_controls_reversed = False
        self.head_pulse_timer = 0.0 # For enormous head pulse
        self.gun_anim_timer = random.uniform(0, 2 * math.pi); self.gun_angle_offset = 0.0; self.gun_tip_pos = (0, 0)
        self.is_tumbling = False; self.tumble_timer = 0.0; self.rotation_angle = 0.0; self.rotation_velocity = 0.0
    def start_tumble(self):
        if not self.is_tumbling:
             self.is_tumbling = True; self.tumble_timer = TUMBLE_DURATION
             self.rotation_velocity = random.uniform(PLAYER_TUMBLE_ROT_SPEED_MIN, PLAYER_TUMBLE_ROT_SPEED_MAX) * random.choice([-1, 1])
             self.is_kicking = False; self.kick_timer = 0
    def apply_powerup(self, powerup_type, other_player=None):
        current_val = self.active_powerups.get(powerup_type, 0)
        if powerup_type == "FLIGHT":
            self.active_powerups["FLIGHT"] = POWERUP_FLIGHT_DURATION; self.is_flying = True; print(f"Flight activated/refreshed: {POWERUP_FLIGHT_DURATION:.1f}s")
        elif powerup_type == "ROCKET_LAUNCHER":
            new_ammo = current_val + 3; self.active_powerups["ROCKET_LAUNCHER"] = new_ammo; print(f"Rocket Launcher ammo: {new_ammo}")
        elif powerup_type == "BIG_PLAYER":
            self.active_powerups["BIG_PLAYER"] = POWERUP_BIG_PLAYER_DURATION; self.is_big = True
            if "SHRUNK" in self.active_powerups: del self.active_powerups["SHRUNK"]; self.is_shrunk = False
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
             ball.is_frozen = True; ball.freeze_effect_timer = 0; print(f"Ball Freeze extended: {ball_freeze_timer:.1f}s")
             ball.vx = 0; ball.vy = 0
        elif powerup_type == "LOW_GRAVITY":
             self.active_powerups["LOW_GRAVITY"] = POWERUP_LOW_GRAVITY_DURATION; print(f"Low Gravity activated: {POWERUP_LOW_GRAVITY_DURATION:.1f}s")
        elif powerup_type == "REVERSE_CONTROLS":
             if other_player: other_player.apply_reverse_controls()
        elif powerup_type == "ENORMOUS_HEAD":
             self.active_powerups["ENORMOUS_HEAD"] = POWERUP_ENORMOUS_HEAD_DURATION; self.is_enormous_head = True
             if "SHRUNK" in self.active_powerups: del self.active_powerups["SHRUNK"]; self.is_shrunk = False # Cancel shrink
             self.calculate_current_sizes(); print(f"Enormous Head activated: {POWERUP_ENORMOUS_HEAD_DURATION:.1f}s")
        elif powerup_type == "GOAL_ENLARGER":
             if self is player1: global p2_goal_enlarged_timer; p2_goal_enlarged_timer = POWERUP_GOAL_ENLARGER_DURATION; print("P2 Goal Enlarged!")
             elif self is player2: global p1_goal_enlarged_timer; p1_goal_enlarged_timer = POWERUP_GOAL_ENLARGER_DURATION; print("P1 Goal Enlarged!")
        elif powerup_type == "SWORD":
             self.active_powerups["SWORD"] = POWERUP_SWORD_DURATION; self.is_sword = True; print(f"Sword Mode! {POWERUP_SWORD_DURATION:.1f}s")
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
    def apply_force_push(self, opponent, ball): # Keep stub or remove if fully deprecated
        pass
    def calculate_current_sizes(self):
        body_scale = 1.0
        if self.is_big: body_scale = POWERUP_BIG_PLAYER_SCALE
        elif self.is_shrunk: body_scale = POWERUP_SHRINK_PLAYER_SCALE
        self.torso_length = self.base_torso_length * body_scale
        self.limb_width = self.base_limb_width * (1.0 + (body_scale - 1.0) * 0.5)
        self.upper_arm_length = self.base_upper_arm_length * body_scale; self.forearm_length = self.base_forearm_length * body_scale
        self.thigh_length = self.base_thigh_length * body_scale; self.shin_length = self.base_shin_length * body_scale

        head_scale = body_scale # Default to body scale
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
        if direction != 0: self.facing_direction = direction
    def stop_move(self):
        if self.is_tumbling: return
        self.vx = 0
    def jump(self):
        if self.is_tumbling: return
        can_jump_now = False
        if "FLIGHT" in self.active_powerups:
            if not self.is_kicking: can_jump_now = True
        else:
            # Tillåt hopp om man inte redan hoppar, står på en annan spelare, ELLER står på en av ribborna
            if (not self.is_jumping or self.on_other_player_head or self.on_left_crossbar or self.on_right_crossbar) and not self.is_kicking:
                can_jump_now = True
        if can_jump_now:
            was_on_head = self.on_other_player_head
            was_on_crossbar = self.on_left_crossbar or self.on_right_crossbar # Kolla om vi var på ribban
            play_sound(loaded_sounds['jump']);
            if was_on_head: play_sound(loaded_sounds['combo'])
            if was_on_crossbar: play_sound(loaded_sounds['ball_bounce']) # Lägg till ett litet studsljud?
            self.is_jumping = True; self.on_other_player_head = False
            self.on_left_crossbar = False # Nollställ ribb-status vid hopp
            self.on_right_crossbar = False
            self.vy = self.jump_power; self.walk_cycle_timer = 0
            if "FLIGHT" in self.active_powerups: self.start_wing_flap()
    def start_kick(self):
        if self.is_tumbling: return
        if not self.is_kicking:
            if "ROCKET_LAUNCHER" in self.active_powerups: 
                self.fire_rocket()
            else: 
                self.is_kicking = True
                self.kick_timer = 0
                self.vx = 0
                
                # Use wall_hit sound as sword swing sound when player has sword
                if self.is_sword:
                    play_sound(loaded_sounds['wall_hit'])
                else:
                    play_sound(loaded_sounds['kick'])
    def fire_rocket(self):
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
    def start_wing_flap(self):
         if not self.wing_flapping: self.wing_flapping = True; self.wing_flap_timer = self.wing_flap_duration
    def randomize_nose(self):
        random_factor = random.uniform(1.0, 5.0); self.current_nose_length = self.base_nose_length * random_factor; self.current_nose_width = self.base_nose_width * random_factor; self.current_nose_width = min(self.current_nose_width, self.current_nose_length * 0.8)
    def update(self, dt, other_player):
        if self.is_tumbling:
            self.tumble_timer -= dt
            if self.tumble_timer <= 0: self.is_tumbling = False; self.tumble_timer = 0.0; self.rotation_angle = 0.0; self.rotation_velocity = 0.0; print(f"Player {1 if self.facing_direction==1 else 2} finished tumble.")
            else: self.rotation_angle += self.rotation_velocity * dt; self.rotation_velocity *= (PLAYER_TUMBLE_DAMPING ** (dt * 60))
        expired_powerups = []
        for p_type, value in list(self.active_powerups.items()):
            if p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "REFLECT_SHIELD", "ENORMOUS_HEAD"]:
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
                    elif p_type == "REFLECT_SHIELD": print("Reflect Shield ended")
                    elif p_type == "ENORMOUS_HEAD": self.is_enormous_head = False; self.calculate_current_sizes(); print("Enormous Head ended")
                else:
                    self.active_powerups[p_type] = new_timer
        for p_type in expired_powerups:
            if p_type in self.active_powerups: del self.active_powerups[p_type]
        if "ROCKET_LAUNCHER" in self.active_powerups: self.gun_anim_timer += dt * GUN_ANIM_SPEED; self.gun_angle_offset = math.sin(self.gun_anim_timer) * GUN_ANIM_MAGNITUDE
        if self.is_enormous_head: # Update pulse timer and recalculate sizes
             self.head_pulse_timer += dt * 5.0
             self.calculate_current_sizes()

        current_gravity = GRAVITY * POWERUP_LOW_GRAVITY_FACTOR if "LOW_GRAVITY" in self.active_powerups else GRAVITY
        weather_effect = WEATHER_EFFECTS.get(current_weather, WEATHER_EFFECTS["SUNNY"])
        current_gravity *= weather_effect.get("gravity", 1.0) # Apply weather gravity multiplier
        
        # Apply wind force to player
        if current_weather == "WINDY":
            # Use the currently randomized wind force and direction
            self.vx += (CURRENT_WIND_FORCE * WEATHER_WIND_DIRECTION * 0.03 * dt) # Apply wind force to vx (Increased multiplier from 0.01)
        elif current_weather == "GOTHENBURG_WEATHER":
            # Apply Gothenburg specific wind
             wind_force = weather_effect.get("wind_force", 0.0)
             wind_angle = weather_effect.get("wind_angle", math.pi) # Default to horizontal left if not defined
             self.vx += (wind_force * math.cos(wind_angle) * 0.02 * dt) # Increased multiplier from 0.01
             self.vy += (wind_force * math.sin(wind_angle) * 0.01 * dt) # Increased multiplier from 0.005
            
        was_airborne = self.is_jumping or (not self.on_other_player_head and not self.on_left_crossbar and not self.on_right_crossbar and self.y < self.base_y)
        was_on_head = self.on_other_player_head
        was_on_left_crossbar = self.on_left_crossbar
        was_on_right_crossbar = self.on_right_crossbar
        landed_on_head_this_frame = False
        landed_on_ground_this_frame = False
        landed_on_crossbar_this_frame = False

        # Plattformsdetektering - marken, huvud eller tvärstång
        platform_y = self.base_y  # Standard plattform är marken
        
        # Få måttuppgifter för crossbars (använd samma som för bollkollisioner)
        # Vänster mål
        left_goal_width = abs(GOAL_DEPTH_X) * 2.0
        left_crossbar_y = GOAL_Y_POS
        left_crossbar_height = 8  # Samma som i draw_goal_isometric
        left_crossbar_x = GOAL_LINE_X_LEFT
        
        # Höger mål
        right_goal_width = abs(GOAL_DEPTH_X) * 2.0
        right_crossbar_y = GOAL_Y_POS
        right_crossbar_height = 8  # Samma som i draw_goal_isometric
        right_crossbar_x = GOAL_LINE_X_RIGHT
        
        # Crossbar tops
        left_crossbar_top = left_crossbar_y - left_crossbar_height/2
        right_crossbar_top = right_crossbar_y - right_crossbar_height/2
        
        # Kolla om spelaren är inom räckhåll för vänster tvärstång
        is_aligned_for_left_crossbar = (self.x + self.limb_width/2 >= left_crossbar_x - left_goal_width/2 and 
                                       self.x - self.limb_width/2 <= left_crossbar_x + left_goal_width/2)
        
        # Kolla om spelaren är inom räckhåll för höger tvärstång
        is_aligned_for_right_crossbar = (self.x + self.limb_width/2 >= right_crossbar_x - right_goal_width/2 and 
                                        self.x - self.limb_width/2 <= right_crossbar_x + right_goal_width/2)
        
        # Hämta andra spelarens huvud för plattformsdetektering
        other_head_pos, other_head_radius = other_player.get_head_position_radius()
        head_top_y = other_head_pos[1] - other_head_radius
        dist_x_head = self.x - other_head_pos[0]
        is_aligned_for_head = abs(dist_x_head) < (other_head_radius + self.head_radius + HEAD_PLATFORM_RADIUS_BUFFER)
        
        # Uppdatera position baserat på fysik
        if not was_on_head and not was_on_left_crossbar and not was_on_right_crossbar:
            self.vy += GRAVITY
        elif was_on_head and not is_aligned_for_head:
            self.on_other_player_head = False
            self.is_jumping = True
            self.vy += GRAVITY
        elif was_on_head and is_aligned_for_head:
            self.y = head_top_y
            self.vy = 0
        elif was_on_left_crossbar and not is_aligned_for_left_crossbar:
            self.on_left_crossbar = False
            self.is_jumping = True
            self.vy += GRAVITY
        elif was_on_left_crossbar and is_aligned_for_left_crossbar:
            self.y = left_crossbar_top
            self.vy = 0
        elif was_on_right_crossbar and not is_aligned_for_right_crossbar:
            self.on_right_crossbar = False
            self.is_jumping = True
            self.vy += GRAVITY
        elif was_on_right_crossbar and is_aligned_for_right_crossbar:
            self.y = right_crossbar_top
            self.vy = 0
            
        next_y = self.y + self.vy
        
        # Landningskontroller
        if self.vy >= 0:
            # Kontrollera landning på huvud först
            can_land_on_head_now = (is_aligned_for_head and next_y >= head_top_y and self.y < head_top_y + 5)
            
            # Kontrollera landning på vänster tvärstång
            can_land_on_left_crossbar = (is_aligned_for_left_crossbar and 
                                        next_y >= left_crossbar_top and 
                                        self.y < left_crossbar_top + 5)
            
            # Kontrollera landning på höger tvärstång
            can_land_on_right_crossbar = (is_aligned_for_right_crossbar and 
                                         next_y >= right_crossbar_top and 
                                         self.y < right_crossbar_top + 5)
            
            # Landning på huvud
            if can_land_on_head_now:
                self.y = head_top_y
                self.vy = 0
                self.is_jumping = False
                self.on_other_player_head = True
                self.on_left_crossbar = False
                self.on_right_crossbar = False
                landed_on_head_this_frame = True
            # Landning på vänster tvärstång
            elif can_land_on_left_crossbar:
                self.y = left_crossbar_top
                self.vy = 0
                self.is_jumping = False
                self.on_other_player_head = False
                self.on_left_crossbar = True
                self.on_right_crossbar = False
                landed_on_crossbar_this_frame = True
            # Landning på höger tvärstång
            elif can_land_on_right_crossbar:
                self.y = right_crossbar_top
                self.vy = 0
                self.is_jumping = False
                self.on_other_player_head = False
                self.on_left_crossbar = False
                self.on_right_crossbar = True
                landed_on_crossbar_this_frame = True
            # Landning på marken
            elif not landed_on_head_this_frame and not landed_on_crossbar_this_frame and next_y >= self.base_y:
                self.y = self.base_y
                self.vy = 0
                self.is_jumping = False
                self.on_other_player_head = False
                self.on_left_crossbar = False
                self.on_right_crossbar = False
                landed_on_ground_this_frame = True
            else:
                # Fortstätt falla
                self.y = next_y
                if self.y < self.base_y and not landed_on_head_this_frame and not landed_on_crossbar_this_frame:
                    self.on_other_player_head = False
                    self.on_left_crossbar = False
                    self.on_right_crossbar = False
        else:
            # Åker uppåt
            self.y = next_y
            self.on_other_player_head = False
            self.on_left_crossbar = False
            self.on_right_crossbar = False
        
        # Sanitetskontroll - se till att spelaren inte faller utanför spelplanens botten
        if self.y > self.base_y and not self.on_other_player_head and not self.on_left_crossbar and not self.on_right_crossbar:
            self.y = self.base_y
            
        # Stoppa vertikal rörelse om vi är på marken
        if self.vy > 0 and self.y == self.base_y:
            self.vy = 0
            self.is_jumping = False
            
        # Spela landningsljud om vi landat på en plattform (mark eller huvud eller tvärstång)
        is_now_grounded = landed_on_ground_this_frame or landed_on_head_this_frame or landed_on_crossbar_this_frame
        if was_airborne and is_now_grounded and not self.is_tumbling:
            play_sound(loaded_sounds['land'])
            
        intended_vx = self.vx
        if not self.is_kicking:
            effective_vx = intended_vx
            if self.on_other_player_head: effective_vx += other_player.vx
            if self.is_tumbling and not self.on_other_player_head and self.y < self.base_y:
                 self.vx *= 0.99; effective_vx = self.vx
            self.x += effective_vx
            self.x = max(self.limb_width / 2, min(self.x, SCREEN_WIDTH - self.limb_width / 2))
        if "FLIGHT" in self.active_powerups:
            rest_l_base = math.pi * 0.8; rest_r_base = math.pi * 0.2; flap_down_l_base = rest_l_base + self.wing_flap_magnitude; flap_down_r_base = rest_r_base - self.wing_flap_magnitude
            if self.wing_flapping:
                self.wing_flap_timer -= dt
                if self.wing_flap_timer <= 0: self.wing_flapping = False; self.wing_flap_timer = 0.0; self.l_wing_base_angle = rest_l_base; self.r_wing_base_angle = rest_r_base
                else: progress = 1.0 - (self.wing_flap_timer / self.wing_flap_duration); flap_phase = math.sin(progress * math.pi); self.l_wing_base_angle = rest_l_base + (flap_down_l_base - rest_l_base) * flap_phase; self.r_wing_base_angle = rest_r_base + (flap_down_r_base - rest_r_base) * flap_phase
            else: lerp_speed = 6.0 * dt; self.l_wing_base_angle += (rest_l_base - self.l_wing_base_angle) * lerp_speed; self.r_wing_base_angle += (rest_r_base - self.r_wing_base_angle) * lerp_speed
            self.l_wing_upper_angle = self.l_wing_base_angle - 0.4; self.l_wing_lower_angle = self.l_wing_base_angle + 0.6; self.r_wing_upper_angle = self.r_wing_base_angle + 0.4; self.r_wing_lower_angle = self.r_wing_base_angle - 0.6
        if not self.is_tumbling:
            is_walking = abs(intended_vx) > 0 and not self.is_jumping and not self.is_kicking and not self.on_other_player_head
            if is_walking: self.walk_cycle_timer += WALK_CYCLE_SPEED
            elif not self.is_jumping and not self.is_kicking: self.walk_cycle_timer *= 0.9
            if abs(self.walk_cycle_timer) < 0.1: self.walk_cycle_timer = 0
            if self.is_kicking:
                 self.walk_cycle_timer = 0; self.kick_timer += 1; progress = min(self.kick_timer / self.kick_duration, 1.0); windup_end = 0.20; impact_start = 0.25; impact_end = 0.50; follow_end = 1.0
                 if progress < windup_end: thigh_prog_angle = KICK_THIGH_WINDUP_ANGLE * (progress / windup_end)
                 elif progress < impact_end: impact_progress = (progress - windup_end) / (impact_end - windup_end); thigh_prog_angle = KICK_THIGH_WINDUP_ANGLE + (KICK_THIGH_FOLLOW_ANGLE - KICK_THIGH_WINDUP_ANGLE) * impact_progress
                 else: follow_progress = (progress - impact_end) / (follow_end - impact_end); ease_out_factor = 1.0 - follow_progress**1.5; thigh_prog_angle = KICK_THIGH_FOLLOW_ANGLE * ease_out_factor
                 if progress < impact_start: shin_prog_angle = KICK_SHIN_WINDUP_ANGLE * (progress / impact_start)
                 elif progress < impact_end: impact_progress = (progress - impact_start) / (impact_end - impact_start); ease_in_factor = impact_progress ** 2; shin_prog_angle = KICK_SHIN_WINDUP_ANGLE + (KICK_SHIN_IMPACT_ANGLE - KICK_SHIN_WINDUP_ANGLE) * ease_in_factor
                 else: follow_progress = (progress - impact_end) / (follow_end - impact_end); shin_prog_angle = KICK_SHIN_IMPACT_ANGLE + (KICK_SHIN_FOLLOW_ANGLE - KICK_SHIN_IMPACT_ANGLE) * follow_progress
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
        else:
            tumble_speed = self.rotation_velocity * 1.5; current_time_ms = pygame.time.get_ticks()
            self.l_upper_arm_angle = math.sin(current_time_ms * 0.01 + 1) * 0.8 + tumble_speed * 0.05
            self.r_upper_arm_angle = math.sin(current_time_ms * 0.01 + 2) * 0.8 - tumble_speed * 0.05
            self.l_forearm_angle = math.sin(current_time_ms * 0.015 + 3) * 1.2
            self.r_forearm_angle = math.sin(current_time_ms * 0.015 + 4) * 1.2
            self.l_thigh_angle = math.sin(current_time_ms * 0.01 + 5) * 0.6 - tumble_speed * 0.04
            self.r_thigh_angle = math.sin(current_time_ms * 0.01 + 6) * 0.6 + tumble_speed * 0.04
            self.l_shin_angle = math.sin(current_time_ms * 0.015 + 7) * 1.0
            self.r_shin_angle = math.sin(current_time_ms * 0.015 + 0) * 1.0
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
        body_width = self.limb_width * 1.5
        self.body_rect.width = int(body_width); self.body_rect.height = max(1, int(self.hip_pos[1] - self.neck_pos[1])); self.body_rect.centerx = int(self.hip_pos[0]); self.body_rect.top = int(self.neck_pos[1])
    def get_kick_impact_point(self): # ... (no change) ...
        impact_start = 0.25; impact_end = 0.6
        if self.is_kicking:
            if self.kick_duration <= 0: return None
            progress = self.kick_timer / self.kick_duration
            if impact_start < progress < impact_end: return self.r_foot_pos if self.facing_direction == 1 else self.l_foot_pos
        return None
    def get_head_position_radius(self): return self.head_pos, self.head_radius
    def get_body_rect(self): return self.body_rect
    
    def get_sword_position(self):
        """Return sword data for collision detection: (tip_x, tip_y, base_x, base_y, angle)"""
        if not self.is_sword:
            return None
        
        hand_pos = self.r_hand_pos if self.facing_direction == 1 else self.l_hand_pos
        sword_len = self.torso_length * SWORD_LENGTH_FACTOR
        
        # Calculate sword tip and base positions based on hand position and sword angle
        tip_x = hand_pos[0] + sword_len * math.cos(self.sword_angle)
        tip_y = hand_pos[1] + sword_len * math.sin(self.sword_angle)
        
        return (tip_x, tip_y, hand_pos[0], hand_pos[1], self.sword_angle)
        
    def draw(self, screen): # ... (no change) ...
        all_points = [self.head_pos, self.neck_pos, self.hip_pos, self.shoulder_pos, self.l_elbow_pos, self.r_elbow_pos, self.l_hand_pos, self.r_hand_pos, self.l_knee_pos, self.r_knee_pos, self.l_foot_pos, self.r_foot_pos]
        if "ROCKET_LAUNCHER" in self.active_powerups: all_points.append(self.gun_tip_pos)
        
        # Add sword tip point to all_points if the player has a sword
        if self.is_sword:
            sword_data = self.get_sword_position()
            if sword_data:
                tip_x, tip_y, base_x, base_y, angle = sword_data
                all_points.append((tip_x, tip_y))  # Add sword tip to points
                
                # Add more points around the sword to ensure proper rendering
                sword_len = self.torso_length * SWORD_LENGTH_FACTOR
                sword_width = self.limb_width * SWORD_WIDTH_FACTOR
                
                # Calculate points at the edges of the sword for proper bounding box
                perp_x = math.cos(angle + math.pi/2) * sword_width
                perp_y = math.sin(angle + math.pi/2) * sword_width
                
                # Add edges of the sword
                all_points.append((tip_x + perp_x, tip_y + perp_y))
                all_points.append((tip_x - perp_x, tip_y - perp_y))
                all_points.append((base_x + perp_x, base_y + perp_y))
                all_points.append((base_x - perp_x, base_y - perp_y))
        
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
        pygame.draw.circle(temp_surf, ITALY_WHITE, head_center_int, int(self.head_radius), 0)
        eye_offset_x = self.head_radius * 0.35 * self.facing_direction; eye_offset_y = -self.head_radius * 0.1; eye_radius = int(max(1, 3 * (self.head_radius / self.base_head_radius)))
        eye_pos_x = int(head_center_int[0] + eye_offset_x); eye_y = int(head_center_int[1] + eye_offset_y)
        pygame.draw.circle(temp_surf, self.eye_color, (eye_pos_x, eye_y - eye_radius // 2 - 1), eye_radius); pygame.draw.circle(temp_surf, self.eye_color, (eye_pos_x, eye_y + eye_radius // 2 + 1), eye_radius)
        nose_tip_x = head_center_int[0] + (self.head_radius * 0.5 + self.current_nose_length) * self.facing_direction; nose_tip_y = head_center_int[1] + self.head_radius * 0.1
        nose_base_x = head_center_int[0] + (self.head_radius * 0.3) * self.facing_direction; nose_base_y1 = nose_tip_y - self.current_nose_width / 2; nose_base_y2 = nose_tip_y + self.current_nose_width / 2
        nose_points = [(int(nose_base_x), int(nose_base_y1)), (int(nose_tip_x), int(nose_tip_y)), (int(nose_base_x), int(nose_base_y2))]; pygame.draw.polygon(temp_surf, NOSE_COLOR, nose_points)
        pygame.draw.circle(temp_surf, BLACK, head_center_int, int(self.head_radius), 1)
        torso_start_pos = offset_pos(self.neck_pos); torso_segment_height = self.torso_length / 3; current_torso_y = torso_start_pos[1]
        for i in range(3): rect_center_x = torso_start_pos[0]; rect_center_y = current_torso_y + torso_segment_height / 2; draw_rotated_rectangle(temp_surf, self.torso_colors[i], (rect_center_x, rect_center_y), self.limb_width, torso_segment_height, 0); current_torso_y += torso_segment_height
        def draw_limb_segment_offset(start_pos, end_pos, length, color, limb_w):
            o_start = offset_pos(start_pos); o_end = offset_pos(end_pos); center_x = (o_start[0] + o_end[0]) / 2; center_y = (o_start[1] + o_end[1]) / 2
            dx = o_end[0] - o_start[0]; dy = o_end[1] - o_start[1]; draw_length = math.hypot(dx, dy);
            if draw_length < 1: draw_length = 1
            angle = math.atan2(dy, dx); draw_rotated_rectangle(temp_surf, color, (center_x, center_y), draw_length, limb_w, angle + math.pi/2)
        draw_limb_segment_offset(self.shoulder_pos, self.l_elbow_pos, self.upper_arm_length, self.arm_colors[0], self.limb_width); draw_limb_segment_offset(self.l_elbow_pos, self.l_hand_pos, self.forearm_length, self.arm_colors[1], self.limb_width)
        draw_limb_segment_offset(self.shoulder_pos, self.r_elbow_pos, self.upper_arm_length, self.arm_colors[0], self.limb_width); draw_limb_segment_offset(self.r_elbow_pos, self.r_hand_pos, self.forearm_length, self.arm_colors[1], self.limb_width)
        draw_limb_segment_offset(self.hip_pos, self.l_knee_pos, self.thigh_length, self.leg_colors[0], self.limb_width); draw_limb_segment_offset(self.l_knee_pos, self.l_foot_pos, self.shin_length, self.leg_colors[1], self.limb_width)
        draw_limb_segment_offset(self.hip_pos, self.r_knee_pos, self.thigh_length, self.leg_colors[0], self.limb_width); draw_limb_segment_offset(self.r_knee_pos, self.r_foot_pos, self.shin_length, self.leg_colors[1], self.limb_width)
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

        # --- Draw Sword --- # Added
        if self.is_sword:
            print(f"Drawing sword for player {1 if self.facing_direction == 1 else 2}") if debug_mode else None
            hand_pos = self.r_hand_pos if self.facing_direction == 1 else self.l_hand_pos
            o_hand_pos = offset_pos(hand_pos)
            # REMOVED local constant definitions - Use global ones
            sword_len = self.torso_length * SWORD_LENGTH_FACTOR
            sword_width = self.limb_width * SWORD_WIDTH_FACTOR
            hilt_length = sword_width * 3 # Relative to sword width
            hilt_width = sword_width * 3 # Hilt crossguard width
            
            # Determine sword angle based on kick animation or default holding angle
            kick_progress = 0.0
            if self.is_kicking:
                # Ensure kick_duration is not zero to avoid division error
                if self.kick_duration > 0:
                    kick_progress = min(self.kick_timer / self.kick_duration, 1.0)
                else:
                    kick_progress = 1.0 # Or 0.0, depending on desired end state

                windup_end = 0.20; impact_start = 0.25; impact_end = 0.50; follow_end = 1.0
                if kick_progress < impact_start: # Windup
                    swing_prog = kick_progress / impact_start if impact_start > 0 else 1.0
                    base_angle_offset = -math.pi * 0.8 * (swing_prog**2)
                elif kick_progress < follow_end: # Swing + Follow
                    # Ensure denominator is not zero
                    duration_follow = follow_end - impact_start
                    follow_prog = (kick_progress - impact_start) / duration_follow if duration_follow > 0 else 1.0

                    max_forward_angle = math.pi * 0.3
                    if follow_prog < 0.5:
                       ease_in_swing = (follow_prog * 2)**1.5
                       base_angle_offset = -math.pi*0.8 + (max_forward_angle - (-math.pi*0.8)) * ease_in_swing
                    else:
                       ease_out_follow = 1.0 - ((follow_prog - 0.5) * 2)**1.5
                       base_angle_offset = max_forward_angle * ease_out_follow
                else: # End of kick
                     base_angle_offset = 0
            else: # Idle holding angle
                base_angle_offset = -math.pi / 4

            # Set the angle for drawing and collision detection
            # Old angle calculation that worked for hitting the ball
            if self.facing_direction == 1:
                self.sword_angle = base_angle_offset * self.facing_direction + (-math.pi / 2)  # Right-facing player
            else:
                self.sword_angle = base_angle_offset * self.facing_direction + (math.pi/2)  # Left-facing player
            
            if debug_mode:
                print(f"Sword angle: {self.sword_angle}, Hand pos: {hand_pos}, Offset hand: {o_hand_pos}")
                
            # Play sword swing sound if kicking
            # Removed duplicate sound playing since we now handle it in start_kick

            # Draw the sword based on reference image
            # Calculate coordinates in world space
            sword_base_x = hand_pos[0]
            sword_base_y = hand_pos[1]
            
            # Calculate blade coordinates
            blade_length = sword_len * 1.2  # Make blade longer
            blade_width = sword_width * 0.6  # Make blade thinner
            blade_start_x = sword_base_x
            blade_start_y = sword_base_y
            blade_end_x = blade_start_x + blade_length * math.cos(self.sword_angle)
            blade_end_y = blade_start_y + blade_length * math.sin(self.sword_angle)
            blade_center_x = blade_start_x + (blade_length/2) * math.cos(self.sword_angle)
            blade_center_y = blade_start_y + (blade_length/2) * math.sin(self.sword_angle)
            
            # Calculate crossguard coordinates (perpendicular to blade)
            crossguard_angle = self.sword_angle + math.pi/2
            crossguard_length = hilt_width * 2
            crossguard_width = blade_width * 1.5
            crossguard_center_x = sword_base_x
            crossguard_center_y = sword_base_y
            
            # Calculate handle coordinates (opposite direction from blade)
            handle_length = sword_len * 0.3
            handle_width = blade_width * 0.8
            handle_center_x = sword_base_x - (handle_length/2) * math.cos(self.sword_angle)
            handle_center_y = sword_base_y - (handle_length/2) * math.sin(self.sword_angle)
            
            # Draw handle (dark brown)
            draw_rotated_rectangle(screen, (101, 67, 33), 
                                  (handle_center_x, handle_center_y), 
                                  handle_length, handle_width, 
                                  self.sword_angle)
            
            # Draw crossguard (metallic silver)
            draw_rotated_rectangle(screen, (169, 169, 169), 
                                  (crossguard_center_x, crossguard_center_y), 
                                  crossguard_length, crossguard_width, 
                                  crossguard_angle)
            
            # Draw blade (metallic silver with gradient)
            # Main blade
            draw_rotated_rectangle(screen, (192, 192, 192), 
                                  (blade_center_x, blade_center_y), 
                                  blade_length, blade_width, 
                                  self.sword_angle)
            
            # Blade edge highlight
            blade_edge_width = max(1, int(blade_width * 0.3))
            pygame.draw.line(screen, (220, 220, 220), 
                            (int(blade_start_x), int(blade_start_y)), 
                            (int(blade_end_x), int(blade_end_y)), 
                            blade_edge_width)
            
            # Blade tip highlight
            pygame.draw.circle(screen, (220, 220, 220), 
                              (int(blade_end_x), int(blade_end_y)), 
                              int(blade_width * 0.4))

        # --- Tumble Rotation and Blitting ---


# --- Ball Class ---
# ... (Ball class unchanged) ...
class Ball:
    def __init__(self, x, y, radius):
        self.x = x; self.y = y; self.radius = radius; self.vx = 0; self.vy = 0;
        self.last_hit_by = None; self.rotation_angle = 0
        self.is_frozen = False; self.freeze_effect_timer = 0.0
        self.on_left_crossbar = False  # Håller reda på om bollen redan är på vänster ribba
        self.on_right_crossbar = False  # Håller reda på om bollen redan är på höger ribba
    def apply_force(self, force_x, force_y, hitter='player'):
        if self.is_frozen: return
        self.vx += force_x; self.vy += force_y; self.last_hit_by = hitter
    def update(self, dt):
        if debug_mode and dt > 0:  # Add debug output for ball height
            screen_height_percent = ((SCREEN_HEIGHT - self.y) / SCREEN_HEIGHT) * 100
            print(f"Ball height: {SCREEN_HEIGHT - self.y:.1f} ({screen_height_percent:.1f}% of screen)")
            
        if self.freeze_effect_timer > 0: self.freeze_effect_timer -= dt
        if self.is_frozen: return False
        
        # Get weather effects for current weather
        weather_effect = WEATHER_EFFECTS.get(current_weather, WEATHER_EFFECTS["SUNNY"])
        
        # Apply gravity based on weather
        current_gravity = GRAVITY * weather_effect.get("gravity", 1.0)
        
        # Apply wind force if in windy weather
        if current_weather == "WINDY":
            wind_force = weather_effect.get("wind_force", 0.0)
            self.vx += (wind_force * WEATHER_WIND_DIRECTION * 0.03 * dt)
        
        # Update physics with weather-modified values
        self.rotation_angle += self.vx * 0.015
        self.rotation_angle %= (2 * math.pi)
        self.vy += current_gravity
        self.vx *= BALL_FRICTION
        self.x += self.vx
        self.y += self.vy
        
        hit_ground = False
        hit_wall_this_frame = False
        hit_shield_this_frame = False
        hit_crossbar_this_frame = False
        
        # Get current goal dimensions accounting for enlargement
        current_goal_height_p1 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        current_goal_y_p1 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        current_goal_height_p2 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        current_goal_y_p2 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        
        # Crossbar collision - left goal
        left_goal_width = abs(GOAL_DEPTH_X) * 2.0  # Match the width used in draw_goal_isometric
        left_crossbar_y = current_goal_y_p1
        left_crossbar_height = 8  # Match the height from draw_goal_isometric
        
        # Spara det tidigare tillståndet
        was_on_left_crossbar = self.on_left_crossbar
        self.on_left_crossbar = False
        
        # Check if ball is in horizontal range of the crossbar
        if (self.x - self.radius <= GOAL_LINE_X_LEFT + left_goal_width/2 and 
            self.x + self.radius >= GOAL_LINE_X_LEFT - left_goal_width/2):
            
            # Check if ball is in vertical range of the crossbar
            crossbar_top = left_crossbar_y - left_crossbar_height/2
            crossbar_bottom = left_crossbar_y + left_crossbar_height/2
            
            if (self.y + self.radius >= crossbar_top and
                self.y - self.radius <= crossbar_bottom):
                
                # Markera att bollen nu är på ribban
                self.on_left_crossbar = True
                
                # Calculate the hit position relative to the center of the crossbar
                hit_offset = (self.y - left_crossbar_y) / (left_crossbar_height/2)
                hit_offset = max(-1.0, min(1.0, hit_offset))  # Clamp to [-1, 1]
                
                # Determine if approaching from top or bottom
                from_top = self.vy > 0
                
                # Bara korrigera positionen om bollen kommer tillräckligt snabbt
                if abs(self.vy) > 0.5 or not was_on_left_crossbar:
                    if from_top:
                        # Hit from top - push up
                        self.y = crossbar_top - self.radius
                        
                        # Angle the bounce based on hit position (center vs edge)
                        bounce_angle = hit_offset * 0.3  # Up to 0.3 radians (about 17 degrees)
                        bounce_vx = self.vx + (self.vy * bounce_angle * 0.5)
                        self.vy *= -BALL_BOUNCE * 0.9
                        self.vx = bounce_vx
                    else:
                        # Hit from bottom - push down
                        self.y = crossbar_bottom + self.radius
                        
                        # Angle the bounce based on hit position (center vs edge)
                        bounce_angle = hit_offset * 0.3  # Up to 0.3 radians (about 17 degrees)
                        bounce_vx = self.vx - (self.vy * bounce_angle * 0.5)
                        self.vy *= -BALL_BOUNCE * 0.9
                        self.vx = bounce_vx
                    
                    # Sätt bara hit_crossbar_this_frame när det är en verklig kollision
                    if abs(self.vy) > 0.5:
                        hit_crossbar_this_frame = True
        
        # Crossbar collision - right goal
        right_goal_width = abs(GOAL_DEPTH_X) * 2.0  # Match the width used in draw_goal_isometric
        right_crossbar_y = current_goal_y_p2
        right_crossbar_height = 8  # Match the height from draw_goal_isometric
        
        # Spara det tidigare tillståndet
        was_on_right_crossbar = self.on_right_crossbar
        self.on_right_crossbar = False
        
        # Check if ball is in horizontal range of the crossbar
        if (self.x - self.radius <= GOAL_LINE_X_RIGHT + right_goal_width/2 and 
            self.x + self.radius >= GOAL_LINE_X_RIGHT - right_goal_width/2):
            
            # Check if ball is in vertical range of the crossbar
            crossbar_top = right_crossbar_y - right_crossbar_height/2
            crossbar_bottom = right_crossbar_y + right_crossbar_height/2
            
            if (self.y + self.radius >= crossbar_top and
                self.y - self.radius <= crossbar_bottom):
                
                # Markera att bollen nu är på ribban
                self.on_right_crossbar = True
                
                # Calculate the hit position relative to the center of the crossbar
                hit_offset = (self.y - right_crossbar_y) / (right_crossbar_height/2)
                hit_offset = max(-1.0, min(1.0, hit_offset))  # Clamp to [-1, 1]
                
                # Determine if approaching from top or bottom
                from_top = self.vy > 0
                
                # Bara korrigera positionen om bollen kommer tillräckligt snabbt
                if abs(self.vy) > 0.5 or not was_on_right_crossbar:
                    if from_top:
                        # Hit from top - push up
                        self.y = crossbar_top - self.radius
                        
                        # Angle the bounce based on hit position (center vs edge)
                        bounce_angle = hit_offset * 0.3  # Up to 0.3 radians (about 17 degrees)
                        bounce_vx = self.vx + (self.vy * bounce_angle * 0.5)
                        self.vy *= -BALL_BOUNCE * 0.9
                        self.vx = bounce_vx
                    else:
                        # Hit from bottom - push down
                        self.y = crossbar_bottom + self.radius
                        
                        # Angle the bounce based on hit position (center vs edge)
                        bounce_angle = hit_offset * 0.3  # Up to 0.3 radians (about 17 degrees)
                        bounce_vx = self.vx - (self.vy * bounce_angle * 0.5)
                        self.vy *= -BALL_BOUNCE * 0.9
                        self.vx = bounce_vx
                    
                    # Sätt bara hit_crossbar_this_frame när det är en verklig kollision
                    if abs(self.vy) > 0.5:
                        hit_crossbar_this_frame = True
        
        # Play sound if crossbar was hit (och endast om bollen inte var på ribban i förra framen)
        if hit_crossbar_this_frame and ((self.on_left_crossbar and not was_on_left_crossbar) or 
                                       (self.on_right_crossbar and not was_on_right_crossbar)):
            # Spela ljudet endast om hastigheten är tillräckligt hög
            if abs(self.vy) > 3.0:  # Minsta hastighet för att generera ljud
                play_sound(loaded_sounds['crossbar_hit'])
        
        # Shield collision
        if p1_shield_active:
            shield_rect = pygame.Rect(0, current_goal_y_p1, POWERUP_GOAL_SHIELD_WIDTH, current_goal_height_p1)
            if self.x - self.radius < shield_rect.right and self.x + self.radius > shield_rect.left and \
               self.y + self.radius > shield_rect.top and self.y - self.radius < shield_rect.bottom:
                if self.vx < 0: self.x = shield_rect.right + self.radius; self.vx *= -BALL_BOUNCE; hit_shield_this_frame = True
        if p2_shield_active:
            shield_rect = pygame.Rect(SCREEN_WIDTH - POWERUP_GOAL_SHIELD_WIDTH, current_goal_y_p2, POWERUP_GOAL_SHIELD_WIDTH, current_goal_height_p2)
            if self.x + self.radius > shield_rect.left and self.x - self.radius < shield_rect.right and \
               self.y + self.radius > shield_rect.top and self.y - self.radius < shield_rect.bottom:
                if self.vx > 0: self.x = shield_rect.left - self.radius; self.vx *= -BALL_BOUNCE; hit_shield_this_frame = True
        
        # Spela shield-ljudet bara om vi verkligen har en kollision och hastigheten är tillräckligt stor
        if hit_shield_this_frame and abs(self.vx) > 1.0: 
            play_sound(loaded_sounds['wall_hit'])
        
        # Wall collision  
        if self.x + self.radius >= SCREEN_WIDTH: self.x = SCREEN_WIDTH - self.radius; self.vx *= -BALL_BOUNCE * 0.8; hit_wall_this_frame = True
        elif self.x - self.radius <= 0: self.x = self.radius; self.vx *= -BALL_BOUNCE * 0.8; hit_wall_this_frame = True
        
        # Spela wall-ljudet bara om vi har en kollision med väggen (inte med shield) och hastigheten är tillräckligt stor
        if hit_wall_this_frame and not hit_shield_this_frame and abs(self.vx) > 1.0:
            play_sound(loaded_sounds['wall_hit'])
            
        # Ground collision
        if self.y + self.radius >= GROUND_Y:
            if self.vy >= 0:
                impact_vy = abs(self.vy); self.y = GROUND_Y - self.radius; self.vy *= -BALL_BOUNCE; self.vx *= 0.9
                if abs(self.vy) < 1: self.vy = 0
                if impact_vy > 1.5: play_sound(loaded_sounds['ball_bounce'])
                hit_ground = True
        if abs(self.vx) < 0.1 and self.is_on_ground(): self.vx = 0
        return hit_ground
    def is_on_ground(self): return self.y + self.radius >= GROUND_Y - 0.5
    def draw(self, screen):
        center_tuple = (int(self.x), int(self.y));
        pygame.draw.circle(screen, WHITE, center_tuple, self.radius)
        pent_size = self.radius * 0.40; hex_size = self.radius * 0.42; dist_factor = 0.65; num_around = 5; angle_step = 2 * math.pi / num_around
        draw_pentagon(screen, BLACK, center_tuple, pent_size, self.rotation_angle)
        for i in range(num_around):
            angle = self.rotation_angle + (i * angle_step) + angle_step / 2; shape_center_x = center_tuple[0] + self.radius * dist_factor * math.cos(angle); shape_center_y = center_tuple[1] + self.radius * dist_factor * math.sin(angle); shape_center = (shape_center_x, shape_center_y)
            if i % 2 == 0: draw_hexagon(screen, BLACK, shape_center, hex_size, angle + self.rotation_angle * 0.5, width=1)
            else: draw_pentagon(screen, BLACK, shape_center, pent_size, angle + self.rotation_angle * 0.5)
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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)); pygame.display.set_caption("Ciao Kick!");
clock = pygame.time.Clock()

# --- Sound Loading ---
# ... (sound loading unchanged) ...
def load_sounds(sound_dir="sounds"):
    sounds = {}
    sound_files = {
        "kick": ["kick_ball1.wav", "kick_ball2.wav"],
        "jump": ["jump1.wav"],
        "land": ["land1.wav"],
        "wall_hit": ["wall_hit1.wav"],
        "player_bump": ["player_bump1.wav"],
        "headbutt": ["headbutt1.wav"],
        "body_hit": ["body_hit1.wav"],
        "combo": ["combo_sparkle1.wav", "combo_sparkle2.wav", "combo_sparkle3.wav", "combo_sparkle4.wav"],
        "ball_bounce": ["ball_bounce1.wav"],
        "nils_wins": ["nils_wins.wav"],
        "harry_wins": ["harry_wins.wav"],
        "nils_ahead": ["nils_ahead.wav"],
        "harry_ahead": ["harry_ahead.wav"],
        "super_jackpot": ["super_jackpot.wav"],
        "sword_hit": ["sword_hit.wav"], # Sound for sword hitting objects
        "crossbar_hit": ["crossbar_hit.wav"], # Sound for ball hitting the crossbar
        # Weather announcement sounds
        # "weather_sunny": ["sunny.wav"],
        # "weather_rainy": ["rainy.wav"],
        # "weather_windy": ["windy.wav"],
        # "weather_snowy": ["snowy.wav"],
        # "weather_foggy": ["foggy.wav"],
        # "weather_gothenburg": ["gothenburg_weather.wav"]
    }
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
    required_keys = ["goal_p1", "goal_p2", "kick", "jump", "land", "wall_hit", "player_bump", "headbutt", "body_hit", "combo", "ball_bounce", "nils_wins", "harry_wins", "nils_ahead", "harry_ahead", "super_jackpot", "crossbar_hit", # Add weather keys
                     "weather_sunny", "weather_rainy", "weather_windy", "weather_snowy", "weather_foggy", "weather_gothenburg"]
    for key in required_keys:
        if key not in sounds: sounds[key] = []
    if 'numbers' not in sounds: sounds['numbers'] = {}
    
    # Explicitly remove weather sound keys if commented out, so the check later doesn't fail
    weather_keys_to_remove = ["weather_sunny", "weather_rainy", "weather_windy", "weather_snowy", "weather_foggy", "weather_gothenburg"]
    for w_key in weather_keys_to_remove:
        if w_key in sounds:
             # Check if the sound list is empty or not properly loaded (might happen if file existed but failed loading)
            if not sounds[w_key]: 
                del sounds[w_key]
                print(f"Ensured removal of commented/missing weather sound key: {w_key}")

    return sounds
# --- Sound Playing Helpers ---
def play_sound(sound_list): # Modifierad för att implementera ljudsäkerhet
    global sound_last_played
    if not sound_list:
        return
    
    # Skapa en dictionary för att lagra senaste tidpunkt för ljuduppspelning om den inte redan finns
    if 'sound_last_played' not in globals():
        global sound_last_played
        sound_last_played = {}
    
    # Hämta aktuell tid
    current_time = time.time()
    
    # Skapa nyckeln baserat på ID för första ljudet i listan (alla ljud i en grupp hanteras tillsammans)
    sound_key = id(sound_list[0]) if sound_list else None
    
    # Kontrollera om ljudet nyligen har spelats
    if sound_key in sound_last_played:
        # Standard cooldown på 0.15 sekunder för alla ljud
        cooldown = 0.15
        
        time_since_last_played = current_time - sound_last_played[sound_key]
        if time_since_last_played < cooldown:
            # För tidigt att spela ljudet igen
            return
    
    # Spela ljudet och uppdatera tidsstämpel
    sound_to_play = random.choice(sound_list)
    ch = pygame.mixer.find_channel(True)
    if ch: 
        ch.play(sound_to_play)
        sound_last_played[sound_key] = current_time
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
# Pass team colors during instantiation
player1 = StickMan(SCREEN_WIDTH // 4, GROUND_Y, facing=1, team_color=P1_COLOR_MAIN, team_accent=P1_COLOR_ACCENT)
player2 = StickMan(SCREEN_WIDTH * 3 // 4, GROUND_Y, facing=-1, team_color=P2_COLOR_MAIN, team_accent=P2_COLOR_ACCENT) # Pass P2 colors
player_list = [player1, player2]
ball = Ball(SCREEN_WIDTH // 2, GROUND_Y - 20, 15)
font_large = pygame.font.Font(None, 50); font_medium = pygame.font.Font(None, 36); font_small = pygame.font.Font(None, 28)
font_timestamp = pygame.font.Font(None, 20); font_goal = pygame.font.Font(None, 80)
winner_images = {}
try:
    winner_images[1] = pygame.image.load("images/nils_wins.png").convert_alpha()
    winner_images[2] = pygame.image.load("images/harry_wins.png").convert_alpha()
    winner_images["harry_eats"] = pygame.image.load("images/harry_eats.png").convert_alpha()
    print("Loaded winner images.")
except pygame.error as e:
    print(f"Warning: Could not load winner images: {e}")
    winner_images[1] = None; winner_images[2] = None
    winner_images["harry_eats"] = None

# --- Score & State Variables ---
player1_score = 0; player2_score = 0; p1_games_won = 0; p2_games_won = 0
game_scores = []; match_active = True; match_over_timer = 0.0; game_over = False
match_winner = None; overall_winner = None; match_end_sound_played = False
game_over_sound_played = False
announcement_queue = []
goal_message_timer = 0; screen_flash_timer = 0
ball_was_on_ground = True; particles = []; p1_can_headbutt = True; p2_can_headbutt = True
p1_body_collision_timer = 0; p2_body_collision_timer = 0; current_hit_count = 0
powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
active_rockets = []; active_explosions = []
ball_freeze_timer = 0.0
p1_shield_active = False; p1_shield_timer = 0.0
p2_shield_active = False; p2_shield_timer = 0.0
jackpot_triggered_this_match = False
p1_goal_enlarged_timer = 0.0
p2_goal_enlarged_timer = 0.0
weather_message_text = ""
weather_message_timer = 0.0

# --- Weather Variables ---
current_weather = random.choice(WEATHER_TYPES)
weather_particles = []
weather_wind_change_timer = 15.0  # Time until wind direction changes


# --- Reset/Start Functions ---
def reset_positions(): # Keeps powerups active, resets player state only
    global ball_was_on_ground, current_hit_count, p1_can_headbutt, p2_can_headbutt, p1_body_collision_timer, p2_body_collision_timer, active_rockets, active_explosions
    ball.x = SCREEN_WIDTH // 2; ball.y = SCREEN_HEIGHT // 3; ball.vx = 0; ball.vy = 0;
    if ball.is_frozen: ball.freeze_effect_timer = POWERUP_BALL_FREEZE_DURATION * 0.1
    player1.x = SCREEN_WIDTH // 4; player1.y = GROUND_Y; player1.vx = 0; player1.vy = 0; player1.is_kicking = False; player1.on_other_player_head = False; player1.facing_direction = 1; player1.is_jumping = False; player1.is_tumbling = False; player1.rotation_angle = 0; player1.rotation_velocity = 0; player1.is_controls_reversed = False
    player2.x = SCREEN_WIDTH * 3 // 4; player2.y = GROUND_Y; player2.vx = 0; player2.vy = 0; player2.is_kicking = False; player2.on_other_player_head = False; player2.facing_direction = -1; player2.is_jumping = False; player2.is_tumbling = False; player2.rotation_angle = 0; player2.rotation_velocity = 0; player2.is_controls_reversed = False
    # Keep player active_powerups dictionaries
    # Keep global timers (freeze, shield, goal enlarge)
    current_hit_count = 0; ball_was_on_ground = False; p1_can_headbutt = True; p2_can_headbutt = True; p1_body_collision_timer = 0; p2_body_collision_timer = 0;
    active_rockets = []; active_explosions = []
def start_new_match(): # Full reset for new match
    global player1_score, player2_score, match_active, match_winner, match_over_timer, match_end_sound_played, announcement_queue, powerup_spawn_timer, active_powerups, ball_freeze_timer, p1_shield_active, p1_shield_timer, p2_shield_active, p2_shield_timer, jackpot_triggered_this_match, p1_goal_enlarged_timer, p2_goal_enlarged_timer, current_weather, weather_particles, weather_wind_change_timer, CURRENT_WIND_FORCE, WEATHER_WIND_DIRECTION, current_time_of_day, weather_message_text, weather_message_timer # Added message variables
    player1_score = 0; player2_score = 0; match_active = True; match_winner = None; match_over_timer = 0.0; match_end_sound_played = False
    announcement_queue = []; reset_positions()
    player1.active_powerups = {}; player1.is_flying = False; player1.is_big = False; player1.is_shrunk = False; player1.is_enormous_head = False; player1.jump_power = BASE_JUMP_POWER; player1.player_speed = BASE_PLAYER_SPEED; player1.calculate_current_sizes()
    player2.active_powerups = {}; player2.is_flying = False; player2.is_big = False; player2.is_shrunk = False; player2.is_enormous_head = False; player2.jump_power = BASE_JUMP_POWER; player2.player_speed = BASE_PLAYER_SPEED; player2.calculate_current_sizes()
    active_powerups = []
    ball_freeze_timer = 0.0; ball.is_frozen = False; ball.freeze_effect_timer = 0.0
    p1_shield_active = False; p1_shield_timer = 0.0; p2_shield_active = False; p2_shield_timer = 0.0
    p1_goal_enlarged_timer = 0.0; p2_goal_enlarged_timer = 0.0
    player1.randomize_nose(); player2.randomize_nose()
    powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
    jackpot_triggered_this_match = False
    
    # Determine Time of Day based on total games played
    total_games = p1_games_won + p2_games_won
    time_index = total_games % len(TIMES_OF_DAY)
    current_time_of_day = TIMES_OF_DAY[time_index]
    print(f"Starting match at time: {current_time_of_day}")
    
    # Set up new weather conditions for this match
    current_weather = random.choice(WEATHER_TYPES)
    weather_particles = []
    weather_wind_change_timer = 15.0
    CURRENT_WIND_FORCE = 0 # Reset current wind force
    WEATHER_WIND_DIRECTION = random.choice([-1, 1]) # Random initial direction for WINDY
    
    weather_effect = WEATHER_EFFECTS.get(current_weather, {})
    if current_weather == "WINDY":
        min_force, max_force = weather_effect.get("wind_force_range", (0.0, 0.0))
        CURRENT_WIND_FORCE = random.uniform(min_force, max_force)
        print(f"Starting WINDY match. Initial Force: {CURRENT_WIND_FORCE:.1f}, Direction: {'RIGHT' if WEATHER_WIND_DIRECTION > 0 else 'LEFT'}")
    elif current_weather == "GOTHENBURG_WEATHER":
         print(f"Starting GOTHENBURG_WEATHER match. Brace yourselves!")
    else:
         print(f"Starting {current_weather} match.")
         
    # Create weather particles
    for _ in range(WEATHER_PARTICLE_COUNT.get(current_weather, 0)):
        weather_particles.append(WeatherParticle(current_weather, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    print(f"Starting new match with {current_weather} weather.")

    # Select and set weather message (Added)
    possible_messages = WEATHER_MESSAGES.get(current_weather, [f"{current_weather.replace('_', ' ').title()} weather."])
    weather_message_text = random.choice(possible_messages)
    weather_message_timer = WEATHER_MESSAGE_DURATION
    
    # Queue weather sound (If sound files exist)
    weather_sound_key = f"weather_{current_weather.lower()}"
    if loaded_sounds.get(weather_sound_key):
        # Queue sound after a short delay to not overlap with message
        # (We'll handle the queuing logic later if needed, for now just prepare key)
        print(f"Attempting to queue sound: {weather_sound_key}") 
        # queue_sound(loaded_sounds[weather_sound_key]) # Uncomment later if sound queuing is desired
def start_new_game(): # Full reset
    global p1_games_won, p2_games_won, game_scores, game_over, overall_winner, announcement_queue, game_over_sound_played, active_powerups
    p1_games_won = 0; p2_games_won = 0; game_scores = []; game_over = False; overall_winner = None; game_over_sound_played = False
    active_powerups = []
    announcement_queue = []; start_new_match(); print("Starting new game.")

# --- Collision Handling Function (Player-Ball) ---
# ... (unchanged) ...
def handle_player_ball_collisions(player, ball, can_headbutt, body_collision_timer, is_ball_airborne):
    global current_hit_count
    kick_performed = False; headbutt_performed = False; score_increase = False; kick_pt = None; sword_hit = False
    
    # Check for sword collision with the ball
    if player.is_sword and player.is_kicking:  # Only check when the player has a sword and is kicking (swinging)
        sword_data = player.get_sword_position()
        if sword_data:
            tip_x, tip_y, base_x, base_y, angle = sword_data
            
            # Check if ball is colliding with the sword line segment
            # Using line-circle intersection with increased radius for easier hits
            dx = tip_x - base_x
            dy = tip_y - base_y
            line_len_sq = dx*dx + dy*dy
            
            if line_len_sq > 0:  # Avoid division by zero
                # Calculate closest point on line to circle center
                t = max(0, min(1, ((ball.x - base_x) * dx + (ball.y - base_y) * dy) / line_len_sq))
                closest_x = base_x + t * dx
                closest_y = base_y + t * dy
                
                # Check if the distance from closest point to ball center is less than ball radius
                # Use increased collision radius for sword (2.5x the ball radius) to match the new graphic
                dist_sq = (closest_x - ball.x)**2 + (closest_y - ball.y)**2
                if dist_sq < (ball.radius * 2.5)**2:
                    # We have a collision!
                    if player.kick_duration <= 0: progress = 1.0
                    else: progress = player.kick_timer / player.kick_duration
                    
                    # Only apply force during active part of swing
                    if 0.25 < progress < 0.6:
                        # Direction is perpendicular to the sword
                        perp_x = -dy / math.sqrt(line_len_sq)  # Normalized
                        perp_y = dx / math.sqrt(line_len_sq)   # Normalized
                        
                        # Apply force in the perpendicular direction with player's facing
                        force_x = SWORD_HIT_FORCE * perp_x * player.facing_direction
                        force_y = -SWORD_HIT_FORCE * 0.6  # Increased upward component (was 0.05)
                        
                        # Apply force with player velocity factor
                        if player.vx != 0:
                            force_x += player.vx * 0.5  # Reduced from 1.0
                        
                        # Apply force to ball
                        ball.apply_force(force_x, force_y, hitter=player)
                        play_sound(loaded_sounds.get('sword_hit', loaded_sounds['wall_hit']))
                        sword_hit = True
                        kick_pt = (closest_x, closest_y)  # Use collision point as kick point for particles
                        
                        if is_ball_airborne:
                            current_hit_count += 1
                            score_increase = True
    
    # Original kick detection logic
    local_kick_point = player.get_kick_impact_point()
    if local_kick_point and not sword_hit:  # Only check normal kicks if sword didn't hit
        dist_x = local_kick_point[0] - ball.x; dist_y = local_kick_point[1] - ball.y; dist_sq = dist_x**2 + dist_y**2
        eff_kick_rad = KICK_RADIUS_NORMAL + (KICK_RADIUS_FALLING_BONUS if ball.vy > BALL_FALLING_VELOCITY_THRESHOLD else 0)
        if dist_sq < (ball.radius + eff_kick_rad * (player.head_radius / player.base_head_radius))**2:
             if player.kick_duration <= 0: progress = 1.0
             else: progress = player.kick_timer / player.kick_duration
             if 0.25 < progress < 0.6:
                 kick_x = BASE_KICK_FORCE_X * KICK_FORCE_LEVEL * player.facing_direction; kick_y = BASE_KICK_FORCE_Y * KICK_FORCE_LEVEL
                 if player.vy < 0: kick_y += player.vy * 0.4
                 ball.apply_force(kick_x, kick_y, hitter=player); kick_performed = True; kick_pt = local_kick_point; play_sound(loaded_sounds['kick']);
                 if is_ball_airborne: current_hit_count += 1; score_increase = True
    
    # Rest of the function remains the same
    head_pos, head_radius = player.get_head_position_radius(); dist_x_head = ball.x - head_pos[0]; dist_y_head = ball.y - head_pos[1]
    dist_head_sq = dist_x_head**2 + dist_y_head**2; headbutt_cooldown_just_applied = False
    if dist_head_sq < (ball.radius + head_radius)**2:
        if can_headbutt:
            force_y = -HEADBUTT_UP_FORCE;
            if player.vy < 0: force_y -= abs(player.vy) * HEADBUTT_VY_MULTIPLIER
            force_x = player.vx * HEADBUTT_PLAYER_VX_FACTOR - dist_x_head * HEADBUTT_POS_X_FACTOR
            ball.apply_force(force_x, force_y, hitter=player); headbutt_cooldown_just_applied = True; headbutt_performed = True; play_sound(loaded_sounds['headbutt']);
            if is_ball_airborne: current_hit_count += 1; score_increase = True
    new_can_headbutt = can_headbutt
    if headbutt_cooldown_just_applied: new_can_headbutt = False
    elif not new_can_headbutt and dist_head_sq > (ball.radius + head_radius + 15)**2: new_can_headbutt = True
    new_body_collision_timer = body_collision_timer
    if not kick_performed and not headbutt_performed and body_collision_timer == 0:
        player_rect = player.get_body_rect(); closest_x = max(player_rect.left, min(ball.x, player_rect.right)); closest_y = max(player_rect.top, min(ball.y, player_rect.bottom))
        delta_x = ball.x - closest_x; delta_y = ball.y - closest_y; dist_sq_body = delta_x**2 + delta_y**2
        if dist_sq_body < ball.radius**2:
             collision_occurred = False
             if dist_sq_body > 0:
                 distance = math.sqrt(dist_sq_body); overlap = ball.radius - distance; collision_normal_x = delta_x / distance; collision_normal_y = delta_y / distance
                 push_amount = overlap + 0.2; ball.x += collision_normal_x * push_amount; ball.y += collision_normal_y * push_amount
                 rel_vx = ball.vx - player.vx; rel_vy = ball.vy - player.vy; vel_along_normal = rel_vx * collision_normal_x + rel_vy * collision_normal_y
                 if vel_along_normal < 0:
                     impulse_scalar = -(1 + PLAYER_BODY_BOUNCE) * vel_along_normal; bounce_vx = impulse_scalar * collision_normal_x; bounce_vy = impulse_scalar * collision_normal_y
                     bounce_vx += player.vx * PLAYER_VEL_TRANSFER; bounce_vy += player.vy * PLAYER_VEL_TRANSFER
                     new_vel_mag_sq = bounce_vx**2 + bounce_vy**2
                     if new_vel_mag_sq < MIN_BODY_BOUNCE_VEL**2:
                         if new_vel_mag_sq > 0: scale = MIN_BODY_BOUNCE_VEL / math.sqrt(new_vel_mag_sq); bounce_vx *= scale; bounce_vy *= scale
                         else: bounce_vx = collision_normal_x * MIN_BODY_BOUNCE_VEL; bounce_vy = collision_normal_y * MIN_BODY_BOUNCE_VEL
                     ball.vx = bounce_vx; ball.vy = bounce_vy; new_body_collision_timer = PLAYER_BODY_COLLISION_FRAMES; collision_occurred = True
             elif dist_sq_body == 0:
                  ball.y = player_rect.top - ball.radius - 0.1
                  if ball.vy > 0: ball.vy *= -PLAYER_BODY_BOUNCE
                  new_body_collision_timer = PLAYER_BODY_COLLISION_FRAMES; collision_occurred = True
             if collision_occurred: play_sound(loaded_sounds['body_hit'])
    return score_increase, new_can_headbutt, new_body_collision_timer, kick_pt

# --- Welcome Screen ---
def draw_welcome_screen(screen, font_large, font_medium, font_small):
    # Fill the background
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    
    # Draw title
    title_text = "AWESOMEBALL!"
    title_surf = font_large.render(title_text, True, YELLOW)
    title_rect = title_surf.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//4)
    title_shadow = title_surf.get_rect(centerx=SCREEN_WIDTH//2+3, centery=SCREEN_HEIGHT//4+3)
    
    # Draw shadow first
    title_shadow_surf = font_large.render(title_text, True, BLACK)
    screen.blit(title_shadow_surf, title_shadow)
    screen.blit(title_surf, title_rect)
    
    # Subtitle
    subtitle = "The epic battle between brothers Nils and Harry!"
    subtitle_surf = font_small.render(subtitle, True, BLACK)
    subtitle_rect = subtitle_surf.get_rect(centerx=SCREEN_WIDTH//2, top=title_rect.bottom + 20)
    screen.blit(subtitle_surf, subtitle_rect)
    
    # Game rules text
    rules = [
        "First to win 5 matches wins the game!",
        "Each match is played to 5 points."
    ]
    
    rules_y = subtitle_rect.bottom + 15
    for rule in rules:
        rule_surf = font_small.render(rule, True, BLACK)
        rule_rect = rule_surf.get_rect(centerx=SCREEN_WIDTH//2, top=rules_y)
        screen.blit(rule_surf, rule_rect)
        rules_y += 25
    
    # Setup fonts for the different sections
    small_font = pygame.font.Font(None, 24)
    smaller_font = pygame.font.Font(None, 20)
    
    # Create a cool font for powerups
    try:
        # Try to load a system font that might look cool
        cool_font = pygame.font.SysFont("impact", 28)
    except:
        # Fallback to default font
        cool_font = pygame.font.Font(None, 28)
    
    # Left side - Player 1 controls
    p1_controls = [
        "Player 1 (Nils):",
        "Move: A / D",
        "Jump: W",
        "Kick: S"
    ]
    
    # Right side - Player 2 controls
    p2_controls = [
        "Player 2 (Harry):",
        "Move: Left / Right Arrow",
        "Jump: Up Arrow",
        "Kick: Down Arrow"
    ]
    
    # Position for player 1 controls (left side)
    p1_x = SCREEN_WIDTH // 4
    # Position for player 2 controls (right side)
    p2_x = 3 * SCREEN_WIDTH // 4
    controls_y = rules_y + 30
    
    # Create background boxes for controls
    p1_controls_height = len(p1_controls) * 22
    p1_controls_width = 200
    p1_bg_rect = pygame.Rect(p1_x - p1_controls_width//2, controls_y, p1_controls_width, p1_controls_height)
    p2_controls_width = 230
    p2_bg_rect = pygame.Rect(p2_x - p2_controls_width//2, controls_y, p2_controls_width, p1_controls_height)
    
    # Draw background boxes
    pygame.draw.rect(screen, (30, 30, 40, 180), p1_bg_rect, border_radius=8)
    pygame.draw.rect(screen, (30, 30, 40, 180), p2_bg_rect, border_radius=8)
    
    for i, line in enumerate(p1_controls):
        if i == 0:  # Header
            text_surf = small_font.render(line, True, P1_COLOR_MAIN)
        else:
            text_surf = smaller_font.render(line, True, WHITE)
        
        text_rect = text_surf.get_rect(centerx=p1_x, top=controls_y)
        screen.blit(text_surf, text_rect)
        controls_y += 22
    
    # Position for player 2 controls (right side)
    p2_x = 3 * SCREEN_WIDTH // 4
    controls_y = rules_y + 30
    
    for i, line in enumerate(p2_controls):
        if i == 0:  # Header
            text_surf = small_font.render(line, True, P2_COLOR_MAIN)
        else:
            text_surf = smaller_font.render(line, True, WHITE)
        
        text_rect = text_surf.get_rect(centerx=p2_x, top=controls_y)
        screen.blit(text_surf, text_rect)
        controls_y += 22
    
    # Draw player models right below the control boxes
    player_y = p1_bg_rect.bottom + 50  # Position players below control boxes
    
    # Player 1 (Nils)
    player1_demo = StickMan(p1_x, player_y, facing=1, team_color=P1_COLOR_MAIN, team_accent=P1_COLOR_ACCENT)
    player1_demo.update = lambda dt, other: None  # Disable update method
    player1_demo.draw(screen)
    
    # Player 2 (Harry)
    player2_demo = StickMan(p2_x, player_y, facing=-1, team_color=P2_COLOR_MAIN, team_accent=P2_COLOR_ACCENT)
    player2_demo.update = lambda dt, other: None  # Disable update method
    player2_demo.draw(screen)
    
    # Draw a ball - position it between the players
    ball_x, ball_y = SCREEN_WIDTH//2, player_y - 30
    
    # Draw a soccer-like ball with pentagon pattern
    # Main ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), 25)
    
    # Draw black pentagons to make it look like a soccer ball
    num_pentagons = 5
    pentagon_radius = 8
    for i in range(num_pentagons):
        angle = i * (2 * math.pi / num_pentagons)
        # Position pentagons around the ball surface
        x = ball_x + int(15 * math.cos(angle))
        y = ball_y + int(15 * math.sin(angle))
        draw_pentagon(screen, BLACK, (x, y), pentagon_radius, angle)
    
    # Border
    pygame.draw.circle(screen, BLACK, (ball_x, ball_y), 25, 1)
    
    # Start instruction directly under the ball
    start_text = "Press R to Start Game"
    start_surf = font_medium.render(start_text, True, RED)
    start_rect = start_surf.get_rect(centerx=SCREEN_WIDTH//2, top=ball_y + 35)
    screen.blit(start_surf, start_rect)
    
    # PowerUp section with cool font - positioned below the players
    powerup_text = "Collect power-ups for special abilities!"
    powerup_surf = cool_font.render(powerup_text, True, (255, 128, 0))  # Orange color
    
    # Create a cool background for the powerup text
    powerup_rect = powerup_surf.get_rect(centerx=SCREEN_WIDTH//2, top=player_y + 80)
    bg_rect = powerup_rect.inflate(20, 10)
    bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    bg_surf.fill((0, 0, 100, 160))  # Semi-transparent blue
    
    # Draw the powerup section
    screen.blit(bg_surf, bg_rect.topleft)
    screen.blit(powerup_surf, powerup_rect)

# --- Start First Game ---
start_new_game()

# --- Main Game Loop ---
running = True
showing_welcome_screen = True  # Start with welcome screen

while running:
    dt = clock.tick(FPS) / 1000.0; dt = min(dt, 0.1)

    # --- Global Input & Event Processing ---
    # ... (event loop unchanged) ...
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        if event.type == SOUND_FINISHED_EVENT: play_next_announcement()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            if event.key == pygame.K_7: debug_mode = not debug_mode; print(f"Debug Mode {'ACT' if debug_mode else 'DEACT'}IVATED")
            elif event.key == pygame.K_4:
                # Randomize weather on key press 4
                if match_active:
                    # Choose a different weather than current
                    old_weather = current_weather
                    possible_weathers = [w for w in WEATHER_TYPES if w != old_weather]
                    current_weather = random.choice(possible_weathers)
                    
                    # Clear and recreate weather particles
                    weather_particles.clear()
                    for _ in range(WEATHER_PARTICLE_COUNT.get(current_weather, 0)):
                        weather_particles.append(WeatherParticle(current_weather, SCREEN_WIDTH, SCREEN_HEIGHT))
                    
                    # Reset wind change timer if it's windy
                    if current_weather == "WINDY":
                        weather_wind_change_timer = random.uniform(10.0, 20.0)
                        # Update CURRENT_WIND_FORCE and WEATHER_WIND_DIRECTION as well
                        weather_effect = WEATHER_EFFECTS.get(current_weather, {})
                        min_force, max_force = weather_effect.get("wind_force_range", (0.0, 0.0))
                        CURRENT_WIND_FORCE = random.uniform(min_force, max_force)
                        WEATHER_WIND_DIRECTION = random.choice([-1, 1])
                    
                    print(f"Weather changed from {old_weather} to {current_weather}")

                    # Select and set weather message (ADDED FOR MANUAL CHANGE)
                    possible_messages = WEATHER_MESSAGES.get(current_weather, [f"{current_weather.replace('_', ' ').title()} weather."])
                    weather_message_text = random.choice(possible_messages)
                    weather_message_timer = WEATHER_MESSAGE_DURATION

                else:
                    print("Weather can only be changed during an active match")
            elif event.key == pygame.K_6:
                if match_active:
                    print("DEBUG: Forcing powerup spawn."); new_powerup = ParachutePowerup(); new_powerup.spawn(); active_powerups.append(new_powerup); powerup_spawn_timer = random.uniform(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
                else: print("DEBUG: Match inactive, cannot force spawn.")
            elif event.key == pygame.K_5:
                if match_active:
                    print("DEBUG: Spawning SWORD powerup.")
                    new_powerup = ParachutePowerup()
                    # Override the normal random selection with SWORD
                    new_powerup.active = True
                    new_powerup.powerup_type = "SWORD"
                    new_powerup.x = random.randint(GOAL_MARGIN_X + 50, SCREEN_WIDTH - GOAL_MARGIN_X - 50)
                    new_powerup.y = -new_powerup.chute_radius * 2
                    new_powerup.vx = random.uniform(-POWERUP_DRIFT_SPEED, POWERUP_DRIFT_SPEED)
                    active_powerups.append(new_powerup)
                    print(f"Powerup spawned: SWORD at ({new_powerup.x:.0f}, {new_powerup.y:.0f})")
                else:
                    print("DEBUG: Match inactive, cannot spawn SWORD.")
            elif event.key == pygame.K_r: 
                if showing_welcome_screen:
                    showing_welcome_screen = False
                    start_new_game()
                elif game_over:
                    start_new_game()
            elif match_active and not showing_welcome_screen:
                if not player1.is_tumbling:
                    if event.key == pygame.K_a: player1.move(-1)
                    elif event.key == pygame.K_d: player1.move(1)
                    elif event.key == pygame.K_w: player1.jump()
                    elif event.key == pygame.K_s: player1.start_kick()
                if not player2.is_tumbling:
                    if event.key == pygame.K_LEFT: player2.move(-1)
                    elif event.key == pygame.K_RIGHT: player2.move(1)
                    elif event.key == pygame.K_UP: player2.jump()
                    elif event.key == pygame.K_DOWN: player2.start_kick()
        if event.type == pygame.KEYUP:
             if match_active and not showing_welcome_screen:
                if not player1.is_tumbling:
                    if event.key == pygame.K_a and player1.vx < 0: player1.stop_move()
                    elif event.key == pygame.K_d and player1.vx > 0: player1.stop_move()
                if not player2.is_tumbling:
                    if event.key == pygame.K_LEFT and player2.vx < 0: player2.stop_move()
                    elif event.key == pygame.K_RIGHT and player2.vx > 0: player2.stop_move()

    # Check if we should show welcome screen
    if showing_welcome_screen:
        draw_welcome_screen(screen, font_goal, font_large, font_medium)
        pygame.display.flip()
        continue

    # --- Handle Game Over State ---
    if game_over: # ... (unchanged) ...
        if not game_over_sound_played:
            announcement_queue = [];
            if overall_winner == 1: queue_sound(loaded_sounds['nils_wins'])
            elif overall_winner == 2: queue_sound(loaded_sounds['harry_wins'])
            play_next_announcement(); game_over_sound_played = True
        bg_color = DEBUG_BG_COLOR if debug_mode else SKY_BLUE
        screen.fill(bg_color); pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        winner_name = "Nils" if overall_winner == 1 else "Harry";
        draw_trophy(screen, winner_name, font_goal, font_large)
        
        # Draw the trophy at the center
        trophy_center_x = SCREEN_WIDTH // 2
        trophy_base_y = SCREEN_HEIGHT // 2 + 180
        
        # Display Harry's images if Harry wins
        if overall_winner == 2:
            # First, draw harry_eats.png on the left
            if winner_images.get("harry_eats"):
                harry_eats_image = winner_images["harry_eats"]
                eats_rect = harry_eats_image.get_rect()
                eats_center_y = SCREEN_HEIGHT // 2 + 180 - 40 - 100 // 2
                eats_rect.center = (trophy_center_x - 280, eats_center_y)  # 280 pixels to the left of trophy (was 300)
                screen.blit(harry_eats_image, eats_rect)
                
            # Then, draw harry_wins.png on the right
            if winner_images.get(overall_winner):
                winner_image = winner_images[overall_winner]
                image_rect = winner_image.get_rect()
                image_center_y = SCREEN_HEIGHT // 2 + 180 - 40 - 100 // 2
                image_rect.center = (trophy_center_x + 300, image_center_y)  # 300 pixels to the right of trophy
                image_rect.right = min(image_rect.right, SCREEN_WIDTH - 10)
                screen.blit(winner_image, image_rect)
        # Display Nils' image if Nils wins
        elif overall_winner == 1 and winner_images.get(overall_winner):
            winner_image = winner_images[overall_winner]
            image_rect = winner_image.get_rect()
            base_width = 140
            padding = 50
            image_center_x = trophy_center_x + base_width // 2 + image_rect.width // 2 + padding
            image_center_y = SCREEN_HEIGHT // 2 + 180 - 40 - 100 // 2
            image_rect.center = (image_center_x, image_center_y)
            image_rect.right = min(image_rect.right, SCREEN_WIDTH - 10)
            screen.blit(winner_image, image_rect)
            
        draw_game_scores(screen, game_scores, font_small); pygame.display.flip(); continue

    # --- Handle Match Over State ---
    if match_over_timer > 0: # ... (unchanged) ...
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
            ball.is_frozen = False; ball.freeze_effect_timer = POWERUP_BALL_FREEZE_DURATION * 0.1 ; print("Ball un-frozen")
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
        ball_hit_ground_this_frame = ball.update(dt)

        # Update active powerups and remove inactive
        active_powerups = [p for p in active_powerups if p.update(dt)] # Corrected filter

        particles = [p for p in particles if p.update(dt)]
        active_rockets = [r for r in active_rockets if r.active and not r.update(dt, player_list, ball)]
        active_explosions = [e for e in active_explosions if e.update(dt)]
        
        # --- Weather Updates ---
        # Update weather particles
        for p in weather_particles:
            p.update(dt)
            
        if current_weather == "WINDY":
            weather_wind_change_timer -= dt
            if weather_wind_change_timer <= 0:
                WEATHER_WIND_DIRECTION = -WEATHER_WIND_DIRECTION # Flip direction
                min_force, max_force = WEATHER_EFFECTS["WINDY"].get("wind_force_range", (0.0, 0.0))
                CURRENT_WIND_FORCE = random.uniform(min_force, max_force) # New random force
                print(f"Wind changed! New Force: {CURRENT_WIND_FORCE:.1f}, Direction: {'RIGHT' if WEATHER_WIND_DIRECTION > 0 else 'LEFT'}")
                
                # Create wind change particles/effects
                wind_color = (200, 200, 255, 150) 
                for _ in range(20):
                    start_x = random.randint(0, SCREEN_WIDTH)
                    start_y = random.randint(50, GROUND_Y - 50)
                    # Angle override based on new direction
                    angle_ov = 0 if WEATHER_WIND_DIRECTION > 0 else math.pi 
                    particles.append(Particle(
                        start_x, start_y, 
                        colors=[wind_color], 
                        speed_min=CURRENT_WIND_FORCE * 5, # Adjusted speed based on force
                        speed_max=CURRENT_WIND_FORCE * 10, 
                        size=3, 
                        angle_override=angle_ov
                    ))
                
                weather_wind_change_timer = random.uniform(8.0, 18.0) # Reset timer
                
                # Recreate wind particles with new direction/speed potentially
                # (Optional: Could make existing particles change direction too)
                for i, p in enumerate(weather_particles):
                    if p.weather_type == "WINDY":
                        p.speed = random.uniform(100, 200) * WEATHER_WIND_DIRECTION  # Ta bort negativa tecknet här också

        # --- Power-up Collection ---
        collected_powerups_indices = [] # ... (unchanged logic including BALL_FREEZE trigger) ...
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
        kick_push_amount = ball.radius * 1.5; kick_push_vx_base = 5
        p1_kick_point = player1.get_kick_impact_point()
        if p1_kick_point and p2_rect.collidepoint(p1_kick_point) and not player2.is_tumbling:
            print("P1 kicked P2")
            kick_multiplier = BIG_PLAYER_KICK_MULTIPLIER if player1.is_big else 1.0
            kick_push_vx = kick_push_vx_base * kick_multiplier
            player2.x += kick_push_amount * player1.facing_direction * kick_multiplier
            player2.vx += kick_push_vx * player1.facing_direction
            player2.vy -= 3 * kick_multiplier; player2.is_jumping = True
            play_sound(loaded_sounds['body_hit'])
        p2_kick_point = player2.get_kick_impact_point()
        if p2_kick_point and p1_rect.collidepoint(p2_kick_point) and not player1.is_tumbling:
            print("P2 kicked P1")
            kick_multiplier = BIG_PLAYER_KICK_MULTIPLIER if player2.is_big else 1.0
            kick_push_vx = kick_push_vx_base * kick_multiplier
            player1.x += kick_push_amount * player2.facing_direction * kick_multiplier
            player1.vx += kick_push_vx * player2.facing_direction
            player1.vy -= 3 * kick_multiplier; player1.is_jumping = True
            play_sound(loaded_sounds['body_hit'])
            
        # --- SWORD-PLAYER COLLISIONS ---
        # Check for player1's sword hitting player2
        if player1.is_sword and player1.is_kicking and not player2.is_tumbling:
            sword_data = player1.get_sword_position()
            if sword_data:
                tip_x, tip_y, base_x, base_y, angle = sword_data
                # Check if sword line collides with player2's rect using clipline
                if p2_rect.clipline(base_x, base_y, tip_x, tip_y):
                    print("P1 sword hit P2!")
                    player2.x += SWORD_PLAYER_HIT_FORCE * 0.01 * player1.facing_direction
                    player2.vx += SWORD_PLAYER_HIT_FORCE * 0.1 * player1.facing_direction
                    player2.vy -= SWORD_PLAYER_UPWARD_BOOST * 0.1
                    player2.is_jumping = True
                    player2.start_tumble()
                    play_sound(loaded_sounds.get('sword_hit', loaded_sounds['wall_hit']))
        
        # Check for player2's sword hitting player1
        if player2.is_sword and player2.is_kicking and not player1.is_tumbling:
            sword_data = player2.get_sword_position()
            if sword_data:
                tip_x, tip_y, base_x, base_y, angle = sword_data
                # Check if sword line collides with player1's rect using clipline
                if p1_rect.clipline(base_x, base_y, tip_x, tip_y):
                    print("P2 sword hit P1!")
                    player1.x += SWORD_PLAYER_HIT_FORCE * 0.01 * player2.facing_direction
                    player1.vx += SWORD_PLAYER_HIT_FORCE * 0.1 * player2.facing_direction
                    player1.vy -= SWORD_PLAYER_UPWARD_BOOST * 0.1
                    player1.is_jumping = True
                    player1.start_tumble()
                    play_sound(loaded_sounds.get('sword_hit', loaded_sounds['wall_hit']))
                
        player1.x = max(player1.limb_width / 2, min(player1.x, SCREEN_WIDTH - player1.limb_width / 2))
        player2.x = max(player2.limb_width / 2, min(player2.x, SCREEN_WIDTH - player2.limb_width / 2))

        # Combo Reset
        is_ball_airborne = not ball.is_on_ground()
        if not is_ball_airborne and ball_hit_ground_this_frame and not ball_was_on_ground: current_hit_count = 0
        ball_was_on_ground = not is_ball_airborne

        # Player-Ball Collisions (only if not tumbling)
        p1_hit, p1_can_headbutt, p1_body_collision_timer, p1_kick_pt = False, p1_can_headbutt, p1_body_collision_timer, None
        p2_hit, p2_can_headbutt, p2_body_collision_timer, p2_kick_pt = False, p2_can_headbutt, p2_body_collision_timer, None
        if not player1.is_tumbling: p1_hit, p1_can_headbutt, p1_body_collision_timer, p1_kick_pt = handle_player_ball_collisions(player1, ball, p1_can_headbutt, p1_body_collision_timer, is_ball_airborne)
        if not player2.is_tumbling: p2_hit, p2_can_headbutt, p2_body_collision_timer, p2_kick_pt = handle_player_ball_collisions(player2, ball, p2_can_headbutt, p2_body_collision_timer, is_ball_airborne)
        score_increased_this_frame = p1_hit or p2_hit
        last_kick_point = p1_kick_pt if p1_kick_pt else p2_kick_pt

        # Combo Trigger
        if score_increased_this_frame and last_kick_point and current_hit_count > 0 and current_hit_count % 5 == 0:
            play_sound(loaded_sounds['combo'])
            num_kick_particles = PARTICLE_COUNT // 2
            for _ in range(num_kick_particles): particle_x = last_kick_point[0] + random.uniform(-5, 5); particle_y = last_kick_point[1] + random.uniform(-5, 5); particles.append(Particle(particle_x, particle_y))


    # --- Goal Detection & Effects ---
    goal_scored_this_frame = False; scorer = 0
    goal_height_p1 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
    goal_y_p1 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
    goal_height_p2 = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
    goal_y_p2 = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)

    if match_active and not ball.is_frozen:
        if ball.x + ball.radius >= GOAL_LINE_X_RIGHT and ball.y > goal_y_p2 and not p2_shield_active:
            player1_score += 1; scorer = 1; goal_message_timer = GOAL_MESSAGE_DURATION; goal_scored_this_frame = True; goal_pos_x = SCREEN_WIDTH; print(f"GOAL! Player 1 Score: {player1_score}"); screen_flash_timer = SCREEN_FLASH_DURATION
        elif ball.x - ball.radius <= GOAL_LINE_X_LEFT and ball.y > goal_y_p1 and not p1_shield_active:
            player2_score += 1; scorer = 2; goal_message_timer = GOAL_MESSAGE_DURATION; goal_scored_this_frame = True; goal_pos_x = 0; print(f"GOAL! Player 2 Score: {player2_score}"); screen_flash_timer = SCREEN_FLASH_DURATION

    if goal_scored_this_frame: # --- Goal Effects ---
        if scorer == 1: play_sound(loaded_sounds['goal_p1']);
        if player1_score > 0 and player1_score % 5 == 0: play_sound(loaded_sounds['combo'])
        elif scorer == 2: play_sound(loaded_sounds['goal_p2']);
        if player2_score > 0 and player2_score % 5 == 0: play_sound(loaded_sounds['combo'])
        goal_center_y = GOAL_Y_POS + GOAL_HEIGHT / 2
        for _ in range(GOAL_PARTICLE_COUNT): particles.append(Particle(goal_pos_x, goal_center_y, colors=GOAL_EXPLOSION_COLORS, speed_min=GOAL_PARTICLE_SPEED_MIN, speed_max=GOAL_PARTICLE_SPEED_MAX, lifespan=GOAL_PARTICLE_LIFESPAN))

        # --- Match/Game Win Check ---
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

        # Reset positions, keep powerups active
        reset_positions()
        continue


    # --- Drawing ---
    # Determine background color based on weather and time of day
    weather_effect = WEATHER_EFFECTS.get(current_weather, {})
    # Default to time of day color
    bg_color = TIME_OF_DAY_COLORS.get(current_time_of_day, SKY_BLUE) 
    # Override if weather has a specific background color
    if "background_color" in weather_effect:
        bg_color = weather_effect["background_color"]
        
    if debug_mode: bg_color = DEBUG_BG_COLOR
    screen.fill(bg_color)
    
    # Draw stars if it's night
    if current_time_of_day == "Night":
        star_color = (255, 255, 220) # Pale yellow
        for x, y in STARS:
            size = random.randint(1, 2)
            pygame.draw.rect(screen, star_color, (x, y, size, size))

    # Draw weather effects in the background
    for p in weather_particles:
        p.draw(screen)
        
    # Add fog overlay if foggy
    # MOVED FOG DRAWING TO LATER
    # if current_weather == "FOGGY":
    #     fog_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    #     fog_surf.fill((255, 255, 255, 70))  # Semi-transparent white
    #     screen.blit(fog_surf, (0, 0))

    pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    # Draw Goals using effective height/y based on timers
    draw_goal_isometric(screen, GOAL_LINE_X_LEFT, GOAL_Y_POS, GOAL_HEIGHT, -GOAL_DEPTH_X, GOAL_DEPTH_Y, GOAL_POST_THICKNESS, GOAL_COLOR, GOAL_NET_COLOR, enlarged_height=(POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0))
    draw_goal_isometric(screen, GOAL_LINE_X_RIGHT, GOAL_Y_POS, GOAL_HEIGHT, GOAL_DEPTH_X, GOAL_DEPTH_Y, GOAL_POST_THICKNESS, GOAL_COLOR, GOAL_NET_COLOR, enlarged_height=(POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0))


    # Draw Goal Shields with Pulse
    current_time = pygame.time.get_ticks() / 1000.0
    pulse = (math.sin(current_time * POWERUP_GOAL_SHIELD_PULSE_SPEED) + 1) / 2
    shield_alpha = int(POWERUP_GOAL_SHIELD_MIN_ALPHA + pulse * (POWERUP_GOAL_SHIELD_MAX_ALPHA - POWERUP_GOAL_SHIELD_MIN_ALPHA))
    shield_color_with_alpha = (POWERUP_GOAL_SHIELD_COLOR[0], POWERUP_GOAL_SHIELD_COLOR[1], POWERUP_GOAL_SHIELD_COLOR[2], shield_alpha)

    if p1_shield_active: # P1 Shield on Left Goal
        shield_height = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        shield_y = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p1_goal_enlarged_timer > 0 else 0)
        shield_rect = pygame.Rect(GOAL_LINE_X_LEFT - POWERUP_GOAL_SHIELD_WIDTH // 2, shield_y, POWERUP_GOAL_SHIELD_WIDTH, shield_height)
        shield_surf = pygame.Surface(shield_rect.size, pygame.SRCALPHA); shield_surf.fill(shield_color_with_alpha)
        screen.blit(shield_surf, shield_rect.topleft); pygame.draw.rect(screen, WHITE, shield_rect, 1)

    if p2_shield_active: # P2 Shield on Right Goal
        shield_height = GOAL_HEIGHT + (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        shield_y = GOAL_Y_POS - (POWERUP_GOAL_ENLARGER_HEIGHT_INCREASE if p2_goal_enlarged_timer > 0 else 0)
        shield_rect = pygame.Rect(GOAL_LINE_X_RIGHT - POWERUP_GOAL_SHIELD_WIDTH // 2, shield_y, POWERUP_GOAL_SHIELD_WIDTH, shield_height)
        shield_surf = pygame.Surface(shield_rect.size, pygame.SRCALPHA); shield_surf.fill(shield_color_with_alpha)
        screen.blit(shield_surf, shield_rect.topleft); pygame.draw.rect(screen, WHITE, shield_rect, 1)


    if screen_flash_timer > 0: flash_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA); flash_alpha = int(255 * (screen_flash_timer / SCREEN_FLASH_DURATION)); flash_surf.fill((SCREEN_FLASH_COLOR[0], SCREEN_FLASH_COLOR[1], SCREEN_FLASH_COLOR[2], flash_alpha)); screen.blit(flash_surf, (0,0))

    # Draw Game Elements
    for p in particles: p.draw(screen)
    for pup in active_powerups: pup.draw(screen)
    for r in active_rockets: r.draw(screen)
    player1.draw(screen); player2.draw(screen)
    ball.draw(screen)
    for e in active_explosions: e.draw(screen)
    draw_offscreen_arrow(screen, ball, None)

    # Draw fog overlay AFTER game elements but BEFORE UI
    if current_weather == "FOGGY":
        fog_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        fog_surf.fill((210, 210, 215, 130))  # Slightly grayish and much less transparent
        screen.blit(fog_surf, (0, 0))

    # --- Draw UI ---
    draw_scoreboard(screen, player1_score, player2_score, p1_games_won, p2_games_won, font_large, font_medium, font_small, goal_message_timer > 0 or match_over_timer > 0)
    draw_game_scores(screen, game_scores, font_small)
    
    # Draw weather info
    weather_font = font_small
    weather_label = f"Weather: {current_weather.replace('_', ' ').title()}"
    weather_effect = WEATHER_EFFECTS.get(current_weather, {})
    effects_text = []
    
    if "gravity" in weather_effect and weather_effect["gravity"] != 1.0:
        if weather_effect["gravity"] < 1.0: effects_text.append("Low gravity")
        else: effects_text.append("High gravity")
            
    if current_weather == "WINDY":
        direction = "→" if WEATHER_WIND_DIRECTION > 0 else "←"
        effects_text.append(f"Wind {direction} ({CURRENT_WIND_FORCE:.0f})")
    elif current_weather == "GOTHENBURG_WEATHER":
        effects_text.append(f"Wind ↗ ({weather_effect.get('wind_force', 0.0):.0f})") # Indicate direction
        
    if current_weather == "FOGGY": effects_text.append("Low visibility")
    
    effects_str = ", ".join(effects_text) if effects_text else "Normal"
    weather_text = f"{weather_label} [{effects_str}]"
    
    weather_color = {
        "SUNNY": (255, 200, 0),
        "RAINY": (100, 140, 255),
        "WINDY": (200, 200, 200),
        "SNOWY": (220, 240, 255),
        "FOGGY": (180, 180, 180),
        "GOTHENBURG_WEATHER": (120, 150, 200)
    }.get(current_weather, WHITE)
    
    weather_surf = weather_font.render(weather_text, True, weather_color)
    weather_rect = weather_surf.get_rect(top=10, right=SCREEN_WIDTH - 10)
    
    # Add background to make text readable
    weather_bg = weather_rect.inflate(10, 6)
    weather_bg_surf = pygame.Surface(weather_bg.size, pygame.SRCALPHA)
    weather_bg_surf.fill((0, 0, 0, 150))
    screen.blit(weather_bg_surf, weather_bg.topleft)
    screen.blit(weather_surf, weather_rect)
    
    # Draw Weather Message (Added)
    if weather_message_timer > 0:
        # weather_message_timer -= dt # Decrease timer here << MOVED
        if weather_message_timer > 0: # Check again in case dt made it zero
            msg_font = font_medium # Use medium font for message
            msg_surf = msg_font.render(weather_message_text, True, WHITE)
            msg_rect = msg_surf.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 3)
            
            # Background for the message
            msg_bg_rect = msg_rect.inflate(20, 10)
            msg_bg_surf = pygame.Surface(msg_bg_rect.size, pygame.SRCALPHA)
            msg_bg_surf.fill((0, 0, 50, 180)) # Dark blueish background
            screen.blit(msg_bg_surf, msg_bg_rect.topleft)
            screen.blit(msg_surf, msg_rect)
        weather_message_timer -= dt # << MOVED HERE

    if goal_message_timer > 0 and match_active:
        # Removed GOAL text display
        pass
    # --- Modified Match Over Drawing with Transition ---
    if match_over_timer > 0 and not game_over:
        # Calculate transition progress (0.0 to 1.0) as timer counts down
        transition_progress = 1.0 - (match_over_timer / MATCH_OVER_DURATION)
        
        # Determine colors for transition
        # Color of the match that just ended
        current_total_games = p1_games_won + p2_games_won -1 # -1 because score is updated *before* this runs
        current_time_index = current_total_games % len(TIMES_OF_DAY)
        start_time_of_day = TIMES_OF_DAY[current_time_index]
        start_color = TIME_OF_DAY_COLORS.get(start_time_of_day, SKY_BLUE)
        # Check if weather had an override for the completed match (Need to store last weather? Or approximate)
        # For simplicity, we'll just use the time_of_day color for the start transition.
        
        night_color = TIME_OF_DAY_COLORS["Night"]
        
        # Color for the upcoming match
        next_total_games = p1_games_won + p2_games_won
        next_time_index = next_total_games % len(TIMES_OF_DAY)
        next_time_of_day = TIMES_OF_DAY[next_time_index]
        end_color = TIME_OF_DAY_COLORS.get(next_time_of_day, SKY_BLUE)
        # Consider next match's weather override? Too complex for transition. Use time_of_day.
        
        # Interpolate background color
        if transition_progress < 0.5: # Fade to night
            factor = transition_progress * 2 # Scale 0.0 -> 1.0
            bg_color = lerp_color(start_color, night_color, factor)
        else: # Fade from night to next day
            factor = (transition_progress - 0.5) * 2 # Scale 0.0 -> 1.0
            bg_color = lerp_color(night_color, end_color, factor)
            
        # Draw transitioning background
        screen.fill(bg_color)
        
        # Draw moon near the middle of the transition (peak night)
        if 0.4 < transition_progress < 0.6:
            moon_size = 30
            moon_pos = (SCREEN_WIDTH - moon_size * 2, moon_size * 2)
            moon_color = (255, 255, 220)
            draw_moon(screen, moon_pos, moon_size, moon_color)
        elif transition_progress >= 0.5 and next_time_of_day == "Night": # Also draw stars if next phase is night
            star_color = (255, 255, 220)
            for x, y in STARS:
                size = random.randint(1, 2)
                pygame.draw.rect(screen, star_color, (x, y, size, size))

        # Draw grass over the transitioning background
        pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
        
        # Draw the text overlay
        winner_name = "Nils" if match_winner == 1 else "Harry"; match_win_text = f"{winner_name} Wins the Match!"; match_win_surf = font_large.render(match_win_text, True, YELLOW); match_win_rect = match_win_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
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
                           "ENORMOUS_HEAD": (255, 100, 200), "GOAL_ENLARGER": (50, 200, 150)}
        powerup_texts = { "FLIGHT": "Flight: {:.1f}", "ROCKET_LAUNCHER": "ROCKET(x{})", "BIG_PLAYER": "BIG: {:.1f}",
                          "SUPER_JUMP": "JUMP: {:.1f}", "SPEED_BOOST": "SPEED: {:.1f}", "GOAL_SHIELD": "SHIELD: {:.1f}",
                          "SHRUNK": "Shrunk: {:.1f}", "LOW_GRAVITY": "LOW-G: {:.1f}", "REVERSE_CONTROLS": "REVERSED: {:.1f}",
                          "ENORMOUS_HEAD": "BIG HEAD: {:.1f}", "GOAL_ENLARGER": "GOAL+: {:.1f}"}

        # Player 1 UI
        p1_ui_y = SCREEN_HEIGHT - 30
        for p_type in sorted(player1.active_powerups.keys()):
            val = player1.active_powerups[p_type]; text_template = powerup_texts.get(p_type, p_type); text = ""
            if p_type == "ROCKET_LAUNCHER": text = text_template.format(val)
            elif p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD"]: text = text_template.format(val)
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
            elif p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", "ENORMOUS_HEAD"]: text = text_template.format(val)
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
        if ball.is_frozen:
            freeze_text = "BALL FROZEN: {:.1f}".format(ball_freeze_timer); freeze_surf = powerup_font.render(freeze_text, True, (180, 220, 255)); freeze_rect = freeze_surf.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)); screen.blit(freeze_surf, freeze_rect)

        # Debug info
        if debug_mode:
            pass  # Add any additional debug info here

    pygame.display.flip()

# Cleanup
pygame.quit(); sys.exit()