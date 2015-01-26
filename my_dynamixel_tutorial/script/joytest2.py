#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64 
from sensor_msgs.msg import Joy 

def callback(data):
    rospy.loginfo("*")
    print 'buttons:["%s %s %s %s %s %s %s %s %s %s %s %s %s"]' % (data.buttons[0],data.buttons[1],data.buttons[2],data.buttons[3],data.buttons[4],data.buttons[5],data.buttons[6],data.buttons[7],data.buttons[8],data.buttons[9],data.buttons[10],data.buttons[11],data.buttons[12])
    print 'axes: ["%s %s %s %s %s %s"]' % (data.axes[0],data.axes[1],data.axes[2],data.axes[3],data.axes[4],data.axes[5])


    pub1.publish(data.axes[0]*10)
    pub2.publish(data.axes[0]*10)
    pub3.publish(data.axes[0]*10)
    pub4.publish(data.axes[0]*10)



    pub5.publish(data.axes[3]*50)
    pub6.publish(data.axes[3]*-50)
    pub7.publish(data.axes[3]*-50)
    pub8.publish(data.axes[3]*50)

def listener():
    global pub1
    pub1 = rospy.Publisher('/fl_caster_rotation_joint/command',Float64)
    global pub2
    pub2 = rospy.Publisher('/fl_caster_rotation_joint/command',Float64)
    global pub3
    pub3 = rospy.Publisher('/fl_caster_rotation_joint/command',Float64)
    global pub4
    pub4 = rospy.Publisher('/fl_caster_rotation_joint/command',Float64)

    global pub5
    pub5 = rospy.Publisher('/fl_caster_r_wheel_joint/command',Float64)
    global pub6
    pub6 = rospy.Publisher('/br_caster_r_wheel_joint/command',Float64)
    global pub7
    pub7 = rospy.Publisher('/bl_caster_r_wheel_joint/command',Float64)
    global pub8
    pub8 = rospy.Publisher('/fr_caster_r_wheel_joint/command',Float64)

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("joy", Joy, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

