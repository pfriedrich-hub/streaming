

import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS:                  # K_ASTERISK geht nicht
                mods = pygame.key.get_mods()

                if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_ALT:
                    print("pressed: CTRL+SHIFT+ALT + PLUS")
                elif mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                    print("pressed: CTRL+SHIFT + PLUS")
                elif mods & pygame.KMOD_CTRL and mods & pygame.KMOD_ALT:
                    print("pressed: CTRL+ALT + PLUS")
                elif mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_ALT:
                    print("pressed: SHIFT+ALT + PLUS")
                elif mods & pygame.KMOD_SHIFT:
                    print("pressed: SHIFT + Plus")
                elif mods & pygame.KMOD_CTRL:
                    print("pressed: CTRL + PLUS")
                elif mods & pygame.KMOD_ALT:
                    print("pressed: ALT + PLUS")
                else:
                    print("pressed: B")



pygame.quit()