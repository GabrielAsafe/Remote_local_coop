import socket
import pygame
import vgamepad as vg

# Configuração do servidor
HOST = '0.0.0.0'  # Aceitar conexões de qualquer lugar
PORT = 12345
BUFFER_SIZE = 1024

# Inicializa o pygame e o módulo joystick
pygame.init()


# Cria o gamepad usando o vgamepad
gamepad = vg.VX360Gamepad()

# Inicializa o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Servidor aguardando conexões na porta {PORT}...")

conn, addr = server.accept()
print(f"Conexão estabelecida com {addr}")

# Função para processar os comandos recebidos e aplicar ao gamepad
def process_command(typo: str, command):
    try:
        if typo == "JOYAXISMOTIONESQUERDO" or typo == "JOYAXISMOTIONDIREITO":
            # Espera-se que `command` seja um dicionário com 'x_value' e 'y_value'
            x_value = float(command["x_value"])  # Eixo X
            y_value = float(command["y_value"])  # Eixo Y
            if typo == "JOYAXISMOTIONESQUERDO":
                gamepad.left_joystick_float(x_value_float=x_value, y_value_float=y_value)
            elif typo == "JOYAXISMOTIONDIREITO":
                gamepad.right_joystick_float(x_value_float=x_value, y_value_float=y_value)

        elif typo == "JOYAXISMOTIONTriggerESQUERDO" or typo == "JOYAXISMOTIONTriggerDIREITO":
            # Espera-se que `command` seja um dicionário com 'trigger_value'
            trigger_value = float(command["trigger_value"])  # Gatilho
            if typo == "JOYAXISMOTIONTriggerESQUERDO":
                gamepad.left_trigger_float(trigger_value)
            elif typo == "JOYAXISMOTIONTriggerDIREITO":
                gamepad.right_trigger_float(trigger_value)

        elif typo == "JOYBUTTONDOWN" or typo == "JOYBUTTONUP":
            button_name = command
            if typo == "JOYBUTTONDOWN":
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    gamepad.press_button(button=button_enum)
            elif typo == "JOYBUTTONUP":
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    gamepad.release_button(button=button_enum)

        

    except Exception as e:
        print(f"Erro ao processar comando: {e}")

try:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        typo, command_str = data.decode('utf-8').split(',', 1)
        
        if typo == "JOYAXISMOTIONESQUERDO" or typo == "JOYAXISMOTIONDIREITO" or typo == "JOYAXISMOTIONTriggerESQUERDO" or typo == "JOYAXISMOTIONTriggerDIREITO":
            command = dict(item.split('=') for item in command_str.split(','))

        else:
            command = command_str


        process_command(typo, command)
        gamepad.update()


finally:
    gamepad.reset()
    conn.close()
    server.close()
