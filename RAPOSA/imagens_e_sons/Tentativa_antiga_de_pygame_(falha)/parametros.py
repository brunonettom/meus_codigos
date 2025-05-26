import pygame
from math import *
import os
from sprites_e_classes import objeto, persona


pygame.mixer.init()
pygame.init()

FPS = 60 # Frames por segundo

velocidade_de_rotaca_p_frame = radians(1) # do personagem, ao cair

JANELA = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Fox, a Raposa')

####TAMANHOS 

# TAMANHO DA LINHA E COLUNA
TAMANHO_LINHA_E_COLUNA = 3

#JANELA
LARGURA_JANELA = 1000 # Largura da tela - A DEFINIR
ALTURA_JANELA =  600# Altura da tela - A DEFINIR

#FUNDO
LARGURA_FUNDO = LARGURA_JANELA
ALTURA_FUNDO = LARGURA_JANELA 

#ESPINHOS
LARGURA_ESPINHOS = TAMANHO_LINHA_E_COLUNA #A DEFINIR
ALTURA_ESPINHOS = TAMANHO_LINHA_E_COLUNA #A DEFINIR

#JOGADOR
ALTURA_JOGADOR= TAMANHO_LINHA_E_COLUNA #A DEFINIR
LARGURA_JOGADOR = TAMANHO_LINHA_E_COLUNA #A DEFINIR

#PLATAFORMA
ALTURA_PLATAFORMA = TAMANHO_LINHA_E_COLUNA #A DEFINIR
LARGURA_PLATAFORMA = TAMANHO_LINHA_E_COLUNA #A DEFINIR

#MOEDA
ALTURA_MOEDA = TAMANHO_LINHA_E_COLUNA
LARGURA_MOEDA = TAMANHO_LINHA_E_COLUNA


#CORAÇÕES
LARGURA_CORACAO = TAMANHO_LINHA_E_COLUNA
ALTURA_CORACAO = TAMANHO_LINHA_E_COLUNA

#LINHA DE CHEGADA
ALTURA_CHEGADA = TAMANHO_LINHA_E_COLUNA
LARGURA_CHEGADA = TAMANHO_LINHA_E_COLUNA

########TELAS
#VITORIA
ALTURA_VITORIA = ALTURA_JANELA
LARGURA_VITORIA = LARGURA_JANELA

#VITORIA FINAL
ALTURA_VITORIA_FINAL = ALTURA_JANELA
LARGURA_VITORIA_FINAL = LARGURA_JANELA

#IMAGEM DA TELA INCIAL
LARGURA_INICIO = LARGURA_JANELA
ALTURA_INICIO = ALTURA_JANELA

#IMAGEM DA TELA FINAL
LARGURA_FINAL = LARGURA_JANELA
ALTURA_FINAL = ALTURA_JANELA


clock = pygame.time.Clock()
FPS = 60

# Estabelecer as figuras
img_personagem = pygame.image.load('imagens_e_sons/imagens/garoto/garoto_parado/Idle (1).png').convert_alpha()
img_fundo = pygame.image.load('imagens_e_sons/fundo/Fundo_jogo.jpg').convert_alpha() #O FUNDO SERÁ UMA ANIMAÇÃO
img_plataformas = pygame.image.load('imagens_e_sons/imagens/plataforma.png').convert_alpha()
img_moeda = pygame.image.load('imagens_e_sons/imagens/moeda.png').convert_alpha()
img_espinhos = pygame.image.load('imagens_e_sons/imagens/espinho.png').convert_alpha()
img_coracoes = pygame.image.load('imagens_e_sons/imagens/coracao.png').convert_alpha()   #de vida faltante
img_inicio = pygame.image.load('imagens_e_sons/imagens/inicio.png').convert_alpha() #tela inicial 

img_chegada = pygame.image.load('imagens_e_sons/imagens/portal.png').convert_alpha() #linha de chegada/porta/portal ... = objetivo final da fase
img_vitoria = pygame.image.load('imagens_e_sons/imagens/vitoria.webp').convert_alpha()    #tela do parabens, voce passou de fase
img_vitoria_final = pygame.image.load('imagens_e_sons/imagens/final.jpg').convert_alpha()    #tela de parabens, voce concluiu o jogo

#REDIMENSIONANDO AS FIGURAS
#redimensionando as imagens
#image = pygame.transform.scale(image, (125, 166)) para obter uma nova imagem de 125 X 166 pixels.
img_fundo = pygame.transform.scale(img_fundo, (LARGURA_FUNDO, ALTURA_FUNDO)) #O FUNDO SERÁ UMA ANIMAÇÃO
#img_personagem = pygame.transform.scale(img_personagem, (LARGURA_JOGADOR, ALTURA_JOGADOR))
img_plataformas = pygame.transform.scale(img_plataformas, (LARGURA_PLATAFORMA, ALTURA_PLATAFORMA))
img_moeda = pygame.transform.scale(img_moeda, (LARGURA_MOEDA, ALTURA_MOEDA))
img_espinhos = pygame.transform.scale(img_espinhos, (LARGURA_ESPINHOS, ALTURA_ESPINHOS))
img_inicio =  pygame.transform.scale(img_inicio, (LARGURA_INICIO, ALTURA_INICIO))  #tela inicial

