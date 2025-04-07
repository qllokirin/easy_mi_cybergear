from easy_mi_cybergear import Cybergear
import time
motor = Cybergear()

# 设置电机机械零位（通信类型 6）会把当前电机位置设为机械零位（掉电丢失）
motor.set_motor_zero_position(motor_can_id=127)

# 位置模式，使电机转到2rad的位置，速度限制为1rad/s
motor.set_motor_move_by_position(position=2, speed_limt=1,motor_can_id=127)

time.sleep(1)
motor.set_motor_move_by_position(3)
time.sleep(1)
motor.set_motor_move_by_position(6)
time.sleep(1)
motor.set_motor_move_by_position(9)

# 电机停止运行 （通信类型 4）
motor.set_motor_stop(motor_can_id=127)