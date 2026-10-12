import pytest  # type: ignore

from red_social.publicacion import Publicacion, Retweet, Tweet


@pytest.mark.parametrize("texto", ["", "   ",  "a" * 281])
def test_texto_invalido_lanza_error(ana, texto):
    with pytest.raises(ValueError):
        Tweet(ana, texto)

@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Un texto sin hashtags", []),
        ("Hola #Python #PYTEST", ["#python", "#pytest"]),
        ("#python y otra vez #python", ["#python"]),
        ("Me gusta #python, y mucho #pytest!", ["#python", "#pytest"]),
    ],
)
def test_extraer_hashtags(texto, esperado):
    assert Publicacion.extraer_hashtags(texto) == esperado

def test_retweet_comparte_el_texto_del_original(tweet, luis):
    retweet = Retweet(luis, tweet)

    assert retweet.original is tweet
    assert retweet.texto == tweet.texto
    assert retweet.hashtags == tweet.hashtags
    assert retweet.autor is luis
    