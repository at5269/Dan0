#!/usr/bin/env python2

import traceback
import rospy

from im_pickit_msgs.msg import ObjectArray
from moveit_commander import MoveGroupCommander
from std_msgs.msg import Bool, String

UP = [0, -1.57, 0, 0, 0, 0]
BETWEEN = [0, -1.57/2, 0, 0, 0, 0]
HOME = [0, 0, 0, 0, 0, 0]

STOP_RANGE = 0.65
RESUME_RANGE = 0.8

NODE_RATE = 50

TRIGGER_DETECTION = 'e_look_for_object'


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

        # Clear all the targets from the move group (not sure if this is necessary)
        self.move_group.clear_pose_targets()

    def move_cartesian(self, goal):
        self.move_group.set_pose_target(goal)
        self.move_group.go(wait=True)

    def move_joint(self, goal):
        self.move_group.set_joint_value_target(goal)
        self.move_group.go(wait=True)


class PickitPick(object):
    is_detecting = None

    def __init__(self):

        self.initialize_topics()
        self.rate = rospy.Rate(10)

    def initialize_topics(self):
        rospy.Subscriber('/pickit/is_detecting', Bool, self._is_detecting_cb, queue_size=1)
        rospy.Subscriber('/pickit/objects_wrt_robot_frame', ObjectArray, self._detection_result, queue_size=1)

        self.pickit_command = rospy.Publisher('/pickit/external_cmds', String, queue_size=1)

        rospy.sleep(0.3)

    def wait_detection_done(self):
        rospy.loginfo("Detecting objects ...")
        while not self.is_detecting:
            self.rate.sleep()

        while self.is_detecting:
            self.rate.sleep()
        rospy.loginfo("Detection finished with {} valid objects!".format(self.detection_result.n_valid_objects))

    def trigger_detection(self):
        self.pickit_command.publish(TRIGGER_DETECTION)

    def _is_detecting_cb(self, msg):
        self.is_detecting = msg.data

    def _detection_result(self, msg):
        self.detection_result = msg
        self.pickable_objects = self.detection_result.objects

    def confirm_valid(self):
        if not self.detection_result.n_valid_objects:
            raise Exception("No objects found!")

    def return_pick_poses(self):
        return self.pickable_objects[0].pick_frames[0]


def pose_to_array(pose):
    return [
        pose.position.x,
        pose.position.y,
        pose.position.z,
        pose.orientation.x,
        pose.orientation.y,
        pose.orientation.z,
        pose.orientation.w]


if __name__ == '__main__':
    rospy.init_node('pilz_interrupt_motion')
    try:
        PilzInterruptExample()
        robot = PilzInterruptExample()
        pickit = PickitPick()

        pickit.trigger_detection()
        pickit.wait_detection_done()
        # pickit.confirm_valid()
        pick_poses = pickit.return_pick_poses()

        robot.move_cartesian(pose_to_array(pick_poses.shape_pre_pick_pose))
        robot.move_cartesian(pose_to_array(pick_poses.robot_pick_pose))
        robot.move_cartesian(pose_to_array(pick_poses.shape_post_pick_pose))

    except Exception as e:
        rospy.logerr(
            "Exception occurred in the initialization of the node. Exception:\n{}".format(e))
        rospy.logerr("Traceback:\n{}".format(traceback.format_exc()))
    else:
        rospy.loginfo("Node '{}' has started.".format(rospy.get_name()))
    finally:
        rospy.loginfo("Exiting ...")
