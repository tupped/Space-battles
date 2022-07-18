import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space battle") 

white = (255, 255, 255)
black = (0, 0 ,0)
blue = (138, 183, 255)
yellow = (255, 255, 0)

damage_sfx = pygame.mixer.Sound(os.path.join("Assets", "Hit_Hurt3.mp3"))
shoot_sfx = pygame.mixer.Sound(os.path.join("Assets", "Laser_Shoot4.mp3"))
win_sfx = pygame.mixer.Sound(os.path.join("Assets", "Pickup_Coin3.mp3"))


health_font = pygame.font.SysFont("copperplategothic", 40)
winner_font = pygame.font.SysFont("copperplategothic", 100)

border = pygame.Rect(WIDTH // 2 - 5, 0, 20, HEIGHT)

fps = 60
vel = 5
bullet_vel = 20
max_ammo = 5

spaceship_width, spaceship_height = 100, 100

white_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2


#Spaceship sprite 1 (White Ship)
spaceship_image_1 = pygame.image.load(os.path.join("Assets", "rocket1.png"))
spaceship_image_1 = pygame.transform.scale(spaceship_image_1, (spaceship_height, spaceship_width))

#Spaceship sprite 2 (Blue Ship)
spaceship_image_2 = pygame.image.load(os.path.join("Assets", "rocket2.png"))
spaceship_image_2 = pygame.transform.scale(spaceship_image_2, (spaceship_width, spaceship_height))

#BACKROUND SPRITE
backround_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

def draw_window(spcwhite, spcblue, blue_bullets, white_bullets, white_health, blue_health):
    window.blit(backround_image, (0, 0))
    pygame.draw.rect(window, black, border)
    
    white_health_text = health_font.render("Health: " + str(white_health), 1, white)
    blue_health_text = health_font.render("Health: " + str(blue_health), 1, white)
    window.blit(white_health_text, (WIDTH - white_health_text.get_width() - 10, 10))
    window.blit(blue_health_text, (10, 10))

    window.blit(spaceship_image_1, (spcwhite.x, spcwhite.y))
    window.blit(spaceship_image_2, (spcblue.x, spcblue.y))
    
    for bullet in white_bullets:
        pygame.draw.rect(window, blue, bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(window, yellow, bullet)
    pygame.display.update()

#MOVEMENT HANDLERS
def spcblue_handle_movement(keys_pressed, spcblue):
    if keys_pressed[pygame.K_a] and spcblue.x - vel > 0: # LEFT
            spcblue.x -= vel
    if keys_pressed[pygame.K_d] and spcblue.x + vel + spcblue.width < border.x: # RIGHT
            spcblue.x += vel
    if keys_pressed[pygame.K_w] and spcblue.y - vel > 0: # UP
            spcblue.y -= vel
    if keys_pressed[pygame.K_s] and spcblue.y + vel + spcblue.height < HEIGHT - 5: # DOWN
            spcblue.y += vel
def spcwhite_handle_movement(keys_pressed, spcwhite):
    if keys_pressed[pygame.K_LEFT] and spcwhite.x - vel > border.x + border.width: # LEFT
            spcwhite.x -= vel
    if keys_pressed[pygame.K_RIGHT] and spcwhite.x + vel + spcwhite.width < WIDTH: # RIGHT
            spcwhite.x += vel
    if keys_pressed[pygame.K_UP] and spcwhite.y - vel > 0: # UP
            spcwhite.y -= vel
    if keys_pressed[pygame.K_DOWN] and spcwhite.y + vel + spcwhite.height < HEIGHT - 5: # DOWN
            spcwhite.y += vel


def handle_bullets(white_bullets, blue_bullets, spcwhite, spcblue):
    for bullet in white_bullets:
        bullet.x -= bullet_vel
        if spcblue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(blue_hit))
            white_bullets.remove(bullet)
        elif bullet.x < 0:
            white_bullets.remove(bullet)
    for bullet in blue_bullets:
        bullet.x += bullet_vel
        if spcwhite.colliderect(bullet):
            pygame.event.post(pygame.event.Event(white_hit))
            blue_bullets.remove(bullet)
            
               
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    window.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    spcwhite = pygame.Rect(1700, 300, spaceship_width, spaceship_height)
    spcblue = pygame.Rect(100, 300, spaceship_width, spaceship_height)
    
    white_bullets = []
    blue_bullets = []

    white_health = 3
    blue_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT and len(white_bullets) < max_ammo:
                    shoot_sfx.play()
                    bullet = pygame.Rect(spcwhite.x,  spcwhite.y + spcwhite.height // 2 - 2, 10 , 5)
                    white_bullets.append(bullet)

                if event.key == pygame.K_LSHIFT and len(blue_bullets) < max_ammo:
                    shoot_sfx.play()
                    bullet = pygame.Rect(spcblue.x + spcblue.width, spcblue.y + spcblue.height // 2 - 2, 10 , 5)
                    blue_bullets.append(bullet)
            if event.type == white_hit:
                white_health -= 1
                damage_sfx.play()
            if event.type == blue_hit:
                blue_health -= 1
                damage_sfx.play()
        winner_text = ""
        if white_health <= 0:
            winner_text = "Blue Wins!"

        if blue_health <= 0:
            winner_text = "White Wins!"
    
        if winner_text != "":
            win_sfx.play()
            draw_winner(winner_text)
            break   
            
        
        keys_pressed = pygame.key.get_pressed()
        spcblue_handle_movement(keys_pressed, spcblue)
        spcwhite_handle_movement(keys_pressed, spcwhite)

        handle_bullets(white_bullets, blue_bullets, spcwhite, spcblue)
        
        draw_window(spcwhite, spcblue, blue_bullets, white_bullets, white_health, blue_health)
        
    
   
    



if __name__ == "__main__":
    while True:
        main()
