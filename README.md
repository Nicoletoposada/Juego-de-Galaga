<div align="center">
    <h1>🚀 GALAGA EN PYTHON 👾</h1>
        <p><em>Una recreación del clásico juego arcade desarrollada con Python</em></p>
</div>
      
<div align="center">
    <img src="./assets/Nave.PNG" alt="Galaga Gameplay" width="5%">
    <img src="./assets/Enemigos.png" alt="Galaga Gameplay" width="5%">
</div>
      
## 🎮 Características del Juego
      
- 🛸 **Control de Nave:** Usa las flechas del teclado para moverte
- 🔫 **Sistema de Disparo:** Presiona la barra espaciadora para disparar
- 🚀 **Enemigos Dinámicos:** Enfréntate a oleadas de naves enemigas
- 🏆 **Sistema de Puntuación:** Compite por el puntaje más alto
- 🌟 **Niveles Progresivos:** La dificultad aumenta con cada nivel
- ❤️ **Sistema de Vidas:** 3 vidas para completar tu misión
- 💫 **Power-ups:** Recoge mejoras especiales que aparecen al eliminar enemigos
      
## 🕹️ Cómo Jugar
      
1. Usa las flechas ⬅️➡️⬆️⬇️ para mover tu nave
2. Presiona <kbd>Espacio</kbd> para disparar
3. Elimina enemigos para ganar puntos
4. Evita colisionar con los enemigos y sus disparos
5. ¡Sobrevive el mayor tiempo posible!
      
## 🛠️ Tecnologías Utilizadas
      
<p align="center">
    <img src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" alt="Python" height="80">
    <br>
    <img src="https://www.pygame.org/docs/_static/pygame_logo.svg" alt="Pygame" height="40">
</p>

## 🎨 Gráficos

El juego utiliza imágenes personalizadas:

- `Nave.PNG`: Representa la nave del jugador
- `Enemigos.png`: Representa a los enemigos
- `heart.png`: Muestra las vidas del jugador y también el power-up de vida extra
- `triple_shot.png`: Power-up de disparo triple
- `speed.png`: Power-up de velocidad
- `rapid_fire.png`: Power-up de disparo rápido

Estas imágenes se encuentran en la carpeta `assets`.

## 🕹️ Controles Adicionales

- Presiona <kbd>Enter</kbd> en el menú principal para iniciar el juego
- Presiona <kbd>Esc</kbd> en el menú principal para salir del juego

## 🌟 Características Adicionales

- **Sistema de Vidas:** Comienza con 3 vidas, ¡úsalas sabiamente!
- **Disparos Enemigos:** Los enemigos también disparan, ¡cuidado con sus balas!
- **Power-ups Variados:** 30% de probabilidad de obtener power-ups al eliminar enemigos:
  - 🔺 **Disparo Triple:** Dispara tres balas en abanico
  - ❤️ **Vida Extra:** Recupera una vida (máximo 3)
  - ⚡ **Velocidad Aumentada:** Mayor velocidad de movimiento
  - 🔥 **Disparo Rápido:** Reduce el tiempo entre disparos
- **Aumento de Dificultad:** El juego se vuelve más desafiante a medida que avanzas:
  - La velocidad de los enemigos aumenta con cada nivel
  - Se añaden más enemigos cada 10 enemigos eliminados

## 🛠️ Estructura del Código

El juego está organizado en varias clases principales:

- `Jugador`: Controla la nave del jugador y gestiona las vidas
- `Enemigo`: Maneja el comportamiento de los enemigos
- `Bala`: Representa los disparos del jugador
- `BalaEnemiga`: Representa los disparos de los enemigos
- `PowerUp`: Gestiona los power-ups y sus efectos

## 📊 Sistema de Puntuación y Niveles

- Gana 1 punto por cada enemigo eliminado
- El nivel aumenta cada 10 enemigos eliminados
- El puntaje, nivel actual y vidas restantes se muestran en la pantalla de juego

## 📈 Desarrollo Futuro
      
- [ ] Añadir efectos de sonido y música
- [ ] Implementar sistema de varias naves para jugar
- [ ] Diseñar niveles de jefe
- [ ] Agregar nuevos tipos de power-ups
      
## 👨‍💻 Autor
      
<div align="center">
    <strong>Nicolás Posada García</strong>
    <p>Futuro Ingenierio de sistemas y computación | Entusiasta de los Videojuegos</p>
        <a href="https://www.linkedin.com/in/nicolasposada/">
          <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=Linkedin&logoColor=white" alt="LinkedIn">
        </a>
        <a href="https://github.com/Nicoletoposada">
          <img src="https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub">
        </a>
</div>

<div align="center">
    <br>
    <p>🎮 ¡Disfruta jugando Galaga en Python! 🎮</p>
</div>
