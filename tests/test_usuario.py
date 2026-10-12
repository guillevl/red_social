import pytest  # type: ignore


def test_seguir_anade_al_otro_usuario(ana, luis):
    ana.seguir(luis)
    assert ana.sigue_a(luis)
    assert ana.numero_seguidos == 1
    assert not luis.sigue_a(ana)

def test_seguirse_a_si_mismo_lanza_error(ana):
    with pytest.raises(ValueError):
        ana.seguir(ana)