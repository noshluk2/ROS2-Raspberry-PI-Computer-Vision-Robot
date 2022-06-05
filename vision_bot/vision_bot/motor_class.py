
import RPi.GPIO as GPIO
import sys



class setup(object):
    def __init__(self,mr_a,mr_b,mr_en,ml_a,ml_b,ml_en):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(mr_a, GPIO.OUT)
        GPIO.setup(mr_b, GPIO.OUT)
        GPIO.setup(mr_en,GPIO.OUT)

        GPIO.setup(ml_a, GPIO.OUT)
        GPIO.setup(ml_b, GPIO.OUT)
        GPIO.setup(ml_en,GPIO.OUT)

        GPIO.setmode(GPIO.BCM)
        self.mr_a=mr_a;self.mr_b=mr_b;
        self.ml_a=ml_a;self.ml_b=ml_b;
        self.mr_en=mr_en;self.ml_en=ml_en
        self.pwm_r =  GPIO.PWM(mr_en,1000)
        self.pwm_l =  GPIO.PWM(ml_en,1000)
        self.pwm_l.start(30)
        self.pwm_r.start(30)



    def stop(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_l.ChangeDutyCycle(0)

    def direction_set(self,left_wheel_vel , right_wheel_vel):
        GPIO.output(self.ml_a,left_wheel_vel >0 );
        GPIO.output(self.ml_b,left_wheel_vel < 0);
        GPIO.output(self.mr_a,right_wheel_vel > 0 );
        GPIO.output(self.mr_b,right_wheel_vel < 0);


    def motor_turn_off(self):
        GPIO.cleanup()
        sys.exit(0)
