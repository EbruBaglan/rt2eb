#!/usr/bin/env python


"""
.. module:: mod3_controller
   :platform: Unix
   :synopsis: Python module for the controller of modality 3: assisted drive
   
.. moduleauthor:: Ebru Baglan baglanebru@gmail.com

The node receives the user commands from mod3_teleop_twist_keyboard node by subscribing to the /cmd_vel_raw topic. Upon comparing this command with the obstacle distance received from /scan topic, if there is an obstacle in the desired direction, that velocity is set to zero to avoid collision. So the suicidal tendencies of the user is prevented and an expensive robot is saved, WIN-WIN! Then the modified velocity is sent to /cmd_vel.

Subscribes to:
	/cmd_vel_raw
	/scan
	
Publishes to:
	/cmd_vel
"""
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

vel_ = Twist()
"""
Global Twist variable for robot velocity
"""
vel_.linear.x = 0.0
vel_.angular.z = 0.0 

pub = rospy.Publisher("/cmd_vel", Twist)
"""
Global publisher
"""

def take_action(regions):
    """
    The function decides to whether keep the user velocity to the /cmd_vel or not. 5 region of the /scan readings are checked and if user wants to drive in the direction of a close obstacle, the velocity in that direction is set to zero. It is then sent to /cmd_vel.
    
    Args:
    	regions(dictionary): The parsed /scan readings to 5 regions. Every key has minimum of each region's closest obstacle distance as value.
    """
    msg = Twist()
    linear_x = vel_.linear.x
    angular_z = vel_.angular.z

    state_description = ''

    if regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        if linear_x > 0:
            linear_x = 0
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        if angular_z < 0:
            angular_z = 0
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        if angular_z > 0:
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        if linear_x > 0 or angular_z < 0:
            linear_x = 0
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        if linear_x > 0 or angular_z > 0:
            linear_x = 0
            angular_z = 0
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        if linear_x > 0:
            linear_x = 0
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        if angular_z != 0:
            angular_z = 0
    else:
        state_description = 'unknown case'

    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def clbck_laser(msg):
    """
    The callback function for /scan readings. Parsed into 5 direction and assigned the minimum value of respective region. Then sent to take_action() function for further steps.
    
    Args:
    	msg(list): /scan readings
    """
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }
    take_action(regions)
    
def clbck2(msg):
    """
    The callback function for /cmd_vel_raw. Assigns the user command to global variable vel
    
    Args:
    	msg(Twist): User command for velocity.
    
    """
    global vel_
    vel_ = msg

def controller():
    """
    The main function to initiate node, subscrive to the topics and spin.
    """
    rospy.init_node("mod3_controller")

    rospy.Subscriber('/scan', LaserScan, clbck_laser)
    rospy.Subscriber('/cmd_vel_raw', Twist, clbck2)   
    rospy.spin()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass
