from datetime import datetime
import numpy as np
from wordfreq import word_frequency, top_n_list
from filtra_palavras import lista_de_palavras
import random
import unicodedata


class Termoo():
    def __init__(self):
        # self.dicionarioTodo = todasAsPalavras
        self.en = top_n_list('en', 100000, wordlist='large')
        self.dicionarioTodo=top_n_list('pt', 300000)
        # self.possiveisChaves=palavras
        self.vermelho = '\033[91m'
        self.cinza = "\033[37m"
        self.amarelo = "\033[33m"
        self.verde = "\033[32m"
        self.resetar_cor = "\033[0m"
        self.palavrasChutadas = []
        self.nPalavras = None
        self.nLetras = None
        self.nLinhasFaltantes = None
        self.lChavesEscolhidas = []
        self.palavrasErradas=[]
        self.lChavesEscolhidasOriginais = []
        self.lChavesPossiveis = []
        self.palavrasAcertadasConfere=[]
        self.palavrasAcertadas = set()
        self.historicoColunas = {}
        self.flagChuteValido=True
        self.flagDebuggar=False
        self.flagVerIteracoes=False
    
    def remover_acentos(self, palavra):
        """
        Remove acentos e substitui 'ç' por 'c' na palavra fornecida.
        
        Args:
            palavra (str): A palavra a ser processada.
        
        Returns:
            str: A palavra sem acentos e com 'ç' substituído por 'c'.
        """
        # Normaliza a palavra para decompor caracteres acentuados
        nfkd = unicodedata.normalize('NFD', palavra)
        # Remove os caracteres de marcação de acentuação
        sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        # Substitui 'ç' por 'c'
        sem_acentos = sem_acentos.replace('ç', 'c').replace('Ç', 'C')
        return sem_acentos

    def chavesEscolhidas(self):
        """
        Seleciona aleatoriamente um conjunto de palavras como chaves do jogo.
        
        Returns:
            list: Lista de palavras selecionadas como chaves.
        """
        ChavesEscolhidas = []
        lPreChavesEscolhidas = [word.lower() for word in self.possiveisChaves if ' ' not in word and '-' not in word]
        
        # Garante que a lista lPreChavesEscolhidas tenha palavras suficientes para seleção
        if len(lPreChavesEscolhidas) < self.nPalavras:
            print("Erro: Não há palavras suficientes para selecionar.")
            return []

        for _ in range(self.nPalavras):
            sorteada=random.choice(lPreChavesEscolhidas)
            while len(sorteada) != self.nLetras or sorteada in ChavesEscolhidas:
                sorteada=random.choice(lPreChavesEscolhidas)

            ChavesEscolhidas.append(sorteada)

        self.lChavesEscolhidasOriginais0 = ChavesEscolhidas
        lChavesEscolhidas = [self.remover_acentos(palavra) for palavra in ChavesEscolhidas]
        return lChavesEscolhidas

  
    def listaDeCorDoChute(self, chute, chave):
        if len(chute) != self.nLetras or len(chave) != self.nLetras:
            print(f"Erro: A palavra deve ter exatamente {self.nLetras} letras.")
            return [self.cinza] * self.nLetras, 0
        
        listaDeCorDoChute = [self.cinza] * self.nLetras
        nVerdes = 0
        chuteVAmarelo = list(chave)

        for i in range(self.nLetras):
            if chute[i] == chave[i]:
                listaDeCorDoChute[i] = self.verde
                nVerdes += 1
                chuteVAmarelo[i] = None

        for i in range(self.nLetras):
            if listaDeCorDoChute[i] == self.cinza and chute[i] in chuteVAmarelo:
                listaDeCorDoChute[i] = self.amarelo
                index_amarelo = chuteVAmarelo.index(chute[i])
                chuteVAmarelo[index_amarelo] = None

        return listaDeCorDoChute, nVerdes


    def pintaPalavra(self, chute, listaDeCorDoChute):
        palavraPintada = ""
        for i in range(len(chute)):
            palavraPintada += listaDeCorDoChute[i] + chute[i] + " "
        palavraPintada += self.resetar_cor
        return palavraPintada

    def chuteColorido(self, chute, palavraPintada):
        return palavraPintada

    def trataChute(self, chave, chute):
        listaDeCorDoChute, nVerdes = self.listaDeCorDoChute(chute, chave)
        palavraPintada = self.pintaPalavra(chute, listaDeCorDoChute)
        chuteColorido = self.chuteColorido(chute, palavraPintada)
        return chuteColorido, nVerdes

    def linhaVazia(self):
        return "_ " * self.nLetras + "\n"

    def colunai(self, chave, iColuna):
        resultado = []
        acertou = False

        for chute in self.palavrasChutadas:
            if chute == chave and not acertou:
                # Palavra acertada — pinta ela de verde completamente
                lista_cor = [self.verde] * self.nLetras
                resultado.append(self.pintaPalavra(chave, lista_cor))
                acertou = True
            elif not acertou:
                chuteColorido, _ = self.trataChute(chave, chute)
                resultado.append(chuteColorido)

        # Preenche linhas restantes com "_" depois do acerto
        while len(resultado) < self.nChutesTotais:
            resultado.append("_ " * self.nLetras)

        return resultado



    def tabela_letras_detalhada(self):
        letras_atuais = sorted(set("".join(self.palavrasChutadas)))

        if self.quer_trapaca:
            print(f'\nCHAVES: {self.lChavesEscolhidas} \n\n')

        for letra in letras_atuais:
            linha = f"{letra.upper()}: "
            for chave in self.lChavesEscolhidasOriginais:
                cor = self.vermelho  # cor padrão vermelho
                ultimo_chute = self.palavrasChutadas[-1]

                # Checar posição correta primeiro
                for i in range(self.nLetras):
                    if ultimo_chute[i] == letra and chave[i] == letra:
                        cor = self.verde
                        break  # posição certa tem prioridade máxima

                # Se não achou posição correta, verificar se está na palavra
                if cor != self.verde and letra in chave:
                    cor = self.amarelo

                linha += cor + "■ " + self.resetar_cor

            print(linha)
        print('\n\n')


    
    def fazChutes(self):
        self.nLinhasFaltantes = self.nChutesTotais - len(self.palavrasChutadas) - 1

        while self.nLinhasFaltantes > 0 and self.lChavesEscolhidas:
            self.nLinhasFaltantes = self.nChutesTotais - len(self.palavrasChutadas)

            chute = input("\nDigite um chute: ").lower()
            if chute == "" or not chute:
                print(self.vermelho + "FAÇA UM CHUTE!!!" + self.cinza)
                continue
            if chute in ['desisto', 'q', 'quit', 'sair']:
                self.nLinhasFaltantes = 0
                continue
            if len(chute) != self.nLetras:
                print(f"Por favor, digite uma palavra com {self.nLetras} letras.")
                self.flagChuteValido = False
                continue
            if chute not in self.dicionarioTodo:
                self.flagChuteValido = False
                print("Palavra não encontrada no dicionário.")
                continue

            self.palavrasChutadas.append(chute)

            # Exibe o tabuleiro antes de verificar acertos
            self.tabela_letras_detalhada()
            print(self.todasAsColunas())
            # self.mostrar_status_alfabeto()
            palavrasSobrantes = [p for p in self.lChavesEscolhidasOriginais if p not in self.palavrasAcertadas]

            print(self.vermelho + f"Vidas restantes: {self.nLinhasFaltantes}" + self.cinza)
            print(self.amarelo + f"Palavras faltentes: {len(palavrasSobrantes)}" + self.cinza + "\n")

            if not self.flagDebuggar:
                print(self.amarelo + f'NÚMERO DE PALAVRAS QUE FALTAM: {len(palavrasSobrantes)}' + self.cinza)
            if self.flagDebuggar:
                print(self.amarelo + f"CHAVES ESCOLHIDAS : {', '.join(chave.upper() for chave in palavrasSobrantes)}" + self.cinza)

            if len(self.palavrasAcertadasConfere) != 0:
                print(self.verde + f"PALAVRAS ACERTADAS : {', '.join(p.upper() for p in self.palavrasAcertadasConfere)}" + self.cinza)

            # TRATA CHUTES
            if chute in self.lChavesEscolhidas:
                print(self.verde + f"\nParabéns! Você acertou a palavra '{chute}'!".upper() + self.cinza)
                self.palavrasAcertadasConfere.append(chute)
                self.lChavesEscolhidas.remove(chute)
                self.palavrasAcertadas.add(chute)

                # ← AQUI ESTÁ A LINHA ADICIONADA
                print(self.todasAsColunas())

                if not self.lChavesEscolhidas:
                    print(self.verde + "\n\nVocê acertou todas as palavras! Parabéns!".upper())
                    break
            else:
                self.palavrasErradas.append(chute)

            if len(self.palavrasErradas) != 0:
                print(self.vermelho + f"PALAVRAS ERRADAS : {', '.join(p.upper() for p in self.palavrasErradas)}" + self.cinza)

        if self.nLinhasFaltantes == 0:
            print(f"Suas vidas acabaram! As palavras eram: {', '.join(self.lChavesEscolhidasOriginais0)}".upper())

    def fazChaves(self):
        if type(input('qual é o nivel de dificuldade desejada? (1 a 100)')) ==float:
            dificuldade = float(input('qual é o nivel de dificuldade desejada? (1 a 100)'))/100
            if 0>dificuldade>100:
                self.possiveisChaves=lista_de_palavras(dificuldade)
            else:
                self.possiveiwsChaves=lista_de_palavras(0.5)
        else:
            self.possiveisChaves=lista_de_palavras(0.5)
        
        preNLetras = input("Quantas letras você quer por palavra? (5) ")
        if preNLetras=='' or not preNLetras:
            self.nLetras=5
        else:
            self.nLetras = int(preNLetras)
        
        preNPalavras= input("Quantas palavras? (4) ")

        if preNPalavras=='' or not preNPalavras:
            self.nPalavras=4
        else:
            self.nPalavras = int(preNPalavras)
        
        escolherNChutes=input("Quer escolher quantos chutes quer? (N/s) ")
        if escolherNChutes=='s' or escolherNChutes=='y':
            self.nChutesTotais = int(input("Quantos chutes você quer? "))
        trapaca=input("Quer trapaça? (N/s) ")
        if trapaca == "s" or trapaca=="y":
            self.quer_trapaca=True
        else:
            self.quer_trapaca=False

        if not(preNPalavras=='s' or preNPalavras=='y'):
            self.nChutesTotais=self.nLetras+1
            self.nChutesTotais+=self.nPalavras-1



        print("chutes TOTAIS",self.nChutesTotais)
        

        self.lChavesEscolhidas = self.chavesEscolhidas()
        self.lChavesEscolhidasOriginais = self.lChavesEscolhidas.copy()
        return True

    def todasAsColunas(self):
        colunas = [[] for _ in range(self.nPalavras)]

        for iColuna in range(self.nPalavras):
            chave_atual = self.lChavesEscolhidasOriginais[iColuna]
            if chave_atual in self.palavrasAcertadas:
                colunas[iColuna] = self.colunai(chave_atual, iColuna)
            else:
                linhas_coluna = []
                for chute in self.palavrasChutadas:
                    chuteColorido, _ = self.trataChute(chave_atual, chute)
                    linhas_coluna.append(chuteColorido)
                for _ in range(self.nChutesTotais - len(self.palavrasChutadas)):
                    linhas_coluna.append("_ " * self.nLetras)
                colunas[iColuna] = linhas_coluna

        # Transpor as linhas para exibir lado a lado
        saida = ""
        for linha in zip(*colunas):
            saida += "   ".join(linha) + "\n"
        return saida
    def mostrar_status_alfabeto(self):
        alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        resultado = []

        for letra in alfabeto:
            foi_chutada = any(letra in chute for chute in self.palavrasChutadas)
            if not foi_chutada:
                resultado.append(f"{letra.upper()} (0)")
                continue

            status_por_palavra = []
            for i, chave in enumerate(self.lChavesEscolhidasOriginais):
                cor = self.cinza
                for chute in self.palavrasChutadas:
                    if letra in chute:
                        if any(chute[idx] == letra and chave[idx] == letra for idx in range(self.nLetras)):
                            cor = self.verde
                            break
                        elif letra in chave:
                            cor = self.amarelo
                status_por_palavra.append(f"{cor}{i+1}{self.resetar_cor}")

            resultado.append(f"{letra.upper()} ({', '.join(status_por_palavra)})")

        print("\n" + ", ".join(resultado) + "\n")






if __name__ == "__main__":
    termoo = Termoo()
    if termoo.fazChaves():
        termoo.fazChutes()













    
    