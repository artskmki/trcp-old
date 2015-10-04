#!/usr/bin/python
# -*- coding: utf-8 -*-

import hsrb_interface
import rospy
import sys
from hsrb_interface import geometry

# 移動のタイムアウト[s]
_MOVE_TIMEOUT=60.0

# ロボット機能を使うための準備
robot = hsrb_interface.Robot()
omni_base = robot.get('omni_base')
whole_body = robot.get('whole_body')
gripper = robot.get('gripper')
tts = robot.get('default', robot.Items.TEXT_TO_SPEECH)

# handを0.1[m]上に移動させる姿勢
hand_up = geometry.pose(x=0.1)

# handを0.5[m]手前に移動させる姿勢
hand_back = geometry.pose(z=-0.5)

if __name__=='__main__':

    # まずは一言
    rospy.sleep(5.0)
    tts.say('こんにちはHSRだよ。これから部屋の中を移動するよ。')
    rospy.sleep(5.0)

    tts.say('はじめに50センチ前に進むよ。')	
    rospy.sleep(3.0)
    try:
    # 相対移動で，前に50cm移動（制限時間は30秒）
	_MOVE_TIMEOUT=30.0		
	omni_base.go(0.5, 0.0, 0.0, _MOVE_TIMEOUT, relative=True)
    except:
        tts.say('移動に失敗')
        rospy.logerr('fail to move')
        sys.exit()
		
    tts.say('次に50センチ後ろにに戻るよ。')			
    rospy.sleep(3.0)
    try:
    # 相対移動で，後ろに50cm移動（制限時間は30秒）
	_MOVE_TIMEOUT=30.0		
 	omni_base.go(-0.5, 0.0, 0.0, _MOVE_TIMEOUT, relative=True)
    except:
        tts.say('移動に失敗')
        rospy.logerr('fail to move')
        sys.exit()	
		
    tts.say('最後に回転するよ。')					
    rospy.sleep(3.0)
    try:
        # 相対移動で，回転（制限時間は60秒）
	_MOVE_TIMEOUT=30.0		
	omni_base.go(0.0, 0.0, 1.0, _MOVE_TIMEOUT, relative=True)
    except:
        tts.say('回転に失敗')
        rospy.logerr('fail to move')
        sys.exit()	
