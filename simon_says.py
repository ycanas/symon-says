"""

Juego simon dice Raspberry pi pico
Created by: @ycanas
29/04/2023

Entradas:

    - GP10: Boton color verde
    - GP11: Boton color rojo
    - GP12: Boton color amarillo
    - GP13: Boton color azul

Salidas:
    
    - GP00: Buzzer
    - GP21: Led verde
    - GP20: Led rojo
    - GP19: Led amarillo
    - GP18: Led azul

"""

from machine import Pin, PWM
from random  import randint
from utime   import sleep

# Función que inicializa el juego y declara las variables
def start():
    global level
    global levels
    global user_input
    global random_sequence
    
    level = 0
    levels = 20
    user_input = 0
    random_sequence = []
    
    random_sequence = [randint(0, 3) for _ in range(levels)]
    
    for index in range(len(OUTPUTS)):
        generate_sequence(index, 0.05)
    
    sleep(0.1)


# Función que genera las secuencias
def generate_sequence(index, delay):
    led = OUTPUTS[index]
    
    speaker.freq((index + 3) * 100)
    speaker.duty_u16(32768)
    
    led.value(True)
    
    sleep(delay)
    
    speaker.duty_u16(0)
    speaker.deinit()
    
    led.value(False)
    sleep(delay)


# Función que genera las secuencias aleatorias
def generate_random_sequence(level):
    delay_random = 0.35
    
    for pin in range(level + 1):
        index = random_sequence[pin]
        generate_sequence(index, delay_random)


# Función que verifica las secuencias
def verify_sequences(index):
    return random_sequence[index] == user_input


# Función que se encaraga de ingresar la secuencia del usuario
def input_sequence():
    global user_input
    
    delay_user = 0.25
    
    for index, button in enumerate(INPUTS):
        if not button.value():
            user_input = index
            generate_sequence(index, delay_user)
            
            return True
    
    return False
        

# Declaración del buzzer
speaker = PWM(Pin(0, Pin.OUT))

# Declaración de las entradas (pulsadores en configuración pull up)
INPUTS = [
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
    Pin(12, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP)
]


# Declaración de las salidas (leds de colores)
OUTPUTS = [
    Pin(21, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT)
]

# Inicialización del juego
start()

# Bucle de repetición del juego
while True:
    generate_random_sequence(level)
    level = level + 1
    
    for index in range(level):
        while True:
            if input_sequence():
                break
        
        if not verify_sequences(index):
            start()
            break
    
    if level == levels:
        start()
    
    sleep(0.3)
    