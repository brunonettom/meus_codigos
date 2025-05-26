"""
Solução para o problema de compatibilidade do main.py com Pygbag

Este arquivo corrige os problemas identificados na comparação entre main.py e 
termoo_pygame_paia_mas_funiona.py, permitindo que o main.py funcione corretamente
no navegador usando Pygbag.
"""
import pygame
import sys
import asyncio

# Problemas identificados:
# 1. Implementação da classe TelaConfiguracao
# 2. Loop principal não está corretamente adaptado para funcionar em Pygbag
# 3. processamento de eventos de forma assíncrona
# 4. Possíveis imports problemáticos

class TelaConfiguracao:
    """
    Esta classe está implementada de forma simplificada para garantir que
    seja compatível com Pygbag. O problema no main.py pode ser que a classe
    TelaConfiguracao não está definida corretamente ou tem dependências
    problemáticas.
    """
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont('Arial', 24) if pygame.font.get_init() else None
        self.input_text = ""
        self.input_active = False
        
        # Configurações padrão
        self.configuracoes = {
            "num_palavras": 4,
            "dificuldade": 50,
            "num_letras": 5,
            "num_tentativas": 6,
            "trapaca": False
        }
        
        # Posição e dimensões da caixa de entrada
        largura_tela, altura_tela = self.tela.get_size()
        self.input_box = pygame.Rect(largura_tela // 4, 300, largura_tela // 2, 40)
        
        # Elemento atual selecionado no menu
        self.opcao_atual = 0
        self.opcoes = ["num_palavras", "num_letras", "num_tentativas", "dificuldade", "trapaca", "Iniciar Jogo"]
        self.labels = ["Número de palavras:", "Número de letras:", "Número de tentativas:", 
                       "Dificuldade (%):", "Modo trapaça:", ""]
                
    def processar_eventos(self):
        """
        Processa os eventos da tela de configuração.
        Retorna um dicionário com o resultado.
        """
        resultado = {"acao": "continuar"}
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                resultado = {"acao": "sair"}
            
            # Ativar/desativar caixa de entrada
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(evento.pos):
                    self.input_active = True
                else:
                    self.input_active = False
            
            # Processar teclas
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    resultado = {"acao": "sair"}
                
                # Navegação entre opções
                elif evento.key == pygame.K_UP:
                    self.opcao_atual = (self.opcao_atual - 1) % len(self.opcoes)
                elif evento.key == pygame.K_DOWN:
                    self.opcao_atual = (self.opcao_atual + 1) % len(self.opcoes)
                
                # Iniciar o jogo
                elif evento.key == pygame.K_RETURN:
                    if self.opcao_atual == len(self.opcoes) - 1:  # "Iniciar Jogo"
                        resultado = {"acao": "iniciar_jogo", "config": self.configuracoes}
                    else:
                        # Alternar modo trapaça
                        if self.opcoes[self.opcao_atual] == "trapaca":
                            self.configuracoes["trapaca"] = not self.configuracoes["trapaca"]
                
                # Editar valores numéricos
                elif self.opcao_atual < len(self.opcoes) - 1 and self.opcoes[self.opcao_atual] != "trapaca":
                    opcao_key = self.opcoes[self.opcao_atual]
                    
                    if evento.key == pygame.K_LEFT:
                        if self.configuracoes[opcao_key] > 1:
                            self.configuracoes[opcao_key] -= 1
                    elif evento.key == pygame.K_RIGHT:
                        max_valor = 100 if opcao_key == "dificuldade" else 10
                        if self.configuracoes[opcao_key] < max_valor:
                            self.configuracoes[opcao_key] += 1
        
        return resultado
        
    def renderizar(self):
        """Renderiza a tela de configuração."""
        self.tela.fill((240, 240, 240))  # Fundo claro
        
        # Título
        titulo_font = pygame.font.SysFont('Arial', 36) if pygame.font.get_init() else None
        if titulo_font:
            titulo = titulo_font.render("CONFIGURAÇÕES DO JOGO", True, (0, 0, 0))
            self.tela.blit(titulo, (self.tela.get_width() // 2 - titulo.get_width() // 2, 50))
        
        # Lista de opções
        y_pos = 150
        for i, (opcao, label) in enumerate(zip(self.opcoes, self.labels)):
            cor = (255, 0, 0) if i == self.opcao_atual else (0, 0, 0)
            
            # Texto da opção
            texto_opcao = label
            
            # Valor da opção
            if i < len(self.opcoes) - 1:  # Exceto "Iniciar Jogo"
                if opcao == "trapaca":
                    valor = "Sim" if self.configuracoes[opcao] else "Não"
                else:
                    valor = str(self.configuracoes[opcao])
                texto_opcao = f"{texto_opcao} {valor}"
            else:
                texto_opcao = "INICIAR JOGO"
            
            # Renderiza a opção
            if self.fonte:
                texto_surf = self.fonte.render(texto_opcao, True, cor)
                self.tela.blit(texto_surf, (self.tela.get_width() // 2 - texto_surf.get_width() // 2, y_pos))
            
            y_pos += 40
        
        # Instruções
        if self.fonte:
            instrucoes = self.fonte.render("Use ↑↓ para navegar, ←→ para ajustar valores", True, (0, 0, 150))
            self.tela.blit(instrucoes, (self.tela.get_width() // 2 - instrucoes.get_width() // 2, self.tela.get_height() - 50))
        
        pygame.display.flip()

class TermooPygame:
    """
    Implementação simplificada do jogo Termoo para demonstração.
    """
    def __init__(self, config):
        self.config = config
        self.tela = pygame.display.get_surface()
        self.largura_tela, self.altura_tela = self.tela.get_size()
        
        self.fonte = pygame.font.SysFont('Arial', 24) if pygame.font.get_init() else None
        self.fonte_grande = pygame.font.SysFont('Arial', 32) if pygame.font.get_init() else None
        
        # Configurações
        self.num_palavras = config["num_palavras"]
        self.num_letras = config["num_letras"]
        self.num_tentativas = config["num_tentativas"]
        self.modo_trapaca = config["trapaca"]
        
        # Dados do jogo
        self.palavras_chave = ["casa", "bola", "gato", "pato"][:self.num_palavras]
        self.palavras_chave_originais = self.palavras_chave.copy()
        self.tentativas = []
        self.tentativa_atual = 0
        self.palavras_acertadas = set()
        self.palavras_erradas = []
        self.entrada_atual = ""
        self.cursor_pos = 0
        self.jogo_terminado = False
        self.resultado_jogo = ""
        
        # Mensagem temporária
        self.mensagem = ""
        self.contador_mensagem = 0
        
        # Status das letras
        self.letras_usadas = set()
        self.status_letras = {}
        
        # Botão home
        self.botao_home_rect = pygame.Rect(20, 20, 40, 40)
    
    def processar_eventos(self):
        """Processa os eventos do jogo."""
        resultado = "continuar"
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                resultado = "sair"
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se clicou no botão home
                if self.botao_home_rect.collidepoint(evento.pos):
                    resultado = "reiniciar"
                    
            elif evento.type == pygame.KEYDOWN:
                if self.jogo_terminado:
                    if evento.key == pygame.K_RETURN:
                        resultado = "reiniciar"
                    elif evento.key == pygame.K_ESCAPE:
                        resultado = "sair"
                else:
                    if evento.key == pygame.K_ESCAPE:
                        resultado = "sair"
                    elif evento.key == pygame.K_RETURN:
                        # Processa tentativa
                        if len(self.entrada_atual) == self.num_letras:
                            self._processar_tentativa(self.entrada_atual)
                    elif evento.key == pygame.K_BACKSPACE:
                        if self.cursor_pos > 0:
                            # Remove o caractere à esquerda do cursor
                            self.entrada_atual = self.entrada_atual[:self.cursor_pos-1] + self.entrada_atual[self.cursor_pos:]
                            self.cursor_pos -= 1
                    elif evento.key == pygame.K_LEFT:
                        if self.cursor_pos > 0:
                            self.cursor_pos -= 1
                    elif evento.key == pygame.K_RIGHT:
                        if self.cursor_pos < len(self.entrada_atual):
                            self.cursor_pos += 1
                    elif evento.unicode.isalpha():
                        # Insere o caractere na posição do cursor
                        if len(self.entrada_atual) < self.num_letras:
                            self.entrada_atual = self.entrada_atual[:self.cursor_pos] + evento.unicode.lower() + self.entrada_atual[self.cursor_pos:]
                            self.cursor_pos += 1
        
        return resultado
    
    def _processar_tentativa(self, tentativa):
        """Processa uma tentativa de palavra."""
        # Verificações básicas
        if len(tentativa) != self.num_letras:
            self.mensagem = f"A palavra deve ter {self.num_letras} letras!"
            self.contador_mensagem = 120
            return
        
        # Adiciona a tentativa à lista
        self.tentativas.append(tentativa)
        self.tentativa_atual += 1
        
        # Verifica se acertou alguma palavra
        for palavra in list(self.palavras_chave):
            if tentativa == palavra:
                self.palavras_acertadas.add(palavra)
                self.palavras_chave.remove(palavra)
                self.mensagem = f"Parabéns! Você acertou a palavra: {palavra}"
                self.contador_mensagem = 120
                break
        else:
            self.palavras_erradas.append(tentativa)
            self.mensagem = "Tente novamente!"
            self.contador_mensagem = 60
        
        # Atualiza o status das letras
        self._atualizar_status_letras()
        
        # Limpa a entrada e reseta o cursor
        self.entrada_atual = ""
        self.cursor_pos = 0
        
        # Verifica condições de fim de jogo
        if not self.palavras_chave:
            self.jogo_terminado = True
            self.resultado_jogo = "vitoria"
            self.mensagem = "PARABÉNS! VOCÊ VENCEU!"
            self.contador_mensagem = 0  # Mantém a mensagem permanentemente
        
        if self.tentativa_atual >= self.num_tentativas and not self.jogo_terminado:
            self.jogo_terminado = True
            self.resultado_jogo = "derrota"
            self.mensagem = f"GAME OVER! As palavras eram: {', '.join(self.palavras_chave_originais)}"
            self.contador_mensagem = 0  # Mantém a mensagem permanentemente
    
    def _atualizar_status_letras(self):
        """Atualiza o status de cada letra usada nas tentativas."""
        alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        
        # Inicializa status para todas as letras
        for letra in alfabeto:
            if letra not in self.status_letras:
                self.status_letras[letra] = [0] * self.num_palavras  # 0=não usado, 1=posição errada, 2=correto
        
        # Atualiza status baseado nas tentativas
        for tentativa in self.tentativas:
            for i, letra in enumerate(tentativa):
                self.letras_usadas.add(letra)
                
                for j, palavra in enumerate(self.palavras_chave_originais):
                    if i < len(palavra):
                        if letra == palavra[i]:
                            self.status_letras[letra][j] = 2  # Posição correta
                        elif letra in palavra and self.status_letras[letra][j] < 2:
                            self.status_letras[letra][j] = 1  # Letra presente, posição errada
    
    def renderizar(self):
        """Renderiza a tela do jogo."""
        self.tela.fill((255, 255, 255))  # Fundo branco
        
        # Título
        if self.fonte_grande:
            titulo = self.fonte_grande.render("TERMOO", True, (0, 0, 0))
            self.tela.blit(titulo, (self.largura_tela // 2 - titulo.get_width() // 2, 20))
        
        # Botão home
        pygame.draw.rect(self.tela, (200, 200, 200), self.botao_home_rect)
        pygame.draw.rect(self.tela, (0, 0, 0), self.botao_home_rect, 2)
        
        # Status das letras
        self._renderizar_status_letras(80)
        
        # Tabuleiro
        self._renderizar_tabuleiro(180)
        
        # Área de entrada
        self._renderizar_entrada(self.altura_tela - 120)
        
        # Estatísticas
        self._renderizar_estatisticas(self.altura_tela - 60)
        
        # Mensagem temporária
        if self.mensagem and self.contador_mensagem > 0:
            self._renderizar_mensagem()
            self.contador_mensagem -= 1
        
        # Tela de fim de jogo
        if self.jogo_terminado:
            self._renderizar_fim_jogo()
        
        pygame.display.flip()
    
    def _renderizar_status_letras(self, pos_y):
        """Renderiza o status das letras do alfabeto."""
        if not self.fonte:
            return
            
        # Desenha o fundo da área
        pygame.draw.rect(self.tela, (230, 230, 230), 
                       pygame.Rect(20, pos_y, self.largura_tela - 40, 80))
        
        # Escreve as letras do alfabeto
        alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        x_pos = 30
        y_pos = pos_y + 10
        
        for i, letra in enumerate(alfabeto):
            # Quebra de linha a cada 13 letras
            if i % 13 == 0 and i > 0:
                x_pos = 30
                y_pos += 30
            
            # Determina a cor da letra
            cor = (100, 100, 100)  # Cinza para não usadas
            if letra in self.letras_usadas:
                # Verifica se a letra está em alguma palavra
                if any(status == 2 for status in self.status_letras.get(letra, [])):
                    cor = (0, 200, 0)  # Verde para posição correta
                elif any(status == 1 for status in self.status_letras.get(letra, [])):
                    cor = (200, 200, 0)  # Amarelo para letra correta, posição errada
                else:
                    cor = (200, 0, 0)  # Vermelho para letra errada
            
            # Renderiza a letra
            texto = self.fonte.render(letra.upper(), True, cor)
            self.tela.blit(texto, (x_pos, y_pos))
            x_pos += 28
    
    def _renderizar_tabuleiro(self, pos_y):
        """Renderiza o tabuleiro com as tentativas."""
        # Calcula o tamanho das células para que caibam na tela
        largura_disponivel = self.largura_tela - 40
        cel_size = min(40, largura_disponivel // (self.num_palavras * self.num_letras + self.num_palavras - 1))
        
        # Para cada palavra
        for p_idx, palavra in enumerate(self.palavras_chave_originais):
            # Posição inicial desta palavra no tabuleiro
            pos_x = 20 + p_idx * (self.num_letras * (cel_size + 2) + 20)
            
            # Para cada linha (tentativa)
            for t_idx in range(self.num_tentativas):
                for l_idx in range(self.num_letras):
                    # Calcula posição da célula
                    cell_x = pos_x + l_idx * (cel_size + 2)
                    cell_y = pos_y + t_idx * (cel_size + 2)
                    
                    # Desenha a célula
                    pygame.draw.rect(self.tela, (200, 200, 200), 
                                   pygame.Rect(cell_x, cell_y, cel_size, cel_size))
                    
                    # Se já temos uma tentativa para esta linha
                    if t_idx < len(self.tentativas):
                        tentativa = self.tentativas[t_idx]
                        
                        # Se esta célula tem uma letra
                        if l_idx < len(tentativa):
                            letra = tentativa[l_idx]
                            
                            # Determina a cor de fundo baseada na comparação com a palavra
                            cor_fundo = (200, 200, 200)  # Cinza padrão
                            
                            if palavra in self.palavras_acertadas and tentativa == palavra:
                                cor_fundo = (0, 200, 0)  # Verde se acertou a palavra
                            elif letra == palavra[l_idx]:
                                cor_fundo = (0, 200, 0)  # Verde se letra na posição correta
                            elif letra in palavra:
                                cor_fundo = (200, 200, 0)  # Amarelo se letra existe na palavra
                            else:
                                cor_fundo = (100, 100, 100)  # Cinza escuro se letra não existe
                            
                            # Desenha o fundo colorido
                            pygame.draw.rect(self.tela, cor_fundo, 
                                           pygame.Rect(cell_x, cell_y, cel_size, cel_size))
                            
                            # Desenha a letra
                            if self.fonte:
                                texto = self.fonte.render(letra.upper(), True, (255, 255, 255))
                                self.tela.blit(texto, (cell_x + cel_size//2 - texto.get_width()//2, 
                                                     cell_y + cel_size//2 - texto.get_height()//2))
    
    def _renderizar_entrada(self, pos_y):
        """Renderiza a área de entrada de texto."""
        if not self.fonte:
            return
            
        # Textos informativos
        texto_info = self.fonte.render("Digite sua tentativa:", True, (0, 0, 0))
        self.tela.blit(texto_info, (self.largura_tela // 2 - texto_info.get_width() // 2, pos_y - 30))
        
        # Caixa de entrada
        input_box = pygame.Rect(self.largura_tela // 2 - 150, pos_y, 300, 40)
        pygame.draw.rect(self.tela, (255, 255, 255), input_box)
        pygame.draw.rect(self.tela, (0, 0, 255), input_box, 2)
        
        # Texto na caixa
        texto_entrada = self.fonte.render(self.entrada_atual, True, (0, 0, 0))
        self.tela.blit(texto_entrada, (input_box.x + 10, input_box.y + 10))
        
        # Cursor
        if pygame.time.get_ticks() % 1000 < 500:  # Pisca o cursor
            cursor_pos_x = input_box.x + 10
            if self.entrada_atual:
                parte_texto = self.fonte.render(self.entrada_atual[:self.cursor_pos], True, (0, 0, 0))
                cursor_pos_x += parte_texto.get_width()
            
            pygame.draw.line(self.tela, (0, 0, 0), 
                           (cursor_pos_x, input_box.y + 10),
                           (cursor_pos_x, input_box.y + 30), 2)
    
    def _renderizar_estatisticas(self, pos_y):
        """Renderiza estatísticas do jogo."""
        if not self.fonte:
            return
            
        # Tentativas restantes
        texto_tentativas = self.fonte.render(f"Tentativas restantes: {self.num_tentativas - self.tentativa_atual}", True, (0, 0, 0))
        self.tela.blit(texto_tentativas, (20, pos_y))
        
        # Palavras faltantes
        texto_palavras = self.fonte.render(f"Palavras faltantes: {len(self.palavras_chave)}", True, (0, 0, 0))
        self.tela.blit(texto_palavras, (20, pos_y + 25))
    
    def _renderizar_mensagem(self):
        """Renderiza mensagem temporária."""
        if not self.fonte or not self.mensagem:
            return
            
        # Cria superfície semi-transparente
        overlay = pygame.Surface((self.largura_tela, 50), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.tela.blit(overlay, (0, self.altura_tela - 50))
        
        # Texto da mensagem
        texto_mensagem = self.fonte.render(self.mensagem, True, (255, 255, 255))
        self.tela.blit(texto_mensagem, (self.largura_tela // 2 - texto_mensagem.get_width() // 2, 
                                      self.altura_tela - 35))
    
    def _renderizar_fim_jogo(self):
        """Renderiza tela de fim de jogo."""
        if not self.fonte or not self.fonte_grande:
            return
            
        # Cria superfície semi-transparente
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.tela.blit(overlay, (0, 0))
        
        # Texto principal
        texto_principal = self.fonte_grande.render(
            "VOCÊ VENCEU!" if self.resultado_jogo == "vitoria" else "VOCÊ PERDEU!",
            True, (0, 255, 0) if self.resultado_jogo == "vitoria" else (255, 0, 0))
        
        self.tela.blit(texto_principal, (self.largura_tela // 2 - texto_principal.get_width() // 2, 
                                       self.altura_tela // 2 - 50))
        
        # Palavras (apenas se perdeu)
        if self.resultado_jogo == "derrota":
            texto_palavras = self.fonte.render(f"As palavras eram: {', '.join(self.palavras_chave_originais)}", 
                                             True, (255, 255, 255))
            self.tela.blit(texto_palavras, (self.largura_tela // 2 - texto_palavras.get_width() // 2, 
                                          self.altura_tela // 2))
        
        # Instruções
        texto_instrucoes = self.fonte.render("Pressione ENTER para jogar novamente ou ESC para sair", 
                                           True, (255, 255, 255))
        self.tela.blit(texto_instrucoes, (self.largura_tela // 2 - texto_instrucoes.get_width() // 2, 
                                        self.altura_tela // 2 + 50))

async def main():
    """
    Função principal com loop assíncrono para compatibilidade com Pygbag.
    Esta implementação corrige o problema do main.py que impede seu funcionamento
    no navegador.
    """
    pygame.init()
    pygame.font.init()
    
    # Configuração da tela
    tamanho_tela = (800, 600)
    tela = pygame.display.set_mode(tamanho_tela)
    pygame.display.set_caption("Termoo - Versão Web Compatível")
    
    # Estados do jogo
    estado_atual = "configuracao"
    tela_config = TelaConfiguracao(tela)
    jogo = None
    
    # Loop principal
    clock = pygame.time.Clock()
    rodando = True
    
    while rodando:
        if estado_atual == "configuracao":
            resultado = tela_config.processar_eventos()
            if resultado["acao"] == "sair":
                rodando = False
            elif resultado["acao"] == "iniciar_jogo":
                jogo = TermooPygame(resultado["config"])
                estado_atual = "jogo"
                
            tela_config.renderizar()
        
        elif estado_atual == "jogo":
            resultado = jogo.processar_eventos()
            if resultado == "sair":
                rodando = False
            elif resultado == "reiniciar":
                estado_atual = "configuracao"
                tela = pygame.display.get_surface()
                tela_config = TelaConfiguracao(tela)
                
            jogo.renderizar()
        
        # Controle de FPS
        clock.tick(60)
        
        # CRUCIAL para compatibilidade com Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    # Detecta plataforma para execução apropriada
    if sys.platform == 'emscripten':
        # No navegador usando Pygbag
        asyncio.run(main())
    else:
        # Em desktop
        try:
            asyncio.run(main())
        except (SystemExit, KeyboardInterrupt):
            pygame.quit()
