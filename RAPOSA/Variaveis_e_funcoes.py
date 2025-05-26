
#Chama todas as bibliotécas que serão usadas ao longo de todo o código
import pygame
import random
from os import path

#inicializa  o pygame
pygame.init()
#inicializa  o pygame mixer (parte que controla o som)
pygame.mixer.init()
pygame.init()

#define e inicializa a parte de joystick do pygame
if pygame.joystick.get_count() != 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controle conectado: {joystick.get_name()}")
        

#Define as variáveis que controlarão o jogo, 
jogando = 0
DONE = 1
inicio = 3
bonequinho = "Imagem"

#Define o relógio a ser usado durante todo o jogo
clock = pygame.time.Clock()

#Define a imagem de inicio, a famosa tela inicial
img_inicio = pygame.image.load('imagens_e_sons/imagens/inicio.png')#tela inicial 

#define qual será o título do jogo, muito criativo
TITULO = 'Fox, a raposa'

#Variáveis de dimensionamento da janela principal, largura e altura
largura = 1360
altura = 680 

#Define o tamanho dos azulejos do jogo (o piso)
tamanho_azulejo = 40

#define o tamanho do jogador, a nossa raposa, com relação ao tamanho do azulejo
largura_do_jogador = tamanho_azulejo
altura_do_jogador = int(tamanho_azulejo * 1)

#Define a taxa de frames do jogo
FPS = 60

#Define a cor preta
amarelo = (255,255,0)
preto = (0, 0, 0)
branco = (255,255,255)
vermelho = (200, 100, 100)

#define a velocidade no eixo x (esquerda e direita)
velocidade_no_eixo_x = 20

#Variáveis usadas na contrução do mapa
#A variável "B" define o que é um bloco
B = 1

#Define os espaços que ficarão vazios
V = 2

#Define onde estarão as galinhas que a raposa irá buscar
G = 3

#As próximas 5 variáveis vão definir o que é um espinho e para qual lado ele irá apontar
#ESPINHOS VIRADOS PARA: ED = DIREITA, EE = ESQUERDA, EB = BAIXO, EC = CIMA
ED = 4
EE = 5
EB = 6
EC = 7
E = 10 #espinho

#A variável "O" define o ponto final, uma espécie de portal pelo qual a raposa tenta chegar
O = 8

#O "R" vai definir em que parte do mapa a raposa irá ser gerada
R = 9

MAPAS = {}
#O mapa em si, em que cada variável acima é chamada e preeenche um espaço do mapa
#O mapa em si, em que cada variável acima é chamada e preeenche um espaço do mapa
MAPAS['MAPA1'] =  [
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B],
    [B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B],
    [B,O,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,G,V,V,V,V,V,V,B,B],
    [ED,V,V,V,V,G,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,V,V,V,V,V,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,B,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,B,B,B,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,B,B,B,B,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,B,V,V,V,V,G,B,B,B,B,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,V,V,R,V,V,V,V,V,V,V,V,V,V,V,G,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B]]

MAPAS['MAPA2'] = [
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,EB,B,B,B,B,B,B,B,V,V,V,V,V,O,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,B,B,B,V,V,V,V,V,G,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,G,B,B,B,B,V,V,B,B,B,B,B],
    [ED,V,V,V,V,V,V,V,V,V,V,V,V,V,G,B,B,B,G,V,V,V,B,B,B,B,B,V,V,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B,V,V,V,V,V,B,B,B,B,B,V,V,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B,B,B,B,V,V,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,EB,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,B,V,V,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,V,V,B,B,B,B,B],
    [B,V,V,B,B,B,B,B,V,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,B,V,V,B,B,B,B,B],
    [B,G,V,B,B,B,B,B,V,V,V,V,B,V,V,V,V,V,V,V,V,G,B,B,B,V,B,V,V,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,B,B,B,B],
    [B,V,V,V,V,V,R,V,V,V,V,G,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,V,V,V,B,V,V,V,B,B,B,B,V,V,V,B,B,B,B,V,V,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,EC,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B]]

