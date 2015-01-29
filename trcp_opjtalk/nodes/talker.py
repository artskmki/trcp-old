#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String


def talker():
    pub = rospy.Publisher('jtalk', String)
    rospy.init_node('talker')
    str = "私の名前は岡田です"
    rospy.loginfo(str)
    pub.publish(String(str))
    rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
