import pygame
pygame.init()

from parametros import *
from PARTE_PRINCIPAL import *



'''
    def cooldown(self):
        agora = pygame.time.get_ticks()

        delta_pulo = agora - ultimo_pulo
        if delta_pulo > 50:
            pular(botao)
    '''

class persona (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,linha,coluna)

        
        self.orientacao = de_peh

        self.i = 0
        self.tempo_ult_img = pygame.time.get_ticks()

        self.estado = parado
        

        self.imagem = pygame.transform.rotate(anim_parado[0], self.orientacao)
        self.mascara = pygame.mask.from_surface(self.imagem)
        self.rect = self.imagem.get_rect()
        
        #ESTADO INICIAL DO PERSONAGEM - POSIÇÃO E PARADO
        self.rect.centerx =coluna
        self.rect.bottom = linha
        self.velocidadex = 0
        self.velocidadey = 0

        self.lista_estados = []

    def update(self): #MOVIMENTO - VELOCIDADE À DEFINIR
        #atualizando a posição do player
        
        #MOVIMENTANDO O PERSONAGEM
        self.rect.x += self.velocidadex
        self.rect.y += self.velocidadey


        #ESTÁ PARADO
        if self.velocidadex == 0 and self.velocidadey == 0:
            self.estado = parado
            self.lista_estados.append(self.estado)
        if self.estado == parado:
            self.imagem = pygame.transform.rotate(anim_parado[sef(self.i)], self.orientacao)  
            self.mascara = pygame.mask.from_surface(self.imagem)

        if int(self.i) == len(anim_parado):
            self.i = 0
        

        #ESTÁ PULANDO
        if self.velocidadex != 0 or self.velocidadex != 0:
            self.estado = pulando
            self.lista_estados.append(self.estado)
        if self.estado == pulando:
            self.imagem = pygame.transform.rotate(anim_parado[int(self.i)], self.orientacao) 
            self.mascara = pygame.mask.from_surface(self.imagem)
            
        if int(self.i) == len(anim_pulando):
            self.i = 0

        
        if self.estado != self.lista_estados[len(self.lista_estados)-1]:
            self.i = 0

        #dentro da tela - desacelerando e mantendo dentro da tela - NO FUTURO, DEVO FAZER O MESMO PARA QUANDO O PERSONAGEM COLIDIR COM AS PAREDES
        if self.rect.right >= LARGURA_JANELA:
            self.velocidadex = 0
            self.rect.right = LARGURA_JANELA
        if self.rect.left <= 0:
            self.velocidadex = 0
            self.rect.left = 0
        if self.rect.top <= 0:
            self.velocidadey = 0
            self.rect.top = 0
        if self.rect.bottom >= ALTURA_JANELA:
            self.rect.bottom = ALTURA_JANELA
            self.velocidadey = 0



class objeto:
    def __init__(self, fila, coluna, imagem, orientacao):
        
        self.imagem = pygame.transform.rotate(imagem,orientacao)
        self.rect = self.imagem.get_rect()
        self.rect.x = fila
        self.rect.y = coluna
        x_original = fila
        y_original = coluna



#class morrendo(pygame.sprite.Sprite):
    # Construtor da classe.
    #def __init__(self, center):


#SPRITE  - MORRENDO
class sprite_morrendo(pygame.sprite.Sprite):    #vai gerar a animação do personagem

    def __init__(self, centro):
        pygame.sprite.Sprite.__init__(self)

        # ATUALIZANDO A ANIMAÇÃO DO PERSONAGEM MORRENDO
        self.anim_morrendo = anim_morrendo

        
        self.frame = 0  #NUMERANDO O PRIMEIRO FRAME - SE ATUALIZARÁ
        self.imagem = pygame.transform.rotate(self.anim_morrendo[0], self.orientacao)   #SELECIONANDO O ARQUIVO DA ANIMAÇÃO CORRESPONDENTE AO FRAME E
        #ACRESCENTANDO A ROTACAO
        
        #ATUALIZANDO A POSIÇÃO
        self.rect = self.image.get_rect()
        self.rect.centro = centro # O CENTRO SERÁ DADO QUANDO A CLASSE FOR EVOCADO
        
        
        self.ultimo_update = pygame.time.get_ticks() #QUANDO A PRIMEIRA IMAGEM FOI MOSTRADA

        self.espera = 50 #AGUARDO ENTRE UM FRAME E O PRÓXIMO


    def update(self):
        
        agora = pygame.time.get_ticks() #ve a posicao atual
        
        
        tempo_decorrido = agora - self.ultimo_update #tempo decorrido desde a ultima mudanca de frame

        # Se já está na hora de mudar de imagem...
        if tempo_decorrido > self.espera: #se o tempo que passou for maior que o tempo de espera 
            
            self.ultimo_update = agora # atualiza o ultimo update para agora

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            
            if self.frame == len(self.anim_morrendo): #se acabar a animacao ele morre

                self.kill()
            else:
                # troca de imagem se n terminou a animacao
                centro = self.rect.centro
                self.imagem = self.anim_morrendo[self.frame] 
                self.rect = self.image.get_rect()
                self.rect.centro = centro