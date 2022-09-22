#!/usr/bin/env python2

import rosbag
import rospy
import rospkg

from im_pickit_msgs.msg import ObjectArray
from std_msgs.msg import String, Bool

DETECTED_OBJECTS_TOPIC = '/pickit/objects_wrt_robot_frame'
IS_DETECTING_TOPIC = '/pickit/is_detecting'

TRIGGER_DETECTION = 'e_look_for_object'

DETECTION_TIME = 5


class PickitDummy(object):

    def __init__(self):
        self.init_data()
        self.init_topics()

    def init_topics(self):
        self.objects_pub = rospy.Publisher(DETECTED_OBJECTS_TOPIC, ObjectArray, queue_size=1)
        self.is_detecting_pub = rospy.Publisher(IS_DETECTING_TOPIC, Bool, queue_size=1, latch=True)
        self.is_detecting_pub.publish(False)
        rospy.Subscriber('/pickit/external_cmds', String, self.external_cmds_callback)

    def init_data(self):
        rospack = rospkg.RosPack()
        bag_path = rospack.get_path('fe_ur') + '/data/pickit.bag'
        self.object_data = []
        with rosbag.Bag(bag_path) as bag:
            for topic, msg, t in bag.read_messages(topics=[DETECTED_OBJECTS_TOPIC]):
                self.object_data.append(msg)

            is_detecting_data = []
            for topic, msg, t in bag.read_messages(topics=[IS_DETECTING_TOPIC]):
                is_detecting_data.append(msg)


    def external_cmds_callback(self, msg):
        if msg.data == TRIGGER_DETECTION:
            self.is_detecting_pub.publish(True)
            rospy.sleep(DETECTION_TIME)
            self.is_detecting_pub.publish(False)
            self.objects_pub.publish(ObjectArray(objects=self.object_data[0].objects))

if __name__ == '__main__':
    rospy.init_node('pickit_dummy')
    try:
        PickitDummy()
    except Exception as e:
        rospy.logerr("Exception occurred when initializing the node. Exception:\n{}".format(e))
    else:
        rospy.loginfo("Node '{}' has started.".format(rospy.get_name()))
        rospy.spin()
    finally:
        rospy.loginfo("Exiting ...")
