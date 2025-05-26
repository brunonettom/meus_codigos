import pygame
import os
from math import *
import pygame
import random

pygame.init()
pygame.mixer.init()

#ESTABELECER OS SONS
pygame.mixer.music.load('imagens_e_sons/sons/som_de_fundo.mp3') #Fonte: https://youtu.be/dDOfzfifwGE?si=GfIuDBJCHU0t26uN
pygame.mixer.music.set_volume(0.6)

###########################################################JOGO#################################################

# CRIANDO A JANELA - PARTE PRINCIPAL
JANELA = pygame.display.set_mode((1000, 500))
pygame.display.set_caption('Fox, a Raposa')


# ESTADOS - JOGANDO
GAME_OVER  = 0
JOGANDO = 1
MORRENDO = 2
DONE = 3
INICIO = 4
VITORIA = 5


############################################# PARAMETROS - NÃO IMPORTA NADA

FPS = 60 # Frames por segundo

velocidade_de_rotaca_p_frame = radians(1) # do personagem, ao cair



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
FPS = 30

# Estabelecer as figuras
img_personagem = pygame.image.load('imagens_e_sons/imagens/garoto/garoto_parado/Idle (1).png').convert_alpha()
img_fundo = pygame.image.load('imagens_e_sons/fundo/Fundo_jogo.jpg').convert_alpha() #O FUNDO SERÁ UMA ANIMAÇÃO
img_plataformas = pygame.image.load('imagens_e_sons/imagens/plataforma.png').convert_alpha()
img_moeda = pygame.image.load('imagens_e_sons/imagens/moeda.png').convert_alpha()
img_espinhos = pygame.image.load('imagens_e_sons/imagens/espinho.png').convert_alpha()
img_coracoes = pygame.image.load('imagens_e_sons/imagens/coracao.png').convert_alpha()   #de vida faltante
img_inicio = pygame.image.load('imagens_e_sons/imagens/inicio.png').convert_alpha() #tela inicial 
img_fim = pygame.image.load('imagens_e_sons/imagens/fim.png').convert_alpha()    #tela do game over
img_chegada = pygame.image.load('imagens_e_sons/imagens/portal.png').convert_alpha() #linha de chegada/porta/portal ... = objetivo final da fase
img_vitoria = pygame.image.load('imagens_e_sons/imagens/vitoria.webp').convert_alpha()    #tela do parabens, voce passou de fase
img_vitoria_final = pygame.image.load('imagens_e_sons/imagens/vitoria.webp').convert_alpha()    #tela de parabens, voce concluiu o jogo

#REDIMENSIONANDO AS FIGURAS
#redimensionando as imagens
#image = pygame.transform.scale(image, (125, 166)) para obter uma nova imagem de 125 X 166 pixels.
img_fundo = pygame.transform.scale(img_fundo, (LARGURA_FUNDO, ALTURA_FUNDO)) #O FUNDO SERÁ UMA ANIMAÇÃO
#img_personagem = pygame.transform.scale(img_personagem, (LARGURA_JOGADOR, ALTURA_JOGADOR))
img_plataformas = pygame.transform.scale(img_plataformas, (LARGURA_PLATAFORMA, ALTURA_PLATAFORMA))
img_moeda = pygame.transform.scale(img_moeda, (LARGURA_MOEDA, ALTURA_MOEDA))
img_espinhos = pygame.transform.scale(img_espinhos, (LARGURA_ESPINHOS, ALTURA_ESPINHOS))
img_inicio =  pygame.transform.scale(img_inicio, (LARGURA_INICIO, ALTURA_INICIO))  #tela inicial
img_fim =  pygame.transform.scale(img_fim, (LARGURA_FINAL, ALTURA_FINAL)) #tela final
img_chegada = pygame.transform.scale(img_chegada, (LARGURA_CHEGADA, ALTURA_CHEGADA)) #linha de chegada
img_vitoria = pygame.transform.scale(img_vitoria, (LARGURA_VITORIA, ALTURA_VITORIA)) #tela de vitoria - pode passar para a proxima fase
img_vitoria_final = pygame.transform.scale(img_vitoria_final, (LARGURA_VITORIA_FINAL, ALTURA_VITORIA_FINAL)) #ultima tela de vitoria
img_coracoes = pygame.transform.scale(img_coracoes, (LARGURA_CORACAO, ALTURA_CORACAO)) #imagem dos coracoes de vida do personagem
#TEXTO
fonte_pontos =  pygame.font.Font('imagens_e_sons/imagens/pontos.ttf', 28) #como sera o marcador de pontos - DEFINIR O TAMANHO



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

