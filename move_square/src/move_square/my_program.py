#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time

class shifty():
    
    def __init__(self):
        self.tb2_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)
        self.rate = rospy.Rate(5) # 10hz
    
    
    
    def publish_once_in_cmd_vel(self, cmd):
        
        while not self.ctrl_c:
            connections = self.tb2_vel_publisher.get_num_connections()
            if connections > 0:
                self.tb2_vel_publisher.publish(cmd)
                rospy.loginfo("Cmd Published")
                break
            else:
                self.rate.sleep()
    
    
    def shutdownhook(self):
            
            self.stop_tb2()
            self.ctrl_c = True

    def stop_tb2(self):
        rospy.loginfo("shutdown time! Stop the robot")
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.publish_once_in_cmd_vel(cmd)


    def move_x_time(self, moving_time, linear_speed, angular_speed):
        
        cmd = Twist()
        cmd.linear.x = linear_speed
        cmd.angular.z = angular_speed
        
        rospy.loginfo("Moving Forwards")
        self.publish_once_in_cmd_vel(cmd)
        time.sleep(moving_time)
        self.stop_tb2()
        rospy.loginfo("######## Finished Moving Forwards")
    
    def move_square(self):
        
        i = 0
        while not self.ctrl_c and i < 12:
            # Move Forwards
            self.move_x_time(moving_time=2, linear_speed=0.15, angular_speed=0.0)
            # Stop
            self.move_x_time(moving_time=1, linear_speed=0.0, angular_speed=0.0)
            # Turn 90 degree
            self.move_x_time(moving_time=2, linear_speed=0.0, angular_speed=1.5708/2)
            # Stop
            self.move_x_time(moving_time=2, linear_speed=0.0, angular_speed=0.0)
            
            i += 1
        rospy.loginfo("Finished Moving in a Square")
        

            
if __name__ == '__main__':
    rospy.init_node('move_tb2_test', anonymous=True)
    shifty_object = shifty()
    try:
        shifty_object.move_square()
    except rospy.ROSInterruptException:
        pass
