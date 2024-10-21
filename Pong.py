import pygame , sys, random
# sys gives us access to more function in our system, but we will be usign it to close the game once were done

def ball_animation():
    #NOTE usign the global function is onlly useful for simple projects for more complex ones its not a good idea
    # It would be better to use return statement *Cough cough (DO this for your iteration)
    # Or use a class like we did with ball.x and ball.y
    global ball_speed_x, ball_speed_y,player_score,opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #This if statement making usre it never leaves from bottom and if it does it goes opposite way for vertical
    if ball.top <=0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_collision)
        #This will make it negative and go opposite direction
        ball_speed_y *=-1
    #This does smae thing for horizontal
    if ball.left <= 0:
        pygame.mixer.Sound.play(pong_score)
        player_score +=1
        score_time = pygame.time.get_ticks()
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(pong_score)
        opponent_score +=1
        score_time = pygame.time.get_ticks()

    #pygame has a .colliderect(rect) that returns true if it does collide
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_collision)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs (ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs (ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and  ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_collision)
        if abs(ball.left - opponent.right) < 10:
         ball_speed_x *= -1
        elif abs (ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs (ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3",False, light_grey)
        screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))

    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2",False, light_grey)
        screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1",False, light_grey)
        screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))
    
    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0,0
    
    else:
        ball_speed_y = 7*random.choice((1,-1))
        ball_speed_x = 7*random.choice((1,-1))
        score_time=None

#General
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()
#pygame.init() initiates all of pygames modules, we need this for any type of pygame code

#Main Window
screen_width = 1280
screen_height = 900
#Sets up the main window size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
# This returns a display surface object

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width -20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140 )
#Note the coordicantes of a rectangle is x,y and the origin of a rectagle is the top left
#Also to make a rectangle we use pygame.Rect(x,y, height, width)
#We dont just do screen width/2 because it will not really be centered it will be off by a bit

#Colors
bg_color = pygame.Color('grey12')
light_grey =  (200,200,200)

#Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

#Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf",32)

#Sound
pong_collision = pygame.mixer.Sound("CollisionSoundEffect-Pong.mp3")
pong_score = pygame.mixer.Sound("Score - Sound EffectforPong.mp3")


#Score Timer
score_time= True


#Font that comes in computer already or we can donwload new one
#Idea: Use retro font

# To use the draw function we do pygame.draw(surface,color,rect)
# To make colors we can use r,g,b values which just stand for red green and blue
# We can also chnage purity of color using numbers 0-255
# 0 being absence of colro and 255 being that pure color

while True:
    #Note pygame calls any user interaction an event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #Both of these commands together effectively close the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed +=7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -=7
            if event.key == pygame.K_UP:
                player_speed += 7

    #Game Logic
    ball_animation()
    player_animation()
    opponent_ai()
    
    #Visuals        
    #To do correctly make usre we do order correclty as these things should be drawn on top of eachother
    # For example if we had put screen.fill last we would only be seeing that black screen
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    #stands for antialiased line meaning its the outline so that we see the objects more smoothly 
    pygame.draw.aaline(screen, light_grey,(screen_width/2,0),(screen_width/2, screen_height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    #.blit puts one surface on the other
    screen.blit(player_text, (660,470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    #.blit puts one surface on the other
    screen.blit(opponent_text, (600,470))


    pygame.display.flip()
    #This is clock we made earlier and it limits how fast the loop is executed if we dont specify
    #It may go so quick that we dont even get to see anything
    #This is same as 60fps
    clock.tick(60)