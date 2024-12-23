import socket
import pygame
import vgamepad as vg
import pyautogui
import cv2
import numpy as np
import time  # Para limitar FPS

# Configuração do servidor
HOST = '0.0.0.0'  # Aceitar conexões de qualquer lugar
PORT = 12345
BUFFER_SIZE = 1024

# Criar o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Servidor aguardando conexão na porta {PORT}...")

conn, addr = server.accept()
print(f"Conexão estabelecida com {addr}")

# Inicialização global do gamepad
gamepad = vg.VX360Gamepad()

def process_command(typo: str, command):
    try:
        if typo in ["JOYAXISMOTIONESQUERDO", "JOYAXISMOTIONDIREITO"]:
            x_value = float(command.get("x_value", 0))  # Eixo X
            y_value = float(command.get("y_value", 0))  # Eixo Y
            if typo == "JOYAXISMOTIONESQUERDO":
                gamepad.left_joystick_float(x_value_float=x_value, y_value_float=y_value)
            elif typo == "JOYAXISMOTIONDIREITO":
                gamepad.right_joystick_float(x_value_float=x_value, y_value_float=y_value)

        elif typo in ["JOYAXISMOTIONTriggerESQUERDO", "JOYAXISMOTIONTriggerDIREITO"]:
            trigger_value = float(command.get("trigger_value", 0))  # Gatilho
            if typo == "JOYAXISMOTIONTriggerESQUERDO":
                gamepad.left_trigger_float(trigger_value)
            elif typo == "JOYAXISMOTIONTriggerDIREITO":
                gamepad.right_trigger_float(trigger_value)

        elif typo in ["JOYBUTTONDOWN", "JOYBUTTONUP"]:
            button_name = command
            button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
            if button_enum:
                if typo == "JOYBUTTONDOWN":
                    gamepad.press_button(button=button_enum)
                elif typo == "JOYBUTTONUP":
                    gamepad.release_button(button=button_enum)
    except Exception as e:
        print(f"Erro ao processar comando: {e}")

def receive_data_from_client(data):
    try:
        typo, command_str = data.decode('utf-8').split(',', 1)
        if typo.startswith("JOYAXISMOTION"):
            command = {k: v for k, v in (item.split('=') for item in command_str.split(','))}
        else:
            command = command_str
        process_command(typo, command)
        gamepad.update()
    except Exception as e:
        print(f"Erro ao receber dados: {e}")

def send_screen():
    try:
        # Capturar a tela
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)  # Converter para array numpy
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converter para formato RGB

        # Codificar o frame como JPEG
        _, frame_encoded = cv2.imencode('.jpg', frame)
        frame_data = frame_encoded.tobytes()

        # Enviar o tamanho do frame
        frame_size = len(frame_data)
        conn.sendall(frame_size.to_bytes(4, 'big'))

        # Enviar o frame
        conn.sendall(frame_data)
    except Exception as e:
        print(f"Erro ao enviar tela: {e}")

def main():
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break

            # Processar comando recebido
            receive_data_from_client(data)

            # Enviar a tela para o cliente
            send_screen()

            # Limitar o FPS
            time.sleep(1 / 30)  # 30 FPS
    finally:
        print("Encerrando o servidor...")
        gamepad.reset()
        conn.close()
        server.close()

if __name__ == "__main__":
    main()
