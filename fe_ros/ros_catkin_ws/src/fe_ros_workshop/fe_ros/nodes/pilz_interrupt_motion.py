#!/usr/bin/env python2

import traceback
import rospy

from moveit_commander import MoveGroupCommander

from sensor_msgs.msg import LaserScan

UP = [0, -1.57, 0, 0, 0, 0]
BETWEEN = [0, -1.57/2, 0, 0, 0, 0]
HOME = [0, 0, 0, 0, 0, 0]

STOP_RANGE = 0.65
RESUME_RANGE = 0.8

NODE_RATE = 50


class PilzInterruptExample(object):

    def __init__(self):

        # Safety attribute
        self.safety_stop = True

        # Rate class to use in the `wait_safety` method
        self.rate = rospy.Rate(NODE_RATE)

        # Create the list of goals
        goals = [HOME, BETWEEN, UP]

        # Setup MoveIt commander
        self.move_group = MoveGroupCommander('manipulator')
        self.move_group.set_planner_id('PTP')
        self.move_group.set_max_acceleration_scaling_factor(0.50)
        self.move_group.set_pose_reference_frame('base_link')
        self.move_group.set_max_velocity_scaling_factor(0.50)

        # Create a subscriber
        rospy.Subscriber("/scanner1/sick_safetyscanners/scan", LaserScan, self.laser_callback)

        # Register a shutdown hook
        rospy.on_shutdown(self.print_stop_info)

        # Clear all the targets from the move group (not sure if this is necessary)
        self.move_group.clear_pose_targets()

        # Wait that it's safe to start
        self.wait_safety()

        # The main loop
        while not rospy.is_shutdown():
            for goal in goals:
                self.move_robot(goal)

        # Clear the Move Group before exiting
        self.move_group.stop()
        self.move_group.clear_pose_targets()

    def print_stop_info(self):
        """Prints some information the moment a shutdown is requested."""
        rospy.logwarn("Ctrl+C pressed. The program will stop when robot goes through all goals!")

    def wait_safety(self):
        """A function that waits until it's safe to move."""
        while self.safety_stop:
            self.rate.sleep()
            rospy.logwarn_throttle(1, "Waiting for obstacle to be removed!")

    def move_robot(self, goal):
        """Recursive function that allows stopping and resuming the robot motion"""
        self.move_group.go(goal, wait=True)
        if self.safety_stop:
            self.wait_safety()
            self.move_robot(goal)
        return

    def timer_event(self, event):
        """Timer event function. Toggles the current value of self.safety_stop"""
        rospy.loginfo("Toggle safety stop! From {} to {}".format(
            self.safety_stop, not self.safety_stop))
        self.safety_stop = not self.safety_stop
        if self.safety_stop:
            self.move_group.stop()
            self.move_group.clear_pose_targets()

    def laser_callback(self, msg):
        """Laser scanner callback function. Stop robot if obstacle is detected"""
        min_range = min(msg.ranges)
        if min_range < STOP_RANGE:
            rospy.logwarn_throttle(0.5, "Safety stop [r = {}]!".format(min_range))
            if not self.safety_stop:
                self.move_group.stop()
                self.move_group.clear_pose_targets()
            self.safety_stop = True
            return
        elif self.safety_stop and min_range < RESUME_RANGE:
            rospy.logwarn_throttle(0.5, "Stopped but not out of range [r = {}]!".format(min_range))
            return
        else:
            self.safety_stop = False
            rospy.loginfo_throttle(0.5, "Safe to move [r = {}]!".format(min_range))


if __name__ == '__main__':
    rospy.init_node('pilz_interrupt_motion')
    try:
        PilzInterruptExample()
        rospy.spin()
    except Exception as e:
        rospy.logerr(
            "Exception occurred in the initialization of the node. Exception:\n{}".format(e))
        rospy.logerr("Traceback:\n{}".format(traceback.format_exc()))
    else:
        rospy.loginfo("Node '{}' has started.".format(rospy.get_name()))
    finally:
        rospy.loginfo("Exiting ...")
