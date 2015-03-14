#!/usr/bin/env python

import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import Twist
from trcp_basicF.task_setup import *
import easygui
import datetime
from collections import OrderedDict

# A list of rooms and tasks
task_list = {'pp_room':['goto_position'], 'at_room':['mop_floor'], 'wdys_room':['goto_position', 'mop_floor'], 'leaving_arena':['mop_floor']}


class GotoPosition(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'goto_position'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('Go to the position in the ' + str(self.room))
    
        message = "Done go to the position in the " + str(self.room) + "!"
        rospy.loginfo(message)
        easygui.msgbox(message, title="Succeeded")

        update_task_list(self.room, self.task)



class MopFloor(State):
    def __init__(self, room, timer):
        State.__init__(self, outcomes=['succeeded','aborted','preempted'])

        self.task = 'mop_floor'
        self.room = room
        self.timer = timer
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)

    def execute(self, userdata):
        rospy.loginfo('Mopping the floor in the ' + str(self.room))
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = 0.05
        cmd_vel_msg.angular.z = 1.2
        counter = self.timer
        while counter > 0:
            self.cmd_vel_pub.publish(cmd_vel_msg)
            cmd_vel_msg.linear.x *= -1
            rospy.loginfo(counter)
            counter -= 1
            rospy.sleep(1)

        self.cmd_vel_pub.publish(Twist())
        message = "Done mopping the " + str(self.room) + "!"
        rospy.loginfo(message)
        easygui.msgbox(message, title="Succeeded")

        update_task_list(self.room, self.task)

        return 'succeeded'



def update_task_list(room, task):
    task_list[room].remove(task)
    if len(task_list[room]) == 0:
        del task_list[room]



class main():
    def __init__(self):
        rospy.init_node('basic_function', anonymous=False)

        # Set the shutdown function (stop the robot)
        rospy.on_shutdown(self.shutdown)

        # Initialize a number of parameters and variables
        setup_task_environment(self)

        # Turn the room locations into SMACH move_base action states
        nav_states = {}

        for room in self.room_locations.iterkeys():
            nav_goal = MoveBaseGoal()
            nav_goal.target_pose.header.frame_id = 'map'
            nav_goal.target_pose.pose = self.room_locations[room]
            move_base_state = SimpleActionState('move_base', MoveBaseAction, goal=nav_goal, result_cb=self.move_base_result_cb,
                                                exec_timeout=rospy.Duration(15.0),
                                                server_wait_timeout=rospy.Duration(10.0))
            nav_states[room] = move_base_state

       ''' Create individual state machines for assigning tasks to each room '''

        # Create a state machine for the pp room subtask(s)
        sm_pp_room = StateMachine(outcomes=['succeeded','aborted','preempted'])

        # Then add the subtask(s)
        with sm_pp_room:
            StateMachine.add('GOTO_POSITION', GotoPosition('pp_room', 5), transitions={'succeeded':'','aborted':'','preempted':''})







if __name__ == '__main__':
    main()
