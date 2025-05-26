# pylint: disable=no-member

import pygame
from parametros import *
from sprites_e_classes import *
from jogando import *
from tela0_de_derrota_e_vitoria import *
from math import *
from jogando import *
from mapa import MAPA_1, MAPA_2, MAPA_3
pygame.init()


window = pygame.display.set_mode((1000, 600))

# CRIANDO A JANELA
JANELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption('Fox, a Raposa')

###############CRIANDO AS PLATAFORMAS

estado_do_jogo = INICIO
FASE = 1

#iniciando o loop dos estados

while estado_do_jogo != DONE:
    ultimo_pulo = pygame.time.get_ticks()
    #analisa se o jogo foi fechado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            estado_do_jogo = DONE
    if estado_do_jogo == INICIO:
        estado_do_jogo = tela_inicial(JANELA)
    if estado_do_jogo == JOGANDO:
        #DEFININDO O MAPA E OS DICIONÁRIOS A SEREM UTILIZADOS
        if   FASE == 1:
            F = F1
            MAPA = MAPA_1
        elif FASE == 2:
            F = F2
            MAPA = MAPA_2
        elif FASE == 3:
            F = F3
            MAPA = MAPA_3
        estado_do_jogo = jogando(JANELA)
    if estado_do_jogo == GAME_OVER:
        estado_do_jogo = tela_final(JANELA)
    if estado_do_jogo == VITORIA:
        FASE +=1
    if FASE!=4:
        estado_do_jogo = tela_de_vitoria(JANELA)
    else:
        estado_do_jogo = fim_vitorioso(JANELA)


"""

#fecha a janela
pygame.quit()



game = True


while game:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game = False


    window.fill((0, 71, 171)) 
    pygame.display.update()


pygame.quit()

"""