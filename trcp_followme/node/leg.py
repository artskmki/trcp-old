#!/usr/bin/env python

import rospy
import people_msgs
from people_msgs.msg import PositionMeasurementArray 

def callback(data):
    rospy.loginfo(len(data.people))
    for l in data.people:
        rospy.loginfo(l.reliability)
        rospy.loginfo(l.pos)

def leg():
    rospy.init_node('leg', anonymous=True)
    rospy.Subscriber("/leg_tracker_measurements", PositionMeasurementArray, callback)
    rospy.spin()


if __name__ == '__main__':
    leg()


