import pygame
import math
import random

# Constants from main.py that we need
GRAVITY = 0.9
BASE_PLAYER_SPEED = 3.0
BASE_JUMP_POWER = -0.03
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ITALY_WHITE = (245, 245, 245)
NOSE_COLOR = (255, 153, 102)

# Timing and physics constants
TUMBLE_DURATION = 2.0
PLAYER_TUMBLE_ROT_SPEED_MIN = 3.0
PLAYER_TUMBLE_ROT_SPEED_MAX = 5.0
PLAYER_TUMBLE_DAMPING = 0.95
HEAD_PLATFORM_RADIUS_BUFFER = 4

# PowerUp constants
POWERUP_LOW_GRAVITY_FACTOR = 0.5
POWERUP_FLIGHT_DURATION = 10.0
POWERUP_BIG_PLAYER_DURATION = 10.0
POWERUP_BIG_PLAYER_SCALE = 1.5
POWERUP_SHRINK_PLAYER_DURATION = 10.0
POWERUP_SHRINK_PLAYER_SCALE = 0.75
POWERUP_SUPER_JUMP_DURATION = 10.0
POWERUP_SUPER_JUMP_MULTIPLIER = 1.5
POWERUP_SPEED_BOOST_DURATION = 10.0
POWERUP_SPEED_BOOST_MULTIPLIER = 1.5
POWERUP_REVERSE_CONTROLS_DURATION = 5.0
POWERUP_ENORMOUS_HEAD_DURATION = 10.0
POWERUP_ENORMOUS_HEAD_SCALE = 2.0
POWERUP_SWORD_DURATION = 10.0

# Kick animation constants
KICK_THIGH_WINDUP_ANGLE = math.radians(-30)
KICK_THIGH_FOLLOW_ANGLE = math.radians(60)
KICK_SHIN_WINDUP_ANGLE = math.radians(30)
KICK_SHIN_IMPACT_ANGLE = math.radians(-60)

# Simple helper function to draw rotated rectangles
def draw_rotated_rectangle(surface, color, rect_center, width, height, angle_rad):
    """Draw a rotated rectangle on the surface."""
    points = []
    cx, cy = rect_center
    angle_cos = math.cos(angle_rad)
    angle_sin = math.sin(angle_rad)
    
    # Calculate corner points
    hw, hh = width / 2, height / 2
    points.append((cx + hw * angle_cos - hh * angle_sin, cy + hw * angle_sin + hh * angle_cos))
    points.append((cx - hw * angle_cos - hh * angle_sin, cy - hw * angle_sin + hh * angle_cos))
    points.append((cx - hw * angle_cos + hh * angle_sin, cy - hw * angle_sin - hh * angle_cos))
    points.append((cx + hw * angle_cos + hh * angle_sin, cy + hw * angle_sin - hh * angle_cos))
    
    pygame.draw.polygon(surface, color, points)
    
