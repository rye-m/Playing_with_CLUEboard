from adafruit_clue import clue
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)

    print('Waiting for connection...')
    while not ble.connected:
        pass # Wait here until the wizard connects using Bluefruit Connect

    print('Connected!\n')
    while ble.connected:
        # Transmit device state to wizard.
        if clue.button_a:
            uart.write('\nUser pressed button A!\n')
        if clue.button_b:
            uart.write('\nUser pressed button B!\n')

        # Receive state from wizard; device should react.
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    if packet.button == ButtonPacket.BUTTON_1:
                        print('Do something for button 1!')
                    if packet.button == ButtonPacket.BUTTON_2:
                        print('Do something for button 2!')
                    if packet.button == ButtonPacket.BUTTON_3:
                        print('Do something for button 3!')
                    if packet.button == ButtonPacket.BUTTON_4:
                        print('Do something for button 4!')
                    elif packet.button == ButtonPacket.UP:
                        print('Do something for UP button!')
                    elif packet.button == ButtonPacket.DOWN:
                        print('Do something for DOWN button!')
                    elif packet.button == ButtonPacket.LEFT:
                        print('Do something for LEFT button!')
                    elif packet.button == ButtonPacket.RIGHT:
                        print('Do something for RIGHT button!')

    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
    print('Disconnected!\n')