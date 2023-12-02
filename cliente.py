import socket
import tkinter as tk
import random


def obtener_temperatura():
    return random.uniform(23, 23.80)

def enviar_comando(comando):
    # Función para enviar el comando al servidor
    client.send(comando.encode())

def toggle_color(btn):
    # Función para alternar el color del botón
    if btn['bg'] == 'green':
        btn.config(bg='red')
    else:
        btn.config(bg='green')

def actualizar_temperatura():
    temperatura = obtener_temperatura()
    porcentaje = int((temperatura - 23) / (23.8 - 23) * 100)  # Calcula el porcentaje de temperatura
    canvas_temperatura.itemconfig(barra_temperatura, width=porcentaje)  # Actualiza la barra de progreso
    etiqueta_temperatura.config(text=f'Temperatura: {temperatura:.2f} °C')  # Actualiza el número de temperatura
    root.after(4300, actualizar_temperatura)  # Llama a la función cada 2.3 segundos

# Configuración de la interfaz gráfica
root = tk.Tk()
root.configure(bg='yellow')
root.title("Cliente para enviar comandos")

frame = tk.Frame(root)
frame.pack(padx=40, pady=40)

commands = {
    "Encender/Apagar el Bomba Manual": "TOGGLE_LED_MANUAL",
    "Encender/Apagar el Ventilador Manual": "TOGGLE_VENTILADOR_MANUAL",
    "Encender/Apagar las Luces Manual": "TOGGLE_LUCES_MANUAL",
    "Secuencia Automática": "TOGGLE_SECUENCIA",
    "Actualizar Valores de los Sensores": "REFRESH_SENSORES",
    "ABRIR PUERTA": "GIRAR_HORARIO",
    "CERRAR PUERTA": "GIRAR_ANTIHORARIO"
}

buttons = []
for label, command in commands.items():
    btn = tk.Button(frame, text=label, command=lambda cmd=command: enviar_comando(cmd))
    btn.pack(pady=9)
    btn.config(width=40, bg='red')  # Dimensión y color inicial del botón
    btn.bind('<Button-1>', lambda event, b=btn: toggle_color(b))  # Cambio de color al hacer clic
    buttons.append(btn)

# Canvas para representar la barra de progreso de la temperatura
canvas_temperatura = tk.Canvas(root, width=300, height=20, bg='white', highlightthickness=0)
canvas_temperatura.pack(pady=20)


barra_temperatura = canvas_temperatura.create_rectangle(0, 0, 0, 20, fill='blue')

# Etiqueta para mostrar el número de temperatura
etiqueta_temperatura = tk.Label(root, text='', font=('Arial', 12))
etiqueta_temperatura.pack()

# Conexión al servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.66.114', 5555))  

# Inicia la actualización de la temperatura
actualizar_temperatura()

root.mainloop()
