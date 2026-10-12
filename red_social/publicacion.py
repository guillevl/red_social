from abc import ABC, abstractmethod

LIMTE_CARACTERES = 280
class Publicacion(ABC):
    def __init__(self, autor, texto):

        if not texto.strip():
            raise ValueError("El texto de la publicación no puede estar vacío.")

        if len(texto) > LIMTE_CARACTERES:
            raise ValueError(f"El texto de la publicación no puede superar los {LIMTE_CARACTERES} caracteres.")
        
        self.autor = autor
        self.texto = texto
        self.me_gusta = 0

    @abstractmethod
    def __str__(self):
        pass

    @staticmethod
    def extraer_hashtags(texto):
        hastags = []

        for palabra in texto.split():
            if palabra.startswith("#"):
                hashtag = palabra.lower().strip(",.;:!?¡¿")

                if hashtag != "#" and hashtag not in hastags:
                    hastags.append(hashtag)

        return hastags

    @property
    def hashtags(self):
        return self.extraer_hashtags(self.texto)

    def dar_me_gusta(self):
        self.me_gusta += 1

class Tweet(Publicacion):
    def __str__(self):
        return f"{self.autor.alias}: {self.texto}"

class Respuesta(Publicacion):
    def __init__(self, autor, texto, original):
        super().__init__(autor, texto)
        self.original = original

    def __str__(self):
        return f"{self.autor.alias} ↩ {self.original.autor.alias}: {self.texto}"

class Retweet(Publicacion):
    def __init__(self, autor, original):
        super().__init__(autor, original.texto)
        self.original = original

    def __str__(self):
        return f"{self.autor.alias} 🔁 {self.original}"