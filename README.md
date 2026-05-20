# Desempenho Acadêmico: alunos que estudam por mais horas têm melhores notas?

### Desenvolvido por:
#### Alana Silva Sales
#### Guilherme Leitão Bastos
#### Marcelo Antônio Dantas Filho
#### Marcos Martenier Santos Oliveira

---

## Introdução

Este projeto, desenvolvido para a disciplina de Probabilidade e Estatística, no curso de Engenharia de Computação, apresenta uma análise exploratória de dados sobre desempenho acadêmico, com foco na relação entre tempo semanal de estudo e nota final dos alunos.

A pergunta central do estudo é:

**Alunos que estudam por mais horas tendem a obter melhores notas finais?**

Para responder a essa pergunta, foi utilizada uma base de dados real, a **Student Performance**, disponibilizada pela UCI Machine Learning Repository. A análise foi desenvolvida em Python, utilizando estatística descritiva, visualizações gráficas e métodos estatísticos apropriados para variáveis ordinais.

## Base de dados

Este projeto utiliza o arquivo `student-mat.csv`, referente ao desempenho de alunos na disciplina de Matemática.

Fonte da base:

https://archive.ics.uci.edu/dataset/320/student+performance

O arquivo da base está localizado em:

```text
data/student-mat.csv
```

Caso seja necessário baixar novamente:

1. Acesse a página da base na UCI.
2. Baixe os arquivos da base **Student Performance**.
3. Extraia o arquivo `student-mat.csv`.
4. Coloque o arquivo dentro da pasta `data/`.

## Variáveis analisadas

A análise utiliza duas variáveis principais:

- `studytime`: tempo semanal de estudo, representado por categorias ordinais.
- `G3`: nota final do aluno em Matemática, em escala de 0 a 20.

As categorias de `studytime` são:

| Código | Interpretação |
| --- | --- |
| 1 | menos de 2 horas |
| 2 | de 2 a 5 horas |
| 3 | de 5 a 10 horas |
| 4 | mais de 10 horas |

## Objetivo

O objetivo do projeto é investigar se existe associação entre o tempo semanal de estudo e o desempenho final dos alunos. Para isso, busca-se observar:

- a distribuição das notas;
- a frequência das categorias de estudo;
- diferenças entre grupos de tempo de estudo;
- a intensidade da associação entre as variáveis.

O estudo não tem como objetivo provar causalidade. Ou seja, mesmo que exista alguma tendência positiva, não é possível afirmar apenas com esses dados que estudar mais causa diretamente notas maiores, já que fatores externos também podem influenciar o desempenho acadêmico.

## Como a análise foi feita

O arquivo `analise_student.py` executa as seguintes etapas:

- carregamento da base de dados;
- seleção das variáveis `studytime` e `G3`;
- verificação de tipos e valores nulos;
- limpeza básica dos dados;
- cálculo de estatísticas descritivas;
- geração de histogramas, boxplots e gráfico de barras;
- cálculo da correlação de Spearman;
- comparação entre grupos usando o teste de Kruskal-Wallis;
- cálculo do tamanho do efeito utilizando epsilon squared (`ε²`).

A escolha desses métodos foi feita porque `studytime` é uma variável qualitativa ordinal agrupada em categorias, o que torna inadequado o uso de regressão linear simples e correlação de Pearson como análise principal, o que era realizado na versão anterior.

## Estrutura do projeto

```text
.
|-- analise_student.py
|-- requirements.txt
|-- data/
|   |-- student-mat.csv
|-- outputs/
|   |-- histograma_g3.png
|   |-- boxplot_g3.png
|   |-- barras_studytime.png
|   |-- boxplot_studytime_g3.png
```

## Como instalar as dependências

```bash
pip install -r requirements.txt
```

Se estiver usando ambiente virtual:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Como executar

```bash
python analise_student.py
```

Ou, usando diretamente a `venv` no Windows:

```bash
.\.venv\Scripts\python.exe analise_student.py
```

## Resultados descritivos

A base analisada possui **395 alunos** e não apresentou valores nulos nas variáveis selecionadas.

Resumo das principais medidas:

| Variável | Média | Mediana | Moda | Desvio padrão | Mínimo | Máximo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `studytime` | 2.04 | 2.00 | 2 | 0.84 | 1 | 4 |
| `G3` | 10.42 | 11.00 | 10 | 4.58 | 0 | 20 |

A categoria de tempo de estudo mais frequente foi **2 - de 2 a 5 horas**. A faixa de notas mais comum foi **10 a 14**.

## Visualizações e interpretações

### Histograma das notas finais

![Histograma das notas finais](outputs/histograma_g3.png)

O histograma mostra a distribuição das notas finais `G3`. A maior concentração de alunos aparece em notas intermediárias, especialmente entre 10 e 14 pontos. Também existem notas muito baixas, inclusive valores próximos de 0, o que mostra uma dispersão considerável no desempenho.

### Boxplot das notas finais

![Boxplot das notas finais](outputs/boxplot_g3.png)

