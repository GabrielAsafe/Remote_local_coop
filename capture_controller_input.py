import pygame
import vgamepad as vg


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




#cria o gamepad usango o vigem eventialmente meter uma UI para decidir o tipo de controle
gamepad = vg.VX360Gamepad()


keyBindingsXbox = {
    # Botões principais
    0: 'XUSB_GAMEPAD_A',       # Bola
    2: 'XUSB_GAMEPAD_X',       # Quadrado
    3: 'XUSB_GAMEPAD_Y',       # Triângulo
    1: 'XUSB_GAMEPAD_B',       # Círculo

    # Ombros e gatilhos
    10: 'XUSB_GAMEPAD_RIGHT_SHOULDER',  # R1
    9: 'XUSB_GAMEPAD_LEFT_SHOULDER',   # L1
    4: 'XUSB_GAMEPAD_LEFT_TRIGGER',    # L2 (eixo)
    5: 'XUSB_GAMEPAD_RIGHT_TRIGGER',   # R2 (eixo)

    # Direcionais (D-Pad)
    11: 'XUSB_GAMEPAD_DPAD_UP',        # Cima
    12: 'XUSB_GAMEPAD_DPAD_DOWN',      # Baixo
    13: 'XUSB_GAMEPAD_DPAD_LEFT',      # Esquerda
    14: 'XUSB_GAMEPAD_DPAD_RIGHT',     # Direita

    # Analógicos
    'LX': 'XUSB_GAMEPAD_LEFT_THUMB_X',   # Eixo X do analógico esquerdo
    'LY': 'XUSB_GAMEPAD_LEFT_THUMB_Y',   # Eixo Y do analógico esquerdo
    'RX': 'XUSB_GAMEPAD_RIGHT_THUMB_X',  # Eixo X do analógico direito
    'RY': 'XUSB_GAMEPAD_RIGHT_THUMB_Y',  # Eixo Y do analógico direito
}

keyBindingsPS4 = {
    # Botões principais
    0: 'XUSB_GAMEPAD_SQUARE',   # Quadrado
    1: 'XUSB_GAMEPAD_CIRCLE',   # Círculo
    2: 'XUSB_GAMEPAD_CROSS',    # X (Cruz)
    3: 'XUSB_GAMEPAD_TRIANGLE', # Triângulo

    # Ombros e gatilhos
    10: 'XUSB_GAMEPAD_RIGHT_SHOULDER',  # R1
    9: 'XUSB_GAMEPAD_LEFT_SHOULDER',   # L1
    4: 'XUSB_GAMEPAD_LEFT_TRIGGER',    # L2 (eixo)
    5: 'XUSB_GAMEPAD_RIGHT_TRIGGER',   # R2 (eixo)

    # Direcionais (D-Pad)
    11: 'XUSB_GAMEPAD_DPAD_UP',        # Cima
    12: 'XUSB_GAMEPAD_DPAD_DOWN',      # Baixo
    13: 'XUSB_GAMEPAD_DPAD_LEFT',      # Esquerda
    14: 'XUSB_GAMEPAD_DPAD_RIGHT',     # Direita

    # Analógicos
    'LX': 'XUSB_GAMEPAD_LEFT_THUMB_X',   # Eixo X do analógico esquerdo
    'LY': 'XUSB_GAMEPAD_LEFT_THUMB_Y',   # Eixo Y do analógico esquerdo
    'RX': 'XUSB_GAMEPAD_RIGHT_THUMB_X',  # Eixo X do analógico direito
    'RY': 'XUSB_GAMEPAD_RIGHT_THUMB_Y',  # Eixo Y do analógico direito
}



  # Game loop



while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button in keyBindingsXbox:
                button_name = keyBindingsXbox.get(event.button)
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    gamepad.press_button(button=button_enum)
                else:
                    print(f"Button {button_name} not found in vg.XUSB_BUTTON.")
        
        elif event.type == pygame.JOYBUTTONUP:
            if event.button in keyBindingsXbox:
                button_name = keyBindingsXbox.get(event.button)
                button_enum = getattr(vg.XUSB_BUTTON, button_name, None)
                if button_enum:
                    gamepad.release_button(button=button_enum)
                else:
                    print(f"Button {button_name} not found in vg.XUSB_BUTTON.")
        
        elif event.type == pygame.JOYAXISMOTION:
    
            if event.axis == 0 or event.axis == 1:  # Eixo do joystick esquerdo
                x_value = joystick.get_axis(0)   # Inverta o eixo X
                y_value = joystick.get_axis(1)    * -1  # Mantenha o eixo Y como está
                gamepad.left_joystick_float(x_value_float=round(x_value, 2), y_value_float=round(y_value, 2))
            
            elif event.axis == 2 or event.axis == 3:  # Eixo do joystick direito
                x_value = joystick.get_axis(2)   # Inverta o eixo X
                y_value = joystick.get_axis(3)    * -1  # Mantenha o eixo Y como está
                gamepad.right_joystick_float(x_value_float=round(x_value, 2), y_value_float=round(y_value, 2))
            
            elif event.axis == 4:  # Gatilho esquerdo
                trigger_value = joystick.get_axis(4)  # Mantenha o mesmo valor
                gamepad.left_trigger_float(value_float=round(trigger_value, 2))
            
            elif event.axis == 5:  # Gatilho direito
                trigger_value = joystick.get_axis(5)  # Mantenha o mesmo valor
                gamepad.right_trigger_float(value_float=round(trigger_value, 2))





            
        # Update and reset gamepad state after processing events
        gamepad.update()
