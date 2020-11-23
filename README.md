# araig_calculator

## Installation
```
$ cd <path/to/workspace/src> git clone -b master https://github.com/ipa-hsd/rosgraph_monitor/
$ cd <path/to/workspace/src> git clone -b SoSymPaper https://github.com/ipa-nhg/ros_graph_parser
$ cd <path/to/workspace/src> git clone -b master https://github.com/ipa-rwu/araig_calculator
$ cd <path/to/workspace>
$ source /opt/ros/melodic/setup.bash
$ rosdep install --from-paths src --ignore-src -r -y
$ catkin build 
$ source <path/to/workspace/devel/>setup.bash
```

## Running the system  
source the workspace in all the terminals

```
# Terminal 1
$ roscore

# Terminal 2
$ rosrun araig_calculator calculator


# In a new terminal 
$ rosservice call /load_observer "name: 'ComparatorRobotHasStopped'"
```
