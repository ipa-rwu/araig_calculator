#!/usr/bin/env python

from calculators.comparator import ComparatorEqualToZero
from calculator.msg import Calculation_result
from std_msgs.msg import Float64
import rospy

class ComparatorRobotHasStopped(ComparatorEqualToZero):
    def __init__(self, 
    comparator_name = "comparator_robot_has_stopped",
    input_topics = [("/data/robot/odom/twist/x", Float64)],
    fix_param = 0,
    output_topic_name = "/event/obs/robot_has_stopped",
    msg_type = "Result",
    loop_rate_hz = 1,
    ):
        super(ComparatorRobotHasStopped,self).__init__(
            comparator_name,
            input_topics,
            fix_param,
            output_topic_name,
            msg_type,
            loop_rate_hz,
            )