MAPAS['MAPA3'] = [
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [ED,V,V,V,G,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,G,V,V,V,V,V,V,V,V,EE,B],
    [B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,O,B,B],
    [B,V,V,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,V,V,B,B,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,V,V,V,V,V,G,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,B,B,B,B,B,B,B,B,B,B,B,V,V,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,V,V,B,V,V,V,V,V,V,B,B,V,V,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,V,G,B,V,V,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,B,B,B,B,B,B,B,V,V,V,B,B,B,B,B,B,B,B],
    [B,V,V,R,V,V,V,G,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B,B,B,B,B,B,B],
    [B,B,B,B,EC,EC,B,B,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,EC,EC,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B]]


MAPAS['MAPA4'] = [
    [B,B,B,B,B,B,B,B,EB,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B,B],
    [B,V,V,V,V,V,V,V,V,B,V,G,V,V,V,B,V,V,V,V,EE,ED,V,V,V,V,V,V,V,B,V,O,V,B],
    [B,V,V,V,B,V,B,B,V,V,V,V,V,V,V,V,G,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,V,V,V,V,V,EE,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,V,V,V,V,V,B,B,V,V,EC,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,B],
    [B,R,V,V,V,B,V,V,V,V,B,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,EC,V,V,B,V,V,V,V,V,V,V,V,V,B,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,EB,V,V,V,V,V,V,V,V,V,EC,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,V,V,V,B,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,B],
    [B,V,V,V,V,EB,B,G,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,B],
    [B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,V,V,B,V,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,V,B],
    [B,V,V,V,V,V,V,V,B,V,V,V,V,V,B,V,V,V,V,V,EB,V,V,V,V,V,V,V,B,V,V,V,V,B],
    [B,V,V,V,V,V,B,V,V,V,V,V,V,V,B,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B],
    [B,B,V,V,V,V,V,B,V,V,V,B,V,V,ED,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,V,V,V,B],
    [ED,V,V,V,V,V,V,V,V,V,V,V,V,V,V,B,EC,V,V,V,V,V,V,V,B,V,V,V,V,V,V,V,V,E],
    [B,B,B,B,EC,EC,B,B,B,B,B,EC,B,EC,B,B,B,B,B,B,B,B,B,B,B,EC,B,B,B,B,B,B,B,B]]
#Estabelece as imagens a serem usadas
def bases_carregando(none):
    assets = {}
    assets[bonequinho] = pygame.image.load(path.join('imagens_e_sons/imagens/Walk_(1).png')).convert_alpha() #Fonte: https://grappe.itch.io/pixelportal
    assets["img_fundo"] = pygame.image.load('imagens_e_sons/imagens/Fundo_jogo.jpg').convert_alpha() #Fonte: https://pt.vecteezy.com/arte-vetorial/9877673-pixel-art-sky-background-with-clouds-cloudy-blue-sky-vector-for-8bit-game-on-white-background
    assets["plataformas"] = pygame.image.load('imagens_e_sons/imagens/plataforma.png').convert_alpha() #Fonte: https://www.pngwing.com/pt/free-png-czlvo
    assets[B] = pygame.image.load(path.join('imagens_e_sons/imagens/plataforma.png')).convert() #Fonte: https://www.pngwing.com/pt/free-png-czlvo
    assets[E] = pygame.image.load(path.join('imagens_e_sons/imagens/espinho.png')).convert_alpha() #Fonte: https://www.flaticon.com/br/icone-gratis/espinho_4139931
    assets[G] = pygame.image.load(path.join('imagens_e_sons/imagens/galinha.webp')).convert_alpha() #Fonte: https://br.freepik.com/vetores-premium/icone-de-pixel-art-de-frango-branco-passaro-do-pais-logotipo-de-animal-de-fazenda_23568997.htm
    assets[O] = pygame.image.load(path.join('imagens_e_sons/imagens/portal.png')).convert_alpha() #Fonte: https://www.artstation.com/marketplace/p/97xV/portal
    assets[R] = pygame.image.load(path.join('imagens_e_sons/imagens/Walk_(1).png')).convert_alpha() #Fonte: https://www.pngegg.com/pt/search?q=pixel+raposa
    assets["fonte_dos_pontos"] = pygame.font.Font('imagens_e_sons/imagens/PressStart2P.ttf', 28) #Fonte: https://www.pngegg.com/pt/search?
    assets['anim_raposa'] = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = f'imagens_e_sons/imagens/garoto/raposa_parada/Idle ({i+1}).png'
        img = pygame.image.load(path.join(f'imagens_e_sons/imagens/garoto/raposa_parada/Idle ({i+1}).png')).convert_alpha() 
        assets['anim_raposa'].append(img)
    return assets







#Cria a função 
class azulejo(pygame.sprite.Sprite):

    # Constrói a classe
    def __init__(self, foto_do_azulejo, filas, colunas):
        
        pygame.sprite.Sprite.__init__(self)

        #adicona a foto do azulejo a uma variável
        foto_do_azulejo = pygame.transform.scale(foto_do_azulejo, (tamanho_azulejo, tamanho_azulejo))

#Cria a variavel responável por determinar a quantidade de vidas que o jogador ainda tem 
vidas = 3

pode_passar = 200000000000000000000000
#Cuida do estado de jogo
jogando = 0
DONE = 1
morreu_de_vez = 2
morreu = 3
vitoria = 4
sim = 5
vivo = 6
INICIO = 7
#Marca o loop principal em que o jogo irá funcionar

estado_do_jogador = vivo

#ORIENTACAO
de_peh = 0
com_o_peh_pra_direita = 90
com_o_peh_pra_esquerda = 270
de_ponta_cabeca = 180


class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, foto_do_azulejo, filas, colunas, orientacao):
        
        pygame.sprite.Sprite.__init__(self)

        
        foto_do_azulejo = pygame.transform.rotate(pygame.transform.scale(foto_do_azulejo, (tamanho_azulejo, tamanho_azulejo)), orientacao)

        #Puxa as imagens
        self.image = foto_do_azulejo
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.mask.get_rect()
        self.rect = self.image.get_rect()

        #define o tamanho dos azulejos
        self.rect.x = tamanho_azulejo * colunas
        self.rect.y = tamanho_azulejo * filas


#Cria o jogador definindo a sua classe
class Player(pygame.sprite.Sprite):

    def __init__(self, assets, filas, colunas, piso_parede):
        #Chama a função do sprite
        pygame.sprite.Sprite.__init__(self)

        self.i = 1
        

        #puxa as imagens
        self.lista_anim = assets['anim_raposa']
        self.image = pygame.transform.scale(assets['anim_raposa'][int(self.i)], (largura_do_jogador, altura_do_jogador))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_rect = self.mask.get_rect()
        self.rect = self.image.get_rect()
        self.piso_parede = piso_parede
        self.rect.x = colunas * tamanho_azulejo
        self.rect.bottom = filas * tamanho_azulejo

        self.speedx = 0
        self.speedy = 0
    
    #Função resposável por definir as atualizações de estado
    
    def update(self):

        
        
        self.rect.y += self.speedy

        #TENTANDO ANIMAR
        self.i+=1/(10)
        if self.i>=len(self.lista_anim):
            self.i=1
        self.image = pygame.transform.scale(self.lista_anim[int(self.i)], (largura_do_jogador, altura_do_jogador))
        

        #define o dicionário que será criado caso haja colisões
        colisoes = pygame.sprite.spritecollide(self, self.piso_parede, False, pygame.sprite.collide_mask)
        
        #confere as colisões no topo e na base
        for colisao in colisoes:
            
            #confere se a velocidade está ou não mais 
            if self.speedy > 0:
                self.rect.bottom = colisao.rect.top
                self.speedy = 0

            #confere se a velocidade está ou não mais 
            elif self.speedy < 0:
                self.rect.top = colisao.rect.bottom
                self.speedy = 0

        #confere se a velocidade está ou não mais 
        self.rect.x += self.speedx
        
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= largura:
            self.rect.right = largura - 1
        
        #define o dicionário que será criado caso haja colisões
        colisoes = pygame.sprite.spritecollide(self, self.piso_parede, False, pygame.sprite.collide_mask)
        

        #Confere as colisões na esquerda e na direita
        for colisao in colisoes:
            
            #confere se a velocidade está ou não mais 
            if self.speedx > 0:
                self.rect.right = colisao.rect.left #+largura_do_jogador/2
                self.speedx = 0
            #confere se a velocidade está ou não mais 
            elif self.speedx < 0:
                self.rect.left = colisao.rect.right 
                self.speedx = 0






