import random
import time

class AdivinaAnimal:
    def __init__(self, intentos=5):
        self.animales = [
            'perro', 'gato', 'elefante', 'jirafa', 'león',
            'tigre', 'oso', 'zorro', 'conejo', 'lobo'
        ]
        self.intentos_max = intentos
        self.intentos_restantes = intentos
        self.respuesta_correcta = random.choice(self.animales)

    def reiniciar(self):
        self.intentos_restantes = self.intentos_max
        self.respuesta_correcta = random.choice(self.animales)

    def verificar(self, intento):
        intento = intento.lower().strip()
        if intento == self.respuesta_correcta:
            return '¡Correcto!'

        else:
            self.intentos_restantes -= 1
            return 'Incorrecto'

    def mostrar_pistas(self):
        return (
            f'Pista: empieza con "{self.respuesta_correcta[0]}" '
            f'y tiene {len(self.respuesta_correcta)} letras.'
        )

    def mostrar_instrucciones(self):
        return (
            '''            ADIVINA EL ANIMAL
            Tenes que adivinar el nombre de un animal secreto.
            Dispones de 5 intentos. Cada vez que fallas, pierdes un intento.
            Se te dará una pista con la primera letra del animal y la 
            cantidad de letras.'''
        )


class AdivinaNumero:
    def __init__(self, intentos=5):
        self.numero = random.randint(1, 10)
        self.intentos_max = intentos
        self.intentos_restantes = intentos

    def reiniciar(self):
        self.numero = random.randint(1, 10)
        self.intentos_restantes = self.intentos_max

    def verificar(self, intento):
        try:
            intento = int(intento)
        except ValueError:
            return 'Entrada no válida'
        if intento < self.numero:
            self.intentos_restantes -= 1
            return 'Demasiado bajo'
        elif intento > self.numero:
            self.intentos_restantes -= 1
            return 'Demasiado alto'
        else:
            return '¡Correcto!'

    def mostrar_instrucciones(self):
        return (
            '''             ADIVINA EL NÚMERO
            Debes adivinar un número secreto entre 1 y 10.
            Cada vez que falles, se te dirá si fue muy alto o muy bajo.
            ¡Tienes un número limitado de intentos!'''
        )

def obtener_hora():
    return time.strftime('%H:%M:%S')

def actualizar_reloj(label_reloj):
    hora_actual = obtener_hora()
    label_reloj.config(text=hora_actual)
    label_reloj.after(1000, actualizar_reloj, label_reloj)