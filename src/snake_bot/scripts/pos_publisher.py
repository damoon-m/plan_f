#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Float32MultiArray, Float64
from std_msgs.msg import Int64, Int16,Int16MultiArray,MultiArrayLayout,MultiArrayDimension
import numpy as np
import pickle
import sys, select, termios, tty
from threading import Thread
from time import sleep
#from pos_publisher_functions import initialize, encoder_sub_cb, control,pos_publish, getKey

pre_rec_poses=[]
#pos_cmd_pub = rospy.Publisher('pos_cmd', Float32MultiArray, queue_size=10)
move_pub=rospy.Publisher('move_cmd', Int16, queue_size=10)


settings = termios.tcgetattr(sys.stdin)
global pos_servo
pos_servo=np.array([0,0,0, 0,0,0])
global base_locs
int_base_loc=0
global speed
speed=150
global SERVO_MAX
SERVO_MAX= np.deg2rad(150)
global PI
PI=np.deg2rad(180)
#pre recorded base loacations

def initialize():

    global pre_rec_poses
    global base_locs
    rospy.init_node('pos_publisher', anonymous=True)

    with open('/home/mohamadi/snake_bot_files/pre_rec_poses.pkl', 'rb') as infile:
        pre_rec_poses =pickle.load(infile)
        pre_rec_poses =pre_rec_poses[0]
        base_locs=np.zeros(len(pre_rec_poses))

    for i in range(len(pre_rec_poses)):
        base_locs[i]=pre_rec_poses[i][0]+915 #so it starts from 0

    rospy.loginfo("length %i lkdjf" % len(pre_rec_poses))
    rospy.loginfo(pre_rec_poses[0][0])
    rospy.loginfo(pre_rec_poses[0][1])
    rospy.loginfo(pre_rec_poses[0][1][5])

def encoder_sub_cb(data):
    global base_locs
    global int_base_loc
    global pos_servo
    tmp=data.data*1.1875-915
    base_loc=np.clip(tmp,np.min(base_locs), np.max(base_locs))
    int_base_loc=np.int(np.rint(base_loc))
    pos_servo=pre_rec_poses[int_base_loc][1]
    pos_servo=fmap(pos_servo,-PI, PI, -SERVO_MAX, SERVO_MAX)

def control():
    global speed
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "\n Time: %s \n Base Location: %.2f mm \n \
        Move Speed: %i \n" % (rospy.get_time(), int_base_loc, speed)
        rospy.loginfo(hello_str)
        key=getKey()

        if key=='w':
            move_pub.publish(+11)
        elif key=="s":
            move_pub.publish(-11)

        elif (key=="q"):
            speed=min(speed+10,500)
            move_pub.publish(speed)
        elif (key=="a") & (speed > 0):
            speed=speed-10
            move_pub.publish(speed)
        elif key=="\x03":
            rospy.signal_shutdown('Bye Bye')
        else:
            move_pub.publish(0)

        rate.sleep()

def pos_publish1():
    global pos_servo
    global SERVO_MAX
    global PI
    sect1_pub=rospy.Publisher('/joint1_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        servo_cmd_msg.data=-1*pos_servo[0]
        sect1_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish2():
    global pos_servo
    global SERVO_MAX
    global PI
    sect2_pub=rospy.Publisher('/joint2_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[1]
        sect2_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish3():
    global pos_servo
    global SERVO_MAX
    global PI
    sect3_pub=rospy.Publisher('/joint3_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        servo_cmd_msg.data=-1*pos_servo[2]
        sect3_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish4():
    global pos_servo
    global SERVO_MAX
    global PI
    sect4_pub=rospy.Publisher('/joint4_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        servo_cmd_msg.data=pos_servo[3]
        sect4_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish5():
    global pos_servo
    global SERVO_MAX
    global PI
    sect5_pub=rospy.Publisher('/joint5_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        servo_cmd_msg.data=-1*pos_servo[4]
        sect5_pub.publish(servo_cmd_msg)
        rate.sleep()

def pos_publish6():
    global pos_servo
    global SERVO_MAX
    global PI
    sect6_pub=rospy.Publisher('/joint6_controller/command', Float64, queue_size=10)
    servo_cmd_msg=Float64()
    rate = rospy.Rate(5)
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



rospy.Subscriber('encoder_pos', Int64, encoder_sub_cb)

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
