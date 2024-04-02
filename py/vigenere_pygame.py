import pygame
from pygame.locals import *
from mylib import ALPHABET, VKEY as encryptor
from vigenere import vigenere_encrypt_char


pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Vigenère Live-Tastendruck')

font = pygame.font.Font(None, 74)

running = True
key_index = 0
display_text = ''

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.unicode.upper() in ALPHABET:
                encrypted_char, key_index = vigenere_encrypt_char(event.unicode, encryptor, key_index)
                display_text = encrypted_char  # Aktualisiere den anzuzeigenden Text
                print(f"Verschlüsselter Buchstabe: {encrypted_char}")
            if event.key == K_RETURN:
                key_index = 0
                display_text = ''  # Leere den Text bei Enter
        elif event.type == KEYUP:
            if event.key == K_RETURN:
                running = False
    
    screen.fill((0, 0, 0))  # Leere den Bildschirm
    
    # Rendere den Text
    text = font.render(display_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(320, 240))
    screen.blit(text, text_rect)
    
    pygame.display.flip()  # Aktualisiere den Bildschirm

pygame.quit()