#fUNÇÃO QUE VAI EXIBIR O TEXTO INICIAL PARA O USÚÁRIO
def tela_inicial_de_texto(janela):

    pygame.mixer.music.load('imagens_e_sons/sons/tela_inicial.mp3') #Fonte: https://youtu.be/dDOfzfifwGE?si=GfIuDBJCHU0t26uN
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)
    
    frases_para_serem_exibidas = [

    'Você vai jogar algo muito incrivel',
    'Há poucas regras',
    'Clique nas setas para mover-se', 
    'Caso queira apelar, aperte r para reiniciar as vidas',
    'Caso queira voltar à tela inicial, aperte esc',
    'Pegue todas as galinhas e mude de fase',
    'E, depois, entre dentro do portal'

    ]
    
    #Define a fonte do texto que será usada
    font = pygame.font.SysFont(None, 45)

    #inicializa o indice do texto para que ele seja percorrido
    indice_do_textoo = 0

    #loop principal da tela de inicio, em que será rodado e exibido os textos
    while indice_do_textoo < len(frases_para_serem_exibidas):

        #usa o tmepo de acordo com a taxa de FPS determinada previamente
        clock.tick(FPS)

        #para cada evento ele vai ficar conferindo e vendo o que há para fazer dentro dos "IFs"
        for evento in pygame.event.get():
            
            #Determina quando tem que sair dessa tela


            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.JOYBUTTONDOWN:
                    pressao_no_botao = evento.button  # Obtém o número do botão pressionado
                    


                    #Verifica-se e converte-se o botão do joystivk para como se fosse um botão do teclado
                    # Por exemplo:
                    if pressao_no_botao == 3:  # Botão A
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
                    elif pressao_no_botao == 1:  # Botão B
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
                    elif pressao_no_botao == 2:  # Botão X
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}))
                    elif pressao_no_botao == 0:  # Botão Y
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))

            #Verifica o fenomeno de apertar uma tecla
            elif evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_ESCAPE:
                    print('ta indo')
                    return INICIO
                else: indice_do_textoo += 1
                #coonfere se a tecla pressionada era o espaço
                #if evento.key == pygame.K_SPACE or evento.key == pygame.K_DOWN:
                    

        #verifica se o indice que ele ta vendo ainda é ou não menor que o comprimento da lista de texto
        if indice_do_textoo < len(frases_para_serem_exibidas):
            texto = frases_para_serem_exibidas[indice_do_textoo]
        else:
            texto = ''
        texto_image = font.render(texto, True, branco)
        img_fundo = pygame.image.load('imagens_e_sons/imagens/inicio.png').convert_alpha()
        img_fundo = pygame.transform.scale(img_fundo, (largura, altura)) 
        janela.blit(img_fundo, (0,0))
   
        # define em que posição o texto irá ser gerado
        janela.blit(texto_image, (375, 550))
        pygame.display.flip()

        
    #retorna o estado do jogo
    return jogando




