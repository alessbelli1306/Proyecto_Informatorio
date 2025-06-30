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
        cantidad_revelada = self.intentos_max - self.intentos_restantes
        revelada = self.respuesta_correcta[:cantidad_revelada]
        oculto = '_' * (len(self.respuesta_correcta) - cantidad_revelada)
        pista = f'Pista: {revelada + oculto} ({len(self.respuesta_correcta)} letras)'
        return pista

    def mostrar_instrucciones(self):
        return (
            '''ADIVINA EL ANIMAL\n
Debes adivinar el nombre de un animal secreto.
Tenes 5 intentos. Cada vez que falles, perdes un intento.
Se te dara una pista que revela más letras a medida que fallas.'''
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
            return 'Entrada no valida'
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
            '''ADIVINA EL NÚMERO\n
Debes adivinar un número secreto entre 1 y 10.
Cada vez que fallas, se te dirá si fue muy alto o muy bajo.
¡Tenes un número limitado de intentos!'''
        )

def obtener_hora():
    return time.strftime('%H:%M:%S')

def actualizar_reloj(label_reloj):
    hora_actual = obtener_hora()
    label_reloj.config(text=hora_actual)
    label_reloj.after(1000, actualizar_reloj, label_reloj)