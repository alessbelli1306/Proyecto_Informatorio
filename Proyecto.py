
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import time
from Biblioteca.Juegos import AdivinaNumero, AdivinaAnimal
import pygame
import threading

def reproducir_musica():
    pygame.mixer.init()
    pygame.mixer.music.load("Sonidos/musica_fondo.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

threading.Thread(target=reproducir_musica, daemon=True).start()

COLOR_FONDO = '#2C4059'
COLOR_BOTON = '#EF7B3E'
COLOR_TEXTO = '#FFD451'
COLOR_ERROR = '#EA5455'
COLOR_ACIERTO = '#66BB6A'
COLOR_INCORRECTO = '#EA5455'
FUENTE_NORMAL = ('Comic Sans MS', 12)
FUENTE_ENCABEZADO = ('Comic Sans MS', 22, 'bold')
FUENTE_ACIERTO = ('Comic Sans MS', 22, 'bold')

ARCHIVO_PUNTAJES = 'puntajes.txt'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('🎮 Juegos')
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry('700x600')
        self.juego = None
        self.alias = ''

        self.solicitar_alias()

        tk.Label(root, text='Elige un juego:', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_ENCABEZADO).pack(pady=20)

        tk.Button(root, text='🔢 Adivina el número', command=self.iniciar_numero, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL, width=30).pack(pady=10)
        tk.Button(root, text='🐾 Adivina el animal', command=self.iniciar_animal, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL, width=30).pack(pady=10)
        tk.Button(root, text='❌ Salir', command=root.quit, bg=COLOR_ERROR, fg='white', font=FUENTE_NORMAL, width=30).pack(pady=10)
        
        self.reloj = tk.Label(root, text=self.obtener_hora(), bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        self.reloj.pack(side='bottom', pady=5)
        self.actualizar_reloj()

        self.mostrar_puntajes()

    def solicitar_alias(self):
        def guardar_alias():
            self.alias = entrada.get().strip()
            if self.alias == '':
                self.alias = 'Jugador Anónimo'
            ventana_alias.destroy()

        ventana_alias = tk.Toplevel(self.root)
        ventana_alias.title("Bienvenido")
        ventana_alias.geometry("350x150")
        ventana_alias.configure(bg=COLOR_FONDO)

        tk.Label(ventana_alias, text="Ingresa tu nombre o alias:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL).pack(pady=10)
        entrada = tk.Entry(ventana_alias, font=FUENTE_NORMAL)
        entrada.pack(pady=5)
        tk.Button(ventana_alias, text="Aceptar", command=guardar_alias, bg=COLOR_BOTON, fg="white", font=FUENTE_NORMAL).pack(pady=10)

        self.root.wait_window(ventana_alias)

    def mostrar_puntajes(self):
        if not os.path.exists(ARCHIVO_PUNTAJES):
            return

        with open(ARCHIVO_PUNTAJES, 'r', encoding='utf-8') as f:
            lineas = [line.strip() for line in f.readlines() if line.strip()]
        lineas.sort(reverse=True)

        marco = tk.LabelFrame(self.root, text="🏆 Puntajes", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL, padx=10, pady=5)
        marco.pack(pady=10)

        for linea in lineas[:5]:  # mostrar top 5
            tk.Label(marco, text=linea, bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL).pack(anchor='w')

    def guardar_puntaje(self, juego, intentos_usados):
        puntaje = max(0, 100 - intentos_usados * 10)
        linea = f"{self.alias} - {juego} - {puntaje} puntos"
        with open(ARCHIVO_PUNTAJES, 'a', encoding='utf-8') as f:
            f.write(linea + "\n")

    def obtener_hora(self):
        return "Es la hora: " + time.strftime('%H:%M:%S')

    def actualizar_reloj(self):
        self.reloj.config(text=self.obtener_hora())
        self.root.after(1000, self.actualizar_reloj)

    def iniciar_numero(self):
        self.juego = AdivinaNumero()
        self.ventana_juego('número')

    def iniciar_animal(self):
        self.juego = AdivinaAnimal()
        self.ventana_juego('animal')

    def ventana_juego(self, tipo):
        win = tk.Toplevel(self.root)
        win.configure(bg=COLOR_FONDO)
        win.geometry('650x550')
        win.title(f'Adivina el {tipo}')

        intentos_previos = []
        instrucciones = self.juego.mostrar_instrucciones() if hasattr(self.juego, 'mostrar_instrucciones') else ''
        tk.Label(win, text=instrucciones, bg=COLOR_FONDO, fg=COLOR_TEXTO, justify='left', font=FUENTE_NORMAL, wraplength=550).pack(pady=10)

        entrada = tk.Entry(win, width=30, font=FUENTE_NORMAL)
        resultado = tk.Label(win, text='', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        label_intentos = tk.Label(win, text=f'Intentos restantes: {self.juego.intentos_restantes}', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        historial = tk.Label(win, text='Intentos anteriores: ', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL, wraplength=600)

        if tipo == 'animal':
            pista = tk.Label(win, text=self.juego.mostrar_pistas(), bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
            pista.pack(pady=5)

        def mostrar_imagen_animal(nombre_animal):
            ruta = f'Imagenes/{nombre_animal}.png'
            if os.path.exists(ruta):            # Para Verificar si la imagen
                img = Image.open(ruta)
                img = img.resize((100, 100), Image.LANCZOS)
                foto = ImageTk.PhotoImage(img)
                panel = tk.Label(win, image=foto, bg=COLOR_FONDO)
                panel.image = foto  # mantener referencia
                panel.pack(pady=10)
            else:
                tk.Label(win, text="Imagen no disponible", bg=COLOR_FONDO, fg=COLOR_ERROR, font=FUENTE_NORMAL).pack(pady=10)

        def verificar():
            intento = entrada.get().strip().lower()
            entrada.delete(0, tk.END)

            if intento in intentos_previos:
                resultado.config(text=f'Ya intentaste con "{intento}". ¡Probá con otro!', fg='orange')
                return

            intentos_previos.append(intento)
            historial.config(text='Intentos anteriores: ' + ', '.join(intentos_previos))

            try:
                respuesta = self.juego.verificar(intento)
            except ValueError:
                respuesta = 'Debes ingresar un número'

            label_intentos.config(text=f'Intentos restantes: {self.juego.intentos_restantes}')

            if respuesta == '¡Correcto!' or respuesta == '¡Genial!':
                win.configure(bg=COLOR_ACIERTO)
                resultado.config(text=respuesta, bg=COLOR_ACIERTO, fg='white', font=FUENTE_ACIERTO)
                self.guardar_puntaje(tipo, len(intentos_previos))
                if tipo == 'animal':
                    mostrar_imagen_animal(self.juego.respuesta_correcta)
                    win.after(3500, lambda: [win.destroy(), messagebox.showinfo('Ganaste', f'¡Adivinaste el {tipo}!')])
                else:
                    messagebox.showinfo('Ganaste', f'¡Adivinaste el {tipo}!')
                    win.destroy()
            else:
                resultado.config(text=respuesta, fg=COLOR_TEXTO)
                if tipo == 'animal':
                    pista.config(text=self.juego.mostrar_pistas())

                if self.juego.intentos_restantes == 0:
                    win.configure(bg=COLOR_INCORRECTO)
                    resultado.config(bg=COLOR_INCORRECTO, fg='white', font=FUENTE_ACIERTO)
                    if tipo == 'animal':
                        mostrar_imagen_animal(self.juego.respuesta_correcta)
                        win.after(3500, lambda: [win.destroy(), messagebox.showinfo('Perdiste', f'El {tipo} era: {self.juego.respuesta_correcta}')])
                    else:
                        mensaje = f'El {tipo} era: {getattr(self.juego, "respuesta_correcta", self.juego.numero)}'
                        messagebox.showinfo('Perdiste', mensaje)
                        win.destroy()

        label_intentos.pack(pady=5)
        entrada.pack(pady=10)
        tk.Button(win, text='Verificar', command=verificar, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL).pack(pady=10)
        resultado.pack(pady=10)
        historial.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()

from pathlib import Path
ruta_imagen = Path(__file__).parent / 'Imagenes/portada_juegos.jpg'
imagen_fondo = Image.open(ruta_imagen)
fondo = ImageTk.PhotoImage(imagen_fondo)
fondo_label = tk.Label(root, image=fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

def reproducir_musica():
    pygame.mixer.init()
    pygame.mixer.music.load("Sonidos/musica_fondo.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

musica_pausada = False

def pausar_musica():
    global musica_pausada
    if not musica_pausada:
        pygame.mixer.music.pause()
        musica_pausada = True

def reanudar_musica():
    global musica_pausada
    if musica_pausada:
        pygame.mixer.music.unpause()
        musica_pausada = False

threading.Thread(target=reproducir_musica, daemon=True).start()
frame_musica= tk.Frame(root, bg="green")
frame_musica.pack(pady=10)
btn_pausa = tk.Button(frame_musica, text="🔇 Pausar Música", command=pausar_musica) 
btn_reanudar = tk.Button(frame_musica, text="🔊 Reanudar Música", command=reanudar_musica)
btn_pausa.pack(side="left", pady=5, padx=5)
btn_reanudar.pack(side="left", pady=5, padx=5)

mensaje = tk.Label(root, text="Bienvenido a los Juegos Educativos", fg='white', bg="green", font=("Comic Sans MS", 22,"bold"))
mensaje.pack(pady=5)

mensaje = tk.Label(root, text="Informatorio Chaco 2025 es la hora de jugar ", fg='white', bg="green", font=("Comic Sans MS", 22,"bold"))
mensaje.pack(pady=5)

app = App(root)
root.mainloop()
