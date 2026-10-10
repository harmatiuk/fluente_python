"""
Exercício: Modelo de Dados do Python aplicado a Engenharia de Dados
====================================================================

Contexto
--------
Seu pipeline consome eventos (ex.: de um tópico Pub/Sub) e os agrupa em lotes
antes de gravar no BigQuery. Hoje cada lote é uma `list[dict]` solta, e o
código está cheio de `len(lote["rows"])`, `lote["rows"][0:500]`,
`[r["valor"] for r in lote["rows"]]`...

Sua missão: criar a classe `RecordBatch`, que se comporta como uma coleção
nativa do Python, usando APENAS métodos especiais (dunder methods).

Exemplo de uso esperado
-----------------------
    >>> schema = ("id", "evento", "valor")
    >>> lote = RecordBatch(schema, [
    ...     {"id": 1, "evento": "click", "valor": 10.0},
    ...     {"id": 2, "evento": "view",  "valor": 3.5},
    ...     {"id": 3, "evento": "click", "valor": 7.25},
    ... ])
    >>> len(lote)
    3
    >>> lote[0]
    {'id': 1, 'evento': 'click', 'valor': 10.0}
    >>> lote[1:]                      # fatia -> novo RecordBatch
    RecordBatch(schema=('id', 'evento', 'valor'), rows=2)
    >>> lote["valor"]                 # acesso por coluna
    [10.0, 3.5, 7.25]
    >>> [r["id"] for r in lote]       # iteração "de graça"
    [1, 2, 3]
    >>> lote + lote                   # concatenação
    RecordBatch(schema=('id', 'evento', 'valor'), rows=6)
    >>> bool(RecordBatch(schema, []))
    False

Requisitos
----------
1. __init__(schema, rows)
   - `schema` é uma tupla com os nomes das colunas.
   - Cada linha deve ter EXATAMENTE as chaves do schema; caso contrário,
     levante ValueError (dica: compare conjuntos).
   - Guarde uma cópia da lista de linhas (não a referência original).

2. __len__  -> número de linhas.

3. __getitem__(key) -> o comportamento depende do TIPO da chave:
   - int    -> retorna a linha (dict). Índices negativos devem funcionar.
   - slice  -> retorna um NOVO RecordBatch com o mesmo schema.
   - str    -> retorna a lista de valores daquela coluna.
               Coluna inexistente -> KeyError.
   - outro  -> TypeError.

4. __repr__ -> RecordBatch(schema=('id', 'evento', 'valor'), rows=3)
   (Não imprima as linhas: um lote pode ter milhões.)

5. __add__(other)
   - Concatena dois lotes e retorna um NOVO RecordBatch.
   - Schemas diferentes -> ValueError.
   - Se `other` não for RecordBatch, retorne NotImplemented
     (NÃO levante a exceção você mesmo; por quê?).

6. __eq__(other) -> True se schema e linhas forem iguais.
   Se `other` não for RecordBatch, retorne NotImplemented.

Restrições
----------
- NÃO implemente __iter__, __bool__ nem __contains__.
  Os testes verificam que iteração, `bool()` e `in` funcionam mesmo assim.

Bônus (opcional)
----------------
- `lote * 2` repete as linhas (como `lista * 2`).
- Um método `chunks(n)` que gera sub-lotes de até `n` linhas, útil para
  respeitar o limite de linhas por request de inserção.
- Transforme `schema` em atributo somente leitura com @property.

Como validar
------------
    pip install pytest
    pytest test_record_batch.py -v
"""


class RecordBatch:
    def __init__(
            self,
            schema: tuple[str, ...],
            rows: list[dict]
            ):
        self.schema = schema
        self.rows = rows.copy()
        self._valid_schema()

    def _valid_schema(self):
        for row in self.rows:
            if set(row) != set(self.schema):
                raise ValueError(f'evento {row} não bate com o schema {self.schema}')

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key]
        if isinstance(key, slice):
            return RecordBatch(self.schema, self.rows[key])
        if isinstance(key, str):
            if key not in self.schema:
               raise KeyError(key)
            return [element[key] for element in self.rows]
        raise TypeError(f'chave inválida: {type(key).__name__}')
    
    def __repr__(self):
        return f"RecordBatch(schema={self.schema}, rows={len(self.rows)})"

    def __eq__(self, other):
        if not isinstance(other, RecordBatch):
            return NotImplemented
        return self.schema == other.schema and self.rows == other.rows
   
    def __add__(self, other):
        if not isinstance(other, RecordBatch):
            return NotImplemented
        if self.schema != other.schema:
            raise ValueError(f"schemas diferentes: {self.schema} != {other.schema}")
        return RecordBatch(self.schema, self.rows + other.rows)
        

