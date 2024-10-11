import pygame #Biblioteca principal para el desarrollo de juegos en Python.
import random #Módulo de Python para generar números aleatorios.
import os #Añade esta importación

#Inicializar Pygame
pygame.init()

#Configuraciones básicas
ANCHO = 500 #Ancho de la ventana del juego
ALTO = 650 #Alto de la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO)) #Crear la ventana del juego
pygame.display.set_caption("Galaga en Python") #Establecer el título de la ventana

#Definición de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

#Configuración de los frames por segundo
FPS = 60

#Fuente para el texto
fuente = pygame.font.Font(None, 36)

#Clase para las balas del jugador
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -10
    
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

#Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, todas_las_sprites, balas):
        super().__init__()
        # Cargar la imagen de la nave
        ruta_imagen = os.path.join("assets", "Nave.PNG")
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 38))  # Ajusta el tamaño si es necesario
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2 #Posición inicial en x
        self.rect.bottom = ALTO - 10 #Posición inicial en y
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.todas_las_sprites = todas_las_sprites
        self.balas = balas
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = 250 #Tiempo mínimo entre disparos (en milisegundos)
    
    def update(self):
        #Actualizar la posición del jugador basado en las teclas presionadas
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
        if teclas[pygame.K_UP]:
            self.velocidad_y = -5
        if teclas[pygame.K_DOWN]:
            self.velocidad_y = 5
        
        #Disparar si la barra espaciadora está presionada
        if teclas[pygame.K_SPACE]:
            self.disparar()
        
        #Aplicar el movimiento
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        #Mantener al jugador dentro de los límites de la pantalla
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < ALTO // 2:
            self.rect.top = ALTO // 2
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

    def disparar(self):
        #Crear una nueva bala si ha pasado suficiente tiempo desde el último disparo
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            bala = Bala(self.rect.centerx, self.rect.top)
            self.todas_las_sprites.add(bala)
            self.balas.add(bala)
            self.ultimo_disparo = ahora

#Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, nivel, todas_las_sprites, balas_enemigas):
        super().__init__()
        # Cargar la imagen del enemigo
        ruta_imagen = os.path.join("assets", "Enemigos.png")
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 38))
        self.image = pygame.transform.flip(self.image, False, True)  # Voltear verticalmente
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(1, 3) + nivel // 5
        self.todas_las_sprites = todas_las_sprites
        self.balas_enemigas = balas_enemigas
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = random.randint(1000, 3000)  # Entre 1 y 3 segundos
    
    def update(self):
        #Mover el enemigo hacia abajo
        self.rect.y += self.velocidad_y
        #Si el enemigo sale de la pantalla, reposicionarlo arriba
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
        
        # Lógica de disparo
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            self.disparar()
            self.ultimo_disparo = ahora

    def disparar(self):
        bala = BalaEnemiga(self.rect.centerx, self.rect.bottom)
        self.todas_las_sprites.add(bala)
        self.balas_enemigas.add(bala)

class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad_y = 5
    
    def update(self):
        #Mover la bala hacia arriba
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.kill()

#Función para mostrar texto en pantalla
def dibujar_texto(superficie, texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie_texto = fuente.render(texto, True, BLANCO)
    rect_texto = superficie_texto.get_rect()
    rect_texto.midtop = (x, y)
    superficie.blit(superficie_texto, rect_texto)

#Función para el menú principal
def menu_principal():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

        pantalla.fill(NEGRO)
        dibujar_texto(pantalla, "GALAGA", 64, ANCHO // 2, ALTO // 4)
        dibujar_texto(pantalla, "Presiona ENTER para jugar", 22, ANCHO // 2, ALTO // 2)
        dibujar_texto(pantalla, "Presiona ESC para salir", 22, ANCHO // 2, ALTO // 2 + 40)
        pygame.display.flip()

#Función principal del juego
def juego():
    #Crear grupos de sprites
    todas_las_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    balas_enemigas = pygame.sprite.Group()

    #Crear el jugador
    jugador = Jugador(todas_las_sprites, balas)
    todas_las_sprites.add(jugador)

    #Crear menos enemigos iniciales
    for _ in range(4):  # Cambiado de 8 a 4
        enemigo = Enemigo(1, todas_las_sprites, balas_enemigas)
        todas_las_sprites.add(enemigo)
        enemigos.add(enemigo)

    #Configurar el reloj para controlar FPS
    reloj = pygame.time.Clock()

    #Inicializar variables de juego
    puntaje = 0
    nivel = 1
    enemigos_eliminados = 0

    #Ciclo principal del juego
    ejecutando = True
    while ejecutando:
        #Mantener FPS constante
        reloj.tick(FPS)

        #Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

        #Actualizar todos los sprites
        todas_las_sprites.update()

        #Revisar colisiones entre balas y enemigos
        impactos = pygame.sprite.groupcollide(enemigos, balas, True, True)
        for impacto in impactos:
            puntaje += 1
            enemigos_eliminados += 1
            enemigo = Enemigo(nivel, todas_las_sprites, balas_enemigas)
            todas_las_sprites.add(enemigo)
            enemigos.add(enemigo)

            #Aumentar nivel cada 10 enemigos eliminados
            if enemigos_eliminados % 10 == 0:
                nivel += 1
                #Añadir nuevos enemigos cada nivel
                for _ in range(2):
                    enemigo = Enemigo(nivel, todas_las_sprites, balas_enemigas)
                    todas_las_sprites.add(enemigo)
                    enemigos.add(enemigo)

        #Revisar colisiones entre jugador y enemigos
        impactos = pygame.sprite.spritecollide(jugador, enemigos, False)
        if impactos:
            return True

        #Revisar colisiones entre jugador y balas enemigas
        impactos_balas_enemigas = pygame.sprite.spritecollide(jugador, balas_enemigas, True)
        if impactos_balas_enemigas:
            return True

        #Dibujar todo en la pantalla
        pantalla.fill(NEGRO)
        todas_las_sprites.draw(pantalla)
        dibujar_texto(pantalla, f"Puntaje: {puntaje}", 22, ANCHO // 2, 10)
        dibujar_texto(pantalla, f"Nivel: {nivel}", 22, ANCHO - 60, 10)

        #Actualizar la pantalla
        pygame.display.flip()

    return False

#Bucle principal del programa
while True:
    jugar = menu_principal()
    if not jugar:
        break
    game_over = juego()
    if not game_over:
        break

#Salir del juego
pygame.quit()
