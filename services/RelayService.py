import RPi.GPIO as GPIO
import logging
from time import sleep
from tornado.options import options

ON = False
OFF = True

window_relay_list = (11, 13)
fan_relay_list = ()
power_relay_list = (15,)

def __init__():
    initPortMode()
    cleanUp()
    logging.getLogger().info('init Relay Service')


def closeWindow():
    initPortMode()
    GPIO.output(power_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(window_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(power_relay_list, ON)
    sleep(options.power_delay_off)
    GPIO.output(power_relay_list, OFF)
    logging.getLogger().info('close window')

def openWindow():
    initPortMode()
    GPIO.output(power_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(window_relay_list, ON)
    sleep(options.power_delay_on)
    GPIO.output(power_relay_list, ON)
    sleep(options.power_delay_off)
    GPIO.output(power_relay_list, OFF)
    logging.getLogger().info('open window')

def closeFan():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(fan_relay_list, GPIO.OUT, initial=OFF)
    GPIO.output(fan_relay_list, OFF)
    logging.getLogger().info('close fan')

def openFan():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(fan_relay_list, GPIO.OUT, initial=OFF)
    GPIO.output(fan_relay_list, ON)
    logging.getLogger().info('open fan')

def takePhoto():
    logging.getLogger().info('take photo')

def initPortMode():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(window_relay_list, GPIO.OUT, initial=OFF)
    GPIO.setup(power_relay_list, GPIO.OUT, initial=OFF)

def cleanUp():
    GPIO.cleanup()
    logging.getLogger().info('clean up gpio')

