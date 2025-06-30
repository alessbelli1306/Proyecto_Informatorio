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

# Colores.
COLOR_FONDO_JUEGO = "#83CECE"
COLOR_TEXTO = '#1B4F72'
COLOR_BOTON = '#5DADE2'
COLOR_SALIR = '#E74C3C'
COLOR_ACIERTO = '#58D68D'
COLOR_INCORRECTO = '#E74C3C'
COLOR_ERROR = '#C0392B'
FUENTE_NORMAL = ('Comic Sans MS', 12)
FUENTE_TITULO = ('Comic Sans MS', 18, 'bold')
FUENTE_ACIERTO = ('Comic Sans MS', 16, 'bold')

ARCHIVO_PUNTAJES = 'puntajes.txt'

class App:
    def __init__(self, root):

        self.root = root
        self.root.title('Juegos')
        self.root.geometry('700x800')
        self.juego = None
        self.alias = ''

        self.root.withdraw()
        self.solicitar_alias()

        imagen_fondo = Image.open('Imagenes/fondo.png')
        self.fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(root, image=self.fondo_tk)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        titulo = tk.Label(root, text='¡BIENVENIDOS!', font=FUENTE_TITULO, bg='white', fg=COLOR_TEXTO)
        titulo.pack(pady=30)

        self.juego_opcion = tk.StringVar(value='Elige un juego')
        menu = tk.OptionMenu(root, self.juego_opcion, 'Adivina el número', 'Adivina el animal')
        menu.config(font=FUENTE_NORMAL, bg='green', width=25)
        menu.pack(pady=10)

        tk.Button(root, text='Jugar', command=self.iniciar_juego, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL, width=20).pack(pady=10)

        tk.Button(root, text='Salir', command=root.quit, bg=COLOR_SALIR, fg='white', font=FUENTE_NORMAL, width=20).pack(pady=20)

        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        menu_integrantes = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Integrantes Grupo 8", menu=menu_integrantes)

# Integrantes Grupo 8...
        integrantes = [
            "Yair Belli",
            "Ingrid Luna",
            "Maite Manca",
            "Matias Martinez",
            "Soledad Sanchez",
            "Cristian Asselle"
        ]

        for nombre in integrantes:
            menu_integrantes.add_command(label=nombre)

        self.reloj = tk.Label(root, text=self.obtener_hora(), font=FUENTE_NORMAL, bg='white', fg=COLOR_TEXTO)
        self.reloj.pack(side='bottom', pady=10)
        self.actualizar_reloj()

        self.mostrar_puntajes()

    def solicitar_alias(self):
        def guardar_alias():
            self.alias = entrada.get().strip()
            if self.alias == '':
                self.alias = 'Jugador Anónimo'
            ventana_alias.destroy()

        ventana_alias = tk.Toplevel(self.root)
        ventana_alias.title("Bienvenid@s")
        ventana_alias.geometry("450x250")
        ventana_alias.configure(bg=COLOR_FONDO_JUEGO)

        tk.Label(ventana_alias, text="Ingresa tu nombre:", bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL).pack(pady=10)
        entrada = tk.Entry(ventana_alias, font=FUENTE_NORMAL)
        entrada.pack(pady=5)
        tk.Button(ventana_alias, text="Aceptar", command=guardar_alias, bg=COLOR_BOTON, fg="white", font=FUENTE_NORMAL).pack(pady=10)

        self.root.wait_window(ventana_alias)
        self.root.deiconify()

    def mostrar_puntajes(self):
        if not os.path.exists(ARCHIVO_PUNTAJES):
            return

        with open(ARCHIVO_PUNTAJES, 'r', encoding='utf-8') as f:
            lineas = [line.strip() for line in f.readlines() if line.strip()]
        lineas.sort(reverse=True)

        marco = tk.LabelFrame(self.root, text="🏆 Puntajes", bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL, padx=10, pady=5)
        marco.pack(pady=10)

        for linea in lineas[:5]:
            tk.Label(marco, text=linea, bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL).pack(anchor='w')

    def guardar_puntaje(self, juego, intentos_usados):
        puntaje = max(0, 100 - intentos_usados * 10)
        linea = f"{self.alias} - {juego} - {puntaje} puntos"
        with open(ARCHIVO_PUNTAJES, 'a', encoding='utf-8') as f:
            f.write(linea + "\n")

    def obtener_hora(self):
        return time.strftime('%H:%M:%S')

    def actualizar_reloj(self):
        self.reloj.config(text=self.obtener_hora())
        self.root.after(1000, self.actualizar_reloj)

    def iniciar_juego(self):
        opcion = self.juego_opcion.get()
        if opcion == 'Adivina el número':
            self.juego = AdivinaNumero()
            self.ventana_juego('número')
        elif opcion == 'Adivina el animal':
            self.juego = AdivinaAnimal()
            self.ventana_juego('animal')

    def ventana_juego(self, tipo):
        win = tk.Toplevel(self.root)
        win.geometry('700x600')
        win.title(f'¡A jugar al {tipo}!')
        win.configure(bg=COLOR_FONDO_JUEGO)

        instrucciones = self.juego.mostrar_instrucciones()
        tk.Label(win, text='Instrucciones:', font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_FONDO_JUEGO).pack(pady=(10, 0))
        tk.Label(win, text=instrucciones, font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_FONDO_JUEGO, wraplength=550, justify='left').pack(pady=5)

        entrada = tk.Entry(win, width=30, font=FUENTE_NORMAL)
        entrada.pack(pady=10)

        resultado = tk.Label(win, text='', bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        resultado.pack(pady=5)

        label_intentos = tk.Label(win, text=f'Intentos restantes: {self.juego.intentos_restantes}', bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        label_intentos.pack()

        intentos_previos = []
        historial = tk.Label(win, text='Intentos anteriores: ', bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        historial.pack()

        if tipo == 'animal':
            pista = tk.Label(win, text=self.juego.mostrar_pistas(), bg=COLOR_FONDO_JUEGO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
            pista.pack(pady=5)

        def mostrar_imagen_animal(nombre_animal):
            ruta = f'Imagenes/{nombre_animal}.png'
            if os.path.exists(ruta):
                img = Image.open(ruta)
                img = img.resize((100, 100), Image.LANCZOS)
                foto = ImageTk.PhotoImage(img)
                panel = tk.Label(win, image=foto, bg=COLOR_FONDO_JUEGO)
                panel.image = foto
                panel.pack(pady=10)
            else:
                tk.Label(win, text="Imagen no disponible", bg=COLOR_FONDO_JUEGO, fg=COLOR_ERROR, font=FUENTE_NORMAL).pack(pady=10)

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

            if tipo == 'animal':
                pista.config(text=self.juego.mostrar_pistas())

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

        tk.Button(win, text='Verificar', command=verificar, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL).pack(pady=10)


if __name__ == '__main__':
    root = tk.Tk()
app = App(root)
root.mainloop()
