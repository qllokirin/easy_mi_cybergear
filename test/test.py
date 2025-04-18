from easy_mi_cybergear import Cybergear
import time
motor = Cybergear(port = "COM10")

print("电机初始化完成")
for i in range(1,7,1):
    motor.set_motor_zero_position(motor_can_id=i)
    pos = 1.57 if i <= 3 else -1.57
    motor.set_motor_move_by_position(position=pos, speed_limt=1,motor_can_id=i)

a = input("按回车键蹲下")

for i in range(1,7,1):
    pos = 3.14*2 if i <= 3 else -3.14*2
    motor.set_motor_move_by_position(position=pos, speed_limt=1,motor_can_id=i)

a = input("按回车键停止电机")

for i in range(1,7,1):
    motor.set_motor_stop(motor_can_id=i)