#!/usr/bin/env python


import rospy
import rosbag
from tf_bag import BagTfTransformer
from std_msgs.msg import String
import numpy as np

global tag_qty
tag_qty=4

def record():

    rospy.init_node('listener', anonymous=True)

    bag_transformer = BagTfTransformer('/home/mohamadi/snake_bot_files/2020-03-11-21-24-15.bag')

    rospy.loginfo(bag_transformer.getTransformFrameTuples())

    rospy.loginfo('\n\n ########## \n')

    time_stamps=[tag_qty*[]]
    translations=[tag_qty*[]]

    rospy.loginfo(time_stamps)
    for i in range(2,tag_qty*2+1,2):
        rospy.loginfo('i = %i' %i)

        target_frame='tag_'+str(i)
        rospy.loginfo('Target frame, : %s \n' %target_frame )

        tmp_times=bag_transformer.getTransformUpdateTimes('camera', target_frame)
        time_stamp_i=[]
        translations_i=[]
        while True:
            try:
                time_instant=next(tmp_times)
                time_stamp_i.append(time_instant.to_sec())
                rospy.loginfo(time_stamp_i[-1])

                tmp_translation_i, quaternion = bag_transformer.lookupTransform('Table_Frame',\
                 target_frame , time_instant)
                translations_i.append(tmp_translation_i)


            except StopIteration:
                break

        translations.append(translations_i)
        time_stamp_i=np.array(time_stamp_i)
        time_stamp_i=time_stamp_i-time_stamp_i[0]
        time_stamps.append(time_stamp_i)
        #rospy.loginfo('last time is %.3f',t[-1])
        rospy.loginfo('lenght of time is: %i ' , len(time_stamp_i))

        #translations=np.array(translations)
        for tt in translations:
            #rospy.loginfo(bag_transformer.getTransformFrameTuples())
            rospy.loginfo(tt)
            #rospy.loginfo(translation)

    np.save('/home/mohamadi/snake_bot_files/recorded_posesnnn.npy', [time_stamps, [translations]], allow_pickle=True)

    rospy.loginfo('The data is saved.')


if __name__ == '__main__':
    record()


























#
