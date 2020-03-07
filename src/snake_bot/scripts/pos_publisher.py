#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32MultiArray, Float64
from std_msgs.msg import Int64, Int16,Int16MultiArray,MultiArrayLayout,MultiArrayDimension
import numpy as np
import pickle
import sys, select, termios, tty
from threading import Thread
from time import sleep

pre_rec_poses=[]
global rate
settings = termios.tcgetattr(sys.stdin)
global pos_servo
pos_servo=np.array([0,0,0, 0,0,0])+np.deg2rad(150)
global base_locs
global int_base_loc
int_base_loc=0
global speed
speed=1
global move_direction
move_direction=1
global SERVO_MAX
SERVO_MAX= np.deg2rad(150)
global PI
PI=np.deg2rad(180)
#pre recorded base loacations

#move_pub=rospy.Publisher('move_cmd', Int16, queue_size=10)
move_pub=rospy.Publisher('/pan_controller/command', Float64, queue_size=10)


def initialize():
    global rate
    global pre_rec_poses
    global base_locs
    rospy.init_node('pos_publisher', anonymous=True)
    rospy.Subscriber('encoder_pos', Int16, encoder_sub_cb)
    rate = rospy.Rate(20)

    with open('/home/mohamadi/snake_bot_files/pre_rec_poses.pkl', 'rb') as infile:
        pre_rec_poses =pickle.load(infile)
        pre_rec_poses =pre_rec_poses[0]
        base_locs=np.zeros(len(pre_rec_poses))

    for i in range(len(pre_rec_poses)):
        base_locs[i]=pre_rec_poses[i][0]+915 #so it starts from 0

def encoder_sub_cb(data):
    global base_locs
    global int_base_loc
    global pos_servo
    tmp=data.data*1.1875
    base_loc=np.clip(tmp,np.min(base_locs), np.max(base_locs))
    #rospy.loginfo(base_loc)
    int_base_loc=np.int(np.rint(base_loc))
    pos_servo=pre_rec_poses[int_base_loc][1]
    pos_servo=fmap(pos_servo,-PI, PI, -SERVO_MAX, SERVO_MAX)
    pos_servo=np.multiply(pos_servo,[1,-1, 1,-1, 1,-1])+np.deg2rad(150)

def control():
    global speed
    global move_direction
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "\n Time: %s \n Base Location: %.2f mm \n \
        Move Speed: %i \n" % (rospy.get_time(), int_base_loc, speed)
        rospy.loginfo(hello_str)
        key=getKey()

        if key=='w':
            move_direction=-1
            move_pub.publish(speed*move_direction)
        elif key=="s":
            move_direction=1
            move_pub.publish(speed*move_direction)

        elif (key=="q"):
            speed=np.clip(speed+0.5,-5,5)
            move_pub.publish(speed*move_direction)
        elif (key=="a") & (speed > 0):
            speed=np.clip(speed-0.5,-5,5)
            move_pub.publish(speed*move_direction)
        elif key=="\x03":
            rospy.signal_shutdown('Bye Bye')
        else:
            move_pub.publish(0)

        rate.sleep()

def pos_publish1():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect1_pub=rospy.Publisher('/joint1_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[0]
        sect1_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish2():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect2_pub=rospy.Publisher('/joint2_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[1]
        sect2_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish3():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect3_pub=rospy.Publisher('/joint3_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[2]
        sect3_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish4():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect4_pub=rospy.Publisher('/joint4_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[3]
        sect4_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish5():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect5_pub=rospy.Publisher('/joint5_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[4]
        sect5_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish6():
    global rate
    global pos_servo
    global SERVO_MAX
    global PI
    sect6_pub=rospy.Publisher('/joint6_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[5]
        sect6_pub.publish(servo_cmd_msg)
        rate.sleep()


def fmap(x, x1, x2, y1, y2):
    return((x-x1)*(y2-y1)/(x2-x1)+y1)

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__ == '__main__':
    initialize()

    Thread(target=pos_publish1).start()
    Thread(target=pos_publish2).start()
    Thread(target=pos_publish3).start()
    Thread(target=pos_publish4).start()
    Thread(target=pos_publish5).start()
    Thread(target=pos_publish6).start()

    try:
        control()
    except rospy.ROSInterruptException:
        pass
