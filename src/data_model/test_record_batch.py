from pytest import fixture, raises
from record_batch import RecordBatch

@fixture
def schema():
    return ("id", "evento", "valor")

@fixture
def data():
    data = [
        {"id": 1, "evento": "click", "valor": 10.0},
        {"id": 2, "evento": "view",  "valor": 3.5},
        {"id": 3, "evento": "click", "valor": 7.25},
    ]           
    return data

@fixture
def lote(schema, data):
    return RecordBatch(schema, data)

@fixture
def lote_vazio(schema):
    return RecordBatch(schema, [])

def test_len_lote(lote: RecordBatch):
    assert len(lote) == 3

def test_copy_init(data, lote):
    data.clear()
    assert len(lote) == 3

def test_get_item_int_um(lote):
    assert lote[0] == {"id": 1, "evento": "click", "valor": 10.0}

def test_get_item_int_menos_um(lote):
    assert lote[-1] == {"id": 3, "evento": "click", "valor": 7.25}

def test_get_item_str_column(lote):
    assert lote['valor'] == [10.0, 3.5, 7.25]

def test_interecao_sem_iter(lote):
    ids = [item['id'] for item in lote]
    assert ids == [1, 2, 3]

def test_coluna_inexistente(lote):
    with raises(KeyError):
        lote['some_value']

def test_coluna_inexistente_em_lote_vazio_levanta_key_error(lote_vazio):
    with raises(KeyError):
        lote_vazio['some_value']

def test_chave_tipo_invalido_levanta_type_error(lote):
    with raises(TypeError):
        lote[1.5]

def test_slice_lote(lote, data):
    fatia = lote[1:]
    assert isinstance(fatia, RecordBatch)
    assert len(fatia) == 2
    assert fatia[0] == data[1]

def test_evento_sem_chave_do_schema_levanta_value_error(schema):
    rows = [
        {"id": 1, "evento": "click", "valor": 10.0},
        {"id": 2, "evento": "view"}, # ← falta "valor"
        {"id": 3, "evento": "click", "valor": 7.25},
    ]

    with raises(ValueError):
        RecordBatch(schema, rows)

def test_evento_com_chave_extra_levanta_value_error(schema):
    rows = [
        {"id": 1, "evento": "click", "valor": 10.0},
        {"id": 2, "evento": "view", "valor": 3.5, "extra": 0},   # ← sobra "extra"
    ]

    with raises(ValueError):
        RecordBatch(schema, rows)

def test_repr(lote):
    assert repr(lote) == "RecordBatch(schema=('id', 'evento', 'valor'), rows=3)"

def test_lotes_com_mesmo_conteudo_sao_iguais(schema, data):
    lote1 = RecordBatch(schema, data)
    lote2 = RecordBatch(schema, data)

    assert lote1 == lote2

def test_lotes_com_linhas_diferentes_nao_sao_iguais(schema, data):
    lote1 = RecordBatch(schema, data)
    lote2 = RecordBatch(schema, data[:2]) # somente as duas primeiras linhas

    assert lote1 != lote2

def test_cocatenacao_de_dois_lotes(schema, data):
    lote1 = RecordBatch(schema, data[:1]) # id 1
    lote2 = RecordBatch(schema, data[1:]) # id 2 e 3
    lote_concatenado = lote1 + lote2

    assert lote_concatenado == RecordBatch(schema, data)

def test_cacatencao_de_schemas_diferentes_levanta_value_error(schema, data):
    lote1 = RecordBatch(schema, data)
    lote2 = RecordBatch(('valor', 'id', 'evento'), data)

    with raises(ValueError):
        lote1 + lote2