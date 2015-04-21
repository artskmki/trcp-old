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


def get_voice_command(self,data):
    print data.data

qa_n=0
def get_qa_count(data):
    print data.data
    global qa_n
    qa_n +=1
    rospy.loginfo('qa count: ' + str(qa_n))

ranges=[]
meanDist=0.0
maxDist=-100.0
minDist= 100.0
def scanLaser(data):
    global ranges
    ranges=data.ranges
    mid_index = len(data.ranges) // 2
    dists = [val for val in ranges[mid_index-10:mid_index+10]
           if not math.isnan(val)]
    if len(dists) != 0:
      global meanDist
      meanDist =  np.mean(dists)
      global maxDist
      maxDist = np.max(dists)
      global minDist
      minDist = np.min(dists)
      rospy.loginfo('range:min mean min >'+str(minDist)+' '+str(meanDist)+' '+str(maxDist))


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



class BF1Task():
    def __init__(self):
        rospy.init_node('bf3task', anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # Initialize Kobuki hardware
        rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback )

        # Subscribe to Laser Range 
        rospy.Subscriber("/scan",LaserScan,scanLaser, queue_size=1)

        # Subscribe to voice command
        #self.voice_commnad = rospy.Subscriber('hsr_c', Int32, self.get_voice_command, queue_size=1)

        # Subscribe to qa count
        rospy.Subscriber('qa_in', Int32, get_qa_count, queue_size=1)
        
        self.say_pub = rospy.Publisher('str_in', String, queue_size=10)
        self.say_pub.publish("")
        rospy.sleep(0.1)

        # Publisher to manually control the robot (e.g. to stop it)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        # Set location
        locations = dict()
        locations['PandP'] = Pose(Point(1.4, 3.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        locations['QA'] = Pose(Point(1.4, 1.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        locations['exit'] = Pose(Point(2.4, 3.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))



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
        msg.pose = Pose(Point(-1.7, 0.0, 0.000), q);
        msg.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853];
        p.pose = msg;
        p.header.stamp = rospy.Time.now()
        p.header.frame_id="map"
        rospy.sleep(2.0)
        rospy.loginfo("Setting Pose")
        pub.publish(p);


        # Wait Button on
        self.say_pub.publish("準備完了です。コブキのボタンを押して下さい。")
        rospy.loginfo("Wait Button on" )
        while True:
          if btn == True:
            break

        # Wait door open
        while True:
          if meanDist > 2.0:
            print "door is now open!!"
            break
        rospy.sleep(2.0)
 
        self.cmd_vel_pub.publish(Twist())
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
        for t in range(100):
            self.cmd_vel_pub.publish(move_cmd)
            rospy.sleep(0.1)

        # Stop the robot
        move_cmd = Twist()
        self.cmd_vel_pub.publish(move_cmd)
        rospy.sleep(3)


        # Go to Pick & Place
        self.say_pub.publish("ピックアンドプレースの部屋に移動します")
        rospy.loginfo("Going to Pick and Place !!")
        # Set up the goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = locations['PandP']
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)

        # Allow 5(3x60=180) minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
        # Check for success or failure
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
              rospy.loginfo("Goal succeeded!")
            else:
              rospy.loginfo("Goal failed")

        # start Pick and Place Task
        #
        #
        # end Pick and Place Task


        # Go to Question 
        self.say_pub.publish("なんでも答えちゃう部屋に移動します")
        rospy.loginfo("Going to Question Place !!")
        # Set up the goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = locations['QA']
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)

        # Allow 5(3x60=180) minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
        # Check for success or failure
        if not finished_within_time:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
              rospy.loginfo("Goal succeeded!")
            else:
              rospy.loginfo("Goal failed")


        # start QA Task
        self.say_pub.publish("さて、なんでも質問に答えちゃいますよ。質問者が見つからないので、私の前に来て質問して下さい。")
        global qa_n
        qa_n = 0
        while True:
          if qa_n == 3:
            break
        rospy.sleep(3.0)
        # exit
        self.say_pub.publish("三つの質問に答えたので退場します。")
        rospy.loginfo("Going to Exit !!")

        locations = dict()
        locations['exit'] = Pose(Point(2.4, 3.0, 0.0), Quaternion(0.000, 0.000, 0.0, 1.0))
        # Set up the goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = locations['exit']
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()

        # Start the robot toward the next location
        self.move_base.send_goal(self.goal)
        # Allow 5(5x60=300) minutes to get there
        finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
 



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
        BF1Task()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("BF1 task finished.")