############################################# QUASE FIM DOS PARAMETROS - FALTA OS DICIONARIOS PARA AS FASES





################################### MAPA ######################################3            NÃO DEPENDE DE NINGUÉM

B = 0 #bloco
P = 0 #preenchimento
L = 0 #limite da tela

# os valores anteriores são iguais, para, caso queiramos colocar uma nova imagem para cada um dos elementos, não seja tão complicado
V = 1 #espaço vazio
EE = 2 #espinho virado para a esquerda
ED = 2 #espinho virado para a direita
EB = 2 #espinho virado para baixo
EC = 2 #espinho virado para cima
R = 6 #posição inicial do personagem
O = 7 #ponto de chegada
#M = 8 #moeda --> galinha
M = 8

MAPA_3 =[
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],
    [ED,V,V,V,M,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,M,V,V,V,V,V,V,V,V,EE],
    [L,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,O,L],
    [L,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,B,V,V,B,B,B,B,B,B,L],
    [L,V,V,B,V,V,V,V,V,V,V,M,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,B,V,V,B,B,B,B,B,B,B,B,B,B,B,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,B,B,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,M,B,V,V,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,B,B,B,B,B,B,V,V,V,B,P,P,P,P,P,L],
    [L,V,V,R,V,V,V,M,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,L],
    [L,B,B,B,EC,EC,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,L],
    [P,P,P,P,P,P,P,P,B,EC,EC,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,L],
    [P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L],
    [P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L]]

#Legenda Bara localização
#O = linha de chegada
#V= VAZIO
#b = BlOco
#ec =  espinho Bara cima
#eB - espinho Bara baixo
#ed = espinho Bara direita


MAPA_2= [
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,O,L],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,M,L],
    [L,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,B,B,L],
    [ED,V,V,V,V,V,V,V,V,V,V,V,V,V,M,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L],
    [L,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,B,V,V,B,P,P,L],
    [L,V,V,B,B,B,B,B,EB,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,P,P,L],
    [L,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L],
    [L,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L],
    [L,V,V,B,V,V,V,B,V,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,B,V,V,B,P,P,L],
    [L,V,V,B,B,B,B,B,V,V,V,V,B,V,V,V,V,V,V,V,V,M,B,B,B,V,B,V,V,B,P,P,L],
    [L,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,P,P,L],
    [L,V,V,V,V,V,R,V,V,B,V,M,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,P,P,L],
    [L,B,B,B,B,B,B,B,B,P,B,B,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,P,P,L],
    [L,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,L],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,EC,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L]]

MAPA_1=[
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L],
    [L,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L],
    [L,O,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,L],
    [L,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,L],
    [L,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,V,V,V,V,V,V,V,L],
    [L,B,B,B,B,B,P,P,P,P,P,P,P,P,P,P,P,P,P,B,V,V,V,V,V,M,V,V,V,V,V,V,L],
    [ED,V,V,V,V,M,B,V,V,V,B,B,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,B,B,L],
    [L,V,V,V,V,V,B,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,P,P,P,P,L],
    [L,V,V,B,B,B,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,B,B,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,P,P,P,P,P,P,L],
    [L,V,V,B,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,P,P,P,P,P,P,L],
    [L,V,V,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,P,P,P,P,P,P,L],
    [L,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L],
    [L,V,V,R,V,V,V,V,V,V,V,V,V,V,V,M,V,B,P,P,P,P,P,P,P,P,P,P,P,P,P,P,L],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L]]






"""
MAPA_MODELO = [
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,L],
    [L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L,L]]
"""



############################################ FIM DO MAPA                -  NÃO DEPENDE DE NINGUÉM 






