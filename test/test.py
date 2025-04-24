import math
from easy_mi_cybergear import Cybergear
import logging
import time
import requests

def to_rad(degree):
    return degree * math.pi / 180

def add_motor_position(motor_can_id, position, speed_limt=1):
    motors_position[motor_can_id] += position
    motor.set_motor_move_by_position(position=motors_position[motor_can_id], speed_limt=speed_limt,motor_can_id=motor_can_id)
def set_motor_position(motor_can_id, position, speed_limt=1):
    motor.set_motor_move_by_position(position=position, speed_limt=speed_limt,motor_can_id=motor_can_id)
    motors_position[motor_can_id] = position
def go_nearst_position(motor_can_id, position):
    '''
    让电机去往最近的角度
    '''
    dr = position - motors_position[motor_can_id] % to_rad(360)
    if dr >= 0 and dr <= to_rad(180):
        add_motor_position(motor_can_id=motor_can_id, position=dr)
    elif dr >= to_rad(180):
        add_motor_position(motor_can_id=motor_can_id, position=dr - to_rad(360))
    elif dr <= 0 and dr >= -to_rad(180):
        add_motor_position(motor_can_id=motor_can_id, position=dr)
    elif dr <= -to_rad(180):
        add_motor_position(motor_can_id=motor_can_id, position=dr + to_rad(360))
    else:
        logging.info("电机已经在目标位置了")

def init():
    global motor
    while True:
        try:
            motor = Cybergear()
            if motor.get_motor_nums() != 6:
                raise Exception("电机数量不对")
            else:
                for i in range(1,7,1):
                    motor.set_motor_zero_position(motor_can_id=i)
                logging.info("初始化成功")
                return
        except Exception as e:
            logging.info("等待1s后重试")
            time.sleep(1)

def stand_up():
    '''
    所有电机都去往最近的±90度位置
    1 2 3是顺时针 4 5 6是逆时针
    '''
    for i in range(1,7,1):
        go_nearst_position(motor_can_id=i, position=to_rad(90) if i <= 3 else to_rad(-90))
    time.sleep(2)

def lie_down():
    '''
    趴下并停止
    '''
    # 复位
    # input("复位")
    # add_motor_position(motor_can_id=1, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
    # add_motor_position(motor_can_id=3, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
    # add_motor_position(motor_can_id=5, position=to_rad(+(alpha)), speed_limt=speed_move_quick)
    # add_motor_position(motor_can_id=2, position=to_rad(+(alpha)), speed_limt=speed_move_quick)
    # add_motor_position(motor_can_id=4, position=to_rad(-(alpha)), speed_limt=speed_move_quick)
    # add_motor_position(motor_can_id=6, position=to_rad(-(alpha)), speed_limt=speed_move_quick)

    # 在站立姿态后一起往前滚就是趴下
    stand_up()
    time.sleep(2)
    for i in range(1,7,1):
        pos = to_rad(270) if i <= 3 else to_rad(-270)
        add_motor_position(position=pos, speed_limt=2,motor_can_id=i)
    time.sleep(5)
    for i in range(1,7,1):
        motor.set_motor_stop(motor_can_id=i)

def init_go_and_back():
    stand_up()

    add_motor_position(motor_can_id=1, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=3, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=5, position=to_rad(+(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=2, position=to_rad(-(alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=4, position=to_rad(+(alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=6, position=to_rad(+(alpha)), speed_limt=speed_move_low)
    time.sleep(2)

def go_forward_one_step():
    '''
    向前走一步
    三角步态 定时步行 1 5 3一组 4 2 6一组
    向后蹬腿 也就是123是逆时针 456是顺时针 数值变大是顺时针
    1   4
    2   5
    3   6
    135先蹬腿，246支撑
    分离度数alpha为30时 支撑腿往后蹬30 摆动腿蹬360-30来到前方30的位置
    然后前方30往后30*2成为支撑腿 后方的腿往前摆动360-30*2来到前方30的位置
    '''
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

def go_backward_one_step():
    '''
    向后走一步
    '''
    add_motor_position(motor_can_id=1, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(+(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(-(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(-(2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)

    add_motor_position(motor_can_id=1, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)

def turn_left_one_step():
    '''
    TODO
    向左转一步
    '''
    add_motor_position(motor_can_id=1, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(-(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)
    
    add_motor_position(motor_can_id=1, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(-(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(-(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(-(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(-(2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)

def turn_right_one_step():
    '''
    TODO
    向右转一步
    '''
    add_motor_position(motor_can_id=1, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(+(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(+(2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(+(2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)
    
    add_motor_position(motor_can_id=1, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=3, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=5, position=to_rad(+(2*alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=2, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=4, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=6, position=to_rad(+(360-2*alpha)), speed_limt=speed_move_quick)
    time.sleep(2)

def init_turn_left_and_right():
    '''
    TODO
    初始化转弯
    '''
    stand_up()

    add_motor_position(motor_can_id=1, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=3, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=5, position=to_rad(-(360-alpha)), speed_limt=speed_move_quick)
    add_motor_position(motor_can_id=2, position=to_rad(-(alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=4, position=to_rad(-(alpha)), speed_limt=speed_move_low)
    add_motor_position(motor_can_id=6, position=to_rad(-(alpha)), speed_limt=speed_move_low)
    time.sleep(2)

def get_current_state():
    '''
    获取当前状态
    '''
    return requests.get('http://127.0.0.1:5000/current_state').json()["current_state"]

motors_position = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}
if __name__ == '__main__':
    current_state = 'lie_down'
    last_state = 'lie_down'
    motor = None
    init()

    alpha = 20
    speed_move_quick = 5
    speed_move_low = 2.5
    while True:
        current_state = get_current_state()
        print(f"current_state: {current_state} last_state: {last_state}")
        if current_state != last_state or current_state in list(['go', 'back', 'left', 'right']):
            if current_state == 'lie_down':
                lie_down()
            elif current_state == 'stand':
                stand_up()
            elif current_state == 'go':
                if last_state != 'go' and last_state != 'back':
                    init_go_and_back()
                go_forward_one_step()
            elif current_state == 'back':
                if last_state != 'go' and last_state != 'back':
                    init_go_and_back()
                go_backward_one_step()
            elif current_state == 'left':
                if last_state != 'left' and last_state != 'right':
                    init_turn_left_and_right()
                turn_left_one_step()
            elif current_state == 'right':
                if last_state != 'right' and last_state != 'left':
                    init_turn_left_and_right()
                turn_right_one_step()
            last_state = current_state
        else:
            time.sleep(1)
