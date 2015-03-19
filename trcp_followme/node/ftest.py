#!/usr/bin/env python
import rospy
from std_msgs.msg import *

class Listener():
    def __init__(self):
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("hsr_c", Int32, self.callback)
        self.f_flag=0
        rospy.spin()

    def callback(self, data):
        rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
        self.f_flag+=data.data
        self.pr_flag()
        print self.f_flag
    def pr_flag(self):
        print self.f_flag

if __name__ == '__main__':
    Listener()


