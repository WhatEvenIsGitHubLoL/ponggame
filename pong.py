#Create pong in Python using Pygame

import pygame, time, random, math

#init
pygame.init()

#Define base color variables
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)

#Define initialization variables
left_side_init_goal = 0 #starting goals of right side
right_side_init_goal = 0 #starting goals of left side
right_side_goal_increment = 1 #increment of goals of right side
left_side_goal_increment = 1 #increment of goals of left side
right_side_cheat = True #cheat mode for right side
left_side_cheat = True #cheat mode for left sidez
right_side_bot = False #bot mode for right side
left_side_bot = False #bot mode for left side
re_random = True #randomize velocities of ball on each goal


#Initialize base variables for screen
width = 1280 #set width of display
height = 720 #set height of display
screen = pygame.display.set_mode((width, height)) #initialize the screen
pygame.display.set_caption("Pong")
debug = True #enable debug logs
DIST_SCORE = 10 #distance of score from the top of screen

#Modular variables for game
FPS = math.inf #set tickrate
frequencyOfSpeedIncreaseInFrames = 10 #after every how many ticks should speed be increased

#Modular variables for ball
ball_radius = 20 #radius of ball (extremely buggy when changed)
init_x_vel = random.uniform(-1, 1) #set the initial x velocity
init_y_vel = random.uniform(-1,1) #set the initial y veloci/ty
speed_increase = 0.1 #percent increase of speed
ball_color = WHITE #color of ball

#Modular variables for left paddle (paddle1)
DIST_TO_BORDER1 = 30 #distance from left border of the left paddle
paddle1_width = 20 #width of left paddle
paddle1_height = 100 #height of left paddle
paddle1_speed = 5 #speed of left paddle
paddle1_color = BLUE #color of left paddle

#Modular variables for right paddle (paddle2)
DIST_TO_BORDER2 = 30 #distance from right border of the right paddle
paddle2_width = 20 #width of right paddle
paddle2_height = 100 #height of right paddle
paddle2_speed = 5 #speed of right paddle
paddle2_color = RED #color of right paddle


