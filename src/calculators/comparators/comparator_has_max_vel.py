#!/usr/bin/env python

from calculators.comparator import Comparator
from calculator.msg import Result
import rospy

class ComparatorHasMaxVel(Comparator):
    def __init__(self, 
    comparator_name = "comparator_robot_has_stopped",
    input_topics = [("/data/robot/odom/twist/x")],
    fix_param = "max_vel",
    output_topic_name = "event",
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
        if fix_param != None:
            self._max_vel = rospy.get_param(fix_param, {}) 

    def calculate_attr(self, msgs):
        status_msg = self._msg_type()

        if len(msgs) > 1:
            calculation = abs(msgs[0].data - msgs[1].data)
            print("abs({0}-{1})").format(msgs[0].data, msgs[1].data)
        if len(msgs) == 1:
            calculation = abs(msgs[0].data - self._fix_param)
            print("abs({0}-{1})").format(msgs[0].data, self._fix_param)

        # !!!Todo: need to change based on msg type. Now will use DiagnosticStatus
        status_msg.values.append(KeyValue("result", str(calculation)))
        status_msg.message = self._messages
    
        return status_msg