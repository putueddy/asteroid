import pygame
import sys
import os
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

HIGH_SCORE_FILE = "high_score.txt"

def load_high_score():
    """Load high score from file, return 0 if file doesn't exist"""
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
    except (ValueError, IOError):
        pass
    return 0

def save_high_score(score):
    """Save high score to file"""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except IOError:
        print(f"Warning: Could not save high score to {HIGH_SCORE_FILE}")

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    
    # Load high score at game start
    high_score = load_high_score()
    print(f"High score loaded: {high_score}")

    while True:
        # Initialize game state
        score = 0
        
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable)
        Shot.containers = (shots, updatable, drawable)
        
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField()
        dt = 0

        # Game loop
        game_running = True
        while game_running:
            log_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Handle Cmd+Q (macOS) or Ctrl+Q (other systems)
                    if event.key == pygame.K_q:
                        keys = pygame.key.get_pressed()
                        # Check for Cmd key (macOS) or Ctrl key (other systems)
                        if keys[pygame.K_LMETA] or keys[pygame.K_RMETA] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                            sys.exit()
            
            updatable.update(dt)

            for asteroid in asteroids:
                if player.check_collision(asteroid):
                    log_event("player_hit")
                    
                    # Check and update high score
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                        print(f"New high score: {high_score}!")
                    
                    print(f"Game over! Final score: {score}")
                    print("Restarting...")
                    game_running = False
                    break

                for shot in shots:
                    if asteroid.check_collision(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        score += 5
                        break

            screen.fill("black")
            
            # Draw high score on top left
            high_score_text = font.render(f"High Score: {high_score}", True, "white")
            high_score_rect = high_score_text.get_rect()
            high_score_rect.topleft = (10, 10)
            screen.blit(high_score_text, high_score_rect)
            
            # Draw score on top right
            score_text = font.render(f"Score: {score}", True, "white")
            score_rect = score_text.get_rect()
            score_rect.topright = (SCREEN_WIDTH - 10, 10)
            screen.blit(score_text, score_rect)
            
            # Draw exit instruction on bottom left
            exit_text = font.render("Exit: [Cmd] + Q", True, "white")
            exit_rect = exit_text.get_rect()
            exit_rect.bottomleft = (SCREEN_WIDTH / 2 - exit_rect.width / 2, SCREEN_HEIGHT - 10)
            screen.blit(exit_text, exit_rect)
            
            for obj in drawable:
                obj.draw(screen)
            
            pygame.display.flip()

            # limit the frame rate to 60 FPS
            dt = clock.tick(FPS) / 1000

if __name__ == "__main__":
    main()
