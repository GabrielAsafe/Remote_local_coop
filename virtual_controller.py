import vgamepad as vg
import time

#cria o gamepad usango o vigem
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
    '0': 'XUSB_GAMEPAD_SQUARE',   # Quadrado
    '1': 'XUSB_GAMEPAD_CIRCLE',   # Círculo
    '2': 'XUSB_GAMEPAD_CROSS',    # X (Cruz)
    '3': 'XUSB_GAMEPAD_TRIANGLE', # Triângulo

    # Ombros e gatilhos
    '10': 'XUSB_GAMEPAD_RIGHT_SHOULDER',  # R1
    '9': 'XUSB_GAMEPAD_LEFT_SHOULDER',   # L1
    '4': 'XUSB_GAMEPAD_LEFT_TRIGGER',    # L2 (eixo)
    '5': 'XUSB_GAMEPAD_RIGHT_TRIGGER',   # R2 (eixo)

    # Direcionais (D-Pad)
    '11': 'XUSB_GAMEPAD_DPAD_UP',        # Cima
    '12': 'XUSB_GAMEPAD_DPAD_DOWN',      # Baixo
    '13': 'XUSB_GAMEPAD_DPAD_LEFT',      # Esquerda
    '14': 'XUSB_GAMEPAD_DPAD_RIGHT',     # Direita

    # Analógicos
    'LX': 'XUSB_GAMEPAD_LEFT_THUMB_X',   # Eixo X do analógico esquerdo
    'LY': 'XUSB_GAMEPAD_LEFT_THUMB_Y',   # Eixo Y do analógico esquerdo
    'RX': 'XUSB_GAMEPAD_RIGHT_THUMB_X',  # Eixo X do analógico direito
    'RY': 'XUSB_GAMEPAD_RIGHT_THUMB_Y',  # Eixo Y do analógico direito
}







# press a button to wake the device up
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
gamepad.update()
time.sleep(0.5)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)






# press buttons and things
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
gamepad.left_trigger_float(value_float=0.5)
gamepad.right_trigger_float(value_float=0.5)
gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.2)
gamepad.right_joystick_float(x_value_float=-1.0, y_value_float=1.0)

gamepad.update()

time.sleep(1.0)

# release buttons and things
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
gamepad.right_trigger_float(value_float=0.0)
gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)

gamepad.update()

time.sleep(1.0)

# reset gamepad to default state
gamepad.reset()

gamepad.update()

time.sleep(1.0)