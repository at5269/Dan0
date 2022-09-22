import rospy

from moveit_commander import MoveGroupCommander

from std_srvs.srv import Empty

class MoveGroupCommander(MoveGroupCommander):

    def __init__(self, name, *args, **kwargs):
        super(MoveGroupCommander, self).__init__(name, *args, **kwargs)

        self.set_max_acceleration_scaling_factor(0.50)
        rospy.Service('interrupt_motion', Empty, self.interrupt_motion)

    def movej(self, target, speed, wait=True):
        """Move in joint space to the specified target with the trapezoidal speed profile.

        Args:
            target (list or JointState or Pose): The target of the motion. Can be in either joint space or Cartesian space.
            speed (float): The speed of the motion in percentage of the maximum speed (between 0.0 and 1.0).
            wait (bool, optional): _description_. Defines if the call this method should be blocking or not. Defaults to True.
        """
        self.set_planner_id('PTP')
        return self.go(target, wait, speed)

    def movel(self, target, speed, wait=True):
        """Move in Cartesian space to the specified target following a straight line.

        Args:
            target (Pose): The target in Cartesian space.
            speed (float): The speed of the motion in percentage of the maximum speed (between 0.0 and 1.0).
            wait (bool, optional): _description_. Defines if the call this method should be blocking or not. Defaults to True.
        """
        self.set_planner_id('LIN')
        return self.go(target, wait, speed)

    def movej_relative(self, offset, speed, frame='ee_link',  wait=True):
        """Move in Cartesian space to the offset relative to the provided frame.

        Args:
            offset (list): The offset in Cartesian space. Can be of size 3 or 6.
            speed (float): The speed of the motion in percentage of the maximum speed (between 0.0 and 1.0).
            frame (str, optional): The frame from which the offset is calculated. Defaults to 'ee_link'.
            wait (bool, optional): Defines if the call this method should be blocking or not. Defaults to True.
        """
        # TO-DO
        pass

    def movel_relative(self, offset, speed, frame='ee_link',  wait=True):
        """Move in Cartesian space to the offset relative to the provided frame.

        Args:
            offset (list): The offset in Cartesian space. Can be of size 3 or 6.
            speed (float): The speed of the motion in percentage of the maximum speed (between 0.0 and 1.0).
            frame (str, optional): The frame from which the offset is calculated. Defaults to 'ee_link'.
            wait (bool, optional): Defines if the call this method should be blocking or not. Defaults to True.
        """
        # TO-DO
        pass

    def go(self, joints=None, wait=True, speed=None):
        self.set_pose_reference_frame('base_link')
        self.set_max_velocity_scaling_factor(speed)
        super(MoveGroupCommander, self).go(joints, wait)

    def interrupt_motion(self, req):
        rospy.logwarn("Interrupting the motion!")
        self.stop()
        return []