############################################# TELA0_DE_DERROTA_E_VITORIA #####################
def tela_inicial(JANELA):
    pygame.mixer.music.play(loops=-1)
    # Carrega o fundo da tela inicial
    estado_do_jogo = INICIO
    while estado_do_jogo == INICIO:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)                                                            #CHAMA O FPS - FEITO

        # Processa os eventos (mouse, teclado, botão, etc).
        for evento in pygame.event.get():
            # Verifica se foi fechado.
            if evento.type == pygame.QUIT:
                pygame.quit()
            #0 = game over, congrats;   1 - fecha; 2,3,5 - congrats, 4 - nao fecha 
            if evento.type == pygame.KEYUP:
                estado_do_jogo = JOGANDO

        # A cada loop, redesenha o fundo e os sprites
        JANELA.blit(img_inicio, (0, 0)) #imagem com o escrito "para recomeçar, pressione qualquer tecla"             - CHAMA A IMG_INICIO - FEITO


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


class objeto:                                                             #SPRITES_E_CLASSES
    def __init__(self, fila, coluna, imagem, orientacao):
        
        self.imagem = pygame.transform.rotate(imagem,orientacao)
        self.rect = self.imagem.get_rect()
        self.rect.x = fila
        self.rect.y = coluna
        x_original = fila
        y_original = coluna

######################################################### CENÁRIO FASE 1 ###################################################    SPRITES_E_CLASSES


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

F1['blocos'] = pygame.sprite.Group()

#MOEDAS - POSIÇÕES E IMAGEM (E TAMANHO) A DEFINIR
F1['moedas'] = pygame.sprite.Group()


F1['all_sprites'] = pygame.sprite.Group()

################################################ FIM DO CENÁRIO 1 - PARAMETROS


class persona (pygame.sprite.Sprite):                  ###############################################SPRITES_E_CLASSES
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,linha,coluna)             #SERÁ DADO QUANDO FOR EVOCADO

        
        self.orientacao = de_peh

        self.i = 0
        self.tempo_ult_img = pygame.time.get_ticks()

        self.estado = parado
        

        self.imagem = pygame.transform.rotate(anim_parado[0], self.orientacao)
        self.mascara = pygame.mask.from_surface(self.imagem)
        self.rect = self.imagem.get_rect()
        
        #ESTADO INICIAL DO PERSONAGEM - POSIÇÃO E PARADO
        posicao_inicial_x = coluna 
        posicao_inicial_y = linha
        self.rect.centerx = coluna
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
            self.imagem = pygame.transform.rotate(anim_parado[int(self.i)], self.orientacao)  
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

###SPRITE_E_CLASSES
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


