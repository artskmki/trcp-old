#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import smach
import smach_ros
import sensor_msgs
import sensor_msgs.msg
import hokuyo_node
import math
from std_msgs.msg import *
from sensor_msgs.msg import LaserScan
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import *
import easygui
import datetime
from collections import OrderedDict
from trcp_basic_function.task_setup import *
#from trcp_utils.kobuki import *
from kobuki_msgs.msg import ButtonEvent
import numpy as np

qa_n=0
def get_qa_count(data):
    print data.data
    global qa_n
    qa_n +=1
    rospy.loginfo('qa count: ' + str(qa_n))

# for KOBUKI hardware
btn=False
button0 = { ButtonEvent.Button0:0, ButtonEvent.Button1:1, ButtonEvent.Button2:2, }
button1 = { ButtonEvent.RELEASED:'Released', ButtonEvent.PRESSED:'Pressed ', }
buttonS = [ 'Released',  'Released',  'Released', ]
def ButtonEventCallback(data):
    buttonS[button0[data.button]]=button1[data.state]
    print "push button"
    global btn
    btn = True



class BF3Task():
    def __init__(self):
        rospy.init_node('bf3task', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # Initialize Kobuki hardware
        rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback )

        # Subscribe to voice command
        self.voice_commnad = rospy.Subscriber('hsr_c', Int32, self.get_voice_command, queue_size=1)

        # Subscribe to qa count
        rospy.Subscriber('qa_in', Int32, get_qa_count, queue_size=1)
        
        self.say_pub = rospy.Publisher('str_in', String, queue_size=10)
        self.say_pub.publish("")
        rospy.sleep(0.1)

        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")

        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        rospy.loginfo("Connected to move base server")

        rospy.loginfo("Setting Initial Pose")
        pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped)
        p   = PoseWithCovarianceStamped();
        msg = PoseWithCovariance();
        angle = 0
        q_angle = quaternion_from_euler(0, 0, angle, 'sxyz')
        q = Quaternion(*q_angle)
        msg.pose = Pose(Point(0.0, 0.0, 0.000), q);
        msg.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853];
        p.pose = msg;
        p.header.stamp = rospy.Time.now()
        p.header.frame_id="map"
        rospy.sleep(2.0)
        rospy.loginfo("Setting Pose")
        pub.publish(p);

        #
        rospy.loginfo('Wait Button on in the ' + str(self.room))
        while True:
          if btn == True:
            break

        rospy.sleep(5.0)
        # Greetings
        self.say_pub.publish("何でも質問に答えますよ")
        self.qa_n = 0
        while True:
          if self.qa_n == 3:
            break


        rospy.loginfo("Starting BF3 test")
        locations = dict()
        locations['exit'] = Pose(Point(0.0, 0.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        # Set up the goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = locations['exit']
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Let the user know where the robot is going next
        rospy.loginfo("Going to: " + str(location))

        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)

        # Allow 5 minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
        # Check for success or failure
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Goal succeeded!")
                rospy.loginfo("State:" + str(state))
            else:
              rospy.loginfo("Goal failed with error code: " + str(goal_states[state]))

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.move_base.cancel_goal()
        rospy.sleep(2)
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

def trunc(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])

if __name__ == '__main__':
    try:
        BF3Task()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("BF3 task finished.")


