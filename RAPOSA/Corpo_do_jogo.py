
#Chama todas as bibliotécas que serão usadas ao longo de todo o código
import pygame
import random
from os import path
from Variaveis_e_funcoes import *
import sys


def qual_o_mapa(FASE, MAPA1, MAPA2, MAPA3):
    if FASE == 1:
        MAPA = MAPA1
    elif FASE == 2:
        MAPA = MAPA2 
    elif FASE == 3:
        MAPA = MAPA3
    
    return MAPA

#Define a tela do jogo e como ela irá funcionar
def tela_do_jogo(janela, FASE, MAPA):
    #SONS DO JOGO
    som_de_galinha = pygame.mixer.Sound('imagens_e_sons/sons/galinha_assustada.mp3')  #fonte: https://www.buscasons.com/_template/player/index.php?SID=https://www.buscasons.com/_arq/2020/galinha_assustada_202005111531.mp3&TITULO=Galinha%20assustada%20002&ID=1628
    som_de_dano = pygame.mixer.Sound('imagens_e_sons/sons/dano.mp3')    #fonte: https://pixabay.com/pt/sound-effects/homemadeoof-47509/
    som_de_erro = pygame.mixer.Sound('imagens_e_sons/sons/errado.mp3')   #fonte https://pixabay.com/pt/users/pixabay-1/
    #SOM DE FUNDO
    pygame.mixer.music.load('imagens_e_sons/sons/som_de_fundo.mp3') #Fonte: https://youtu.be/dDOfzfifwGE?si=GfIuDBJCHU0t26uN
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1)

   
    
    #INICIANDO O CRONOMETRO
    tempo_inicial = pygame.time.get_ticks()
    tempo_atual = 0
    ################################################################################
    
    
    vidas = 3 #vidas iniciais por fase
    estado_do_jogo = jogando

    #define e usa o tempo no jogo
    clock = pygame.time.Clock()
    assets = bases_carregando(0)
    fonte = pygame.font.Font(None, 36) #a fonte do cronometro


    while estado_do_jogo != DONE:
        
        pontos = 0
        n_galinhas = 0
        
        #define os grupos de sprites nas suas respectivas variáveis, isso será usado ao longo de todo o código
        todos_os_sprites= pygame.sprite.Group()
        espinhos = pygame.sprite.Group()
        piso_parede = pygame.sprite.Group()
        galinhas = pygame.sprite.Group()
        objetivo= pygame.sprite.Group()

        
        #Cria o mapa usando um laço de rpetição (FOR) para ler a nossa lista de listas que define o mapa em si 
        for filas in range(len(MAPA)):
            for colunas in range(len(MAPA[filas])):
                tile_type = MAPA[filas][colunas]
                
                #Confere cada letra dentro do dito mapa para atribuir uma carácteristica a ela e uma imagem
                if tile_type == B:  #blocos
                    tile = Tile(assets[tile_type], filas, colunas, de_peh)
                    todos_os_sprites.add(tile)
                    piso_parede.add(tile)
                #ESPINHOS VIRADOS PARA: ED = DIREITA, EE = ESQUERDA, EB = BAIXO, EC = CIMA
                if tile_type == EE:

                    tile_type = E
                    tile = Tile(assets[tile_type], filas, colunas, com_o_peh_pra_direita)
                    todos_os_sprites.add(tile)
                    espinhos.add(tile)

                if tile_type == ED:
                    tile_type = E
                    tile = Tile(assets[tile_type], filas, colunas, com_o_peh_pra_esquerda)
                    todos_os_sprites.add(tile)
                    espinhos.add(tile)

                if tile_type == EB:
                    tile_type = E
                    tile = Tile(assets[tile_type], filas, colunas, de_ponta_cabeca)
                    todos_os_sprites.add(tile)
                    espinhos.add(tile)
                if tile_type == EC:
                    tile_type = E
                    tile = Tile(assets[tile_type], filas, colunas, de_peh)
                    todos_os_sprites.add(tile)
                    espinhos.add(tile)
                #GALINHA
                if tile_type == G:
                    tile = Tile(assets[tile_type], filas, colunas, de_peh)
                    todos_os_sprites.add(tile)
                    galinhas.add(tile)
                    n_galinhas+=1
                #OBJETIVO
                if tile_type == O:
                    portal = Tile(assets[tile_type], filas, colunas, de_peh)
                    todos_os_sprites.add(portal)
                    objetivo.add(portal)
                #RAPOSA
                if tile_type == R:
                    y = filas
                    x = colunas
        
    
        #Define onde o jogador irá ser invocado e inicializado dentro do mapa, nesse caso, pela variável "R"
        player = Player(assets, y, x, piso_parede)
                    
        #Adiciona o player por último para que ele fique desenhado por cima de todos os outros sprites
        todos_os_sprites.add(player)
    

        #Define a imagem de fundo
        img_fundo = assets["img_fundo"]
        img_plataformas = assets["plataformas"]
        
        janela.blit(img_fundo, (0,0))
        todos_os_sprites.draw(janela)

        estado_do_jogador = vivo

        #confere se o jogador ainda têm vidas e se pode continuar jogando ou não
        while estado_do_jogador == vivo and estado_do_jogo == jogando:
            #marca o tempo
            clock.tick(FPS)
            
            

            ##CRONOMETRO############################################################

            tempo_minutos = 0
            tempo_atual = pygame.time.get_ticks() - tempo_inicial   #cronometro em milissegundos
            tempo_segundos = tempo_atual // 1000

            if tempo_segundos>60:
                tempo_minutos = tempo_segundos//60
                tempo_segundos = tempo_segundos%tempo_minutos
            
            tempo_certo = f'{tempo_minutos:02d}:{tempo_segundos:02d}'


        



            #COLISAO COM AS GALINHAS
            colisoess = pygame.sprite.spritecollide(player, galinhas, True, pygame.sprite.collide_mask)
            
            if colisoess:
                pontos +=1 #se colidir com a galinha, dá pontos
                som_de_galinha.play()
                
            
            """
            for colisao in colisoes:
                pontos +=1
                if pontos == n_galinhas:
                    pode_passar = sim
            """
        
            #COLISAO COM OS ESPINHOS
            colisoes = pygame.sprite.spritecollide(player, espinhos, False, pygame.sprite.collide_mask)

            if colisoes:
                vidas-=1
                som_de_dano.play()
                player.kill()
                if vidas == 0: #morreu, morreu, morreu mesmo
                    estado_do_jogo = morreu_de_vez
                    return morreu_de_vez
                else:
                    estado_do_jogador = morreu #isso acontece para sair do loop de quando ele tá vivo e reiniciar o mapa

            #colisão com o objetivo
            colisoes = pygame.sprite.spritecollide(player, objetivo, False, pygame.sprite.collide_mask) #colisao com o objetivo
            
            if colisoes:
                if n_galinhas == pontos: #conferindo se o jogador já pegou todas as galinhas
                    player.kill()    
                    return [vitoria, tempo_certo]
                else:
                    som_de_erro.play()
            

            
            # Verifica os eventos dentro do jogo
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    print('quit')
                    pygame.quit()
                    
                if event.type == pygame.JOYBUTTONDOWN:
                    pressao_no_botao = event.button  # Obtém o número do botão pressionado

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

                                #Confere quando jogador solta uma tecla (após pressionar ela)


                if event.type == pygame.KEYDOWN:
                    
                    #confere cada tecla de movimento
                    if event.key == pygame.K_LEFT:
                        if player.speedy == 0 and player.speedx == 0:
                            player.speedx = -velocidade_no_eixo_x
                    elif event.key == pygame.K_RIGHT:
                        if player.speedy == 0 and player.speedx == 0:
                            player.speedx = +velocidade_no_eixo_x
                    elif event.key == pygame.K_UP: 
                        if player.speedx == 0 and player.speedy == 0 :
                            player.speedy = -velocidade_no_eixo_x
                    elif event.key == pygame.K_DOWN: 
                        if player.speedx==0  and player.speedy == 0 :
                            player.speedy = velocidade_no_eixo_x
                    elif event.key == pygame.K_ESCAPE:
                        print('ta indo')
                        return INICIO
                    elif event.key == pygame.K_r:
                        vidas = 3
                        estado_do_jogador = morreu


            #Atualiza o grupo com todos os sprites
            todos_os_sprites.update()
            
            #Define a imagem de fundo
            img_fundo = assets["img_fundo"]
            img_plataformas = assets["plataformas"]
            
            janela.blit(img_fundo, (0,0))
            todos_os_sprites.draw(janela)

            
            fonte_pontos =  pygame.font.Font('imagens_e_sons/imagens/pontos.ttf', 40) #como sera o marcador de pontos - DEFINIR O TAMANHO
            perfil_texto = assets["fonte_dos_pontos"].render(chr(9829) * vidas , True, vermelho) #faz o coração
            texto_rect = perfil_texto.get_rect() 
            texto_rect.bottomleft = (10, altura - 10) #posiciona o texto
            janela.blit(perfil_texto, texto_rect) #coloca o texto na tela

            perfil_texto = fonte_pontos.render("{:.0f}/{:.0f}".format(pontos, n_galinhas), True, amarelo)  #diz quantas de quantas galinhas a pessoa já pegou     
            texto_rect = perfil_texto.get_rect() 
            texto_rect.midtop = (largura / 2,  10) #posiciona o texto
            janela.blit(perfil_texto, texto_rect) #coloca o texto na tela



            # Renderização do cronômetro na tela
            
            fonte_pontos =  pygame.font.Font(None, 30) #como sera o marcador de pontos - DEFINIR O TAMANHO
            perfil_texto = fonte_pontos.render(f"Tempo: {tempo_certo} ", True, branco)  #diz quantas de quantas galinhas a pessoa já pegou     
            texto_rect = perfil_texto.get_rect() 
            
            #texto_rect.midtop = (50,  10)
            janela.blit(perfil_texto, (10,10)) #coloca o texto na tela

            pygame.display.flip()
        