O boxplot resume a distribuição da nota final. A mediana está em torno de 11, indicando que metade dos alunos ficou abaixo desse valor e metade acima. A caixa concentra a parte central dos dados, aproximadamente entre 8 e 14 pontos, enquanto as hastes mostram a variação geral das notas.

```text
O gráfico aparece dessa forma porque `G3` é uma variável numérica em escala de 0 a 20. Como muitos alunos estão concentrados em notas intermediárias, a caixa fica posicionada no centro da escala. A presença de notas baixas amplia a variação inferior da distribuição.
```

### Distribuição do tempo semanal de estudo

![Grafico de barras do tempo de estudo](outputs/barras_studytime.png)

O gráfico de barras mostra quantos alunos existem em cada categoria de `studytime`. A maior parte dos estudantes está na categoria 2, equivalente a 2 a 5 horas semanais de estudo. As categorias 3 e 4 possuem menos alunos, especialmente a categoria 4, com mais de 10 horas semanais.

Essa visualização ajuda a entender que a amostra não está igualmente distribuída entre os grupos de tempo de estudo. Portanto, comparações entre categorias devem considerar que algumas possuem muito menos observações do que outras.

### Notas finais por categoria de tempo de estudo

![Boxplot studytime x G3](outputs/boxplot_studytime_g3.png)

O boxplot por categoria de estudo permite comparar a distribuição das notas finais entre os grupos de `studytime`.

Cada caixa representa uma categoria de tempo semanal de estudo, enquanto a posição vertical indica a distribuição das notas `G3` naquele grupo.

Observa-se uma leve tendência de aumento das medianas das notas conforme cresce a categoria de estudo. Entretanto, também existe grande dispersão interna dentro de todos os grupos, indicando que alunos com tempos de estudo semelhantes ainda apresentam desempenhos bastante variados.

Esse comportamento sugere que o tempo de estudo pode estar associado ao desempenho acadêmico, mas provavelmente não é o único fator relevante para explicar as diferenças nas notas finais.

## Associação entre tempo de estudo e nota final

### Correlação de Spearman

A correlação de Spearman entre `studytime` e `G3` foi:

```text
ρ = 0.143
```

Esse valor indica uma associação positiva, porém **fraca**. Em termos práticos, existe uma pequena tendência de que alunos em categorias maiores de estudo apresentem notas um pouco maiores.

A correlação de Spearman foi utilizada porque `studytime` é uma variável ordinal categorizada em faixas de horas, e não uma variável contínua. Dessa forma, Spearman é mais apropriado que Pearson para avaliar associações monotônicas entre as variáveis.

## Comparação entre grupos: Kruskal-Wallis

Para verificar se existem diferenças estatisticamente significativas entre os grupos de tempo de estudo, foi utilizado o teste não paramétrico de Kruskal-Wallis.

Resultados obtidos:

```text
H = 7.854
p-valor = 0.049
```

Como o p-valor foi menor que 0.05, conclui-se que existem diferenças estatisticamente significativas entre pelo menos alguns dos grupos de tempo de estudo.

Isso sugere que o desempenho dos alunos varia de forma relevante entre as categorias de estudo analisadas.

## Tamanho do efeito: epsilon squared

O tamanho do efeito foi medido utilizando epsilon squared (`ε²`), apropriado para análises não paramétricas associadas ao teste de Kruskal-Wallis.

Resultado obtido:

```text
ε² = 0.012
```

Esse valor representa um **efeito pequeno**.

Em termos práticos, isso significa que o tempo semanal de estudo possui alguma associação com o desempenho acadêmico, mas explica apenas uma pequena parcela da variação observada nas notas finais.

Mesmo havendo diferença estatisticamente significativa entre os grupos, o impacto isolado de `studytime` sobre `G3` é limitado.

## Considerações finais

A análise realizada indica que há uma associação positiva entre tempo semanal de estudo e nota final, mas essa associação é fraca.

Os alunos que declaram estudar por mais tempo apresentam, em média, notas ligeiramente maiores, especialmente nas categorias de 5 a 10 horas e mais de 10 horas semanais. Entretanto, existe grande variabilidade nas notas dentro de todos os grupos de estudo.

Os testes estatísticos indicaram que:

- existe associação monotônica positiva entre `studytime` e `G3`;
- existem diferenças estatisticamente significativas entre os grupos de estudo;
- o tamanho do efeito observado é pequeno.

Esses resultados mostram que o tempo de estudo possui relação com o desempenho acadêmico, mas não é suficiente para explicar sozinho a maior parte das diferenças nas notas finais.

Isso sugere que outros fatores presentes na base podem ter papel relevante na explicação do desempenho dos estudantes.

Dessa forma, o estudo contribui para compreender que estudar mais pode estar associado a melhores resultados, mas essa relação deve ser analisada com cautela. No conjunto de dados observado, o tempo de estudo apresenta uma tendência favorável, porém limitada.

Portanto, com base nesta análise exploratória, conclui-se que alunos que estudam por mais horas tendem a apresentar notas um pouco maiores, mas o tempo de estudo isoladamente não explica de forma significativa o desempenho acadêmico final.