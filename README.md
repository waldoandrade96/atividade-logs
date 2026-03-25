# Relatório de Benchmark: Processamento Paralelo de Logs em Python

**Disciplina:** Programação Concorrente e Distribuída  
**Estudante:** Waldo Andrade Silva
**Turma:** ADSN04  
**Professor:** Rafael  
**Data:** 25/03/2026  

---

## 1. Escopo do Projeto

O objetivo principal deste código é realizar o processamento simultâneo de 1.000 arquivos de log, distribuindo a carga de trabalho entre múltiplos processos para avaliar o ganho real de velocidade.

A rotina analisa cada documento separadamente. O algoritmo contabiliza a quantidade total de linhas, palavras e caracteres. Além disso, faz a busca e a contagem de termos específicos (como `erro`, `warning` e `info`), consolidando todos os dados em um relatório final único.

| Característica | Detalhe |
|---|---|
| **Propósito** | Medir e comparar tempos ao processar 1.000 arquivos de log de forma simultânea. |
| **Volume de Dados** | 1.000 documentos, totalizando 10 milhões de linhas, 200 milhões de palavras e aproximadamente 1,37 GB de texto. |
| **Complexidade** | O(n/p), indicando que a quantidade de arquivos atribuída a cada processo diminui à medida que mais processos são alocados. |

---

## 2. Hardware e Ambiente de Testes

Os testes foram conduzidos na seguinte máquina:

* **Processador:** Intel Core i5-12500 (12ª Geração) operando a 3.00 GHz
* **Estrutura da CPU:** 6 núcleos físicos e 12 threads lógicas
* **Memória RAM:** 16,0 GB
* **Sistema Operacional:** Windows 11
* **Linguagem e Compilador:** Python 3.x
* **Biblioteca:** `multiprocessing`

---

## 3. Metodologia de Medição

Para garantir uma precisão alta, o tempo foi cronometrado com a função `time.perf_counter()`. O foco foi isolar apenas o tempo de processamento, desconsiderando a etapa de leitura inicial dos arquivos.

Para evitar que anomalias ou picos de uso do sistema operacional afetassem os dados, cada cenário de teste foi repetido 3 vezes, adotando-se a média de tempo dessas execuções.

**Cenários Avaliados:**
* 1 processo
* 2 processos
* 4 processos
* 8 processos
* 12 processos

---

## 4. Tempos Obtidos e Dados Consolidados

**Tempos médios por configuração:**

| Nº Processos | Tempo de Execução (s) |
|:---:|:---:|
| 1 | 83.7459 |
| 2 | 46.2264 |
| 4 | 26.9465 |
| 8 | 14.8504 |
| 12 | 13.0065 |

**Resultados exatos do conteúdo analisado (consistentes em todas as rodadas):**

* O script processou com sucesso 1.000 arquivos.
* Foram contadas 10.000.000 de linhas.
* O total de palavras lidas foi de 200.000.000.
* Foram identificados 1.366.663.305 caracteres no total.
* A palavra-chave `erro` apareceu 33.332.083 vezes.
* A palavra-chave `warning` apareceu 33.330.520 vezes.
* A palavra-chave `info` apareceu 33.329.065 vezes.

---

## 5. Fórmulas de Desempenho (Speedup e Eficiência)

* **Speedup:** Mede o fator de aceleração dividindo o tempo da execução sequencial original pelo tempo da execução paralela com múltiplos processos.
  Speedup(p) = T(1) / T(p)

* **Eficiência:** Avalia se o hardware está sendo bem aproveitado dividindo o valor do Speedup pela quantidade de processos, onde 1,0 representa a eficiência perfeita.
  Eficiência(p) = Speedup(p) / p

---

## 6. Quadro Comparativo de Métricas

| Processos | Tempo (s) | Aceleração (Speedup) | Eficiência |
|:---:|:---:|:---:|:---:|
| 1 | 83.7459 | 1.00 | 1.00 |
| 2 | 46.2264 | 1.81 | 0.91 |
| 4 | 26.9465 | 3.11 | 0.78 |
| 8 | 14.8504 | 6.05 | 0.76 |
| 12 | 13.0065 | 6.44 | 0.54 |


---

## 7. Gráfico de Tempo de Execução

![Gráfico Tempo Execução](tempo.execucao.png)

---

## 8. Gráfico de Speedup

![Gráfico Speedup](speedup.png)

---

## 9. Gráfico de Eficiência

![Gráfico Eficiência](eficiencia.png)

---

## 10. Discussão e Análise

Ao contrário de simulações com matemática simples, processar arquivos de texto exige uma carga pesada tanto da CPU quanto de entrada/saída (I/O). Por conta dessa característica, aplicar paralelismo apresenta um impacto bastante positivo e notável.

O salto de 1 para 2 processos reduziu o tempo drasticamente, entregando um ganho de desempenho de 1.81x. Essa melhora continuou escalando progressivamente até a marca de 8 processos, atingindo um speedup de 6.05x. Contudo, ao adicionar 12 processos, a redução de tempo foi bem menor (caindo apenas de 14.85s para 13.01s). Isso evidencia que a arquitetura atingiu o teto dos recursos físicos disponíveis no sistema (6 núcleos e 12 threads).

A métrica de eficiência permaneceu sólida e útil até 8 processos (0.76). No entanto, despencou para 0.54 com a carga de 12 processos. Esse declínio é o comportamento esperado: quando o número de processos ultrapassa os núcleos físicos, o custo extra de administrar as threads simultâneas e a disputa pela leitura do disco acabam diminuindo o ganho.


---

## 11. Conclusão Final e Análise Crítica

A experimentação realizada com o módulo `multiprocessing` permitiu validar, de forma prática, os benefícios e as limitações do paralelismo em tarefas de processamento intensivo de dados.

### Principais Constatações:
1. **Escalabilidade e Desempenho:** O sistema apresentou um ganho de performance expressivo ao transitar da execução sequencial para a paralela. A configuração com 12 processos atingiu a marca de **13.0065 segundos**, representando uma aceleração (**Speedup**) de **6.44x** em relação ao método original.
   
2. **Impacto do I/O e CPU:** Diferente de cálculos puramente matemáticos, o processamento de logs envolve uma carga mista de leitura de disco (I/O) e análise de strings (CPU). O paralelismo mostrou-se altamente eficaz aqui porque, enquanto um processo aguarda a leitura de um ficheiro, outros podem continuar a processar dados já carregados na memória.

3. **Ponto de Diminuição de Retorno:** Observou-se que a eficiência caiu de **0.76 (8 processos)** para **0.54 (12 processos)**. Este fenómeno ocorre porque o processador utilizado possui 6 núcleos físicos. Ao utilizar 12 processos (o limite das threads lógicas), o ganho marginal de tempo torna-se menor devido ao *overhead* de gestão do Sistema Operativo e à disputa pelos recursos de hardware (cache e barramento de memória).

