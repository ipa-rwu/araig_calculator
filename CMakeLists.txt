cmake_minimum_required(VERSION 2.8.3)
project(araig_calculator)

find_package(catkin REQUIRED COMPONENTS
   roscpp
   rospy
   std_msgs
   message_generation
)

catkin_python_setup()

 add_message_files(
   FILES
   Calculation_result.msg
   Result.msg
 ) 
 
generate_messages(
   DEPENDENCIES
   std_msgs  # Or other packages containing msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES observer_camparator
  CATKIN_DEPENDS rospy message_runtime
#  DEPENDS system_lib
)



catkin_install_python(PROGRAMS
   scripts/calculator
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )


#install(DIRECTORY launch
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
#)

