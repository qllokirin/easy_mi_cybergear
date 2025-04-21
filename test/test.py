import math
from easy_mi_cybergear import Cybergear
import logging
import time

def to_rad(degree):
    return degree * math.pi / 180

motors_position = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}
motor = Cybergear()

def add_motor_position(motor_can_id, position, speed_limt=1):
    motors_position[motor_can_id] += position
    motor.set_motor_move_by_position(position=motors_position[motor_can_id], speed_limt=speed_limt,motor_can_id=motor_can_id)
def set_motor_position(motor_can_id, position, speed_limt=1):
    motor.set_motor_move_by_position(position=position, speed_limt=speed_limt,motor_can_id=motor_can_id)
    motors_position[motor_can_id] = position

# 都转到±90度就是站立
for i in range(1,7,1):
    motor.set_motor_zero_position(motor_can_id=i)
    pos = to_rad(90) if i <= 3 else to_rad(-90)
    set_motor_position(position=pos, speed_limt=3,motor_can_id=i)

# 定时步行 1 5 3一组 4 2 6一组
# 向后蹬腿 也就是123是逆时针 456是顺时针 数值变大是顺时针
# 1   4
# 2   5
# 3   6
# 135先蹬腿，246支撑
# 分离度数为30时 支撑腿往后蹬30 摆动腿蹬360-30来到前方30的位置
# 然后前方30往后30*2成为支撑腿 后方的腿往前摆动360-30*2来到前方30的位置
alpha = 20
speed_move_quick = 5
speed_move_low = 2.5
input("按回车键开始走")
add_motor_position(motor_can_id=1, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=3, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=5, position=to_rad(+(360-alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=2, position=to_rad(-(alpha)), speed_limt=speed_move_low)
add_motor_position(motor_can_id=4, position=to_rad(+(alpha)), speed_limt=speed_move_low)
add_motor_position(motor_can_id=6, position=to_rad(+(alpha)), speed_limt=speed_move_low)

# for i in range(1):
while True:
    if_over = input("是否结束")
    if if_over != "":
        break
    add_motor_position(motor_can_id=1, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)

    add_motor_position(motor_can_id=1, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=3, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=5, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=2, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=4, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=6, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    time.sleep(2)

# 复位
input("复位")
add_motor_position(motor_can_id=1, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=3, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=5, position=to_rad(+(alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=2, position=to_rad(+(alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=4, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
add_motor_position(motor_can_id=6, position=to_rad(-(alpha)), speed_limt=speed_move_quick)

# 在站立姿态后一起往前滚就是趴下
input("按回车键趴下")
for i in range(1,7,1):
    pos = to_rad(270) if i <= 3 else to_rad(-270)
    add_motor_position(position=pos, speed_limt=2,motor_can_id=i)

input("按回车键停止电机")
for i in range(1,7,1):
    motor.set_motor_stop(motor_can_id=i)