import os
import time
from multiprocessing import Process, Queue

# ===============================
# Consolidação dos resultados
# ===============================
def consolidar_resultados(resultados):
    total_linhas = 0
    total_palavras = 0
    total_caracteres = 0

    contagem_global = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for r in resultados:
        total_linhas += r["linhas"]
        total_palavras += r["palavras"]
        total_caracteres += r["caracteres"]

        for chave in contagem_global:
            contagem_global[chave] += r["contagem"][chave]

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem_global
    }

def processar_arquivo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    total_linhas = len(conteudo)
    total_palavras = 0
    total_caracteres = 0

    contagem = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for linha in conteudo:
        palavras = linha.split()

        total_palavras += len(palavras)
        total_caracteres += len(linha)

        for p in palavras:
            if p in contagem:
                contagem[p] += 1

        # Simulação de processamento pesado
        for _ in range(1000):
            pass

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem
    }

def worker(tq, rq):
    while True:
        caminho_arq = tq.get()
        if caminho_arq is None: # Poison pill para encerrar o processo
            break
        # O processamento da contagem de palavras-chave (erro, warning, info) ocorre aqui
        res = processar_arquivo(caminho_arq) 
        rq.put(res)

# ===============================
# Execução Paralela
# ===============================
def executar_paralelo(pasta, num_processos):
    resultados = []
    inicio = time.time()
    
    task_queue = Queue(maxsize=50) 
    result_queue = Queue()

    trabalhadores = []
    for _ in range(num_processos):
        p = Process(target=worker, args=(task_queue, result_queue))
        p.start()
        trabalhadores.append(p)

    arquivos_pasta = os.listdir(pasta)
    for arquivo in arquivos_pasta:
        task_queue.put(os.path.join(pasta, arquivo))

    for _ in range(num_processos):
        task_queue.put(None)

    # Coletando os resultados e preenchendo a lista original
    for _ in range(len(arquivos_pasta)):
        resultados.append(result_queue.get())

    # Aguardando a finalização segura de todos os processos
    for p in trabalhadores:
        p.join()

    fim = time.time()
    resumo = consolidar_resultados(resultados)

    print(f"\n=== EXECUÇÃO PARALELA ({num_processos} PROCESSOS) ===")
    print(f"Arquivos processados: {len(resultados)}")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    print("\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {resumo['linhas']}")
    print(f"Total de palavras: {resumo['palavras']}")
    print(f"Total de caracteres: {resumo['caracteres']}")

    print("\nContagem de palavras-chave:")
    for k, v in resumo["contagem"].items():
        print(f"  {k}: {v}")

    return resumo

# ===============================
# Main
# ===============================
if __name__ == "__main__":
    pasta = "log2"
    
    # Altere este valor para testar com 2, 4, 8 ou 12 processos
    quantidade_de_processos = 12 

    print(f"Iniciando o processamento com {quantidade_de_processos} processos...")
    executar_paralelo(pasta, quantidade_de_processos)
