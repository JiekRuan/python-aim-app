import pygame
import time, random, math 
from target import Target
from bouton import Button
pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aim")
target_increment = 400 
target_event = pygame.USEREVENT
target_padding = 30
lives = 5


label_font = pygame.font.SysFont("opensans", 16)

bg_color = (0, 25, 40)

targets = []
target_clicked = 0
clicks = 0
misses = 0
start_time = 0  

width, height = 800, 600
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aim")
target_increment = 400 
target_event = pygame.USEREVENT
target_padding = 30
lives = 5

def draw(window, targets):
    window.fill(bg_color)

    for target in targets:
        target.draw(window)

def format_time(secs):
    millisec = math.floor(int(secs * 1000 % 1000)/100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}:{millisec:02d}"

def draw_top_bar(window, elapsed_time, target_clicked, misses):
    pygame.draw.rect(window, "white", (0, 0, width, 20))
    time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    window.blit(time_label, (5, 5))
    
    if elapsed_time > 0:
        speed = round(target_clicked / elapsed_time, 1)
    else:
        speed = 0
    
    speed_label = label_font.render(f"Speed: {speed} t/s", 1, "black")
    window.blit(speed_label, (200, 5))
    
    hits_label = label_font.render(f"Hits: {target_clicked}", 1, "black")
    window.blit(hits_label, (400, 5))
    
    lives_label = label_font.render(f"Lives: {lives - misses}", 1, "black")
    window.blit(lives_label, (600, 5))

def end_screen(window, elapsed_time, target_clicked, clicks):
    restart_clicked = False  

    while not restart_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    restart_clicked = True 
                    break 

        window.fill(bg_color)
        time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1, "white")
        window.blit(time_label, (middle(time_label), 100))

        if clicks > 0:  
            speed = round(target_clicked / elapsed_time, 1)
            accuracy = round(target_clicked / clicks * 100, 2)
        else:
            speed = 0
            accuracy = 0

        speed_label = label_font.render(f"Speed: {speed} t/s", 1, "white")
        window.blit(speed_label, (middle(speed_label), 200))

        hits_label = label_font.render(f"Hits: {target_clicked}", 1, "white")
        window.blit(hits_label, (middle(hits_label), 300))

        accuracy_label = label_font.render(f"Accuracy: {accuracy}%", 1, "white")
        window.blit(accuracy_label, (middle(accuracy_label), 400))

        restart_button = pygame.Rect(width // 2 - 50, 450, 100, 50)
        pygame.draw.rect(window, (0, 128, 255), restart_button)
        restart_label = label_font.render("Restart", 1, "white")
        window.blit(restart_label, (width // 2 - 30, 460))

        pygame.display.update()

    restart_game(window)



def middle(surface):
    return width / 2 - surface.get_width() / 2

def restart_game(window):
    global targets, target_clicked, clicks, misses, start_time, elapsed_time, lives  # Ajoutez lives

    targets = []
    target_clicked = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    elapsed_time = 0  
    lives = 5  
    pygame.time.set_timer(target_event, target_increment)

    main()


def main():
    run = True
    clock = pygame.time.Clock()
    pygame.time.set_timer(target_event, target_increment)

    global targets, target_clicked, clicks, misses, start_time

    while run:
        click = False
        clock.tick(60)
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == target_event:
                x = random.randint(target_padding, width - target_padding)
                y = random.randint(target_padding + 50, height - target_padding)
                lifespan = 5  # Durée de vie en secondes de la cible
                target = Target(x, y, lifespan)
                targets.append(target) 

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1 

            expired_targets = [target for target in targets if target.is_expired()]
            for expired_target in expired_targets:
                targets.remove(expired_target)
                if lives > 0:
                    misses += 1

            if misses >= lives:
                end_screen(window, elapsed_time, target_clicked, clicks)
                run = False  

        for target in targets:
            if click and target.collide(*mouse_position):
                targets.remove(target)
                target_clicked += 1

        draw(window, targets)
        draw_top_bar(window, elapsed_time, target_clicked, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()