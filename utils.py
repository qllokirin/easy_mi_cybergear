import struct
def trans_to_4bit_float(float_num: float) -> str:
    '''
    将 float 转为 4字节 bytes（小端序）
    :param float_num: 浮点数
    :return: 字节序列的十六进制字符串，如00 00 46 41
    '''
    byte_data = struct.pack('<f', float_num)
    return byte_data.hex(' ')

if __name__ == "__main__":
    num = 2
    bytes_data = trans_to_4bit_float(num)
    print(bytes_data)

import serial
from serial.serialutil import SerialException

def send_command(ser, hex_data):
    try:
        ser.write(bytes.fromhex(hex_data))
    except SerialException as e:
        print(f"发送错误: {e}")
        ser.close()
        ser.open()

from enum import Enum

class MotionType(Enum):
    # 运控模式：给定电机运控 5 个参数
    MOTION = 0
    # 电流模式：给定电机指定的 Iq 电流
    ELECTRIC = 1
    # 速度模式：给定电机指定的运行速度
    SPEED = 2
    # 位置模式：给定电机指定的位置，电机将运行到该指定的位置
    POSITION = 3
