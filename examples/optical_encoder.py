import asyncio
import sys
import time
from telemetrix_aio import telemetrix_aio

"""
This program continuously monitors an optical encoder Sensor
It reports changes of the wheel orientation.
"""

ENCODER_PIN = 16
INTERRUPT_MODE = 2
WHEEL_GAPS = 20


# A callback function to display the distance
async def the_callback(data):
    """
    The callback function to display the change in distance
    :param data: [report_type = PrivateConstants.ENCODER_REPORT, encoder pin number, encoder ticks, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[3]))
    print(f'Encoder Report: Pin: {data[1]} Ticks: {data[2]} Time: {date}')


async def optical_encoder(my_board, encoder_pin, interrupt_mode=2, wheel_size=20, callback=None):
    """
    Set the pin mode for a encoder device. Results will appear via the
    callback.

    :param my_board: an pymata express instance
    :param encoder_pin: Arduino pin number
    :param interrupt_mode: Arduino Interrupt Mode
    :param wheel_size: Number of gaps in encoder wheel disk
    :param callback: The callback function
    """

    # set the pin mode for the trigger and echo pins
    await my_board.set_pin_mode_encoder(encoder_pin, interrupt_mode, wheel_size, callback)
    # wait forever
    while True:
        try:
            await asyncio.sleep(.01)
        except KeyboardInterrupt:
            await my_board.shutdown()
            sys.exit(0)


# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = telemetrix_aio.TelemetrixAIO()

try:
    # start the main function
    loop.run_until_complete(optical_encoder(board, ENCODER_PIN, INTERRUPT_MODE, WHEEL_GAPS, the_callback))
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
