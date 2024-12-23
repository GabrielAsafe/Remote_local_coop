import pygame
import vgamepad as vg
import socket

# Configuração do cliente
SERVER_IP = '172.31.136.198'  # IP do servidor
PORT = 12345

# Inicializa o cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

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
    0: 'XUSB_GAMEPAD_A',  # Bola
    2: 'XUSB_GAMEPAD_X',  # Quadrado
    3: 'XUSB_GAMEPAD_Y',  # Triângulo
    1: 'XUSB_GAMEPAD_B',  # Círculo
    10: 'XUSB_GAMEPAD_RIGHT_SHOULDER',  # R1
    9: 'XUSB_GAMEPAD_LEFT_SHOULDER',   # L1
    4: 'XUSB_GAMEPAD_LEFT_TRIGGER',    # L2 (eixo)
    5: 'XUSB_GAMEPAD_RIGHT_TRIGGER',   # R2 (eixo)
    11: 'XUSB_GAMEPAD_DPAD_UP',        # Cima
    12: 'XUSB_GAMEPAD_DPAD_DOWN',      # Baixo
    13: 'XUSB_GAMEPAD_DPAD_LEFT',      # Esquerda
    14: 'XUSB_GAMEPAD_DPAD_RIGHT',     # Direita
    'LX': 'XUSB_GAMEPAD_LEFT_THUMB_X',  # Eixo X do analógico esquerdo
    'LY': 'XUSB_GAMEPAD_LEFT_THUMB_Y',  # Eixo Y do analógico esquerdo
    'RX': 'XUSB_GAMEPAD_RIGHT_THUMB_X', # Eixo X do analógico direito
    'RY': 'XUSB_GAMEPAD_RIGHT_THUMB_Y'  # Eixo Y do analógico direito
}

def send_command(type: str, command):
    # Formata o comando para envio
    if isinstance(command, dict):
        command_str = ",".join([f"{key}={value}" for key, value in command.items()])
    else:
        command_str = str(command)

    # Combina tipo e comando em uma única string
    data_to_send = f"{type},{command_str}"
    print(f"Enviando comando: {data_to_send}")  # Para depuração
    client.sendall(data_to_send.encode('utf-8'))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button in keyBindingsXbox:
                button_name = keyBindingsXbox.get(event.button)
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    send_command("JOYBUTTONDOWN", button_name)  # Envia o nome do botão
                    print(f"Botão pressionado: {button_name}")
        
        elif event.type == pygame.JOYBUTTONUP:
            if event.button in keyBindingsXbox:
                button_name = keyBindingsXbox.get(event.button)
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    send_command("JOYBUTTONUP", button_name)  # Envia o nome do botão
                    print(f"Botão solto: {button_name}")
        
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0 or event.axis == 1:  # Eixo do joystick esquerdo
                x_value = joystick.get_axis(0)
                y_value = joystick.get_axis(1) * -1
                if abs(x_value) > 0.06 or abs(y_value) > 0.06:
                    send_command("JOYAXISMOTIONESQUERDO", {"x_value": round(x_value, 2), "y_value": round(y_value, 2)})

            elif event.axis == 2 or event.axis == 3:  # Eixo do joystick direito
                x_value = joystick.get_axis(2)
                y_value = joystick.get_axis(3) * -1
                if abs(x_value) > 0.06 or abs(y_value) > 0.06:
                    send_command("JOYAXISMOTIONDIREITO", {"x_value": round(x_value, 2), "y_value": round(y_value, 2)})

            elif event.axis == 4:  # Gatilho esquerdo
                trigger_value = joystick.get_axis(4)
                send_command("JOYAXISMOTIONTriggerESQUERDO", {"trigger_value": round(trigger_value, 2)})

            elif event.axis == 5:  # Gatilho direito
                trigger_value = joystick.get_axis(5)
                send_command("JOYAXISMOTIONTriggerDIREITO", {"trigger_value": round(trigger_value, 2)})

        gamepad.update()
