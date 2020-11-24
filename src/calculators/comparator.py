#!/usr/bin/env python

from rosgraph_monitor.observer import TopicObserver
import rospy
from calculator.msg import Result, Calculation_result
import calculator.msg 

# x-y 
# default msg_type will be Result in calculator.msg
class Comparator(TopicObserver):
    def __init__(self, comparator_name, input_topics, fix_param, output_topic_name, msg_type, loop_rate_hz):
        super(Comparator, self).__init__(
            name = comparator_name, 
            loop_rate_hz = 10, 
            topics = input_topics, 
            output_topic_name = output_topic_name, 
            msg_type = None)

        if fix_param == None:
            if len(input_topics) < 2:
                raise Exception("Don't have fix parameter. Need to provide more than one topic in the list") 
            self._flag_fix = 0
        else:
            self._flag_fix = 1
            self._fix_param = fix_param

        if output_topic_name == None:
            raise Exception("Please provide output topic name")

        if msg_type == None:
            msg_type = "Result"
            self._msg_type_class = getattr(calculator.msg, msg_type)
            self._pub_diag = rospy.Publisher(
                output_topic_name, self._msg_type_class, queue_size=10)
        else:
            # other message types are defined in calculator.msg
            self._msg_type_class = getattr(calculator.msg, msg_type)
            self._pub_diag = rospy.Publisher(
                output_topic_name, self._msg_type_class, queue_size=10)


        self._messages = comparator_name        
        self._rate = rospy.Rate(loop_rate_hz)


    #  publish result_msg in msg_type: "Result"
    def _run(self):
        while not rospy.is_shutdown() and not self._stopped():
            result_msg = self._msg_type_class()
            result_msg.header.stamp = rospy.get_rostime()

            calculation_result_msg = self.generate_diagnostics()
            result_msg.status.extend(calculation_result_msg)
            self._pub_diag.publish(result_msg)
        
            self._rate.sleep()
    
    def calculate_attr(self, msgs):
        # do calculations
        return Calculation_result()

    def generate_diagnostics(self):
        variables = []
        received_all = True
        print("topics:", self._topics)
        
        if self._flag_fix == 1:
            variables.append(self._fix_param)
        
        for topic, topic_type in self._topics:
            try:
                variables.append(rospy.wait_for_message(topic, topic_type))
            except rospy.ROSException as exc:
                print("Topic {} is not found: ".format(topic) + str(exc))
                received_all = False
                break

        calculation_msgs = Calculation_result()
        if received_all:
            calculation_msgs = self.calculate_attr(variables)

        return calculation_msgs

class ComparatorEqualToZero(Comparator):
    def __init__(self, comparator_name, input_topics, fix_param, output_topic_name, msg_type, loop_rate_hz):
        super(ComparatorEqualToZero, self).__init__(
            comparator_name, 
            input_topics,
            fix_param,
            output_topic_name,
            msg_type,
            loop_rate_hz
            )

    # mags = variables
    def calculate_attr(self, msgs):
        calculation = abs(msgs[0].data - self._zero_vel)
        print("abs({0}-{1})").format(msgs[0].data, self._zero_vel)

        cal_res = Calculation_result()
        cal_res.result_float = calculation

        if cal_res == 0:
            cal_res.result_bool = 1
        else:
            cal_res.result_bool = 0

        return cal_res

class ComparatorCloseToZero(Comparator):
    def __init__(self, comparator_name, input_topics, fix_param, output_topic_name, msg_type, loop_rate_hz):
        super(ComparatorCloseToZero, self).__init__(
            comparator_name, 
            input_topics,
            fix_param,
            output_topic_name,
            msg_type,
            loop_rate_hz
            )

    # mags = variables
    def calculate_attr(self, msgs):
        calculation = abs(msgs[0].data - self._zero_vel)
        print("abs({0}-{1})").format(msgs[0].data, self._zero_vel)

        cal_res = Calculation_result()
        cal_res.result_float = calculation

        if cal_res < 0.02:
            cal_res.result_bool = 1
        else:
            cal_res.result_bool = 0

        return cal_res