################################################################# JOGANDO ###############################################
def jogando(JANELA, MAPA, F):
    cronometro = pygame.time.Clock()
    #chamando o personagem
    
    #CRIANDO O MAPA
    for linha in range(len(MAPA)):                                                                   ### QUANDO O JOGANDO FOR CHAMADO, O MAPA JÁ TERÁ SIDO DEFINIDO
        for coluna in range(len(MAPA)):
                elemento = MAPA[linha] [coluna]
                linha *= TAMANHO_LINHA_E_COLUNA
                coluna *= TAMANHO_LINHA_E_COLUNA
                if elemento == B or elemento == L or elemento == P:
                        imagem = img_plataformas
                        orientacao = de_peh
                        bloco = objeto(linha,coluna, imagem, orientacao)                            ### CHAMA A CLASSE OBJETO()  - FEITO
                        F['plataformas'].add(bloco)                                                 # CHAMA O DICIONARIO F1, P EX - DIC F1 - FEITO
                        F['blocos'].add(bloco)                                                      #O VALOR DO F - será determinado ainda - no principal
                        F['objetos'].add(bloco)
                        F['all_sprites'].add(bloco)
                
                if elemento == M:
                        imagem = img_moeda
                        orientacao = de_peh
                        moeda = objeto(linha,coluna, imagem, orientacao)
                        F['moedas'].add(moeda)
                        F['all_sprites'].add(moeda)
                        F['objetos'].add(moeda)
                        
                
                if elemento == EE:
                        imagem = img_espinhos
                        orientacao = virado_para_a_esquerda
                        espinho = objeto(linha, coluna, imagem, orientacao)
                        F['objetos'].add(espinho)
                        F['all_sprites'].add(espinho)
                        F['espinhos'].add(espinho)
                
                if elemento == ED:
                        imagem = img_espinhos
                        orientacao = virado_para_a_direita
                        espinho = objeto(linha, coluna, imagem, orientacao)
                        F['objetos'].add(espinho)
                        F['all_sprites'].add(espinho)
                        F['espinhos'].add(espinho)
                
                if elemento == EC:
                        imagem = img_espinhos
                        orientacao = de_peh
                        espinho = objeto(linha, coluna, imagem, orientacao)                            #objeto - FEITO
                        F['objetos'].add(espinho)
                        F['all_sprites'].add(espinho)
                        F['espinhos'].add(espinho)
                
                if elemento == EB:
                        imagem = img_espinhos
                        orientacao = de_ponta_cabeca
                        espinho = objeto(linha, coluna, imagem, orientacao)
                        F['objetos'].add(espinho)
                        F['all_sprites'].add(espinho)
                        F['espinhos'].add(espinho)
                
                if elemento == R:
                        personagem = persona(linha, coluna)                                           #persona - FEITO 
                        F['all_sprites'].add(personagem)
                
                if elemento == O:
                        imagem = img_chegada
                        orientacao = de_peh

                        objetivo = objeto(linha, coluna, imagem, orientacao)
                        F['objetos'].add(objetivo)
                        F['all_sprites'].add(objetivo)

    

    personagem.i = 0 #essa contagem, posteriormente será utilizada para a animação do personagem                  #EVOCAÇÃO DO SPRITE DO PERSONAGEM - FEITO

    

    keys_down = {}

    
    estado_do_jogo = JOGANDO
    
    #FAZENDO O MAPA
    for fila in range(len(MAPA)):                                                                                   #O MAPA EM SI - FEITO
        for coluna in range(len(MAPA[fila])):
            tipo_bloco = MAPA[fila][coluna]
            if tipo_bloco == B:                                                                                      #OS MAPAS, EM SI - DEVE SER MOSTRADO MAIS À FRENTE
                bloco = objeto(fila, coluna, img_plataformas, de_peh)                                                #O SIGNIFICADO DE CADA ORIENTACAO - FEITO
                F['all_sprites'].add(bloco)
                F['blocos'].add(bloco)
            elif tipo_bloco == M:
                bloco = objeto(fila, coluna, img_moeda, 0)
                F['all_sprites'].add(bloco)
                F['blocos'].add(bloco)
            
            elif tipo_bloco == EE:
                bloco = objeto(fila, coluna, img_espinhos, 0)
                F['all_sprites'].add(bloco)
                F['blocos'].add(bloco)
                

    F['all_sprites'].add(personagem) # ADICIONANDO O PERSONAGEM
    F['vidas'] = 3 #NUMERO DE VIDAS NO INICIO DA FASE




    
    
    while estado_do_jogo == INICIO:
        clock.tick(FPS) #INTERVALO ENTRE CADA FRAME
        
        #EVENTOS

        for event in pygame.event.get():
            #APERTOU NO X DE SAIR:
            if event.type == pygame.QUIT:
                estado_do_jogo = DONE
            
            #MOVIMENTANDO O PERSONAGEM
            if estado_do_jogo == JOGANDO:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # DEPENDENDO DA TECLA E SE ALGUM OUTRO MOVIMENTO JÁ ESTÁ ACONTECENDO
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a and personagem.velocidadey == 0 :
                        personagem.velocidadex -= 8
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d and personagem.velocidadey == 0 :
                        personagem.velocidadex += 8
                    if event.key == pygame.K_UP or event.key == pygame.K_w and personagem.velocidadex == 0 :
                        personagem.velocidadey -= 8
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s and personagem.velocidadex == 0 :
                        personagem.velocidadey +=8


        #ROTACIONANDO EM RELAÇÃO AO SEU MOVIMENTO - ***CALIBRAR A VELO DISSO
        if personagem.velocidadey>0 and personagem.orientacao != de_peh:    
            personagem.orientacao += velocidade_de_rotaca_p_frame
        
        if personagem.velocidadey<0 and personagem.orientacao != de_ponta_cabeca:
            personagem.orientacao -= velocidade_de_rotaca_p_frame
        
        if personagem.velocidadex >0 and personagem.orientacao != virado_para_a_direita:
            personagem.orientacao +=velocidade_de_rotaca_p_frame
        
        if personagem.velocidadex<0 and personagem.orientacao != virado_para_a_esquerda:
            personagem.orientacao -= velocidade_de_rotaca_p_frame

        
        F['all_sprites'].update()


        if estado_do_jogo == JOGANDO:

            #RESPONDENDO ÀS COLISÕES COM AS PLATAFORMAS
            colisoes_plataformas = pygame.sprite.spritecollide(personagem, F['plataformas'], False, pygame.sprite.collide_mask)
            if colisoes_plataformas:
                if personagem.velocidadex !=0:
                    personagem.velocidadex = 0  # para o jogador
                elif personagem.velocidadey !=0:
                    personagem.velocidadey = 0  # para o jogador
                som_caido.play()

            #COLISOES COM MOEDAS
            colisoes_moedas = pygame.sprite.spritecollide(personagem, F['moedas'], True, pygame.sprite.collide_mask) #MOSTRA SE HOUVERAM COLISÕES
            
            if colisoes_moedas: #CASO TENHAM HAVIDO
                
                F['pontos'] += 1 #ADICIONA UM PONTO 
                som_pegando_moedas.play() #SOM
        

            #COLISÃO COM OS ESPINHOS
            colisoes_espinhos = pygame.sprite.spritecollide(personagem, F['espinhos'], False, pygame.sprite.collide_mask) #MOSTRA SE HOUVERAM COLISÕES
            if colisoes_espinhos:        
                
                som_morrendo.play() #SOM
                personagem.kill() #TIRA O PERSONAGEM DA TELA (SERÁ SUBSTITUIDO POR UMA ANIMAÇÃO DELE MORRENDO)
                F['vidas'] -= 1 #PERDE 1 DAS 3 VIDAS
                morte = sprite_morrendo(personagem.rect.center)                                                            #SPRITE_MORRENDO - FEITO

                F['all_sprites'].add(morte) #ADICIONA A ANIMAÇÃO DELE MORRENDO
                keys_down = {}           #LIMPA O DICIONARIO DOS BOTÕES PRESSIONADOS
                estado_do_jogo = MORRENDO #ATUALIZA O ESTADO DO JOGO
                hora_da_morte = pygame.time.Clock() 
                duracao_da_morte = morrendo.espera * len(morrendo.anim_morrendo) + 400

            
            #COLISAO COM A CHEGADA
            colisao_chegada = pygame.sprite.spritecollide(personagem, F['chegada'], False, pygame.sprite.collide_mask) #MOSTRA SE HOUVERAM COLISÕES
            if colisao_chegada and F['pontos'] == F['galinhas minimas']: #SOMENTE SE A PESSOA COLETOU TODAS AS GALINHAS QUE ELE PODE PROSSEGUIR
                som_vitoria.play()
                estado_do_jogo = VITORIA #ATUALIZA O ESTADO DO JOGO

            
            personagem.i += 1/50 #MUDANDO A IMAGEM DO PERSONAGEM QUE SERÁ EXIBIDA


        elif estado_do_jogo == MORRENDO: #INDO PRA TELA DA MORTE
            agora = pygame.time.get_ticks()

            if agora - hora_da_morte > duracao_da_morte: #AVALIANDO SE A ANIMAÇÃO DO PERSONAGEM MORRENDO JÁ ACABOU
                if F['vidas'] == 0:
                    estado_do_jogo = GAME_OVER   #A PESSOA MORREU E NÃO TEM MAIS VIDAS
                else: 
                    estado_do_jogo = JOGANDO #O JOGO CONTINUA, PORQUE A PESSOA AINDA TEM VIDAS
                    personagem = persona(persona.posicao_inicial_x, persona.posicao_inicial_y) #CONVOCA O PERSONAGEM NAS CONFIGURAÇÕES INICIAIS
                    F['vidas']-=1 #TIRA UMA VIDA 
                    F['all_sprites'].add(personagem) #ADICIONA O PERSONAGEM DE VOLTA NO JOGO

                    #resetar_moedas(F['moedas'])  #ISSO ESTÁ ESCRITO EM PARAMETROS, QUANDO EU DEFINO OS DICIONARIOS DAS FASES


        #GERANDO SAIDAS
        JANELA.fill(PRETO) 
        JANELA.blit(img_fundo,(0,0)) #COLOCA O FUNDO

        F['all_sprites'].draw(JANELA) #POEM OS SPRITES NA TELA

        #PONTUAÇÃO
        perfil_texto = fonte_pontos.render("{:.0f}/{:.0f}".format(F['pontos'], F['galinhas minimas']), True, AMARELO)  #diz quantas de quantas galinhas a pessoa já pegou     
        texto_rect = perfil_texto.get_rect() 
        texto_rect.midtop = (LARGURA_JANELA / 2,  10) #posiciona o texto
        JANELA.blit(perfil_texto, texto_rect) #coloca o texto na tela

        #VIDAS
        perfil_texto = fonte_pontos.render(chr(9829) * F['vidas'] , True, VERMELHO) #faz o coração
        texto_rect = perfil_texto.get_rect() 
        texto_rect.bottomleft = (10, ALTURA_JANELA - 10) #posiciona o texto
        JANELA.blit(perfil_texto, texto_rect) #coloca o texto na tela


        pygame.display.update()
        return estado_do_jogo

