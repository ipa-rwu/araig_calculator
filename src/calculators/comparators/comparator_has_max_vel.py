#!/usr/bin/env python

from calculators.comparator import ComparatorCloseToZero
from calculator.msg import Result
from std_msgs.msg import Float64

import rospy

"fix param should read from testx_param.yaml"
class ComparatorHasMaxVel(ComparatorCloseToZero):
    def __init__(self, 
    comparator_name = "comparator_has_max_vel",
    input_topics = [("/data/robot/odom/twist/x", Float64)],
    fix_param = "max_vel",
    output_topic_name = "/event/obs/has_max_vel",
    msg_type = "Result",
    loop_rate_hz = 1,
    ):
        super(ComparatorHasMaxVel,self).__init__(
            comparator_name,
            input_topics,
            fix_param,
            output_topic_name,
            msg_type,
            loop_rate_hz,
            )