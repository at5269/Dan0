# Installation instructions

## Install the dependencies

Before installing the dependencies, make sure you have `wstool` installed on your system: http://wiki.ros.org/wstool

If you have not yet initialized a wstool environment, do so. First navigate into your catkin workspace and invoke the following command:

```
$ wstool init src
```

Then merge the `.rosinstall` rules from `fe_ros_workshop`:
```
$ wstool merge -t src src/fe_ros_workshop/fe_ros_workshop/fe_ros.rosinstall
```

Finally, update the dependencies:
```
$ wstool update -t src
```
## Build this package

Buld the `fe_ros` package

```
$ catking build fe_ros
```
