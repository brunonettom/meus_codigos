import pygame
import random
from parametros import *
from os import path
from math import *
pygame.init()



def tela_inicial(JANELA):
    
    # Carrega o fundo da tela inicial
    estado_do_jogo = INICIO
    while estado_do_jogo == INICIO:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for evento in pygame.event.get():
            # Verifica se foi fechado.
            if evento.type == pygame.QUIT:
                estado_do_jogo = DONE

            if evento.type == pygame.KEYUP:
                estado_do_jogo = JOGANDO

        # A cada loop, redesenha o fundo e os sprites
        JANELA.blit(img_inicio, (0, 0)) #imagem com o escrito "para recomeçar, pressione qualquer tecla"


        # Depois de desenhar tudo, inverte o display.??????
        pygame.display.flip() 

    return estado_do_jogo


def tela_final(JANELA):
    
    # Carrega o fundo da tela inicial
    estado_do_jogo = GAME_OVER
    while estado_do_jogo == GAME_OVER:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for evento in pygame.event.get():
            # Verifica se foi fechado.
            if evento.type == pygame.QUIT:
                estado_do_jogo = DONE

            if evento.type == pygame.KEYUP:
                estado_do_jogo = JOGANDO

        # A cada loop, redesenha o fundo e os sprites
        JANELA.blit(img_fim, (0, 0)) #imagem com o escrito "para recomeçar, pressione qualquer tecla"


        # Depois de desenhar tudo, inverte o display.??????
        pygame.display.flip() 

    return estado_do_jogo

def tela_de_vitoria(JANELA):
    estado_do_jogo = VITORIA
    while estado_do_jogo == VITORIA:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for evento in pygame.event.get():
            # Verifica se foi fechado.
            if evento.type == pygame.QUIT:
                estado_do_jogo = DONE

            if evento.type == pygame.KEYUP:
                estado_do_jogo = JOGANDO

        # A cada loop, redesenha o fundo e os sprites
        JANELA.blit(img_vitoria, (0, 0)) #imagem com o escrito "para recomeçar, pressione qualquer tecla"


        # Depois de desenhar tudo, inverte o display.??????
        pygame.display.flip() 

    return estado_do_jogo

def fim_vitorioso(JANELA):
    estado_do_jogo = VITORIA
    while estado_do_jogo == VITORIA:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for evento in pygame.event.get():
            # Verifica se foi fechado.
            if evento.type == pygame.QUIT:
                estado_do_jogo = DONE
            if evento.type == pygame.KEYUP:
                estado_do_jogo = DONE

        # A cada loop, redesenha o fundo e os sprites
        JANELA.blit(img_vitoria_final, (0, 0)) #imagem com o escrito "para recomeçar, pressione qualquer tecla"


        # Depois de desenhar tudo, inverte o display.??????
        pygame.display.flip() 

    return estado_do_jogo