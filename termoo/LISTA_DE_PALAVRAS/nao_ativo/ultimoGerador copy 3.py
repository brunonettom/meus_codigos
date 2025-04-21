import requests
from lxml import html
import csv
import os
import time
import threading
import random

# =========================
# CONFIGURAÇÃO DE VELOCIDADE
# =========================
# Número de palavras coletadas por segundo por thread (ex: 2 = 2 palavras/segundo)
COLETA_VELOCIDADE = 2  # Aumente para acelerar, diminua para desacelerar

# =========================
# OUTRAS CONFIGURAÇÕES
# =========================
NUM_THREADS = 10  # Número de threads paralelas
REQUESTS_PARALELAS = 5  # Limite de requisições simultâneas

# Lock para sincronizar escrita no arquivo
arquivo_lock = threading.Lock()
# Semáforo para limitar requisições simultâneas
request_semaphore = threading.Semaphore(REQUESTS_PARALELAS)

# =========================
# BACKOFF CONFIG
# =========================
class BackoffConfig:
    def __init__(self):
        self.min_delay = 0.5  # Delay mínimo inicial
        self.max_delay = 120
        self.current_delay = self.min_delay
        self.backoff_factor = 2
        self.success_streak = 0
        self.required_successes = 3
        self.lock = threading.Lock()
        self.last_increase_time = time.time()
        self.min_time_between_increases = 1

    def increase_delay(self):
        with self.lock:
            current_time = time.time()
            if current_time - self.last_increase_time >= self.min_time_between_increases:
                if self.current_delay == 0:
                    self.current_delay = 0.5  # Começa com meio segundo
                else:
                    self.current_delay = min(self.current_delay * self.backoff_factor, self.max_delay)
                self.last_increase_time = current_time
                self.success_streak = 0
            return self.current_delay

    def decrease_delay(self):
        with self.lock:
            self.success_streak += 1
            if self.success_streak >= self.required_successes:
                self.current_delay = max(self.current_delay / self.backoff_factor, self.min_delay)
                self.success_streak = 0
            return self.current_delay

    def get_current_delay(self):
        with self.lock:
            return self.current_delay

backoff_config = BackoffConfig()

# =========================
# FUNÇÃO DE COLETA
# =========================
def carrega_palavra_secreta():
    url = "https://www.aleatorios.org"
    try:
        with request_semaphore:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                elemento = html.fromstring(resposta.content)
                textos = elemento.xpath('//div//text()')
                textos = [t.strip() for t in textos if t.strip()]
                frase_indicativa = "Sua palavra aleatória é:"
                if frase_indicativa in textos:
                    idx = textos.index(frase_indicativa)
                    palavra_secreta = textos[idx + 1]
                    backoff_config.decrease_delay()
                    return palavra_secreta
                else:
                    raise Exception("Palavra não encontrada na página")
            else:
                raise Exception(f"Status code: {resposta.status_code}")
    except Exception as e:
        novo_delay = backoff_config.increase_delay()
        print(f"Erro ao carregar palavra: {e}. Aumentando delay para {novo_delay:.2f}s")
        return None

def salva_palavra_arquivo(palavra, nome_arquivo='palavras_aleatorias.csv'):
    if not palavra:
        return
    with arquivo_lock:
        arquivo_existe = os.path.exists(nome_arquivo)
        with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            if not arquivo_existe:
                writer.writerow(['palavra'])
            writer.writerow([palavra])

def coletor_palavras(thread_id):
    print(f"Thread {thread_id} iniciada")
    falhas_consecutivas = 0
    max_falhas_consecutivas = 5
    intervalo_minimo = 1 / COLETA_VELOCIDADE  # Intervalo mínimo entre coletas por thread

    while True:
        try:
            inicio = time.time()
            delay_atual = backoff_config.get_current_delay()
            palavra = carrega_palavra_secreta()
            if palavra:
                salva_palavra_arquivo(palavra)
                print(f"Thread {thread_id} coletou: {palavra} (delay atual: {delay_atual:.2f}s)")
                falhas_consecutivas = 0
            else:
                falhas_consecutivas += 1
                if falhas_consecutivas >= max_falhas_consecutivas:
                    print(f"Thread {thread_id}: Muitas falhas consecutivas...")
                    falhas_consecutivas = 0

            # Calcula quanto tempo esperar para respeitar a velocidade desejada
            tempo_gasto = time.time() - inicio
            tempo_espera = max(intervalo_minimo - tempo_gasto, 0)
            # O delay de backoff é somado ao intervalo mínimo se houver
            if delay_atual > 0:
                tempo_espera += delay_atual
            if tempo_espera > 0:
                time.sleep(tempo_espera)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro na thread {thread_id}: {e}")
            time.sleep(1)

def coleta_palavras_paralela(num_threads=NUM_THREADS):
    threads = []
    print(f"Iniciando coleta com {num_threads} threads paralelas...")
    print("Pressione Ctrl+C para parar.")
    try:
        for i in range(num_threads):
            thread = threading.Thread(
                target=coletor_palavras,
                args=(i+1,),
                daemon=True
            )
            threads.append(thread)
            thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando coleta de palavras...")
    for thread in threads:
        thread.join(timeout=1)
    print("Coleta finalizada!")

if __name__ == "__main__":
    coleta_palavras_paralela()
