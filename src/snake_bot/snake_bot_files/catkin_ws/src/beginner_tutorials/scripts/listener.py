#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published
## to the 'chatter' topic

import rospy
import rosbag
from tf_bag import BagTfTransformer
from std_msgs.msg import String
import numpy as np

#from datetime import datetime

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heardd %s', data.data)

def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    #rospy.Subscriber('chatter', String, callback)


    bag_transformer = BagTfTransformer('/home/mohamadi/test_bags/Testbag.bag')

    timess=bag_transformer.getTransformUpdateTimes('world', 'turtle2')
    t=np.array([])
    #translations=np.empty(shape=[3, 0])
    translations=[]
    #t.append(next(timess).to_sec())
    while True:
        try:
            tmp_time=next(timess)
            t=np.append(t,tmp_time.to_sec())
            rospy.loginfo(t[-1])
            translation=[]
            for i in range(2):
                target_frame='turtle'+str(i+1)
                translation_i, quaternion = bag_transformer.lookupTransform('turtle1', target_frame ,tmp_time )
                translation.append(translation_i)
                #translation2, quaternion = bag_transformer.lookupTransform('world', 'turtle2',tmp_time )
                #translations=np.stack((translations, translation))
            translations.append(translation)
        except StopIteration:
            break

    #ttt=t.to_sec()
    t=t-t[0]
    rospy.loginfo('last time is %.3f',t[-1])


    rospy.loginfo('lenght of time is: %i ' , len(t))

    #translations=np.array(translations)
    for tt in translations[::10]:
        #rospy.loginfo(bag_transformer.getTransformFrameTuples())
        rospy.loginfo(tt)
        #rospy.loginfo(translation)

    data=[t, translations]
    np.save('recorded_poses.npy', [t, [translations]], allow_pickle=True)

    rospy.loginfo('The data is saved.')
    rospy.loginfo(ttff)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


























#
