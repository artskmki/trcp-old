#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import String

from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import *
import easygui
import datetime
from collections import OrderedDict
from trcp_basic_function.task_setup import *
from trcp_utils.kobuki import *
from tf.transformations import euler_from_quaternion

def callback(data):
    pass

def listener():
    rospy.init_node('listener', anonymous=True)
    q_angle = quaternion_from_euler(0, 0, 0, 'sxyz')
    q = Quaternion(*q_angle)
    #q = quaternion_from_euler(0, 0, 0, 'ryxz')
    print(q)


    rospy.Subscriber("chatter", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()


