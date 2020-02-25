import RPi.GPIO as GPIO
import logging
from time import sleep
from tornado.options import options
from services.Scheduler import *
import datetime

ON = False
OFF = True

open_window_relay_list = (11,)
close_window_relay_list = (13,)
fan_relay_list = ()

def __init__():
    initPortMode()
    cleanUp()
    logging.getLogger().info('init Relay Service')

def resetCloseWindowRelay():
    initPortMode()
    GPIO.output(close_window_relay_list, OFF)
    logging.getLogger().info('reset close relay to off')

def resetOpenWindowRelay():
    initPortMode()
    GPIO.output(open_window_relay_list, OFF)
    logging.getLogger().info('reset open relay to off')


def closeWindow():
    initPortMode()
    GPIO.output(open_window_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(close_window_relay_list, ON)
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=options.power_delay_off)
    scheduler.add_job(resetCloseWindowRelay, 'date', run_date=run_date)
    logging.getLogger().info('close window')

def openWindow():
    initPortMode()
    GPIO.output(close_window_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(open_window_relay_list, ON)
    sleep(options.power_delay_on)
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=options.power_delay_off)
    scheduler.add_job(resetOpenWindowRelay, 'date', run_date=run_date)
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
    GPIO.setup(open_window_relay_list, GPIO.OUT, initial=OFF)
    GPIO.setup(close_window_relay_list, GPIO.OUT, initial=OFF)

def cleanUp():
    GPIO.cleanup()
    logging.getLogger().info('clean up gpio')

