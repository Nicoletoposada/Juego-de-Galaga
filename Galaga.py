import pygame #Biblioteca principal para el desarrollo de juegos en Python.
import random #Módulo de Python para generar números aleatorios.
import os #Módulo para interactuar con el sistema operativo, útil para manejar rutas de archivos.

#Inicializar Pygame
pygame.init()

#Configuraciones básicas
ANCHO = 500 #Ancho de la ventana del juego
ALTO = 630 #Alto de la ventana del juego
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
        #Cargar la imagen de la nave
        ruta_imagen = os.path.join("assets", "Nave.PNG")
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 38)) #Ajusta el tamaño si es necesario
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2 #Posición inicial en x
        self.rect.bottom = ALTO - 10 #Posición inicial en y
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.todas_las_sprites = todas_las_sprites
        self.balas = balas
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = 250 #Tiempo mínimo entre disparos (en milisegundos)
        #Modificar atributos de power-ups
        self.power_ups_activos = {}
        self.disparo_triple = False
        self.velocidad_normal = 5
        self.cadencia_normal = 250
        self.vidas = 3
        self.vidas_maximas = 3
        #Color original para el efecto de escudo
        self.color_original = self.image.copy()
        self.ultimo_parpadeo = 0
        self.parpadeo_delay = 200 #milisegundos
        #Cargar imagen de corazón para las vidas
        ruta_corazon = os.path.join("assets", "heart.png")
        try:
            self.imagen_vida = pygame.image.load(ruta_corazon).convert_alpha()
            self.imagen_vida = pygame.transform.scale(self.imagen_vida, (25, 25))
        except (pygame.error, FileNotFoundError):
            self.imagen_vida = None
    
    def update(self):
        #Actualizar la velocidad basada en power-ups
        velocidad_actual = self.velocidad_normal * (2 if 'velocidad' in self.power_ups_activos else 1)
        
        self.velocidad_x = 0
        self.velocidad_y = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -velocidad_actual
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = velocidad_actual
        if teclas[pygame.K_UP]:
            self.velocidad_y = -velocidad_actual
        if teclas[pygame.K_DOWN]:
            self.velocidad_y = velocidad_actual
        
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

        #Actualizar power-ups
        ahora = pygame.time.get_ticks()
        power_ups_expirados = []
        for poder, tiempo_fin in self.power_ups_activos.items():
            if ahora >= tiempo_fin:
                power_ups_expirados.append(poder)
        
        for poder in power_ups_expirados:
            self.desactivar_power_up(poder)

        #Efecto visual del escudo
        if 'vida' in self.power_ups_activos:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_parpadeo > self.parpadeo_delay:
                self.ultimo_parpadeo = ahora
                #Alternar entre imagen normal y efecto de escudo
                if self.image == self.color_original:
                    #Crear efecto de escudo (tinte azul)
                    self.image = self.color_original.copy()
                    superficie_azul = pygame.Surface(self.image.get_size()).convert_alpha()
                    superficie_azul.fill((0, 100, 255, 100))
                    self.image.blit(superficie_azul, (0,0))
                else:
                    self.image = self.color_original.copy()

    def disparar(self):
        ahora = pygame.time.get_ticks()
        cadencia_actual = self.cadencia_normal // (2 if 'rapido' in self.power_ups_activos else 1)
        
        if ahora - self.ultimo_disparo > cadencia_actual:
            if self.disparo_triple:
                #Disparo triple
                for offset in [-20, 0, 20]:
                    bala = Bala(self.rect.centerx + offset, self.rect.top)
                    self.todas_las_sprites.add(bala)
                    self.balas.add(bala)
            else:
                #Disparo normal
                bala = Bala(self.rect.centerx, self.rect.top)
                self.todas_las_sprites.add(bala)
                self.balas.add(bala)
            
            self.ultimo_disparo = ahora

    def activar_power_up(self, tipo):
        ahora = pygame.time.get_ticks()
        duracion = {
            'triple': 10000, #10 segundos
            'velocidad': 8000, #8 segundos
            'rapido': 7000, #7 segundos
            'vida': 0 #Efecto instantáneo
        }
        
        if tipo == 'triple':
            self.disparo_triple = True
        elif tipo == 'vida':
            if self.vidas < self.vidas_maximas:
                self.vidas += 1
            return #Efecto instantáneo, no necesita tiempo de expiración
        
        self.power_ups_activos[tipo] = ahora + duracion[tipo]

    def desactivar_power_up(self, tipo):
        if tipo == 'triple':
            self.disparo_triple = False
        
        if tipo in self.power_ups_activos:
            del self.power_ups_activos[tipo]

    def recibir_daño(self):
        if 'vida' not in self.power_ups_activos:
            self.vidas -= 1
            return self.vidas <= 0
        return False

#Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, nivel, todas_las_sprites, balas_enemigas):
        super().__init__()
        #Cargar la imagen del enemigo
        ruta_imagen = os.path.join("assets", "Enemigos.png")
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 38))
        self.image = pygame.transform.flip(self.image, False, True) #Voltear verticalmente
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidad_y = random.randint(1, 3) + nivel // 5
        self.todas_las_sprites = todas_las_sprites
        self.balas_enemigas = balas_enemigas
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = random.randint(1000, 3000) #Entre 1 y 3 segundos
    
    def update(self):
        #Mover el enemigo hacia abajo
        self.rect.y += self.velocidad_y
        #Si el enemigo sale de la pantalla, reposicionarlo arriba
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
        
        #Lógica de disparo
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

#Clase para los power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        #Diccionario actualizado con las características de cada power-up
        self.power_ups = {
            'triple': {
                'imagen': 'triple_shot.png',
                'duracion': 10000,
                'tamaño': (20, 20)
            },
            'vida': { #Reemplazamos 'escudo' por 'vida extra'
                'imagen': 'heart.png', #Asegúrate de tener esta imagen
                'duracion': 0, #Efecto instantáneo
                'tamaño': (20, 20)
            },
            'velocidad': {
                'imagen': 'speed.png',
                'duracion': 8000,
                'tamaño': (20, 20)
            },
            'rapido': {
                'imagen': 'rapid_fire.png',
                'duracion': 7000,
                'tamaño': (20, 20)
            }
        }
        
        #Cargar la imagen del power-up
        try:
            ruta_imagen = os.path.join("assets", self.power_ups[tipo]['imagen'])
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
            self.image = pygame.transform.scale(self.image, self.power_ups[tipo]['tamaño'])
        except (pygame.error, FileNotFoundError):
            #Si no se encuentra la imagen, crear un power-up con forma básica como respaldo
            self.image = pygame.Surface(self.power_ups[tipo]['tamaño'])
            self.image.fill((255, 255, 255)) #Color blanco por defecto
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_y = 2
        
    def update(self):
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
    power_ups = pygame.sprite.Group() #Nuevo grupo para power-ups

    #Crear el jugador
    jugador = Jugador(todas_las_sprites, balas)
    todas_las_sprites.add(jugador)

    #Crear menos enemigos iniciales
    for _ in range(4): #Cambiado de 8 a 4
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
            
            #30% de probabilidad de generar un power-up
            if random.random() < 0.3:
                tipos_power_up = ['triple', 'vida', 'velocidad', 'rapido']
                tipo_elegido = random.choice(tipos_power_up)
                power_up = PowerUp(tipo_elegido, impacto.rect.centerx, impacto.rect.centery)
                todas_las_sprites.add(power_up)
                power_ups.add(power_up)
            
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
        impactos_balas = pygame.sprite.spritecollide(jugador, balas_enemigas, True)
        if impactos or impactos_balas:
            game_over = jugador.recibir_daño()
            if game_over:
                return True
            else:
                #Dar invulnerabilidad temporal y reposicionar
                jugador.rect.centerx = ANCHO // 2
                jugador.rect.bottom = ALTO - 10
                #Eliminar enemigos cercanos para evitar muerte instantánea
                for enemigo in impactos:
                    enemigo.kill()

        #Revisar colisiones entre jugador y power-ups
        impactos_power_ups = pygame.sprite.spritecollide(jugador, power_ups, True)
        for power_up in impactos_power_ups:
            jugador.activar_power_up(power_up.tipo)

        #Dibujar todo en la pantalla
        pantalla.fill(NEGRO)
        todas_las_sprites.draw(pantalla)
        dibujar_texto(pantalla, f"Puntaje: {puntaje}", 22, ANCHO // 2, 10)
        dibujar_texto(pantalla, f"Nivel: {nivel}", 22, ANCHO - 60, 10)

        #Dibujar vidas con imagen de corazón
        if jugador.imagen_vida:
            for i in range(jugador.vidas):
                pantalla.blit(jugador.imagen_vida, (10 + i * 30, 10))
        else:
            #Respaldo si no se encuentra la imagen
            for i in range(jugador.vidas):
                pygame.draw.rect(pantalla, ROJO, (10 + i * 30, 10, 20, 20))

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
