def analyze_raw_data_0(raw_data: str) -> tuple:
    '''
    通信类型 0 的应答帧解析
    '''
    raw_data = raw_data[6:-6].split(" 0d 0a 41 54 ")
    message = []
    for data in raw_data:
        # can_id获取
        motor_can_id_str = ''.join(f'{byte:08b}' for byte in bytes.fromhex(data[0:11]))[:29]
        motor_can_id_int = int(motor_can_id_str, 2)
        motor_can_id_hex = f"{motor_can_id_int:08X}"
        motor_can_id = int(motor_can_id_hex[4:6], 16)
        # mcu_id需要小端输出
        raw_bytes = bytes.fromhex(data[14:])
        parsed_value = int.from_bytes(raw_bytes, byteorder='little')
        mcu_id = hex(parsed_value)[2:]
        message.append((motor_can_id, mcu_id))
    return message


def analyze_can_id_and_communication_type(hex_str: str) -> dict:
    '''
    解析29位ID数据
    左移 3 位，添加 0b100，并截取前 29 位后转换为十六进制
    很奇怪的是这样和直接截取前29位的结果是一样的，目前代码为直接截断前29位

    :param hex_str: 16进制字符串

    :return: 16进制字符串
    如12 00 FD 01
    12:16进制为通信类型18
    00:保留位
    FD:主机id 主机id似乎一直为253？
    01:电机can id 
    '''
    hex_bytes = bytes.fromhex(hex_str)
    motor_can_id_str = ''.join(f'{byte:08b}' for byte in hex_bytes)[:29]
    motor_can_id_int = int(motor_can_id_str, 2)
    motor_can_id_hex = f"{motor_can_id_int:08X}"
    communication_type = int(motor_can_id_hex[0:2], 16)
    reserved = int(motor_can_id_hex[2:4], 16)
    host_id = int(motor_can_id_hex[4:6], 16)
    motor_can_id = int(motor_can_id_hex[6:8], 16)
    return {
        "通信类型": communication_type,
        "00": reserved,
        "主机id": host_id,
        "电机can id": motor_can_id
    }

def generate_can_id_and_communication_type(communication_type: int, motor_can_id: int, host_id: int = 253) -> str:
    '''
    生成29位ID数据
    :param communication_type: 通信类型（10进制）
    :param reserved: 保留位 00
    :param motor_can_id: 电机can id
    :param host_id: 主机id

    :return: 16进制字符串，为扩展帧
    '''
    motor_can_id_bin = f"{''.join(f'{int(i):04b}' for i in f'{communication_type:X}')}00000000{host_id:08b}{motor_can_id:08b}" + "100"
    motor_can_id_int = int(motor_can_id_bin, 2)
    motor_can_id_int = ' '.join([f"{motor_can_id_int:08X}"[i:i+2] for i in range(0, len(f"{motor_can_id_int:08X}"), 2)])
    return motor_can_id_int

if __name__ == "__main__":
    motor_can_id_hex = generate_can_id_and_communication_type(communication_type=1, motor_can_id=127, host_id=253)
    print(f"{motor_can_id_hex}")
    motor_can_id_hex = analyze_can_id_and_communication_type("50 1f eb fc")
    print(f"{motor_can_id_hex}")