############################## FIM DO JOGANDO ############################################33








# pylint: disable=no-member

####################################################### PARTE PRINCIPAL


###############CRIANDO AS PLATAFORMAS

estado_do_jogo = GAME_OVER
FASE = 1

#iniciando o loop dos estados

while estado_do_jogo != DONE:
    FASE = 1
    pontos = 0
    ultimo_pulo = pygame.time.get_ticks()
    #analisa se o jogo foi fechado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            estado_do_jogo = DONE
    if estado_do_jogo == INICIO:
        estado_do_jogo = tela_inicial(JANELA)
    if estado_do_jogo == JOGANDO:        #FECHA NA HORA
            #DEFININDO O MAPA E OS DICIONÁRIOS A SEREM UTILIZADOS
        F = F1
        MAPA = MAPA_1
        
        if  FASE == 1:
            F = F1                                                   #PRECISA DO F1 - FEITO
            MAPA = MAPA_1                                            #PRECISA DO MAPA_1 - FEITO
        elif FASE == 2:
            F = F2                                                   #PRECISA DO F2
            MAPA = MAPA_2                                            #PRECISA DO MAPA_2 - FEITO
        elif FASE == 3:
            F = F3                                                   #PRECISA DO F3
            MAPA = MAPA_3                                            #PRECISA DO MAPA3 - FEITO
        
        estado_do_jogo = jogando(JANELA, MAPA, F)                             #PRECISA DO JOGANDO() - FEITO
    if estado_do_jogo == GAME_OVER:
        estado_do_jogo = tela_final(JANELA)                           #PRECISA DO TELA_FINAL() - FEITO
    if estado_do_jogo == VITORIA:
        FASE +=1
    if FASE!=4:
        estado_do_jogo = tela_de_vitoria(JANELA)                      #PRECISA DA TELA_DE_VITORIA()  - FEITO
    else:
        estado_do_jogo = fim_vitorioso(JANELA)                        #PRECISA DO FIM_VITORIOSO() - FEITO


#fecha a janela



game = True
"""

while game:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game = False


    window.fill((0, 71, 171)) 
    pygame.display.update()


pygame.quit()


"""

############################################# SPRITES_E_CLASSES ##################################################################
'''
    def cooldown(self):
        agora = pygame.time.get_ticks()

        delta_pulo = agora - ultimo_pulo
        if delta_pulo > 50:
            pular(botao)
    '''








#class morrendo(pygame.sprite.Sprite):
    # Construtor da classe.
    #def __init__(self, center):



#################################### FIM DOS SPRITES E CLASSES
