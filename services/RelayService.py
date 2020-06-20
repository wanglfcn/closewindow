import requests

import RPi.GPIO as GPIO
import logging
from time import sleep
from tornado.options import options
from services.Scheduler import *
import datetime
from services.CameraService import *

ON = False
OFF = True

open_window_relay_list = (11,)
close_window_relay_list = (13,)
window_relay_switch = (15,)
fan_relay_list = (16, 18)

def __init__():
    initPortMode()
    cleanUp()
    logging.getLogger().info('init Relay Service')

def resetCloseWindowRelay():
    initPortMode()
    GPIO.output(close_window_relay_list, OFF)
    GPIO.output(window_relay_switch, OFF)
    logging.getLogger().info('reset close relay to off')

def resetOpenWindowRelay():
    initPortMode()
    GPIO.output(open_window_relay_list, OFF)
    GPIO.output(window_relay_switch, OFF)
    logging.getLogger().info('reset open relay to off')


def closeWindow():
    initPortMode()
    GPIO.output(window_relay_switch, OFF)
    GPIO.output(open_window_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(close_window_relay_list, ON)
    sleep(options.power_delay_on)
    GPIO.output(window_relay_switch, ON)
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=options.power_delay_off)
    scheduler.add_job(resetCloseWindowRelay, 'date', run_date=run_date)
    logging.getLogger().info('close window')
    msg = '{"code":0,"status":"success","msg":"window is closed"}'
    requests.post(url=options.log_url, json=msg)

def openWindow():
    initPortMode()
    GPIO.output(window_relay_switch, OFF)
    GPIO.output(close_window_relay_list, OFF)
    sleep(options.power_delay_on)
    GPIO.output(open_window_relay_list, ON)
    sleep(options.power_delay_on)
    GPIO.output(window_relay_switch, ON)
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=options.power_delay_off)
    scheduler.add_job(resetOpenWindowRelay, 'date', run_date=run_date)
    logging.getLogger().info('open window')
    msg = '{"code":0,"status":"success","msg":"window is opened"}'
    requests.post(url=options.log_url, json=msg)

def closeFan():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(fan_relay_list, GPIO.OUT, initial=OFF)
    GPIO.output(fan_relay_list, OFF)
    logging.getLogger().info('close fan')
    msg = '{"code":0,"status":"success","msg":"fan is closed"}'
    requests.post(url=options.log_url, json=msg)

def openFan():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(fan_relay_list, GPIO.OUT, initial=OFF)
    GPIO.output(fan_relay_list, ON)
    logging.getLogger().info('open fan')
    msg = '{"code":0,"status":"success","msg":"fan is opened"}'
    requests.post(url=options.log_url, json=msg)

def takePhoto():
    logging.getLogger().info('take photo')
    c = CameraService()
    fileName = c.takePhoto()
    msg = '{"code":0,"status":"success","msg":"photo is taken file: %s"}' % (fileName,)
    requests.post(url=options.log_url, json=msg)
    files = {'file': open(fileName, 'rb')}
    requests.post(url=options.image_url, files=files)

def initPortMode():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(open_window_relay_list, GPIO.OUT, initial=OFF)
    GPIO.setup(close_window_relay_list, GPIO.OUT, initial=OFF)
    GPIO.setup(window_relay_switch, GPIO.OUT, initial=OFF)
    GPIO.setup(fan_relay_list, GPIO.OUT, initial=OFF)

def cleanUp():
    GPIO.cleanup()
    logging.getLogger().info('clean up gpio')

