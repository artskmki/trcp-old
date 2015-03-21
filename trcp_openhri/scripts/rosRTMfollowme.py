#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file rosRTMfollowme.py
 @brief rosRTM
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Import ROS module
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
rosrtmfollowme_spec = ["implementation_id", "rosRTMfollowme", 
		 "type_name",         "rosRTMfollowme", 
		 "description",       "rosRTM", 
		 "version",           "1.0.0", 
		 "vendor",            "Tamagawa Univ.", 
		 "category",          "ros", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.conf_int", "0",
		 "conf.default.conf_string", "hello",
		 "conf.__widget__.conf_int", "text",
		 "conf.__widget__.conf_string", "text",
		 ""]
# </rtc-template>

##
# @class rosRTMfollowme
# @brief rosRTM
# 
# 
class rosRTMfollowme(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_input_long = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._input_longIn = OpenRTM_aist.InPort("input_long", self._d_input_long)
		self._d_input_str = RTC.TimedString(RTC.Time(0,0),0)
		"""
		"""
		self._input_strIn = OpenRTM_aist.InPort("input_str", self._d_input_str)
		self._d_output_long = RTC.TimedLong(RTC.Time(0,0),0)
		"""
		"""
		self._output_longOut = OpenRTM_aist.OutPort("output_long", self._d_output_long)
		self._d_output_str = RTC.TimedString(RTC.Time(0,0),0)
		"""
		"""
		self._output_strOut = OpenRTM_aist.OutPort("output_str", self._d_output_str)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  conf_int
		 - DefaultValue: 0
		"""
		self._conf_int = [0]
		"""
		
		 - Name:  conf_string
		 - DefaultValue: hello
		"""
		self._conf_string = ['hello']
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("conf_int", self._conf_int, "0")
		self.bindParameter("conf_string", self._conf_string, "hello")
		
		# Set InPort buffers
		self.addInPort("input_long",self._input_longIn)
		self.addInPort("input_str",self._input_strIn)
		
		# Set OutPort buffers
		self.addOutPort("output_long",self._output_longOut)
		self.addOutPort("output_str",self._output_strOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		# Initialize ROS node
		global flg
		flg=0
		global pub
		rospy.init_node('talker', anonymous=True)
		pub = rospy.Publisher('hsr_c', Int32)	
		rospy.loginfo('start ROS node')
		rospy.Subscriber('hsr_s',Int32, callback)
		rospy.Subscriber('str_in',String, self.str_cb)
		return RTC.RTC_OK
	

	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		global flg
		if flg != 0:
			print("FFFFF")
			cmd = RTC.TimedLong(RTC.Time(0,0),flg)
                     #   self._output_long.data = cmd
                        self._output_longOut.write(cmd)
			flg = 0

	        if self._input_longIn.isNew():
	       		self._input_long = self._input_longIn.read()
			print("AAA  ")
			print(self._input_long.data)
			global pub
			pub.publish(Int32(self._input_long.data))

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	

        def str_cb(self, data):
            rospy.loginfo(rospy.get_name()+"Say: %s" % data.data)
            str_cmd = RTC.TimedString(RTC.Time(0,0),data.data)
            self._output_strOut.write(str_cmd)

def callback(data):
    rospy.loginfo(rospy.get_name()+"Int: %s" % data.data)
    global flg
    flg = data.data

def rosRTMfollowmeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=rosrtmfollowme_spec)
    manager.registerFactory(profile,
                            rosRTMfollowme,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    rosRTMfollowmeInit(manager)

    # Create a component
    comp = manager.createComponent("rosRTMfollowme")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

