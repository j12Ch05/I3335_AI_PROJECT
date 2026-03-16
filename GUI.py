import pygame
import Queens, knight_tour

pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont(None, 30)
error_font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

activeQ = False
activeK = False
running = True
errorQ = ""
textQ = "Board Size?"
textK = "Start Position?"

base_r1 = pygame.Rect(180, 220, 280, 280)
base_r2 = pygame.Rect(500, 220, 280, 280)
base_r3 = pygame.Rect(820, 220, 280, 280)
r11 = pygame.Rect(180, 515, 280, 80)
r33 = pygame.Rect(820, 515, 280, 80)
r1 = base_r1.copy()
r2 = base_r2.copy()
r3 = base_r3.copy()
r1_scale = 1.0
r2_scale = 1.0
r3_scale = 1.0

def scaled_rect(rect, scale):
    scaled_width = int(rect.width * scale)
    scaled_height = int(rect.height * scale)
    return pygame.Rect(
        rect.centerx - scaled_width // 2,
        rect.centery - scaled_height // 2,
        scaled_width,
        scaled_height,
    )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            activeQ = r11.collidepoint(event.pos)
            if activeQ and textQ=="Board Size?":
                textQ = ""
            elif not activeQ and textQ=="":
                textQ = "Board Size?"
            elif not activeQ and textQ.isalpha():
                errorQ = "Use Integers"
                textQ = "Board Size?"
            
            activeK = r33.collidepoint(event.pos)
            if activeK and textK=="Start Position?":
                textK = ""
            elif not activeK and textK=="":
                textK = "Start Position?"
            elif not activeK and textK.isalpha():
                errorQ = "Use Integers"
                textQ = "Start Position?"
                
            queensGame = r1.collidepoint(event.pos)
            if queensGame:
                if textQ=="Board Size?":
                    errorQ = "Select the damn board size"
                else:
                    Queens.n = int(textQ)
                    Queens.main()
                    running = False
            
            knightTour = r3.collidepoint(event.pos)
            if knightTour:
                if textK=="Start Position?":
                    errorQ = "Select the start position"
                else:
                    # BE CAREFUL THIS SHIT LITERALLY FROZE MY PC
                    x, y = map(int, textK.replace(",", " ").split())
                    if 0 <= x < 8 and 0 <= y < 8:
                        running = False
                        solver = knight_tour.KnightTourSolver(8)
                        success = solver.solve(x, y)
                        if success:
                            solver.animate_solution(interval=600)
                    else:
                        errorQ = "Use coordinates from 0 to 7"                    

                
        elif event.type == pygame.KEYDOWN:
            if activeQ:
                if event.key == pygame.K_BACKSPACE:
                    textQ = textQ[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Queen: ", textQ)
                else:
                    textQ += event.unicode
                    
            elif activeK:
                if event.key == pygame.K_BACKSPACE:
                    textK = textK[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Knight: ", textK)
                else:
                    textK += event.unicode        

    mouse_pos = pygame.mouse.get_pos()
    target_r1_scale = 1.08 if base_r1.collidepoint(mouse_pos) else 1.0
    target_r2_scale = 1.08 if base_r2.collidepoint(mouse_pos) else 1.0
    target_r3_scale = 1.08 if base_r3.collidepoint(mouse_pos) else 1.0
    animation_speed = 0.18

    r1_scale += (target_r1_scale - r1_scale) * animation_speed
    r2_scale += (target_r2_scale - r2_scale) * animation_speed
    r3_scale += (target_r3_scale - r3_scale) * animation_speed

    r1 = scaled_rect(base_r1, r1_scale)
    r2 = scaled_rect(base_r2, r2_scale)
    r3 = scaled_rect(base_r3, r3_scale)

    screen.fill("black")
    s = pygame.Surface((1280, 720))
    
    pygame.draw.circle(s, "yellow", (320, 360), 2)
    pygame.draw.rect(s,"yellow",r1, 2)
    
    box_colorQ = "yellow" if activeQ else "gray"
    pygame.draw.rect(s, box_colorQ, r11, 2)
    
    pygame.draw.circle(s, "green", (640, 360), 2)
    pygame.draw.rect(s,"green",r2, 2)
    
    pygame.draw.circle(s, "cyan", (960, 360), 2)
    pygame.draw.rect(s,"cyan",r3, 2)
    
    box_colorK = "cyan" if activeK else "gray"
    pygame.draw.rect(s, box_colorK, r33, 2)

    if r11.collidepoint(mouse_pos) or r33.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    elif r1.collidepoint(mouse_pos) or r2.collidepoint(mouse_pos) or r3.collidepoint(mouse_pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    screen.blit(s, (0,0))
    
    textQ_surface = font.render(textQ, True, "yellow")
    textQ_rect = textQ_surface.get_rect(center=r11.center)
    screen.blit(textQ_surface, textQ_rect)
    
    textK_surface = font.render(textK, True, "cyan")
    textK_rect = textK_surface.get_rect(center=r33.center)
    screen.blit(textK_surface, textK_rect)
    
    errorQ_surface = error_font.render(errorQ, True, "red")
    errorQ_rect = errorQ_surface.get_rect(midtop=(r11.centerx, r11.bottom + 8))
    screen.blit(errorQ_surface, errorQ_rect)
    
    clock.tick(60)
    
    pygame.display.flip()
    
pygame.quit()
