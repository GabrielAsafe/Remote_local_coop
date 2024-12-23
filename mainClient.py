import socket
import cv2
import numpy as np
import pygame
import vgamepad as vg
import threading
import time

# Configurações do cliente
SERVER_IP = '192.168.1.111'  # Substitua pelo IP do servidor
PORT = 12345

# Criar o socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print(f"Conectado ao servidor {SERVER_IP}:{PORT}")

# Inicializa o pygame e o módulo joystick
pygame.init()
pygame.joystick.init()

# Detecta se um controle está conectado
if pygame.joystick.get_count() == 0:
    print("Nenhum controle conectado.")
    exit()

# Inicializa o primeiro controle conectado
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controle conectado: {joystick.get_name()}")

# Cria o gamepad usando o vgamepad
gamepad = vg.VX360Gamepad()

keyBindingsXbox = {
    0: 'XUSB_GAMEPAD_A',
    2: 'XUSB_GAMEPAD_X',
    3: 'XUSB_GAMEPAD_Y',
    1: 'XUSB_GAMEPAD_B',
    10: 'XUSB_GAMEPAD_RIGHT_SHOULDER',
    9: 'XUSB_GAMEPAD_LEFT_SHOULDER',
    'LX': 'XUSB_GAMEPAD_LEFT_THUMB_X',
    'LY': 'XUSB_GAMEPAD_LEFT_THUMB_Y',
    'RX': 'XUSB_GAMEPAD_RIGHT_THUMB_X',
    'RY': 'XUSB_GAMEPAD_RIGHT_THUMB_Y'
}

def send_command(type: str, command):
    if isinstance(command, dict):
        command_str = ",".join([f"{key}={value}" for key, value in command.items()])
    else:
        command_str = str(command)
    data_to_send = f"{type},{command_str}"
    client.sendall(data_to_send.encode('utf-8'))

def handle_joystick():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in keyBindingsXbox:
                    button_name = keyBindingsXbox[event.button]
                    send_command("JOYBUTTONDOWN", button_name)
            
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in keyBindingsXbox:
                    button_name = keyBindingsXbox[event.button]
                    send_command("JOYBUTTONUP", button_name)
            
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0 or event.axis == 1:  # Eixos do analógico esquerdo
                    x_value = joystick.get_axis(0)
                    y_value = joystick.get_axis(1) * -1
                    if abs(x_value) > 0.06 or abs(y_value) > 0.06:
                        send_command("JOYAXISMOTIONESQUERDO", {"x_value": round(x_value, 2), "y_value": round(y_value, 2)})
                elif event.axis == 2 or event.axis == 3:  # Eixos do analógico direito
                    x_value = joystick.get_axis(2)
                    y_value = joystick.get_axis(3) * -1
                    if abs(x_value) > 0.06 or abs(y_value) > 0.06:
                        send_command("JOYAXISMOTIONDIREITO", {"x_value": round(x_value, 2), "y_value": round(y_value, 2)})

        gamepad.update()
        time.sleep(0.01)  # Reduz a carga no loop

def handle_screen_stream():
    while True:
        try:
            # Receber o tamanho do frame
            data = client.recv(4)
            if not data:
                break
            frame_size = int.from_bytes(data, 'big')

            # Receber o frame
            frame_data = b""
            while len(frame_data) < frame_size:
                packet = client.recv(8192)
                if not packet:
                    break
                frame_data += packet

            # Reconstruir e exibir o frame
            frame_array = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            cv2.imshow("Stream da Tela", frame)
            if cv2.waitKey(1) == 27:  # Pressione Esc para sair
                break
        except Exception as e:
            print(f"Erro no stream: {e}")
            break

# Criar threads para joystick e streaming
thread_joystick = threading.Thread(target=handle_joystick, daemon=True)
thread_stream = threading.Thread(target=handle_screen_stream, daemon=True)

try:
    thread_joystick.start()
    thread_stream.start()
    thread_joystick.join()
    thread_stream.join()
finally:
    client.close()
    cv2.destroyAllWindows()
    pygame.quit()
