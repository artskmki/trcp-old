#!/usr/bin/env python

import rospy
import smach
import smach_ros
from smach import State, StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from geometry_msgs.msg import Twist
import easygui
import datetime
from collections import OrderedDict
from trcp_basicF.task_setup import *

# A list of rooms and tasks
task_list = {'pp_room':['mop_floor'], 'at_room':['mop_floor'], 'wdys_room':['mop_floor'], 'leaving_arena':['mop_floor']}

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
        rospy.init_node('clean_house', anonymous=False)

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

        # Create a state machine for the pp room subtask(s)
        sm_pp_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_pp_room:
            StateMachine.add('MOP_FLOOR', MopFloor('pp_room', 5), transitions={'succeeded':'','aborted':'','preempted':''})



        # Create a state machine for the at room subtask(s)
        sm_at_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_at_room:
            StateMachine.add('MOP_FLOOR', MopFloor('at_room', 5), transitions={'succeeded':'','aborted':'','preempted':''})



        # Create a state machine for the wdys room subtask(s)
        sm_wdys_room = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_wdys_room:
            StateMachine.add('MOP_FLOOR', MopFloor('wdys_room', 5), transitions={'succeeded':'','aborted':'','preempted':''})



        # Create a state machine for the wdys room subtask(s)
        sm_leaving_arena = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtask(s)
        with sm_leaving_arena:
            StateMachine.add('MOP_FLOOR', MopFloor('leaving_arena', 5), transitions={'succeeded':'','aborted':'','preempted':''})


        # Create a state machine for the hallway subtask(s)
        sm_hallway = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Then add the subtasks
        with sm_hallway:
            StateMachine.add('MOP_FLOOR', MopFloor('hallway', 5), transitions={'succeeded':'','aborted':'','preempted':''})


        # Initialize the overall state machine
        sm_basic_f = StateMachine(outcomes=['succeeded','aborted','preempted'])
        # Build the basic f state machine from the nav states 
        # and task states
        with sm_basic_f:
            StateMachine.add('START', nav_states['hallway'], transitions={'succeeded':'PP_ROOM','aborted':'PP_ROOM','preempted':'PP_ROOM'})

            StateMachine.add('PP_ROOM', nav_states['pp_room'], transitions={'succeeded':'PP_ROOM_TASKS','aborted':'AT_ROOM','preempted':'AT_ROOM'})

            # When the tasks are done, continue on to the AT_ROOM 
            StateMachine.add('PP_ROOM_TASKS', sm_pp_room, transitions={'succeeded':'AT_ROOM','aborted':'AT_ROOM','preempted':'AT_ROOM'})

            StateMachine.add('AT_ROOM', nav_states['at_room'], transitions={'succeeded':'AT_ROOM_TASKS','aborted':'WDYS_ROOM','preempted':'WDYS_ROOM'})

            # When the tasks are done, continue on to the wdys_room
            StateMachine.add('AT_ROOM_TASKS', sm_at_room, transitions={'succeeded':'WDYS_ROOM','aborted':'WDYS_ROOM','preempted':'WDYS_ROOM'})

            StateMachine.add('WDYS_ROOM', nav_states['wdys_room'], transitions={'succeeded':'WDYS_ROOM_TASKS','aborted':'LEAVING_ARENA','preempted':'LEAVING_ARENA'})

            # When the tasks are done, leaving to the arean
            StateMachine.add('WDYS_ROOM_TASKS', sm_wdys_room, transitions={'succeeded':'LEAVING_ARENA','aborted':'LEAVING_ARENA','preempted':'LEAVING_ARENA'})

            StateMachine.add('LEAVING_ARENA', nav_states['leaving_arena'], transitions={'succeeded':'LEAVING_ARENA_TASKS','aborted':'','preempted':''})

            # When the tasks are done, stop
            StateMachine.add('LEAVING_ARENA_TASKS', sm_leaving_arena, transitions={'succeeded':'','aborted':'','preempted':''})

       # Create and start the SMACH introspection server
        intro_server = IntrospectionServer('clean_house', sm_basic_f, '/SM_ROOT')
        intro_server.start()

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










    def move_base_result_cb(self, userdata, status, result):
        if status == actionlib.GoalStatus.SUCCEEDED:
            pass


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

