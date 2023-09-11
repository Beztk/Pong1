import pygame
import math
from random import randint

ANCHO = 800
ALTO = 600
FPS = 60
C_FONDO = pygame.image.load("tennis.jpg")
LETRA_SIZE = 50

C_OBJETOS = (50, 50, 50)
VEL_JUGADOR = 10
ANCHO_PALA = 20
ALTO_PALA = 60
ARRIBA = True
ABAJO = False

MARGEN1 = 21
MARGEN2 = 755
TAM_PELOTA = 10
VEL_MAXIMA = 5
VARIACION_VEL_PELOTA = 5

MAXIMA_PUNTUACION = 2


class Pelota(pygame.Rect):
    def __init__(self):
        super(Pelota, self).__init__((ANCHO-TAM_PELOTA)/2,
                                     (ALTO-TAM_PELOTA)/2, TAM_PELOTA, TAM_PELOTA)
        # definición del rectángulo
        self.velocidad_y = randint(-VEL_MAXIMA, VEL_MAXIMA)
        self.velocidad_x = 0
        while self.velocidad_x == 0:
            self.velocidad_x = randint(-VEL_MAXIMA, VEL_MAXIMA)

    def pintame(self, pantalla):
        # pintar el rectángulo
        pygame.draw.rect(pantalla, C_OBJETOS, self)

    def mover(self):
        # dirección: incremento x, incremento y --> velocidad_x, velocidad_y
        # posición actual, (x, y)
        self.left = self.left + self.velocidad_x
        self.top = self.top + self.velocidad_y

        if self.y <= 0:
            self.y = 0
            self.velocidad_y = -self.velocidad_y

        if self.y >= ALTO-TAM_PELOTA:
            self.y = ALTO-TAM_PELOTA
            self.velocidad_y = -self.velocidad_y

    def comprobar_punto(self):

        if self.right <= 0:
            self.center = (ALTO / 2, ANCHO / 2)
            self.velocidad_y = randint(-VEL_MAXIMA, VEL_MAXIMA)
            self.velocidad_x = randint(-VEL_MAXIMA, -1)
            return 2
        if self.left >= ANCHO:
            self.center = (ALTO / 2, ANCHO / 2)
            self.velocidad_y = randint(-VEL_MAXIMA, VEL_MAXIMA)
            self.velocidad_x = randint(1, VEL_MAXIMA)
            return 1
        return 0


class Marcador:
    def __init__(self):
        self.reset()

    def incrementar(self, jugador):
        self.puntos[jugador-1] += 1

    def reset(self):
        self.puntos = [0, 0]

    def pintame(self, pantalla):
        fuente = pygame.font.Font("freesansbold.ttf", 32)
        texto_x = 56
        texto_y = 10
        texto1 = fuente.render(
            f"Puntaje: {self.puntos[0]}", True, (10, 10, 10))
        pantalla.blit(texto1, (texto_x, texto_y))
        fuente = pygame.font.Font("freesansbold.ttf", 32)
        texto_x = 556
        texto_y = 10
        texto2 = fuente.render(
            f"Puntaje: {self.puntos[1]}", True, (10, 10, 10))
        pantalla.blit(texto2, (texto_x, texto_y))
        fuente = pygame.font.Font("freesansbold.ttf", 32)
        texto_x = 250
        texto_y = 560
        texto2 = fuente.render("Hecho por Santi G.", True, (10, 10, 10))
        pantalla.blit(texto2, (texto_x, texto_y))

    def comprobar_ganador(self):
        if self.puntos[0] == MAXIMA_PUNTUACION:
            return 1
        if self.puntos[1] == MAXIMA_PUNTUACION:
            return 2
        return 0


class Jugador(pygame.Rect):
    def __init__(self, x, y):
        super(Jugador, self).__init__(x, y, ANCHO_PALA, ALTO_PALA)

    def pintame(self, pantalla):
        pygame.draw.rect(pantalla, C_OBJETOS, self)

    def mover(self, direccion):
        if direccion == ARRIBA:
            if self.y <= 0:
                self.y = 0
            else:
                self.y -= VEL_JUGADOR
        if direccion == ABAJO:
            if self.y >= ALTO-ALTO_PALA:
                self.y = ALTO-ALTO_PALA
            else:
                self.y += VEL_JUGADOR


class Pong:
    def __init__(self,) -> None:
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        pos_y = (ALTO - ALTO_PALA) / 2
        self.pelota = Pelota()
        self.jugador1 = Jugador(21, pos_y)
        self.jugador2 = Jugador(755, pos_y)
        self.marcador = Marcador()

        pygame.display.set_caption("Ping - Pong")
        icono = pygame.image.load("ping-pong.png")
        pygame.display.set_icon(icono)

    def jugar(self):

        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE):
                    salir = True

            self.comprobar_teclas()
            # Fondo
            self.pantalla.blit(C_FONDO, (0, 0))

            # Paletas de los jugadores
            self.jugador1.pintame(self.pantalla)
            self.jugador2.pintame(self.pantalla)

            hay_ganador = self.marcador.comprobar_ganador()
            if hay_ganador > 0:
                salir = salir or self.finalizar_partida(hay_ganador)
            else:
                self.comprobar_teclas()
                self.pintar_pelota()
                hay_punto = self.pelota.comprobar_punto()
                if hay_punto > 0:
                    self.marcador.incrementar(hay_punto)
                    self.jugador1 = Jugador(21, (ALTO - ALTO_PALA) / 2)
                    self.jugador2 = Jugador(755, (ALTO - ALTO_PALA) / 2)

            self.marcador.pintame(self.pantalla)

            pygame.display.flip()
            self.reloj.tick(FPS)

        pygame.quit()

    def finalizar_partida(self, hay_ganador):
        mensaje = f"Ha ganado el jugador {hay_ganador}"
        fuente = pygame.font.Font("freesansbold.ttf", LETRA_SIZE)
        texto = fuente.render(mensaje, True, (10, 10, 10))
        self.pantalla.blit(texto, (110, 250))

        mensaje = "Otra partida (s/n)"
        fuente = pygame.font.Font("freesansbold.ttf", 20)
        texto = fuente.render(mensaje, True, (10, 10, 10))
        self.pantalla.blit(texto, (100, 50))

        estado_teclas = pygame.key.get_pressed()
        if estado_teclas[pygame.K_s]:
            self.marcador.reset()
            return False
        if estado_teclas[pygame.K_n]:
            return True

    def comprobar_teclas(self):
        estado_teclas = pygame.key.get_pressed()
        if estado_teclas[pygame.K_a]:
            self.jugador1.mover(ARRIBA)
        if estado_teclas[pygame.K_z]:
            self.jugador1.mover(ABAJO)
        if estado_teclas[pygame.K_UP]:
            self.jugador2.mover(ARRIBA)
        if estado_teclas[pygame.K_DOWN]:
            self.jugador2.mover(ABAJO)

    def pintar_pelota(self):
        self.pelota.mover()
        if self.pelota.colliderect(self.jugador1):
            self.pelota.velocidad_x = randint(1, VEL_MAXIMA)
            self.pelota.velocidad_y = randint(-VEL_MAXIMA, VEL_MAXIMA)
        if self.pelota.colliderect(self.jugador2):
            self.pelota.velocidad_x = randint(-VEL_MAXIMA, -1)
            self.pelota.velocidad_y = randint(-VEL_MAXIMA, VEL_MAXIMA)

        self.pelota.pintame(self.pantalla)


if __name__ == "__main__":
    juego = Pong()
    juego.jugar()
