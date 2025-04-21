import time
import serial
import serial.tools.list_ports
import logging
from serial.serialutil import SerialException
from .utils import send_command, MotionType, trans_to_4bit_float
from .can_id_and_communication_type import analyze_can_id_and_communication_type, generate_can_id_and_communication_type, analyze_raw_data_0

class Cybergear():
    def __init__(self, baud_rate=921600, port="auto", timeout=1):
        if port == "auto":
            ports = list(serial.tools.list_ports.grep('CH340'))
            if ports:
                port = ports[0].device
            else:
                logging.error("没有找到youcee USB-CAN设备")
                raise
        self.current_motion_type = {}
        self.baud_rate = baud_rate
        self.port = port
        self.timeout = timeout
        self.open_serial()
        self.connect_test()

    def open_serial(self):
        '''
        打开串口
        '''
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            logging.info(f"打开串口{self.port}成功")
            # 进入at模式
            send_command(self.ser, '41 54 2b 41 54 0d 0a')
            time.sleep(0.1)
            if self.ser.in_waiting:
                raw_data = self.ser.read(self.ser.in_waiting)
                if raw_data == b'OK\r\n':
                    logging.info("设置AT模式成功")
                else:
                    logging.error(f"AT模式指令返回错误: {raw_data}")
                    raise
            else:
                logging.error("AT模式指令无响应")
                raise
        except SerialException as e:
            logging.error(f"串口{self.port}打开失败 {e}")
            raise
        except Exception as e:
            logging.error(f"串口打开失败 {e}")
            raise

    def close_serial(self):
        '''
        关闭串口
        '''
        try:
            self.ser.close()
            logging.error(f"关闭串口{self.port}成功")
        except Exception as e:
            logging.error(f"关闭串口失败 {e}")
            raise

    # 获取设备 ID （通信类型 0）
    def connect_test(self):
        for i in range(0, 128):
            send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(0,i)} 01 00 0d 0a')
        time.sleep(1)
        if self.ser.in_waiting:
            raw_data = self.ser.read(self.ser.in_waiting)
            message = analyze_raw_data_0(raw_data.hex(' '))
            logging.info(f"找到到{len(message)}个电机")
            for motor_can_id, mcu_id in message:
                logging.info(f"can_id: {motor_can_id}, mcu_id: {mcu_id}")
                self.current_motion_type[motor_can_id] = MotionType.MOTION
        else:
            logging.error("请检查设备连接，未找到可用电机")
            raise

    #  运控模式电机控制指令 （通信类型 1）
    def set_motion_control(self):
        pass

    #  电机反馈数据 （通信类型 2） 用来向主机反馈电机运行状态

    def set_motor_enable(self, motor_can_id: int = 127):
        '''
        电机使能运行 （通信类型 3） 电机会嗡嗡的响
        :param motor_can_id: 电机can id
        '''
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(3, motor_can_id)} 01 00 0d 0a')

    def set_motor_stop(self, motor_can_id: int = 127):
        '''
        电机停止运行 （通信类型 4）
        :param motor_can_id: 电机can id
        '''
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(4, motor_can_id)} 01 00 0d 0a')

    def set_motor_zero_position(self, motor_can_id: int = 127):
        '''
        设置电机机械零位（通信类型 6）会把当前电机位置设为机械零位（掉电丢失）
        :param motor_can_id: 电机can id
        '''
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(6, motor_can_id)} 01 01 0d 0a')


    # 设置电机 CAN_ID（通信类型 7）更改当前电机 CAN_ID , 立即生效

    # 单个参数读取（通信类型 17）

    # 单个参数写入（通信类型 18） （掉电丢失） 这里可以执行各种各样的运动操作
    # 运控模式：给定电机运控 5 个参数 
    # TODO 未完成
    def set_motor_move_by_motion(self, motor_can_id: int = 127):
        if self.current_motion_type[motor_can_id] != MotionType.MOTION:
            send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 05 70 00 00 00 00 00 00 0d 0a')
            self.current_motion_type[motor_can_id] = MotionType.MOTION

    # 电流模式：给定电机指定的 Iq 电流 
    # TODO 未完成
    def set_motor_move_by_electric(self, motor_can_id: int = 127):
        if self.current_motion_type[motor_can_id] != MotionType.ELECTRIC:
            send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 05 70 00 00 03 00 00 00 0d 0a')
            self.current_motion_type[motor_can_id] = MotionType.ELECTRIC

    # 速度模式：给定电机指定的运行速度
    def set_motor_move_by_speed(self, speed: float, electric_limt: float = 23, motor_can_id: int = 127):
        '''
        速度模式：给定电机指定的运行速度
        :param speed: 目标速度 -30~30rad/s
        :param electric_limt: 电流限制 0~23A
        :param motor_can_id: 电机can id
        '''
        if self.current_motion_type[motor_can_id] != MotionType.SPEED:
            send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 05 70 00 00 02 00 00 00 0d 0a')
            self.current_motion_type[motor_can_id] = MotionType.SPEED
        self.set_motor_enable(motor_can_id)
        # 设置电流限制
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 18 70 00 00 {trans_to_4bit_float(electric_limt)} 0d 0a')
        # 设置电机速度
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 0a 70 00 00 {trans_to_4bit_float(speed)} 0d 0a')

    def set_motor_move_by_position(self, position: float, speed_limt: float = 1, motor_can_id: int = 127):
        '''
        位置模式：给定电机指定的位置，电机将运行到该指定的位置
        :param position: 目标位置 rad
        :param speed_limt: 速度限制 0~30rad/s
        :param motor_can_id: 电机can id
        '''
        if self.current_motion_type[motor_can_id] != MotionType.POSITION:
            send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 05 70 00 00 01 00 00 00 0d 0a')
            self.current_motion_type[motor_can_id] = MotionType.POSITION
        self.set_motor_enable(motor_can_id)
        # 设置速度限制
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 17 70 00 00 {trans_to_4bit_float(speed_limt)} 0d 0a')
        # 设置电机位置
        send_command(self.ser, f'41 54 {generate_can_id_and_communication_type(18, motor_can_id)} 08 16 70 00 00 {trans_to_4bit_float(position)} 0d 0a')


    # 通信类型19应该是获取全部的参数
