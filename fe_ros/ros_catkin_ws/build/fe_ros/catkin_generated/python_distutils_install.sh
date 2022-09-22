#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/student/fe_ros/ros_catkin_ws/src/fe_ros_workshop/fe_ros"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/student/fe_ros/ros_catkin_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/student/fe_ros/ros_catkin_ws/install/lib/python2.7/dist-packages:/home/student/fe_ros/ros_catkin_ws/build/fe_ros/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/student/fe_ros/ros_catkin_ws/build/fe_ros" \
    "/usr/bin/python2" \
    "/home/student/fe_ros/ros_catkin_ws/src/fe_ros_workshop/fe_ros/setup.py" \
     \
    build --build-base "/home/student/fe_ros/ros_catkin_ws/build/fe_ros" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/student/fe_ros/ros_catkin_ws/install" --install-scripts="/home/student/fe_ros/ros_catkin_ws/install/bin"
