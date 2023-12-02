import socket
import threading
import tkinter as tk
from tkinter import ttk
import serial
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

arduino_port = "COM7"
ser = serial.Serial(arduino_port, 9600, timeout=1)

led_estado = False
ventilador_estado = False
luces_estado = False
secuencia_estado = False

color_activo = "green"
color_desactivo = "red"

def toggle_led_manual():
    global led_estado
    led_estado = not led_estado
    actualizar_estado_button(btn_toggle_led, led_estado)
    ser.write(b'TOGGLE_LED_MANUAL\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def toggle_secuencia():
    global secuencia_estado
    secuencia_estado = not secuencia_estado
    actualizar_estado_button(btn_toggle_secuencia, secuencia_estado)
    ser.write(b'TOGGLE_SECUENCIA\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def toggle_ventilador_manual():
    global ventilador_estado
    ventilador_estado = not ventilador_estado
    actualizar_estado_button(btn_toggle_ventilador, ventilador_estado)
    ser.write(b'TOGGLE_VENTILADOR_MANUAL\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def toggle_luces_manual():
    global luces_estado
    luces_estado = not luces_estado
    actualizar_estado_button(btn_toggle_luces, luces_estado)
    ser.write(b'TOGGLE_LUCES_MANUAL\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def girar_horario():
    ser.write(b'GIRAR_HORARIO\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def girar_antihorario():
    ser.write(b'GIRAR_ANTIHORARIO\n')
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def actualizar_umbral_led():
    umbral_led = entry_umbral_led.get()
    ser.write(f'U_LED{umbral_led}'.encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def actualizar_umbral_ventilador():
    umbral_ventilador = entry_umbral_ventilador.get()
    ser.write(f'U_VENT{umbral_ventilador}'.encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print(response)

def on_cerrar_ventana():
    ser.close()
    root.destroy()

def actualizar_valores_sensores():
    if not root.winfo_exists():
        return

    try:
        ser.write(b'REFRESH_SENSORES\n')
        time.sleep(0.1)
        response = ser.readline().decode().strip()

        if response.startswith("H:") and "," in response and "T:" in response:
            humedad = int(response.split("H:")[1].split(",")[0])
            humedad_scaled = (humedad / 1023) * 100
            temperatura = int(response.split("T:")[1])

            actualizar_barra_circular(fig_humedad, ax_humedad, humedad_scaled, "Seco")
            actualizar_barra_circular(fig_temperatura, ax_temperatura, temperatura, "Temperatura")

            label_humedad.config(text=f'Seco: {humedad_scaled:.2f}%')
            label_temperatura.config(text=f'Temperatura: {temperatura} °C')
    except Exception as e:
        print(f"Error al actualizar valores de sensores: {e}")

    if root.winfo_exists():
        root.after(1000, actualizar_valores_sensores)

def actualizar_barra_circular(fig, ax, valor, titulo):
    ax.clear()
    ax.set_title(titulo)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    data = [valor, 100 - valor]
    labels = [f'{titulo}\n{valor:.2f}%', '']
    colors = ['#1f77b4', '#d3d3d3']

    wedges, texts, autotexts = ax.pie(data, autopct=lambda p: f'{p:.1f}%', textprops=dict(color="w"), colors=colors)
    ax.legend(wedges, labels, title="Parámetros", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    fig.canvas.draw()

def actualizar_estado_button(button, estado):
    if estado:
        button.config(bg=color_activo)
    else:
        button.config(bg=color_desactivo)
def handle_client(client_socket):
    while True:
        # Recibir datos del cliente
        command = client_socket.recv(1024).decode()

        # Ejecutar comandos basados en lo recibido
        if command == "TOGGLE_LED_MANUAL":
            toggle_led_manual()
        elif command == "TOGGLE_SECUENCIA":
            toggle_secuencia()
        elif command == "TOGGLE_VENTILADOR_MANUAL":
             toggle_ventilador_manual()
        elif command == "TOGGLE_LUCES_MANUAL":
         toggle_luces_manual()
        elif command == "GIRAR_HORARIO":
              girar_horario()
        elif command == "GIRAR_ANTIHORARIO":
              girar_antihorario()


    
        

# Función principal del servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # Puedes elegir el puerto que desees
    server.listen(5)

    while True:
        client, addr = server.accept()
        print(f"Conexión entrante de {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
        
        
 
# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Menu Control")

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=5)
notebook = ttk.Notebook(root)

frame_control = ttk.Frame(notebook)
notebook.add(frame_control, text='Control')

fig_humedad, ax_humedad = plt.subplots(figsize=(4, 4), subplot_kw=dict(aspect="equal"))
fig_temperatura, ax_temperatura = plt.subplots(figsize=(4, 4), subplot_kw=dict(aspect="equal"))

canvas_humedad = FigureCanvasTkAgg(fig_humedad, master=frame_control)
canvas_humedad_widget = canvas_humedad.get_tk_widget()
canvas_humedad_widget.pack(side=tk.LEFT, padx=10, pady=10)

canvas_temperatura = FigureCanvasTkAgg(fig_temperatura, master=frame_control)
canvas_temperatura_widget = canvas_temperatura.get_tk_widget()
canvas_temperatura_widget.pack(side=tk.LEFT, padx=10, pady=10)

label_humedad = tk.Label(frame_control, text='Seco: ')
label_humedad.pack(pady=10)

label_temperatura = tk.Label(frame_control, text='Temperatura: ')
label_temperatura.pack(pady=10)

btn_toggle_led = tk.Button(frame_control, text="Encender/Apagar bomba", command=toggle_led_manual, width=20)
btn_toggle_led.pack(pady=10)

btn_toggle_ventilador = tk.Button(frame_control, text="Encender/Apagar Ventilador", command=toggle_ventilador_manual, width=20)
btn_toggle_ventilador.pack(pady=10)

btn_toggle_luces = tk.Button(frame_control, text="Encender/Apagar Luces", command=toggle_luces_manual, width=20)
btn_toggle_luces.pack(pady=10)

btn_toggle_secuencia = tk.Button(frame_control, text="Modo Automatico", command=toggle_secuencia, width=20)
btn_toggle_secuencia.pack(pady=10)

btn_girar_horario = tk.Button(frame_control, text="Abrir puerta", command=girar_horario, width=20)
btn_girar_horario.pack(pady=10)

btn_girar_antihorario = tk.Button(frame_control, text="Cerrar puerta", command=girar_antihorario, width=20)
btn_girar_antihorario.pack(pady=10)

frame_umbrales = ttk.Frame(notebook)
notebook.add(frame_umbrales, text='Umbrales')

entry_umbral_led = tk.Entry(frame_umbrales, width=10)
entry_umbral_led.insert(0, "600")
entry_umbral_led.pack(pady=5)
btn_actualizar_umbral_led = tk.Button(frame_umbrales, text="Actualizar humedad", command=actualizar_umbral_led)
btn_actualizar_umbral_led.pack(pady=5)

entry_umbral_ventilador = tk.Entry(frame_umbrales, width=10)
entry_umbral_ventilador.insert(0, "24")
entry_umbral_ventilador.pack(pady=5)
btn_actualizar_umbral_ventilador = tk.Button(frame_umbrales, text="Actualizar Temp.", command=actualizar_umbral_ventilador)
btn_actualizar_umbral_ventilador.pack(pady=5)

frame_graficos = ttk.Frame(notebook)
notebook.add(frame_graficos, text='Gráficos')

notebook.pack(expand=True, fill="both")
actualizar_valores_sensores()
root.mainloop()