#Base object
class Object:
    def __init__(self, x, y, w, h, c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c

class Ball:
    def __init__(self, x, y, r, c, vx, vy):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.vx = vx
        self.vy = vy
    def draw(self, screen):
        pygame.draw.circle(screen, self.c, (self.x + self.r, self.y + self.r), self.r)
    def update(self):
        self.x += self.vx
        self.y += self.vy
    def collision(self, obj):
        if isinstance(obj, Paddle):
            if obj.type == 2: #handle for right paddle
                if self.y + self.r >= obj.y and self.y - self.r <= obj.y + obj.h:
                    if self.x + self.r >= obj.x - obj.w and self.x - self.r <= obj.x + obj.w:
                        if self.y + self.r >= obj.y and self.y - self.r <= obj.y + obj.h/2:
                            return 1  # collision with thicker side
                        else:
                            return 2  # collision with thinner side
            if obj.type == 1: #handle for left paddle 
                if self.y + self.r >= obj.y and self.y - self.r <= obj.y + obj.h:
                    if self.x + self.r >= obj.x - obj.w and self.x - self.r <= obj.x:
                        if self.y + self.r >= obj.y and self.y - self.r <= obj.y + obj.h/2:
                            return 1  # collision with thicker side
                        else:
                            return 2  # collision with thinner side
        return 0  # no collision


class Paddle:
    def __init__(self, x, y, w, h, c, lype):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.type = lype
    def draw(self, screen):
        pygame.draw.rect(screen, self.c, (self.x, self.y, self.w, self.h))

def off_bounds(obj):
    #return "codes" for different cases
    #return 1 if the object is going too low, 2 if its going too high, 3 if its going too far to the left, and 4 if its going too far to the right, return 0 if its in bounds
    #also take width/height into account
    if isinstance(obj, Paddle):
        if obj.y < 0:
            return 1
        if obj.y > height - obj.h:
            return 2
        if obj.x < 0:
            return 3
        if obj.x > width - obj.w:
            return 4
    if isinstance(obj, Ball):
        if obj.y < 0:
            return 1
        if obj.y > height - obj.r * 2:
            return 2
        if obj.x < 0:
            return 3
        if obj.x > width - obj.r * 2:
            return 4
    return False

def main():
    global right_side_cheat, init_x_vel, init_y_vel
    #Initialize objects
    ball = Ball(width // 2, height // 2, ball_radius, ball_color, init_x_vel, init_y_vel)
    paddle1 = Paddle(DIST_TO_BORDER1, height // 2, paddle1_width, paddle1_height, paddle1_color, 1)
    paddle2 = Paddle(width - (DIST_TO_BORDER2 + paddle2_width), height // 2, paddle2_width, paddle2_height, paddle2_color, 2)
    blue_score = right_side_init_goal
    red_score = left_side_init_goal
    score_display = "Left: " + str(blue_score) + " Right: " + str(red_score)
    tick = 0
    prev_time, prev_tick = time.perf_counter(), tick
    tickrate = 0
    
    font = pygame.font.SysFont("comicsansms", 30)

    #Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        if right_side_cheat:
            paddle2.y = ball.y - paddle2.w // 2
        if left_side_cheat:
            paddle1.y = ball.y - paddle1.w // 2
        current_time, current_tick = time.perf_counter(), tick
        if current_time - prev_time >= 0.5: #do it every half second
            prev_time = current_time
            tickrate = (current_tick - prev_tick) * 2
            prev_tick = current_tick
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and not (off_bounds(paddle1) == 1) and not left_side_bot:
            paddle1.y -= paddle1_speed
        if keys[pygame.K_s] and not (off_bounds(paddle1) == 2) and not left_side_bot:
            paddle1.y += paddle1_speed
        #add keypresses of "W" and "S" for paddle2
        if keys[pygame.K_u] and not (off_bounds(paddle2) == 1) and not right_side_bot:
            paddle2.y -= paddle2_speed
        if keys[pygame.K_j] and not (off_bounds(paddle2) == 2) and not right_side_bot:
            paddle2.y += paddle2_speed
        if keys[pygame.K_p]:
            paddle2.y = ball.y - paddle2.w // 2
        if keys[pygame.K_r]:
            paddle1.y = ball.y - paddle1.w // 2
        if left_side_bot:
            if paddle1.y > ball.y and not (off_bounds(paddle1) == 1):
                paddle1.y -= paddle1_speed
            if paddle1.y < ball.y and not (off_bounds(paddle1) == 2):
                paddle1.y += paddle1_speed
        if right_side_bot:
            if paddle2.y > ball.y and not (off_bounds(paddle2) == 1):
                paddle2.y -= paddle2_speed
            if paddle2.y < ball.y and not (off_bounds(paddle2) == 2):
                paddle2.y += paddle2_speed
        ball.update()
        if off_bounds(ball) == 1 or off_bounds(ball) == 2:
            ball.vy = -ball.vy
            if debug:
                print("collision with wall")
        if off_bounds(ball) in [3, 4]:
            if re_random:
                init_x_vel = random.uniform(-1, 1)
                init_y_vel = random.uniform(-1, 1)
            if off_bounds(ball) == 3:
                red_score += right_side_goal_increment
            else:
                blue_score += left_side_goal_increment
            tick = 0
            score_display = "Left: " + str(blue_score) + " Right: " + str(red_score)
            ball = Ball(width // 2, height // 2, ball_radius, ball_color, init_x_vel, init_y_vel)
            paddle1 = Paddle(DIST_TO_BORDER1, height // 2, paddle1_width, paddle1_height, paddle1_color, 1)
            paddle2 = Paddle(width - (DIST_TO_BORDER2 + paddle2_width), height // 2, paddle2_width, paddle2_height, paddle2_color, 2)
            if debug:
                print(score_display)
        if ball.collision(paddle1) == 1 or ball.collision(paddle2) == 1:
            ball.vx = -ball.vx
            if debug:
                print("horizontal collision")
            #move the ball back a bit
            if ball.x > width / 2:
                ball.x -= 1
            if ball.x < width / 2:
                ball.x += 1
        if ball.collision(paddle1) == 2 or ball.collision(paddle2) == 2:
            ball.vy = -ball.vy
            if debug:
                print('vertical collision')
            #move the ball back a bit
            # if ball.vy > height / 2:
            #     ball.vy -= 1
            # if ball.vy < height / 2:
            #     ball.vy += 1
        if tick % frequencyOfSpeedIncreaseInFrames == 0 and tick != 0:
            try:
                ball.vx += (speed_increase/100) * ball.vx
            except ZeroDivisionError:
                ball.vx += 1
            try:
                ball.vy += (speed_increase / 100) * ball.vy
            except ZeroDivisionError:
                ball.vy += 1
            # if debug:
            #     print(f"speed increased at tick {tick}")
        ball.draw(screen)
        paddle1.draw(screen)
        paddle2.draw(screen)
        #display the score on the screen
        tickrate_display = font.render("FPS: " + str(tickrate), True, WHITE)
        text = font.render(score_display, True, WHITE)
        screen.blit(text, (width // 2 - 125, DIST_SCORE))
        screen.blit(tickrate_display, (10, 10))
        pygame.display.update()
        tick += 1
        time.sleep(1/FPS)
    pygame.quit()

if __name__ == "__main__":
    main()