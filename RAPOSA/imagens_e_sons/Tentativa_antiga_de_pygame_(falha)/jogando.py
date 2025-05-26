import pygame
import os
from mapa import *
from parametros import *
from math import *
from sprites_e_classes import *


###########################################################JOGO#################################################


def jogando(JANELA):
    cronometro = pygame.time.Clock()
    #chamando o personagem
    
    #CRIANDO O MAPA
    for linha in range(len(MAPA)):
        for coluna in range(len(MAPA)):
                elemento = MAPA[linha] [coluna]
                linha *= TAMANHO_LINHA_E_COLUNA
                coluna *= TAMANHO_LINHA_E_COLUNA
                if elemento == B or elemento == L or elemento == P:
                        imagem = img_plataformas
                        orientacao = de_peh
                        bloco = objeto(linha,coluna, imagem, orientacao)
                        F['plataformas'].add(bloco)
                        F['blocos'].add(bloco)
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
                        espinho = objeto(linha, coluna, imagem, orientacao)
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
                        personagem = persona(linha, coluna)
                        F['all_sprites'].add(personagem)
                
                if elemento == O:
                        imagem = img_chegada
                        orientacao = de_peh

                        objetivo = objeto(linha, coluna, imagem, orientacao)
                        F['objetos'].add(objetivo)
                        F['all_sprites'].add(objetivo)

    

    personagem.i = 0 #essa contagem, posteriormente será utilizada para a animação do personagem

    GAME_OVER  = 0
    JOGANDO = 1
    MORRENDO = 2
    DONE = 3
    INICIO = 4
    VITORIA = 5

    keys_down = {}

    
    estado_do_jogo = JOGANDO
    
    #FAZENDO O MAPA
    for fila in range(len(MAPA)):
        for coluna in range(len(MAPA[fila])):
            tipo_bloco = MAPA[fila][coluna]
            if tipo_bloco == B:
                bloco = objeto(fila, coluna, img_plataformas, de_peh)
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



    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.som_fundo.play(loops=-1)
    
    while estado_do_jogo == JOGANDO:
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
                    if event.key == pygame.DOWN or event.key == pygame.K_s and personagem.velocidadex == 0 :
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
            colisoes_plataformas = pygame.sprite.spritecollide(personagem, F1['plataformas'], False, pygame.sprite.collide_mask)
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
                morte = sprite_morrendo(personagem.rect.center) 

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
                    personagem = persona() #CONVOCA O PERSONAGEM NAS CONFIGURAÇÕES INICIAIS
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

