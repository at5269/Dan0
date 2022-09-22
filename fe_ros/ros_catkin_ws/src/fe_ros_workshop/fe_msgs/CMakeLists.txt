cmake_minimum_required(VERSION 2.8.3)
project(fe_msgs)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_srvs
  std_msgs
  geometry_msgs
  sensor_msgs
)

# Uncomment this once you added files to the 'msg' folder
# Generate messages in the 'msg' folder
# add_message_files(
  # FILES
  # LIST MESSAGES IN THE 'msg' DIR
  # led_light.msg
# )

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
# )

# Uncomment this once you added files to the 'srv' folder
# Generate services in the 'srv' folder
# add_service_files(
  # FILES
  # LIST MESSAGES IN THE 'srv' DIR
  # digital_output.srv
# )

# Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_srvs
  std_msgs
  geometry_msgs
  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS
  message_runtime
  std_srvs
  std_msgs
  geometry_msgs
  sensor_msgs
  )