img_chegada = pygame.transform.scale(img_chegada, (LARGURA_CHEGADA, ALTURA_CHEGADA)) #linha de chegada
img_vitoria = pygame.transform.scale(img_vitoria, (LARGURA_VITORIA, ALTURA_VITORIA)) #tela de vitoria - pode passar para a proxima fase
img_vitoria_final = pygame.transform.scale(img_vitoria_final, (LARGURA_VITORIA_FINAL, ALTURA_VITORIA_FINAL)) #ultima tela de vitoria
img_coracoes = pygame.transform.scale(img_coracoes, (LARGURA_CORACAO, ALTURA_CORACAO)) #imagem dos coracoes de vida do personagem
#TEXTO
fonte_pontos =  pygame.font.Font('imagens_e_sons/imagens/pontos.ttf', 28) #como sera o marcador de pontos


#ESTABELECER OS SONS
som_fundo = pygame.mixer.music.load('imagens_e_sons/sons/som_de_fundo.mp3') #Fonte: https://youtu.be/dDOfzfifwGE?si=GfIuDBJCHU0t26uN

som_caindo = pygame.mixer.Sound('imagens_e_sons/sons/caindo.mp3')

#Falta esses aqui
som_pegando_moedas = pygame.mixer.Sound('imagens_e_sons/sons/coin.mp3') #Fonte: https://pixabay.com/pt/sound-effects/search/game%20coin/
som_caido = pygame.mixer.Sound('imagens_e_sons/sons/caindo.mp3') #quando o cara cai no chao, de fato
som_morrendo = pygame.mixer.Sound('imagens_e_sons/sons/morrendo.mp3') #Fonte: https://pixabay.com/pt/sound-effects/search/dead/
som_game_over =pygame.mixer.Sound('imagens_e_sons/sons/game_over.mp3') #acaba as vidas #Fonte: https://pixabay.com/pt/sound-effects/search/game%20over/
#som_perdendo_vida =  pygame.mixer.music.load('imagens_e_sons/sons/perdendo_vida.ogg') 
som_vitoria =  pygame.mixer.Sound('imagens_e_sons/sons/vitoria.mp3') #quando passa de fase #Fonte: https://pixabay.com/pt/sound-effects/search/win/

#POSIÇÃO INICIAL DO JOGADOR - A DEFINIR
x_meio_inicial_do_personagem = 32
y_peh_inicial_do_personagem = 23


# CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)



#ORIENTAÇÕES
de_peh = radians(0)
de_ponta_cabeca = radians(180)
virado_para_a_esquerda = radians(90)
virado_para_a_direita = radians(270)



# Estados para controle do fluxo da aplicação
GAME_OVER  = 0
JOGANDO = 1
MORRENDO = 2
DONE = 3
INICIO = 4
VITORIA = 5
VITORIA_FINAL = 6


####################******************ANIMAÇÕES - PRO GRAND FINALE
anim_morrendo = []
morrendo = 0
arquivo_morrendo = 'imagens_e_sons/imagens/garoto/garoto_morrendo'
for i in range(15):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(arquivo_morrendo, f'Dead ({i+1}).png')
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (LARGURA_JOGADOR, ALTURA_JOGADOR))
        anim_morrendo.append(img)

parado = 1
anim_parado = []
arquivo_parado = 'imagens_e_sons/imagens/garoto/garoto_parado'
for i in range(15):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(arquivo_parado, f'Idle ({i+1}).png')
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (LARGURA_JOGADOR, ALTURA_JOGADOR))
        anim_parado.append(img)

pulando= 2
anim_pulando = []
arquivo_pulando = 'imagens_e_sons/imagens/garoto/garoto_pulando'
for i in range(15):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(arquivo_pulando, f'Jump ({i+1}).png')
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (LARGURA_JOGADOR, ALTURA_JOGADOR))
        anim_parado.append(img)




#########################################################CENÁRIO FASE 1 ###################################################

import sprites_e_classes
F1 = {}

#OBJETOS - ISSO PODE INCLUIR PAREDES E OUTROS
F1['objetos']= pygame.sprite.Group() 

#PLATAFORMAS - POSIÇÕES E IMAGEM (E TAMANHO) A DEFINIR
F1['plataformas'] = pygame.sprite.Group()


#ESPINHOS - POSIÇÕES E IMAGEM (E TAMANHO) A DEFINIR)
F1['espinhos'] = pygame.sprite.Group()

#QUANTAS GALINHAS A RAPOSA PEGOU
F1['pontos'] = 0

F1['galinhas minimas'] = 5  #o minimo de galinhas que a pessoa tem que pegar para poder mudar de fase


#MOEDAS - POSIÇÕES E IMAGEM (E TAMANHO) A DEFINIR
F1['moedas'] = pygame.sprite.Group()


F1['all_sprites'] = pygame.sprite.Group()


