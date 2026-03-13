import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

active = True
running = True
text = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pygame.K_RETURN:
                print("Value: ", text)
            else:
                text += event.unicode        

    screen.fill("black")
    s = pygame.Surface((1280, 720))
    
    pygame.draw.circle(s, "red", (320, 360), 2)
    r1 = pygame.Rect(180, 220, 280, 280)
    pygame.draw.rect(s,"yellow",r1, 2)
    
    r11 = pygame.Rect(180, 510, 280, 80)
    pygame.draw.rect(s,"orange",r11, 2)
    text_surface = font.render(text, True, "white")
    screen.blit(text_surface, (r11.x + 10, r11.y + 10))
    
    pygame.draw.circle(s, "green", (640, 360), 2)
    r2 = pygame.Rect(500, 220, 280, 280)
    pygame.draw.rect(s,"white",r2, 2)
    
    pygame.draw.circle(s, "blue", (960, 360), 2)
    r3 = pygame.Rect(820, 220, 280, 280)
    pygame.draw.rect(s,"purple",r3, 2)
    
    screen.blit(s, (0,0))
    clock.tick(60)
    
    pygame.display.flip()
    
pygame.quit()