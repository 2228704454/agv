import subprocess
import rospy
from geometry_msgs.msg import PoseStamped
import numpy as np

# 话题接收
def data_reception(msg):
    rospy.loginfo("Received current goal:\n%s", msg)
    data_processing(msg)

# 数据处理
def data_processing(msg):
    position = msg.pose.position
    orientation = msg.pose.orientation

    # TODO JSR坐标

    # 三维坐标
    JSR_x = position.x
    JSR_y = position.y
    JSR_z = position.z

    # 四元素
    JSR_qx = orientation.x
    JSR_qy = orientation.y
    JSR_qz = orientation.z
    JSR_qw = orientation.w

    #  TODO 计算AGV坐标

    # 代入JSR坐标数据
    JSR_position = np.array([JSR_x, JSR_y, JSR_z])
    JSR_quaternion = np.array([JSR_qx, JSR_qy, JSR_qz, JSR_qw])


    # 提取位置分量差异和旋转差异
    position_difference = np.array([-0.786, -0.296,  0.0])
    rotation_difference = np.array([0.74734, -0.66428,  0.0,       0.0    ])

    # 计算AGV坐标数据
    new_position = JSR_position - position_difference

    # 计算AGV四元数
    def quaternion_multiply(q1, q2):
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        result = np.array([
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        ])
        return result

    new_quaternion = quaternion_multiply(JSR_quaternion, rotation_difference)

    # 截取到小数点第三位
    
    new_quaternion = np.round(new_quaternion, 3)

    # 打印结果
    print("给定的JSR位置分量：", JSR_position)
    print("给定的JSR四元数：", JSR_quaternion)
    print("新AGV位置分量：", new_position)
    print("新的AGV四元数：", new_quaternion)
    
 # 执行指令
    agv_x, agv_y, agv_z = new_position
    agv_qx, agv_qy, agv_qz, agv_qw = new_quaternion

    command = "ssh agv \"source /opt/ros/noetic/setup.bash && rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped 'header:\n  seq: 1\n  stamp:\n    secs: 1709043936\n    nsecs: 444000000\n  frame_id: ''map''\npose:\n  position:\n    x: %.3f\n    y: %.3f\n    z: %.3f\n  orientation:\n    x: %.3f\n    y: %.3f\n    z: %.3f\n    w: %.3f'\"" % (agv_x, agv_y, agv_z, agv_qx, agv_qy, agv_qz, agv_qw)
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    rospy.init_node('goal_receiver')
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rospy.Subscriber("/move_base/current_goal", PoseStamped, data_reception)
        rate.sleep()


