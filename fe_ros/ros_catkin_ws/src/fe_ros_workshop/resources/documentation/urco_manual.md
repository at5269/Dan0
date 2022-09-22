# How to run UR and MoveIT

## Quick info
### Intel NUC
The PC on-board the UR platform is an Intel NUC. It's IP is `192.168.88.11`. To log in, use the username `fe` with the password `fe-ros`.

When the system powers on, it should turn on all the necesarry ROS software.

<!-- Check if `systemctl fe-ros-launch` was enabled! -->

## Load a program on the robot
Load a program called `fe-ros.urp`

The program contains only one "line" - `Control by 192.168.88.11`. That's correct! Now we press play and put the teach-pendant away.

## XPS Dell

u: dell
p: airnamicsdell

## Using the UR platform

### Turning on
Turn the switch on the electrical panel to turn the system on

Press the blinking `EMERGENCY STOP RESET` button on the table.

### Connecting to the robot
Connect to the platform using a standard UTP cable and plug it into the Ethernet port on the electric enclusire at the side of the robot arm.

### Setting the environment variables on the computer and `/etc/hosts`
Add the following line to the `/etc/hosts` file:
```192.168.88.11 NUC-11```

Then, run
```
$ ifconfig
```
to discover which IP was assigned to the compute.

Then, set the following environment variables:
```
$ export ROS_MASTER_URI=http://NUC-11:11311
$ export ROS_HOSTNAME=192.168.88.<CHECK IFCONFIG>
```

## Opening and closing the gripper

On start-up, the ROS driver to control the pneumatic gripper starts. To open or close the gripper call the following (`std_srv/SetBool`) service:

```
$ rosservice call /gripper_set_grasp "data: 'true'"
```

### Controling the robot
To control the robot, send a trajectory to the `/scaled_pos_joint_traj_controller/follow_joint_trajectory` action server.



