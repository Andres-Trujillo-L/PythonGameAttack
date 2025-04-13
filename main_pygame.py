import pygame
import random
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Configuracion de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Space Invaders')
icono = pygame.image.load('Assets/ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Assets/Fondo.jpg')

# Musica de fondo
mixer.music.load('Assets/MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Fuente para puntaje
fuente = pygame.font.SysFont('Arial', 32)
fuente_final = pygame.font.SysFont('Arial', 40)

# Variables globales
puntaje = 0
boss_activado = False

class Jugador:
    def __init__(self):
        self.img = pygame.image.load('Assets/cohete-espacial.png')
        self.x = 364
        self.y = 500
        self.velocidad = 1

    def mover(self, direccion):
        self.x += direccion * self.velocidad
        self.x = max(0, min(self.x, ANCHO - 64))

    def dibujar(self):
        pantalla.blit(self.img, (self.x, self.y))

class Enemigo:
    def __init__(self):
        self.img = pygame.image.load('Assets/monstruo.png')
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 200)
        self.x_cambio = 0.7
        self.y_cambio = 50

    def mover(self):
        self.x += self.x_cambio
        if self.x <= 0 or self.x >= 736:
            self.x_cambio *= -1
            self.y += self.y_cambio

    def dibujar(self):
        pantalla.blit(self.img, (self.x, self.y))

class Bala:
    def __init__(self, x, y, velocidad, imagen):
        self.img = pygame.image.load(imagen)
        self.x = x
        self.y = y
        self.velocidad = velocidad

    def mover(self):
        self.y += self.velocidad

    def dibujar(self):
        pantalla.blit(self.img, (self.x + 16, self.y + 10))

    def fuera_de_pantalla(self):
        return self.y < 0 or self.y > 600

class Boss:
    def __init__(self):
        self.img = pygame.image.load('Assets/jefe.png')
        self.x = 300
        self.y = 50
        self.x_cambio = 1
        self.salud = 10
        self.balas = []

    def mover(self  ):
        self.x += self.x_cambio
        if self.x <= 0 or self.x >= 736:
            self.x_cambio *= -1

    def disparar(self):
        if random.randint(0, 50) == 1:
            self.balas.append(Bala(self.x + 16, self.y + 60, 3, 'Assets/bala2.png'))

    def dibujar(self):
        pantalla.blit(self.img, (self.x, self.y))
        for bala in self.balas:
            bala.mover()
            bala.dibujar()

    def fuera_de_pantalla(self):
        return self.y < 0 or self.y > 600


# Funciones auxiliares
def mostrar_puntaje():
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (10, 10))

def texto_final():
    texto = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(texto, (200, 250))

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia < 27

# Instancias de juego
jugador = Jugador()
enemigos = [Enemigo() for _ in range(8)]
balas_jugador = []
boss = None

# Bucle principal
jugando = True
while jugando:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.mover(-1)
    if teclas[pygame.K_RIGHT]:
        jugador.mover(1)
    if teclas[pygame.K_SPACE]:
        if len(balas_jugador) < 5:
            mixer.Sound('Assets/disparo.mp3').play()
            balas_jugador.append(Bala(jugador.x, jugador.y, -5, 'Assets/bala.png'))

    for enemigo in enemigos:
        enemigo.mover()
        enemigo.dibujar()
        if enemigo.y > 500:
            for e in enemigos:
                e.y = 1000
            texto_final()
            jugando = False

    for bala in balas_jugador[:]:
        bala.mover()
        bala.dibujar()
        if bala.y < 0:
            balas_jugador.remove(bala)

    for enemigo in enemigos:
        for bala in balas_jugador:
            if hay_colision(enemigo.x, enemigo.y, bala.x, bala.y):
                mixer.Sound('Assets/golpe.mp3').play()
                enemigos.remove(enemigo)
                balas_jugador.remove(bala)
                puntaje += 1
                enemigos.append(Enemigo())
                break

    # Activar jefe si corresponde
    if puntaje >= 20 and not boss_activado:
        boss = Boss()
        boss_activado = True

    if boss:
        boss.mover()
        boss.disparar()
        boss.dibujar()
        for bala in boss.balas[:]:
            if hay_colision(jugador.x, jugador.y, bala.x, bala.y):
                texto_final()
                jugando = False
        for bala in balas_jugador[:]:
            if hay_colision(boss.x, boss.y, bala.x, bala.y):
                balas_jugador.remove(bala)
                boss.salud -= 1
                if boss.salud <= 0:
                    boss = None

    jugador.dibujar()
    mostrar_puntaje()
    pygame.display.update()


