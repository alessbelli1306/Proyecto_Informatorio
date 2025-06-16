import tkinter as tk
from tkinter import messagebox
# from PIL import Image, ImageTk # PARA VER LAS IMAGENES
import os
import time
from Juegos import AdivinaNumero, AdivinaAnimal

COLOR_FONDO = '#2C4059'
COLOR_BOTON = '#EF7B3E'
COLOR_TEXTO = '#FFD451'
COLOR_ERROR = '#EA5455'
COLOR_ACIERTO = '#66BB6A'
COLOR_INCORRECTO = '#EA5455'
FUENTE_NORMAL = ('Arial', 12)
FUENTE_ENCABEZADO = ('Arial', 22, 'bold')
FUENTE_ACIERTO = ('Arial', 22, 'bold')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Juegos')
        self.root.configure(bg=COLOR_FONDO)
        self.root.geometry('600x500')
        self.juego = None

        tk.Label(root, text='Elige un juego:', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_ENCABEZADO).pack(pady=30)

        tk.Button(root, text='Adivina el número', command=self.iniciar_numero, bg=COLOR_BOTON, fg='white', font=('Arial', 14), width=25).pack(pady=10)
        tk.Button(root, text='Adivina el animal', command=self.iniciar_animal, bg=COLOR_BOTON, fg='white', font=('Arial', 14), width=25).pack(pady=10)
        tk.Button(root, text='Salir', command=root.quit, bg=COLOR_ERROR, fg='white', font=('Arial', 14), width=25).pack(pady=20)

        self.reloj = tk.Label(root, text=self.obtener_hora(), bg=COLOR_FONDO, fg=COLOR_TEXTO, font=('Arial', 14))
        self.reloj.pack(side='bottom', pady=10)
        self.actualizar_reloj()

    def obtener_hora(self):
        return time.strftime('%H:%M:%S')

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
        win.geometry('600x500')
        win.title(f'Adivina el {tipo}')

        instrucciones = self.juego.mostrar_instrucciones()
        tk.Label(win, text=instrucciones, bg=COLOR_FONDO, fg=COLOR_TEXTO, justify='left', font=FUENTE_NORMAL, wraplength=550).pack(pady=10)

        entrada = tk.Entry(win, width=30, font=FUENTE_NORMAL)
        resultado = tk.Label(win, text='', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
        label_intentos = tk.Label(win, text=f'Intentos restantes: {self.juego.intentos_restantes}', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)


        imagen = None
        label_imagen = None

        if tipo == 'animal':
            pista = tk.Label(win, text=self.juego.mostrar_pistas(), bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_NORMAL)
            pista.pack(pady=5)
            # PARA VER LAS IMAGENES
            nombre_img = f'{self.juego.respuesta_correcta}.png'
            ruta_img = os.path.join('imagenes', nombre_img)
            if os.path.exists(ruta_img):
                # img = Image.open(ruta_img).resize((200, 200))
                # imagen = ImageTk.PhotoImage(img)
                # label_imagen = tk.Label(win, image=imagen, bg=COLOR_FONDO)
                # label_imagen.image = imagen
                # label_imagen.pack(pady=10)
                pass

        def verificar():
            intento = entrada.get()
            try:
                respuesta = self.juego.verificar(intento)
            except ValueError:
                respuesta = 'Debes ingresar un número'

            label_intentos.config(text=f'Intentos restantes: {self.juego.intentos_restantes}')

            if respuesta in ('¡Correcto!'):
                win.configure(bg=COLOR_ACIERTO)
                resultado.config(text='¡Correcto!', bg=COLOR_ACIERTO, fg='white', font=FUENTE_ACIERTO)
                messagebox.showinfo('Ganaste', f'¡Adivinaste el {tipo}!')
                win.destroy()
            else:
                resultado.config(text=respuesta)
                if self.juego.intentos_restantes == 0:
                    win.configure(bg=COLOR_INCORRECTO)
                    resultado.config(bg=COLOR_INCORRECTO, fg='white', font=FUENTE_ACIERTO)
                    if tipo == 'animal':
                        mensaje = f'El animal era: {self.juego.respuesta_correcta}'
                    else:
                        mensaje = f'El número era: {self.juego.numero}'
                    messagebox.showinfo('Perdiste', mensaje)
                    win.destroy()

        label_intentos.pack(pady=5)
        entrada.pack(pady=10)
        tk.Button(win, text='Verificar', command=verificar, bg=COLOR_BOTON, fg='white', font=FUENTE_NORMAL).pack(pady=10)
        resultado.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()