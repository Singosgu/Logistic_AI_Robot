#!/usr/bin/python
# coding=utf-8
#本段代码实现树莓派智能小车的红外避障效果
#代码使用的树莓派GPIO是用的BOARD编码方式。
import RPi.GPIO as GPIO
import time
import os

T_SensorRight = 26
T_SensorCenter = 19
T_SensorLeft = 13

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin = 19
Gpin = 5
Rpin = 6

TRIG = 20
ECHO = 21

def t_up(speed, t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2, False)#AIN2
        GPIO.output(AIN1, True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2, False)#BIN2
        GPIO.output(BIN1, True) #BIN1
        time.sleep(t_time)

def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2, False)#AIN2
        GPIO.output(AIN1, False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2, False)#BIN2
        GPIO.output(BIN1, False) #BIN1
        time.sleep(t_time)

def t_down(speed, t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2, True)#AIN2
        GPIO.output(AIN1, False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2, True)#BIN2
        GPIO.output(BIN1, False) #BIN1
        time.sleep(t_time)

def t_left(speed):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2, True)#AIN2
        GPIO.output(AIN1, False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2, False)#BIN2
        GPIO.output(BIN1, True) #BIN1

def t_right(speed):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2, False)#AIN2
        GPIO.output(AIN1, True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2, True)#BIN2
        GPIO.output(BIN1, False) #BIN1

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(T_SensorRight, GPIO.IN)
    GPIO.setup(T_SensorCenter, GPIO.IN)
    GPIO.setup(T_SensorLeft, GPIO.IN)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(PWMA, GPIO.OUT)

    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
    if os.path.exists('/data/pi/tracking.pid'):
        pass
    else:
        with open('/data/pi/tracking.txt', 'r') as f:
            loc = f.readline(3)
            if loc == 'sta':
                setup()
                L_Motor = GPIO.PWM(PWMA, 100)
                L_Motor.start(0)
                R_Motor = GPIO.PWM(PWMB, 100)
                R_Motor.start(0)
                try:
                    pid = str(os.getpid())
                    with open('/data/pi/tracking.pid', 'w') as f:
                        f.write(pid)
                        f.close()
                    os.system("python3 /data/pi/utils/buzzer.py")
                    t_up(25, 0.3)
                    while True:
                        SR = GPIO.input(T_SensorRight)
                        SC = GPIO.input(T_SensorCenter)
                        SL = GPIO.input(T_SensorLeft)
                        dis = distance()
                        if (dis > 50) == True:
                            if SL == True and SR == True:
                                t_up(25, 0)
                            elif SL == True and SR == False:
                                t_left(25)
                            elif SL == False and SR == True:
                                t_right(25)
                            else:
                                t_stop(0)
                                break
                        else:
                            t_stop(0)
                    os.system("python3 /data/pi/utils/buzzer.py")
                    if os.path.exists('/data/pi/tracking.pid'):
                        os.remove('/data/pi/tracking.pid')
                    with open('/data/pi/tracking.txt', 'w') as f:
                        f.write("end")
                        f.close()
                    destroy()
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                    destroy()
            elif loc == 'end':
                setup()
                L_Motor = GPIO.PWM(PWMA, 100)
                L_Motor.start(0)
                R_Motor = GPIO.PWM(PWMB, 100)
                R_Motor.start(0)
                try:
                    pid = str(os.getpid())
                    with open('/data/pi/tracking.pid', 'w') as f:
                        f.write(pid)
                        f.close()
                    os.system("python3 /data/pi/utils/buzzer.py")
                    t_down(25, 0.3)
                    while True:
                        SR = GPIO.input(T_SensorRight)
                        SC = GPIO.input(T_SensorCenter)
                        SL = GPIO.input(T_SensorLeft)
                        dis = distance()
                        if (dis > 50) == True:
                            if SL == True and SR == True:
                                t_down(15, 0)
                            elif SL == True and SR == False:
                                t_left(15)
                            elif SL == False and SR == True:
                                t_right(15)
                            else:
                                t_stop(0)
                                break
                        else:
                            t_stop(0)
                    os.system("python3 /data/pi/utils/buzzer.py")
                    if os.path.exists('/data/pi/tracking.pid'):
                        os.remove('/data/pi/tracking.pid')
                    with open('/data/pi/tracking.txt', 'w') as f:
                        f.write("sta")
                        f.close()
                    destroy()
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                    destroy()
            else:
                pass
