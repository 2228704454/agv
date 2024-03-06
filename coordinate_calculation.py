import numpy as np


# TODO 计算坐标的分量差异与四元素旋转差异

# 提取坐标的三维数据
JSR_position = np.array([2.208, -1.178, 0.00])
AGV_position = np.array([2.994, -0.882, 0.000])

# 计算三维坐标分量差异
position_difference = JSR_position - AGV_position

# 提取四元数
JSR_quaternion = np.array([0.000, 0.000, -0.744, 0.668])
AGV_quaternion = np.array([0.000, 0.000, 1.000, -0.005])

# 四元数乘法函数
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

# 计算四元素旋转差异
rotation_difference = quaternion_multiply(JSR_quaternion, np.conjugate(AGV_quaternion))

# 打印三维坐标分量差异与四元素旋转差异
print("位置分量差异：", position_difference)
print("旋转差异（四元数表示）：", rotation_difference)


# TODO 通过固定的分量差异和旋转差异计算相对位置

# 提取位置分量差异和旋转差异
position_difference = np.array([-0.786, -0.296,  0.0])
rotation_difference = np.array([0.74734, -0.66428,  0.0,       0.0    ])

# 假设给定的坐标数据是JSR_position
JSR_position = np.array([2.208, -1.178, 0.00])
JSR_quaternion = np.array([0.000, 0.000, -0.744, 0.668])

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
new_quaternion = np.round(new_quaternion, 3)


# 打印结果
print("给定的JSR位置分量：", JSR_position)
print("给定的JSR四元数：", JSR_quaternion)
print("新AGV位置分量：", new_position)
print("新的AGV四元数：", new_quaternion)
