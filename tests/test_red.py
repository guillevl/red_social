import json

from red_social.publicacion import Tweet
from red_social.red import RedSocial


def test_timeline_solo_tiene_publicaciones_de_los_seguidos(red):
    ana = red["@ana"]
    luis = red["@luis"]
    marta = red["@marta"]

    primero = red.publicar(Tweet(ana, "Primer tweet"))

    red.publicar(Tweet(luis, "Tweet de Luis"))
    red.publicar(Tweet(marta, "Tweet de Marta"))

    segundo = red.publicar(Tweet(ana, "Segundo tweet"))

    assert red.timeline(luis) == [segundo, primero]
    assert red.timeline(ana) == []

def test_desde_json_construye_usuarios_y_seguimientos(mocker):

    datos = {
        "usuarios": [
            {"nombre": "Ana", "alias": "@ana"},
            {"nombre": "Luis", "alias": "@luis"},
        ],
        "seguimientos": [
            ["@luis", "@ana"],
        ]
    }

    
    apertura =  mocker.mock_open(read_data=json.dumps(datos))
    mocker.patch("builtins.open", apertura)

    red = RedSocial.desde_json("tests/datos_red.json")

    apertura.assert_called_once_with("tests/datos_red.json", encoding="utf-8")

    assert len(red) == 2
    assert red["@ana"].nombre == "Ana"
    assert red["@luis"].nombre == "Luis"
    assert red["@luis"].sigue_a(red["@ana"])
    assert not red["@ana"].sigue_a(red["@luis"])