class SimpleStickMan:
    """A simplified stick man player model optimized for performance."""
    
    def __init__(self, x, y, facing=1, team_color=WHITE, team_accent=BLACK):
        self.x = x
        self.y = y
        self.base_y = y
        self.vx = 0
        self.vy = 0
        self.is_jumping = False
        self.is_kicking = False
        self.kick_timer = 0
        self.kick_duration = 24
        self.walk_cycle_timer = 0.0
        
        # Team colors
        self.team_color = team_color
        self.team_accent = team_accent
        self.eye_color = BLACK
        
        # Base size attributes (simplified)
        self.base_head_radius = 12
        self.base_torso_length = 36
        self.base_limb_width = 6
        self.base_arm_length = 24
        self.base_leg_length = 28
        
        # Current size attributes (initially same as base)
        self.head_radius = self.base_head_radius
        self.torso_length = self.base_torso_length
        self.limb_width = self.base_limb_width
        self.arm_length = self.base_arm_length
        self.leg_length = self.base_leg_length
        
        # Facing direction and state
        self.facing_direction = facing
        self.on_other_player_head = False
        self.on_left_crossbar = False
        self.on_right_crossbar = False
        
        # Animation angles (simplified)
        self.left_thigh_angle = 0
        self.right_thigh_angle = 0
        self.left_shin_angle = 0
        self.right_shin_angle = 0
        self.left_arm_angle = 0
        self.right_arm_angle = 0
        
        # Joint positions
        self.head_pos = (0, 0)
        self.neck_pos = (0, 0)
        self.hip_pos = (0, 0)
        self.left_knee_pos = (0, 0)
        self.right_knee_pos = (0, 0)
        self.left_hand_pos = (0, 0)
        self.right_hand_pos = (0, 0)
        self.left_foot_pos = (0, 0)
        self.right_foot_pos = (0, 0)
        
        # Powerups and state
        self.active_powerups = {}
        self.is_flying = False
        self.is_big = False
        self.is_shrunk = False
        self.is_enormous_head = False
        self.is_controls_reversed = False
        self.is_sword = False
        self.sword_angle = 0
        
        # Physics and movement
        self.jump_power = BASE_JUMP_POWER
        self.player_speed = BASE_PLAYER_SPEED
        
        # Stun and tumble state
        self.is_stunned = False
        self.stun_timer = 0.0
        self.is_tumbling = False
        self.tumble_timer = 0.0
        self.rotation_angle = 0.0
        self.rotation_velocity = 0.0
        
    def get_head_position_radius(self):
        """Return the head position and radius for collision detection."""
        return self.head_pos, self.head_radius
        
    def get_body_rect(self):
        """Return a rectangle representing the body for collision detection."""
        width = self.limb_width * 2
        height = self.torso_length + self.leg_length
        return pygame.Rect(self.x - width/2, self.neck_pos[1], width, height)
    
    def get_kick_impact_point(self):
        """Return the position of the kick impact point."""
        if not self.is_kicking:
            return None
            
        progress = min(self.kick_timer / self.kick_duration, 1.0)
        impact_start = 0.25
        impact_end = 0.50
        
        if progress < impact_start or progress > impact_end:
            return None
            
        kick_foot = self.right_foot_pos if self.facing_direction == 1 else self.left_foot_pos
        return kick_foot
    
    def start_stun(self, duration):
        """Starts the stun effect on the player."""
        if not self.is_stunned:
            self.is_stunned = True
            self.stun_timer = duration
            self.vx = 0
            self.vy = max(0, self.vy)
            self.is_kicking = False
            self.is_jumping = False
            
    def start_tumble(self):
        """Start the tumble animation."""
        if not self.is_tumbling:
            self.is_tumbling = True
            self.tumble_timer = TUMBLE_DURATION
            self.rotation_velocity = random.uniform(PLAYER_TUMBLE_ROT_SPEED_MIN, PLAYER_TUMBLE_ROT_SPEED_MAX) * random.choice([-1, 1])
            self.is_kicking = False
            self.kick_timer = 0
    
    def apply_powerup(self, powerup_type, other_player=None):
        """Apply a powerup to the player."""
        current_val = self.active_powerups.get(powerup_type, 0)
        
        if powerup_type == "FLIGHT":
            self.active_powerups["FLIGHT"] = POWERUP_FLIGHT_DURATION
            self.is_flying = True
        elif powerup_type == "BIG_PLAYER":
            self.active_powerups["BIG_PLAYER"] = POWERUP_BIG_PLAYER_DURATION
            self.is_big = True
            if "SHRUNK" in self.active_powerups:
                del self.active_powerups["SHRUNK"]
                self.is_shrunk = False
            self.calculate_current_sizes()
        elif powerup_type == "SUPER_JUMP":
            self.active_powerups["SUPER_JUMP"] = POWERUP_SUPER_JUMP_DURATION
            self.jump_power = BASE_JUMP_POWER * POWERUP_SUPER_JUMP_MULTIPLIER
        elif powerup_type == "SPEED_BOOST":
            self.active_powerups["SPEED_BOOST"] = POWERUP_SPEED_BOOST_DURATION
            self.player_speed = BASE_PLAYER_SPEED * POWERUP_SPEED_BOOST_MULTIPLIER
        elif powerup_type == "SHRINK_OPPONENT":
            if other_player:
                other_player.apply_shrink()
        elif powerup_type == "LOW_GRAVITY":
            self.active_powerups["LOW_GRAVITY"] = POWERUP_LOW_GRAVITY_FACTOR
        elif powerup_type == "REVERSE_CONTROLS":
            if other_player:
                other_player.apply_reverse_controls()
        elif powerup_type == "ENORMOUS_HEAD":
            self.active_powerups["ENORMOUS_HEAD"] = POWERUP_ENORMOUS_HEAD_DURATION
            self.is_enormous_head = True
            if "SHRUNK" in self.active_powerups:
                del self.active_powerups["SHRUNK"]
                self.is_shrunk = False
            self.calculate_current_sizes()
        elif powerup_type == "SWORD":
            self.active_powerups["SWORD"] = POWERUP_SWORD_DURATION
            self.is_sword = True
    
    def apply_shrink(self):
        """Apply shrink effect to the player."""
        self.active_powerups["SHRUNK"] = POWERUP_SHRINK_PLAYER_DURATION
        self.is_shrunk = True
        if "BIG_PLAYER" in self.active_powerups:
            del self.active_powerups["BIG_PLAYER"]
            self.is_big = False
        if "ENORMOUS_HEAD" in self.active_powerups:
            del self.active_powerups["ENORMOUS_HEAD"]
            self.is_enormous_head = False
        self.calculate_current_sizes()
    
    def apply_reverse_controls(self):
        """Apply reverse controls effect to the player."""
        self.active_powerups["REVERSE_CONTROLS"] = POWERUP_REVERSE_CONTROLS_DURATION
        self.is_controls_reversed = True
    
    def calculate_current_sizes(self):
        """Calculate current sizes based on powerups."""
        body_scale = 1.0
        if self.is_big:
            body_scale = POWERUP_BIG_PLAYER_SCALE
        elif self.is_shrunk:
            body_scale = POWERUP_SHRINK_PLAYER_SCALE
            
        self.torso_length = self.base_torso_length * body_scale
        self.limb_width = self.base_limb_width * body_scale
        self.arm_length = self.base_arm_length * body_scale
        self.leg_length = self.base_leg_length * body_scale
        
        head_scale = body_scale
        if self.is_enormous_head:
            head_scale = POWERUP_ENORMOUS_HEAD_SCALE
            
        self.head_radius = self.base_head_radius * head_scale
    
    def move(self, direction):
        """Move the player in the specified direction."""
        if self.is_tumbling or self.is_stunned:
            return
            
        move_direction = direction
        if self.is_controls_reversed:
            move_direction *= -1
            
        if not self.is_kicking:
            self.vx = move_direction * self.player_speed
            
        if direction != 0:
            self.facing_direction = direction
    
    def stop_move(self):
        """Stop the player's movement."""
        if self.is_tumbling or self.is_stunned:
            return
            
        self.vx = 0
    
    def jump(self):
        """Make the player jump."""
        if self.is_tumbling or self.is_stunned:
            return
            
        can_jump_now = False
        if "FLIGHT" in self.active_powerups:
            if not self.is_kicking:
                can_jump_now = True
        else:
            if (not self.is_jumping or self.on_other_player_head) and not self.is_kicking:
                can_jump_now = True
                
        if can_jump_now:
            self.is_jumping = True
            self.on_other_player_head = False
            # Explicit removal of goal stand state
            self.on_left_crossbar = False
            self.on_right_crossbar = False
            self.vy = self.jump_power
            self.walk_cycle_timer = 0
    
    def start_kick(self):
        """Start the kick animation."""
        if self.is_tumbling or self.is_stunned:
            return
            
        if not self.is_kicking:
            self.is_kicking = True
            self.kick_timer = 0
            self.vx = 0
    
    def update(self, dt, other_player):
        """Update the player's state."""
        # Update stun timer
        if self.stun_timer > 0:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.stun_timer = 0.0
                self.is_stunned = False
            else:
                self.is_stunned = True
                self.vx = 0
                self.vy += GRAVITY * dt
                self.y += self.vy * dt
                
                # Ground collision while stunned
                if self.y >= self.base_y:
                    self.y = self.base_y
                    self.vy = 0
                
                # Update positions but skip rest of update
                self.update_positions()
                return
        
        # Update tumble state
        if self.is_tumbling:
            self.tumble_timer -= dt
            if self.tumble_timer <= 0:
                self.is_tumbling = False
                self.tumble_timer = 0.0
                self.rotation_angle = 0.0
                self.rotation_velocity = 0.0
            else:
                self.rotation_angle += self.rotation_velocity * dt
                self.rotation_velocity *= (PLAYER_TUMBLE_DAMPING ** (dt * 60))
        
        # Update powerups
        expired_powerups = []
        for p_type, value in list(self.active_powerups.items()):
            if p_type in ["FLIGHT", "BIG_PLAYER", "SHRUNK", "SUPER_JUMP", 
                         "SPEED_BOOST", "LOW_GRAVITY", "REVERSE_CONTROLS", 
                         "ENORMOUS_HEAD", "SWORD"]:
                new_timer = value - dt
                if new_timer <= 0:
                    expired_powerups.append(p_type)
                    if p_type == "FLIGHT":
                        self.is_flying = False
                    elif p_type == "BIG_PLAYER":
                        self.is_big = False
                        self.calculate_current_sizes()
                    elif p_type == "SHRUNK":
                        self.is_shrunk = False
                        self.calculate_current_sizes()
                    elif p_type == "SUPER_JUMP":
                        # Override super jump to use base jump power for now
                        self.jump_power = BASE_JUMP_POWER
                    elif p_type == "SPEED_BOOST":
                        self.player_speed = BASE_PLAYER_SPEED * POWERUP_SPEED_BOOST_MULTIPLIER
                    elif p_type == "REVERSE_CONTROLS":
                        self.is_controls_reversed = False
                    elif p_type == "ENORMOUS_HEAD":
                        self.is_enormous_head = False
                        self.calculate_current_sizes()
                    elif p_type == "SWORD":
                        self.is_sword = False
                else:
                    self.active_powerups[p_type] = new_timer
                    
        for p_type in expired_powerups:
            if p_type in self.active_powerups:
                del self.active_powerups[p_type]
        
        # Physics update (simplified)
        current_gravity = GRAVITY
        if "LOW_GRAVITY" in self.active_powerups:
            current_gravity *= POWERUP_LOW_GRAVITY_FACTOR
        
        # Check if player is on another player's head
        other_head_pos, other_head_radius = other_player.get_head_position_radius()
        head_top_y = other_head_pos[1] - other_head_radius
        dist_x_head = self.x - other_head_pos[0]
        is_aligned_for_head = abs(dist_x_head) < (other_head_radius + self.head_radius + HEAD_PLATFORM_RADIUS_BUFFER)
        
        # Apply gravity if not on a platform
        if not self.on_other_player_head:
            self.vy += current_gravity
        elif self.on_other_player_head and not is_aligned_for_head:
            self.on_other_player_head = False
            self.is_jumping = True
            self.vy += current_gravity
        
        # Set explicit on_crossbar to False temporarily - will be handled later
        self.on_left_crossbar = False
        self.on_right_crossbar = False
        
        # Update positions
        self.x += self.vx
        if self.is_jumping or not self.on_other_player_head:
            self.y += self.vy
        
        # Ground collision
        if self.y >= self.base_y:
            self.y = self.base_y
            self.vy = 0
            self.is_jumping = False
        
        # Update kick state
        if self.is_kicking:
            self.kick_timer += 1
            if self.kick_timer >= self.kick_duration:
                self.is_kicking = False
                self.kick_timer = 0
        
        # Update walk cycle
        if abs(self.vx) > 0 and not self.is_jumping and not self.is_kicking:
            self.walk_cycle_timer += dt * 10
        else:
            self.walk_cycle_timer = 0
        
        # Update limb angles based on animation state
        self.update_limb_angles(dt)
        
        # Update character joint positions
        self.update_positions()
    
    def update_limb_angles(self, dt):
        """Update the angles of the limbs based on the current animation state."""
        if self.is_tumbling:
            # Random flailing while tumbling
            current_time_ms = pygame.time.get_ticks()
            tumble_speed = self.rotation_velocity * 1.5
            self.left_arm_angle = math.sin(current_time_ms * 0.01 + 1) * 0.8 + tumble_speed * 0.05
            self.right_arm_angle = math.sin(current_time_ms * 0.01 + 2) * 0.8 - tumble_speed * 0.05
            self.left_thigh_angle = math.sin(current_time_ms * 0.01 + 5) * 0.6 - tumble_speed * 0.04
            self.right_thigh_angle = math.sin(current_time_ms * 0.01 + 6) * 0.6 + tumble_speed * 0.04
            self.left_shin_angle = math.sin(current_time_ms * 0.015 + 7) * 1.0
            self.right_shin_angle = math.sin(current_time_ms * 0.015 + 0) * 1.0
        elif self.is_kicking:
            # Kick animation - FIXED direction based on facing
            progress = min(self.kick_timer / self.kick_duration, 1.0)
            
            # Neutral arms (slightly back)
            self.left_arm_angle = 0.1
            self.right_arm_angle = -0.1
            
            if self.facing_direction == 1:  # Facing right, kick with right leg
                # Stationary left leg slightly back
                self.left_thigh_angle = -0.1 
                self.left_shin_angle = 0.2  

                # Right leg animation - UNCHANGED
                if progress < 0.25: # Windup - Leg moves back
                    interp = progress / 0.25
                    self.right_thigh_angle = KICK_THIGH_WINDUP_ANGLE * interp
                    self.right_shin_angle = KICK_SHIN_WINDUP_ANGLE * interp
                elif progress < 0.5: # Kick - Leg moves forward
                    interp = (progress - 0.25) / 0.25
                    self.right_thigh_angle = KICK_THIGH_WINDUP_ANGLE + (KICK_THIGH_FOLLOW_ANGLE - KICK_THIGH_WINDUP_ANGLE) * interp
                    self.right_shin_angle = KICK_SHIN_WINDUP_ANGLE + (KICK_SHIN_IMPACT_ANGLE - KICK_SHIN_WINDUP_ANGLE) * interp
                else: # Recovery
                    interp = (progress - 0.5) / 0.5
                    self.right_thigh_angle = KICK_THIGH_FOLLOW_ANGLE * (1 - interp)
                    self.right_shin_angle = KICK_SHIN_IMPACT_ANGLE * (1 - interp ** 2)
            else:  # Facing left, kick with left leg
                # Stationary right leg slightly back
                self.right_thigh_angle = 0.1
                self.right_shin_angle = -0.2

                # Left leg animation - FIX: Don't negate the angles
                if progress < 0.25: # Windup - Leg moves back
                    interp = progress / 0.25
                    # KEY FIX: Use POSITIVE KICK_THIGH_WINDUP_ANGLE for left leg (don't negate it)
                    self.left_thigh_angle = KICK_THIGH_WINDUP_ANGLE * interp
                    self.left_shin_angle = KICK_SHIN_WINDUP_ANGLE * interp
                elif progress < 0.5: # Kick - Leg moves forward
                    interp = (progress - 0.25) / 0.25
                    # KEY FIX: Use correct interpolation without negation
                    self.left_thigh_angle = KICK_THIGH_WINDUP_ANGLE + (KICK_THIGH_FOLLOW_ANGLE - KICK_THIGH_WINDUP_ANGLE) * interp
                    self.left_shin_angle = KICK_SHIN_WINDUP_ANGLE + (KICK_SHIN_IMPACT_ANGLE - KICK_SHIN_WINDUP_ANGLE) * interp
                else: # Recovery
                    interp = (progress - 0.5) / 0.5
                    # KEY FIX: Use positive KICK_THIGH_FOLLOW_ANGLE
                    self.left_thigh_angle = KICK_THIGH_FOLLOW_ANGLE * (1 - interp)
                    self.left_shin_angle = KICK_SHIN_IMPACT_ANGLE * (1 - interp ** 2)
                
        elif self.is_jumping:
            # Jumping animation - arms up, legs slightly bent
            self.left_arm_angle = -0.5
            self.right_arm_angle = 0.5
            self.left_thigh_angle = -0.2
            self.right_thigh_angle = 0.2
            self.left_shin_angle = 0.6
            self.right_shin_angle = -0.6
        else:
            # Walking/idle animation
            if abs(self.vx) > 0:
                # Walking animation
                walk_cycle = math.sin(self.walk_cycle_timer)
                self.left_arm_angle = walk_cycle * 0.5
                self.right_arm_angle = -walk_cycle * 0.5
                
                # Förbättrad gång för tydligare benrörelser
                self.left_thigh_angle = -walk_cycle * 0.5
                self.right_thigh_angle = walk_cycle * 0.5
                
                # Förskjut shin-cykeln för mer naturlig gång och tydligare led
                shin_cycle = math.sin(self.walk_cycle_timer + math.pi/3)  # Större fasförskjutning
                self.left_shin_angle = shin_cycle * 0.8  # Öka rörelseomfånget
                self.right_shin_angle = -shin_cycle * 0.8  # Öka rörelseomfånget
            else:
                # Idle animation
                idle_cycle = math.sin(pygame.time.get_ticks() * 0.001) * 0.05
                self.left_arm_angle = 0.1 + idle_cycle
                self.right_arm_angle = -0.1 + idle_cycle
                self.left_thigh_angle = 0
                self.right_thigh_angle = 0
                self.left_shin_angle = 0.2  # Öka vinkeln för vilande position
                self.right_shin_angle = -0.2  # Öka vinkeln för vilande position
    
    def update_positions(self):
        """Update the positions of all body parts based on current state."""
        # Ändra beräkningen så att fötterna rör vid marken
        # Spelaren ska stå på marken (self.y) när hen är på sin bas
        self.hip_pos = (self.x, self.y - self.leg_length)
        self.neck_pos = (self.x, self.hip_pos[1] - self.torso_length)
        self.head_pos = (self.x, self.neck_pos[1] - self.head_radius)
        
        # Calculate arm positions
        arm_attach_y = self.neck_pos[1] + self.torso_length * 0.2
        
        # Left arm
        left_arm_angle = self.left_arm_angle - math.pi/2 if self.facing_direction == 1 else self.left_arm_angle + math.pi/2
        left_hand_x = self.x - self.arm_length * math.cos(left_arm_angle) * self.facing_direction
        left_hand_y = arm_attach_y + self.arm_length * math.sin(left_arm_angle)
        self.left_hand_pos = (left_hand_x, left_hand_y)
        
        # Right arm
        right_arm_angle = self.right_arm_angle - math.pi/2 if self.facing_direction == 1 else self.right_arm_angle + math.pi/2
        right_hand_x = self.x - self.arm_length * math.cos(right_arm_angle) * self.facing_direction
        right_hand_y = arm_attach_y + self.arm_length * math.sin(right_arm_angle)
        self.right_hand_pos = (right_hand_x, right_hand_y)
        
        # Calculate leg positions with separate thigh and shin
        thigh_length = self.leg_length * 0.5
        shin_length = self.leg_length * 0.5
        
        # Fixa beräkningen för att undvika osynliga ben när man går åt höger
        # Använd en annan strategi för att beräkna benvinklarna
        
        # Vänster ben
        left_thigh_base_angle = math.pi/2 - self.left_thigh_angle * self.facing_direction
        left_knee_x = self.hip_pos[0] + thigh_length * math.cos(left_thigh_base_angle)
        left_knee_y = self.hip_pos[1] + thigh_length * math.sin(left_thigh_base_angle)
        self.left_knee_pos = (left_knee_x, left_knee_y)
        
        left_shin_base_angle = left_thigh_base_angle + self.left_shin_angle * self.facing_direction
        left_foot_x = left_knee_x + shin_length * math.cos(left_shin_base_angle)
        left_foot_y = left_knee_y + shin_length * math.sin(left_shin_base_angle)
        self.left_foot_pos = (left_foot_x, left_foot_y)
        
        # Höger ben
        right_thigh_base_angle = math.pi/2 - self.right_thigh_angle * self.facing_direction
        right_knee_x = self.hip_pos[0] + thigh_length * math.cos(right_thigh_base_angle)
        right_knee_y = self.hip_pos[1] + thigh_length * math.sin(right_thigh_base_angle)
        self.right_knee_pos = (right_knee_x, right_knee_y)
        
        right_shin_base_angle = right_thigh_base_angle + self.right_shin_angle * self.facing_direction
        right_foot_x = right_knee_x + shin_length * math.cos(right_shin_base_angle)
        right_foot_y = right_knee_y + shin_length * math.sin(right_shin_base_angle)
        self.right_foot_pos = (right_foot_x, right_foot_y)
    
    def draw(self, screen):
        """Draw the simplified stick man character."""
        # Create a temporary surface for rotating when tumbling
        if self.is_tumbling and self.rotation_angle != 0:
            # Calculate bounding box for all points
            all_points = [
                self.head_pos, self.neck_pos, self.hip_pos,
                self.left_hand_pos, self.right_hand_pos,
                self.left_foot_pos, self.right_foot_pos
            ]
            
            min_x = min(p[0] for p in all_points) - self.head_radius - self.limb_width
            max_x = max(p[0] for p in all_points) + self.head_radius + self.limb_width
            min_y = min(p[1] for p in all_points) - self.head_radius - self.limb_width
            max_y = max(p[1] for p in all_points) + self.head_radius + self.limb_width
            
            width = max(1, int(max_x - min_x))
            height = max(1, int(max_y - min_y))
            
            temp_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            offset_x = -min_x
            offset_y = -min_y
            
            # Draw to temp surface with offset
            self._draw_body_parts(temp_surf, offset_x, offset_y)
            
            # Rotate the surface
            rotated_surf = pygame.transform.rotate(temp_surf, -math.degrees(self.rotation_angle))
            blit_rect = rotated_surf.get_rect(center=self.hip_pos)
            screen.blit(rotated_surf, blit_rect.topleft)
        else:
            # Draw directly to screen
            self._draw_body_parts(screen, 0, 0)
        
        # Draw stun effect
        if self.is_stunned:
            stun_font = pygame.font.Font(None, int(30 * (self.head_radius / self.base_head_radius)))
            stun_text = "Zzz"
            stun_color = (60, 60, 150)  # Dark blue
            
            # Animate the text slightly
            offset_y = math.sin(pygame.time.get_ticks() * 0.01) * 3
            
            stun_surf = stun_font.render(stun_text, True, stun_color)
            stun_rect = stun_surf.get_rect(
                centerx=int(self.head_pos[0]),
                bottom=int(self.head_pos[1] - self.head_radius - 10 + offset_y)
            )
            screen.blit(stun_surf, stun_rect)
        
        # Draw reversed controls indicator
        if self.is_controls_reversed:
            q_font = pygame.font.Font(None, int(24 * (self.head_radius / self.base_head_radius)))
            q_surf = q_font.render("?", True, RED)
            q_rect = q_surf.get_rect(
                centerx=int(self.head_pos[0]),
                bottom=int(self.head_pos[1] - self.head_radius - 5)
            )
            screen.blit(q_surf, q_rect)
    
    def _draw_body_parts(self, surface, offset_x=0, offset_y=0):
        """Draw all body parts to the given surface with optional offset."""
        # Helper function to apply offset
        def offset_pos(pos):
            return (pos[0] + offset_x, pos[1] + offset_y)
        
        # Draw legs with separate thigh and shin segments
        leg_color = self.team_color
        
        # Öka benbredden något
        leg_width = max(1, int(self.limb_width * 1.15))
        
        # Left leg
        pygame.draw.line(
            surface, leg_color, 
            offset_pos(self.hip_pos), 
            offset_pos(self.left_knee_pos), 
            leg_width
        )
        pygame.draw.line(
            surface, leg_color, 
            offset_pos(self.left_knee_pos), 
            offset_pos(self.left_foot_pos), 
            leg_width
        )
        
        # Right leg
        pygame.draw.line(
            surface, leg_color, 
            offset_pos(self.hip_pos), 
            offset_pos(self.right_knee_pos), 
            leg_width
        )
        pygame.draw.line(
            surface, leg_color, 
            offset_pos(self.right_knee_pos), 
            offset_pos(self.right_foot_pos), 
            leg_width
        )
        
        # Gör knälederna tydligare
        knee_radius = max(2, int(self.limb_width * 0.7))  # Större knäcirklar
        
        # Använd en annan färg för knäna för att betona leden
        knee_color = leg_color
        if isinstance(knee_color, tuple) and len(knee_color) >= 3:
            # Skapa något mörkare nyans för knäna
            knee_color = (
                max(0, knee_color[0] - 30),
                max(0, knee_color[1] - 30),
                max(0, knee_color[2] - 30)
            )
        
        pygame.draw.circle(
            surface, knee_color,
            offset_pos(self.left_knee_pos),
            knee_radius
        )
        pygame.draw.circle(
            surface, knee_color,
            offset_pos(self.right_knee_pos),
            knee_radius
        )
        
        # Rita små fotcirklar för att betona foten
        foot_radius = max(1, int(self.limb_width * 0.45))
        pygame.draw.circle(
            surface, knee_color,
            offset_pos(self.left_foot_pos),
            foot_radius
        )
        pygame.draw.circle(
            surface, knee_color,
            offset_pos(self.right_foot_pos),
            foot_radius
        )
        
        # Draw torso
        torso_color = self.team_accent
        pygame.draw.line(
            surface, torso_color, 
            offset_pos(self.hip_pos), 
            offset_pos(self.neck_pos), 
            max(1, int(self.limb_width * 1.2))
        )
        
        # Draw arms
        arm_color = self.team_accent
        arm_attach_pos = (self.x, self.neck_pos[1] + self.torso_length * 0.2)
        pygame.draw.line(
            surface, arm_color, 
            offset_pos(arm_attach_pos), 
            offset_pos(self.left_hand_pos), 
            max(1, int(self.limb_width))
        )
        pygame.draw.line(
            surface, arm_color, 
            offset_pos(arm_attach_pos), 
            offset_pos(self.right_hand_pos), 
            max(1, int(self.limb_width))
        )
        
        # Draw head
        head_center = offset_pos(self.head_pos)
        pygame.draw.circle(surface, ITALY_WHITE, head_center, int(self.head_radius))
        pygame.draw.circle(surface, BLACK, head_center, int(self.head_radius), 1)
        
        # Draw eyes
        eye_offset_x = self.head_radius * 0.35 * self.facing_direction
        eye_offset_y = -self.head_radius * 0.1
        eye_radius = max(1, int(3 * (self.head_radius / self.base_head_radius)))
        eye_pos_x = int(head_center[0] + eye_offset_x)
        eye_pos_y = int(head_center[1] + eye_offset_y)
        
        pygame.draw.circle(surface, self.eye_color, (eye_pos_x, eye_pos_y), eye_radius)
        
        # Draw nose
        nose_length = self.head_radius * 0.4
        nose_width = self.head_radius * 0.2
        nose_tip_x = head_center[0] + (self.head_radius * 0.5) * self.facing_direction
        nose_tip_y = head_center[1] + self.head_radius * 0.1
        nose_base_x = head_center[0] + (self.head_radius * 0.3) * self.facing_direction
        nose_base_y1 = nose_tip_y - nose_width / 2
        nose_base_y2 = nose_tip_y + nose_width / 2
        
        nose_points = [
            (int(nose_base_x), int(nose_base_y1)),
            (int(nose_tip_x), int(nose_tip_y)),
            (int(nose_base_x), int(nose_base_y2))
        ]
        pygame.draw.polygon(surface, NOSE_COLOR, nose_points)
        
        # Draw sword if active
        if self.is_sword:
            hand_pos = offset_pos(self.right_hand_pos if self.facing_direction == 1 else self.left_hand_pos)
            sword_length = self.torso_length * 1.5
            sword_width = self.limb_width * 0.8
            
            # Determine sword angle
            if self.is_kicking:
                progress = min(self.kick_timer / self.kick_duration, 1.0)
                if progress < 0.25:
                    sword_angle = -math.pi * 0.4 * (progress / 0.25)
                elif progress < 0.5:
                    swing_progress = (progress - 0.25) / 0.25
                    sword_angle = -math.pi * 0.4 + math.pi * 0.8 * swing_progress
                else:
                    recovery_progress = (progress - 0.5) / 0.5
                    sword_angle = math.pi * 0.4 * (1 - recovery_progress)
            else:
                sword_angle = -math.pi / 6  # Default holding angle
                
            if self.facing_direction == -1:
                sword_angle = math.pi - sword_angle
                
            # Calculate sword endpoint
            sword_end_x = hand_pos[0] + sword_length * math.cos(sword_angle)
            sword_end_y = hand_pos[1] + sword_length * math.sin(sword_angle)
            
            # Draw sword
            pygame.draw.line(
                surface, (192, 192, 192),  # Silver color
                hand_pos, (sword_end_x, sword_end_y),
                max(1, int(sword_width))
            )
            
            # Draw handle
            handle_length = sword_length * 0.2
            handle_angle = sword_angle + math.pi  # Opposite direction
            handle_end_x = hand_pos[0] + handle_length * math.cos(handle_angle)
            handle_end_y = hand_pos[1] + handle_length * math.sin(handle_angle)
            
            pygame.draw.line(
                surface, (101, 67, 33),  # Brown color
                hand_pos, (handle_end_x, handle_end_y),
                max(1, int(sword_width * 1.2))
            )
            
            # Draw crossguard
            crossguard_length = sword_width * 3
            crossguard_angle = sword_angle + math.pi/2  # Perpendicular
            
            crossguard_x1 = hand_pos[0] + crossguard_length/2 * math.cos(crossguard_angle)
            crossguard_y1 = hand_pos[1] + crossguard_length/2 * math.sin(crossguard_angle)
            crossguard_x2 = hand_pos[0] - crossguard_length/2 * math.cos(crossguard_angle)
            crossguard_y2 = hand_pos[1] - crossguard_length/2 * math.sin(crossguard_angle)
            
            pygame.draw.line(
                surface, (169, 169, 169),  # Metallic silver
                (crossguard_x1, crossguard_y1), (crossguard_x2, crossguard_y2),
                max(1, int(sword_width * 0.8))
            )
    
    def randomize_nose(self):
        """Randomize the player's nose for visual variety (dummy method for compatibility)."""
        # This is just a compatibility method to ensure the same interface as StickMan
        # We don't actually change the nose in the simplified version
        pass 

    def get_sword_position(self):
        """Return sword position data for collision detection."""
        if not self.is_sword:
            return None
            
        hand_pos = self.right_hand_pos if self.facing_direction == 1 else self.left_hand_pos
        sword_length = self.torso_length * 1.5
        
        # Determine sword angle based on kick status
        if self.is_kicking:
            progress = min(self.kick_timer / self.kick_duration, 1.0)
            if progress < 0.25:
                sword_angle = -math.pi * 0.4 * (progress / 0.25)
            elif progress < 0.5:
                swing_progress = (progress - 0.25) / 0.25
                sword_angle = -math.pi * 0.4 + math.pi * 0.8 * swing_progress
            else:
                recovery_progress = (progress - 0.5) / 0.5
                sword_angle = math.pi * 0.4 * (1 - recovery_progress)
        else:
            sword_angle = -math.pi / 6  # Default holding angle
            
        if self.facing_direction == -1:
            sword_angle = math.pi - sword_angle
            
        # Calculate sword endpoint
        tip_x = hand_pos[0] + sword_length * math.cos(sword_angle)
        tip_y = hand_pos[1] + sword_length * math.sin(sword_angle)
        
        return (tip_x, tip_y, hand_pos[0], hand_pos[1], sword_angle) 