def tela_de_derrota(janela):
    pygame.mixer.music.load('imagens_e_sons/sons/morrendo.mp3') #Fonte: https://youtu.be/dDOfzfifwGE?si=GfIuDBJCHU0t26uN
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)


    frase_para_derrota = ["VOCÊ MORREU, Aperte A para continuar"]
    #Define a fonte do texto que será usada
    font = pygame.font.SysFont(None, 45)

    #inicializa o indice do texto para que ele seja percorrido
    indice_do_texto = 0

    #loop principal da tela de inicio, em que será rodado e exibido os textos
    while indice_do_texto < len(frase_para_derrota):

        #usa o tmepo de acordo com a taxa de FPS determinada previamente
        clock.tick(FPS)

        #para cada evento ele vai ficar conferindo e vendo o que há para fazer dentro dos "IFs"
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.K_ESCAPE:
                return INICIO
            elif evento.type == pygame.JOYBUTTONDOWN:
                    pressao_no_botao = evento.button  # Obtém o número do botão pressionado
                    print(f"Botão {pressao_no_botao} pressionado")


                    #Verifica-se e converte-se o botão do joystivk para como se fosse um botão do teclado
                    # Por exemplo:
                    if pressao_no_botao == 3:  # Botão A
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
                    elif pressao_no_botao == 1:  # Botão B
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
                    elif pressao_no_botao == 2:  # Botão X
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}))
                    elif pressao_no_botao == 0:  # Botão Y
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))

            #Verifica o fenomeno de apertar uma tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    print('ta indo')
                    return INICIO
                else: indice_do_texto += 1

        #verifica se o indice que ele ta vendo ainda é ou não menor que o comprimento da lista de texto
        if indice_do_texto < len(frase_para_derrota):
            texto = frase_para_derrota[indice_do_texto]
        else:
            texto = ''
        texto_image = font.render(texto, True, branco)
        img_fim = pygame.image.load('imagens_e_sons/imagens/fim.png').convert_alpha()    #tela do game over
        img_fim =  pygame.transform.scale(img_fim, (largura, altura)) #tela final
        janela.blit(img_fim, (0,0))
   
        #define em que posição o texto irá ser gerado
        janela.blit(texto_image, (300, 550))
        pygame.display.flip()
    #retorna o estado do jogo
    return jogando





def tela_de_vitoria(janela, FASE, tempo_certo):
    frase_para_vitoria = ["MEUS PARABÉNS!!!"]
    frase_para_vitoria2 = [f"Esse foi o seu tempo: {tempo_certo}"]
    frase_para_vitoria3=["Aperte A para continuar"]
    #Define a fonte do texto que será usada
    FASE += 1
    font = pygame.font.SysFont(None, 50)

    #inicializa o indice do texto para que ele seja percorrido
    indice_do_texto = 0

    #loop principal da tela de inicio, em que será rodado e exibido os textos
    while indice_do_texto < len(frase_para_vitoria):

        #usa o tmepo de acordo com a taxa de FPS determinada previamente
        clock.tick(FPS)

        #para cada evento ele vai ficar conferindo e vendo o que há para fazer dentro dos "IFs"
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.K_ESCAPE:
                return INICIO

            elif evento.type == pygame.JOYBUTTONDOWN:
                    pressao_no_botao = evento.button  # Obtém o número do botão pressionado
                    print(f"Botão {pressao_no_botao} pressionado")


                    #Verifica-se e converte-se o botão do joystivk para como se fosse um botão do teclado
                    # Por exemplo:
                    if pressao_no_botao == 3:  # Botão A
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}))
                    elif pressao_no_botao == 1:  # Botão B
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT}))
                    elif pressao_no_botao == 2:  # Botão X
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT}))
                    elif pressao_no_botao == 0:  # Botão Y
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}))

            #Verifica o fenomeno de apertar uma tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    print('ta indo')
                    return INICIO
                else: indice_do_texto += 1
        
        #verifica se o indice que ele ta vendo ainda é ou não menor que o comprimento da lista de texto
        if indice_do_texto < len(frase_para_vitoria):
            texto = frase_para_vitoria[indice_do_texto]
            texto2 = frase_para_vitoria2[indice_do_texto]
            texto3 = frase_para_vitoria3[indice_do_texto]
        else:
            texto = ''
        texto_image = font.render(texto, True, branco)
        texto_image2 = font.render(texto2, True, branco)
        texto_image3 = font.render(texto3, True, branco)
        img_fundo = pygame.image.load('imagens_e_sons/imagens/Fundo_jogo.jpg').convert_alpha() 
        img_fundo =  pygame.transform.scale(img_fundo, (largura, altura)) #tela final
        janela.blit(img_fundo, (0,0))

        #define em que posição o texto irá ser gerado
        janela.blit(texto_image, ((largura/2)*0.75, 150))
        janela.blit(texto_image2, ((largura/2)*0.6666666666, 300)) 
        janela.blit(texto_image3, ((largura/2)*0.7, 450))
        pygame.display.flip()
    #retorna o estado do jogo
    return [FASE, jogando]
