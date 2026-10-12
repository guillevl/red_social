import json
from collections import Counter

from red_social.usuario import Usuario


class RedSocial:
    def __init__(self):
        self.usuarios = {}
        self.publicaciones = []

    def anadir(self, usuario):
        if usuario.alias in self.usuarios:
            raise ValueError(f"El alias {usuario.alias} ya está en uso.")
        
        self.usuarios[usuario.alias] = usuario
        return usuario

    def registrar(self, nombre, alias):
        usuario = Usuario(nombre, alias)
        return self.anadir(usuario)

    def publicar(self, publicacion):
        self.publicaciones.append(publicacion)
        return publicacion

    def timeline(self, usuario):
        publicaciones = []

        for publicacion in reversed(self.publicaciones):
            if usuario.sigue_a(publicacion.autor):
                publicaciones.append(publicacion)

        return publicaciones

    def tendencias(self, n=3):
        contador = Counter()

        for publicacion in self.publicaciones:
            contador.update(publicacion.hashtags)

        return contador.most_common(n)

    def mostrar_timeline(self, alias):
        usuario = self[alias]

        print(f"\nTimeline de {usuario}:")
        for publicacion in self.timeline(usuario):
            print(f"  {publicacion}  ♥ {publicacion.me_gusta}")

    def __getitem__(self, alias):
        return self.usuarios[alias]

    def __contains__(self, alias):
        return alias in self.usuarios

    def __len__(self):
        return len(self.usuarios)

    def __iter__(self):
        for alias in sorted(self.usuarios):
            yield self.usuarios[alias]

    @classmethod
    def desde_json(cls, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        red = cls()

        for usuario_datos in datos["usuarios"]:
            usuario = Usuario.desde_dict(usuario_datos)
            red.anadir(usuario)

        for quien_sigue, a_quien in datos["seguimientos"]:
            red[quien_sigue].seguir(red[a_quien])

        return red

