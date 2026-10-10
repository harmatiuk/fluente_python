# Python Fluente — exercícios

Repositório de estudo do livro **Python Fluente** (*Fluent Python*, 2ª edição, Luciano Ramalho).

## Objetivo

Aprofundar o conhecimento da linguagem Python fazendo exercícios práticos com o conteúdo de cada capítulo do livro.

Os exercícios usam cenários de **engenharia de dados**, como eventos do Pub/Sub e lotes gravados no BigQuery. Assim, cada conceito do livro é aplicado a um problema parecido com os do dia a dia, e não só a exemplos isolados.

## Onde estamos

📍 **Capítulo 1 — O modelo de dados do Python**

| Capítulo | Tema | Pasta | Status |
|---|---|---|---|
| 1 | O modelo de dados do Python | [`src/data_model/`](src/data_model/) | 🟡 Em andamento |

Exercício atual: [`record_batch.py`](src/data_model/record_batch.py). Ele cria uma classe `RecordBatch` que se comporta como uma coleção nativa usando apenas métodos especiais (`__len__`, `__getitem__`, `__repr__`, `__add__`...).

## Roteiro do livro

<details>
<summary>Ver todos os capítulos</summary>

**Parte I — Estruturas de dados**
1. O modelo de dados do Python
2. Uma coleção de sequências
3. Dicionários e conjuntos
4. Texto Unicode versus bytes
5. Fábricas de classes de dados
6. Referências, mutabilidade e memória

**Parte II — Funções como objetos**

7. Funções como objetos de primeira classe
8. Dicas de tipo em funções
9. Decoradores e closures
10. Padrões de projeto com funções de primeira classe

**Parte III — Classes e protocolos**

11. Um objeto pythônico
12. Métodos especiais para sequências
13. Interfaces, protocolos e ABCs
14. Herança: para o bem ou para o mal
15. Mais dicas de tipo
16. Sobrecarga de operadores

**Parte IV — Controle de fluxo**

17. Iteradores, geradores e corrotinas clássicas
18. Instruções `with`, `match` e blocos `else`
19. Modelos de concorrência em Python
20. Executores concorrentes
21. Programação assíncrona

**Parte V — Metaprogramação**

22. Atributos dinâmicos e propriedades
23. Descritores de atributos
24. Metaprogramação com classes

</details>

## Como cada exercício é organizado

Cada capítulo tem sua própria pasta em `src/`. Um arquivo de exercício traz:

- **Contexto e requisitos**: o problema a resolver, na docstring do módulo.
- **Restrições**: o que *não* pode ser usado, para forçar o conceito do capítulo.
- **Perguntas de reflexão** e **bônus**.
- Um esqueleto para implementar e um bloco `# Respostas das perguntas:` no final.

## Como rodar

Requer Python 3.13 e [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                           # instala as dependências
uv run python src/data_model/record_batch.py      # roda um exercício
uv run pytest src/data_model -v                   # roda os testes do capítulo
```
