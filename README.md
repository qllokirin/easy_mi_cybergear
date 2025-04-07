# easy_mi_cybergear

**使用python通过USB-CAN模块轻松控制小米cybergear微电机**

```
pip install easy_mi_cybergear
```

```
from easy_mi_cybergear import Cybergear
import time
motor = Cybergear(baud_rate=921600, port="COM10")

# 电机使能运行 （通信类型 3） 电机会嗡嗡的响
motor.set_motor_enable(motor_can_id=127)

# 电机停止运行 （通信类型 4）
motor.set_motor_stop(motor_can_id=127)

# 设置电机机械零位（通信类型 6）会把当前电机位置设为机械零位（掉电丢失）
motor.set_motor_zero_position(motor_can_id=127)

# 位置模式，使电机转到2rad的位置，速度限制为1rad/s
motor.set_motor_move_by_position(position=2, speed_limt=10,motor_can_id=127)

time.sleep(1)

# 速度模式，设置电机速度为1rad/s，电流限制为23A(默认值)
motor.set_motor_move_by_speed(speed=1, motor_can_id=127)

time.sleep(2)

# 电机停止运行 （通信类型 4）
motor.set_motor_stop(motor_can_id=127)
```

TODO

- [ ] 错误判断
- [ ] 读取当前数据