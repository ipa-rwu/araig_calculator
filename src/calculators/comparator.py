#!/usr/bin/env python

from rosgraph_monitor.observer import TopicObserver
import rospy
from calculator.msg import Result, Calculation_result
import calculator.msg 

class Comparator(TopicObserver):
    def __init__(self, comparator_name, input_topics, fix_param, output_topic_name, msg_type, loop_rate_hz):
        super(Comparator, self).__init__(
            name = comparator_name, 
            loop_rate_hz = 10, 
            topics = input_topics, 
            output_topic_name = output_topic_name, 
            msg_type = None)

        print("Comparator")
        print("output_topic_name", output_topic_name)

        if fix_param == None:
            if len(input_topics) < 2:
                print("Need to provide more than one topic in lists") 
        else:
            self._fix_param = fix_param

        if output_topic_name == None:
            raise Exception("Please provode output topic name")

        if msg_type == None:
            msg_type = "Result"
            self._msg_type_class = getattr(calculator.msg, msg_type)
            self._pub_diag = rospy.Publisher(
                output_topic_name, self._msg_type_class, queue_size=10)
        else:
            self._msg_type_class = getattr(calculator.msg, msg_type)
            self._pub_diag = rospy.Publisher(
                output_topic_name, self._msg_type_class, queue_size=10)


        self._messages = comparator_name        
        self._rate = rospy.Rate(loop_rate_hz)


    def _run(self):

        while not rospy.is_shutdown() and not self._stopped():
            result_msg = self._msg_type_class()
            result_msg.header.stamp = rospy.get_rostime()

            status_msgs = self.generate_diagnostics()
            result_msg.status.extend(status_msgs)
            self._pub_diag.publish(result_msg)
        
            self._rate.sleep()

    def start(self):
        print("from comparator.py")
        
        print("starting {}...".format(self._name))
        self._thread.start()

    def calculate_attr(self, msgs):
        # do calculations
        return Calculation_result()

    def generate_diagnostics(self):
        msgs = []
        received_all = True
        print("topics:", self._topics)
        for topic, topic_type in self._topics:
            try:
                msgs.append(rospy.wait_for_message(topic, topic_type))
            except rospy.ROSException as exc:
                print("Topic {} is not found: ".format(topic) + str(exc))
                received_all = False
                break

        calculation_msgs = Calculation_result()
        if received_all:
            calculation_msgs = self.calculate_attr(msgs)

        return calculation_msgs