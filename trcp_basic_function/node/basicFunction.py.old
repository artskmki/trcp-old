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


# A list of rooms and tasks
task_list = {'ready_pos':['ready_task'], 'pp_room':['mop_floor'], 'at_room':['mop_floor'], 'wdys_room':['mop_floor'], 'leaving_arena':['mop_floor']}

class ReadyTask(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])
        self.task = 'ready_task'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

        self.say_pub = rospy.Publisher('str_in', String, queue_size=10)
        self.say_pub.publish("")
        rospy.sleep(0.1)

    def execute(self, userdata):        
        #
        rospy.loginfo('Wait Button on in the ' + str(self.room))
        while True:
            if btn == True:
                break

        # Greetings
        self.say_pub.publish("こんにちは、私の名前はイレイサーです。よろしくお願いします。")
        rospy.sleep(6.0)

        rospy.loginfo("Setting Initial Pose")
        pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped)
        p   = PoseWithCovarianceStamped();
        msg = PoseWithCovariance();
        #q_angle = quaternion_from_euler(0, 0, 0, 'sxyz')
        #q = Quaternion(*q_angle)
        #msg.pose = Pose(Point(-2.0, 0.0, 0.000), q);
        msg.pose = Pose(Point(-2.0, 0.0, 0.000), Quaternion(0.000, 0.000, 0.0, 1.0));
        msg.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853];
        p.pose = msg;
        p.header.stamp = rospy.Time.now()
        p.header.frame_id="map"
        rospy.sleep(2.0)
        rospy.loginfo("Setting Pose")
        pub.publish(p);

        rospy.loginfo('Wait door open in the ' + str(self.room))
        while True:
            if meanDist > 100.0:
                print "door is now open!!"
                break

        rospy.sleep(5.0)
        self.cmd_vel_pub.publish(Twist())
        move_cmd = Twist()
        move_cmd.linear.x = 0.2
        for t in range(50):
            self.cmd_vel_pub.publish(move_cmd)
            rospy.sleep(0.1)

        # Stop the robot
        move_cmd = Twist()
        self.cmd_vel_pub.publish(move_cmd)
        rospy.sleep(1)


        message = "Done wait door open " + str(self.room) + "!"
        rospy.loginfo(message)

        update_task_list(self.room, self.task)

        return 'succeeded'

