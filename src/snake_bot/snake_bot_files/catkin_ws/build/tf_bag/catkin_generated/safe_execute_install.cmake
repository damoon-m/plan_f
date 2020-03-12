execute_process(COMMAND "/home/mohamadi/catkin_ws/build/tf_bag/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/mohamadi/catkin_ws/build/tf_bag/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