class PickPlace(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('Pick and Place in the ' + str(self.room))
        # Greetings
        self.say_pub.publish("ピックアンドプレースのタスクを開始します")
        rospy.sleep(5.0)

        #while True:
        #    rospy.sleep(1)
        rospy.sleep(5.0)


        message = "Done pick and place the " + str(self.room) + "!"
        rospy.loginfo(message)

        update_task_list(self.room, self.task)

        return 'succeeded'


class AvoidThat(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('Avoid That in the ' + str(self.room))
        # Greetings
        self.say_pub.publish("障害物を避けながら次の部屋に進みます")
        rospy.sleep(5.0)

        message = "Done avoid that the " + str(self.room) + "!"
        rospy.loginfo(message)

        update_task_list(self.room, self.task)

        return 'succeeded'


class WhatDys(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('What did you say in the ' + str(self.room))
        # Greetings
        self.say_pub.publish("何でも質問に答えますよ")
        rospy.sleep(5.0)
        
        self.qa_n = 0
        while True:
          if self.qa_n == 3:
            break 
          rospy.sleel(0.5)
 
        message = "Done what did you say  the " + str(self.room) + "!"
        rospy.loginfo(message)

        update_task_list(self.room, self.task)

        return 'succeeded'

class LeavingArena(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('Leaving Arena in the ' + str(self.room))



        message = "Done leaving arena the " + str(self.room) + "!"
        rospy.loginfo(message)

        update_task_list(self.room, self.task)

        return 'succeeded'

def update_task_list(room, task):
    task_list[room].remove(task)
    if len(task_list[room]) == 0:
        del task_list[room]

class main():
    def __init__(self):
        rospy.init_node('basic_f', anonymous=False)

        # Set the shutdown function (stop the robot)
        rospy.on_shutdown(self.shutdown)



        # Initialize Kobuki hardware
        rospy.Subscriber("/mobile_base/events/button", ButtonEvent, ButtonEventCallback )


        # Initialize a number of parameters and variables
        setup_task_environment(self)

        
        # Turn the room locations into SMACH move_base action states
        nav_states = {}

        for room in self.room_locations.iterkeys():
            nav_goal = MoveBaseGoal()
            nav_goal.target_pose.header.frame_id = 'map'
            nav_goal.target_pose.pose = self.room_locations[room]
            move_base_state = SimpleActionState('move_base', MoveBaseAction, goal=nav_goal,
                                                result_cb=self.move_base_result_cb,
                                                exec_timeout=rospy.Duration(15.0),
                                                server_wait_timeout=rospy.Duration(10.0))
            nav_states[room] = move_base_state


        # Create a state machine for the Ready subtask(s)
        sm_ready_pos = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_ready_pos:
            StateMachine.add('READY_TASK', ReadyTask('ready_pos', 5),
                             transitions={'succeeded':'','aborted':'','preempted':''})
            
        # Create a state machine for the pp room subtask(s)
        sm_pp_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_pp_room:
            StateMachine.add('PICK_PLACE', PickPlace('pp_room', 5),
                             transitions={'succeeded':'','aborted':'','preempted':''})

        # Create a state machine for the at room subtask(s)
        sm_at_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_at_room:
            StateMachine.add('AVOID_THAT', AvoidThat('at_room', 5),
                             transitions={'succeeded':'','aborted':'','preempted':''})

        # Create a state machine for the wdys room subtask(s)
        sm_wdys_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_wdys_room:
            StateMachine.add('WHAT_DYS', WhatDys('wdys_room', 5),
                             transitions={'succeeded':'','aborted':'','preempted':''})

        # Create a state machine for the wdys room subtask(s)
        sm_leaving_arena = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_leaving_arena:
            StateMachine.add('LEAVING_ARENA', LeavingArena('leaving_arena', 5),
                             transitions={'succeeded':'','aborted':'','preempted':''})


        # Initialize the overall state machine
        sm_basic_f = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Build the basic f state machine from the nav states 
        # and task states
        with sm_basic_f:
            StateMachine.add('READY_TASK', sm_ready_pos,
                             transitions={'succeeded':'PP_ROOM','aborted':'PP_ROOM','preempted':'PP_ROOM'})

            StateMachine.add('PP_ROOM', nav_states['pp_room'],
                             transitions={'succeeded':'PP_ROOM_TASKS','aborted':'AT_ROOM','preempted':'AT_ROOM'})

            # When the tasks are done, continue on to the AT_ROOM 
            StateMachine.add('PP_ROOM_TASKS', sm_pp_room,
                             transitions={'succeeded':'AT_ROOM','aborted':'AT_ROOM','preempted':'AT_ROOM'})

            StateMachine.add('AT_ROOM', nav_states['at_room'],
                             transitions={'succeeded':'AT_ROOM_TASKS','aborted':'WDYS_ROOM','preempted':'WDYS_ROOM'})

            # When the tasks are done, continue on to the wdys_room
            StateMachine.add('AT_ROOM_TASKS', sm_at_room,
                             transitions={'succeeded':'WDYS_ROOM','aborted':'WDYS_ROOM','preempted':'WDYS_ROOM'})

            StateMachine.add('WDYS_ROOM', nav_states['wdys_room'], transitions={'succeeded':'WDYS_ROOM_TASKS','aborted':'LEAVING_ARENA','preempted':'LEAVING_ARENA'})

            # When the tasks are done, leaving to the arean
            StateMachine.add('WDYS_ROOM_TASKS', sm_wdys_room,
                             transitions={'succeeded':'LEAVING_ARENA','aborted':'LEAVING_ARENA','preempted':'LEAVING_ARENA'})

            StateMachine.add('LEAVING_ARENA', nav_states['leaving_arena'],
                             transitions={'succeeded':'LEAVING_ARENA_TASKS','aborted':'','preempted':''})

            # When the tasks are done, stop
            StateMachine.add('LEAVING_ARENA_TASKS', sm_leaving_arena,
                             transitions={'succeeded':'','aborted':'','preempted':''})

        # Create and start the SMACH introspection server
        intro_server = IntrospectionServer('basic_f', sm_basic_f, '/SM_ROOT')
        intro_server.start()


        rospy.Subscriber("/scan",LaserScan,scanLaser, queue_size=1)
        
        # Subscribe to voice command
        self.voice_commnad = rospy.Subscriber('hsr_c', Int32, self.get_voice_command, queue_size=1)


        # Subscribe to qa count 
        rospy.Subscriber('qa_in', Int32, get_qa_count, queue_size=1)


        # Execute the state machine
        sm_outcome = sm_basic_f.execute()

        if len(task_list) > 0:
            message = "Ooops! Not all chores were completed."
            message += "The following rooms need to be revisited: "
            message += str(task_list)
        else:
            message = "All chores complete!"

        rospy.loginfo(message)
        easygui.msgbox(message, title="Finished Cleaning")

        intro_server.stop()





    def get_voice_command(self,data):
        print data.data


    def get_qa_count(self,data):
        print data.data
        self.qa_n +=1
        rospy.loginfo('qa count: ' + str(self.qa_n))




    def move_base_result_cb(self, userdata, status, result):
        if status == actionlib.GoalStatus.SUCCEEDED:
            pass

    # シャットダウンの処理
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        #sm_nav.request_preempt()
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        rospy.loginfo("House clearning test finished.")


