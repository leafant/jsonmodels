# coding:utf-8

# 文件信息：将bytes串根据类型转换成对应的数据类型。
# 创建时间：2021-1-5
# 作者：郭晓野/guoxiaoye@tusvn.com

# 修改日志
# 时间/作者/描述
import struct


def bytes_2_string(bytes_string, is_little_endian=False):
    """
    将bytes转换成string
    :param bytes_string:
    :param is_little_endian:
    :return:
    """
    str_value = bytes.decode(bytes_string, encoding='utf-8')

    return str_value


def bytes_2_hex_string(bytes_string, is_little_endian=False):
    return bytes_string.hex()


def bytes_2_float_string(bytes_string, is_little_endian=False):
    """
    将bytes转换成 float string
    :param bytes_string:
    :param is_little_endian:
    :return:
    """
    return bytes_2_string(bytes_string, is_little_endian)


def bytes_2_bool(bool_bytes_string, is_little_endian=False):
    """
    将bool转换成hex串
    :param bool_bytes_string:
    :param is_little_endian:
    :return:
    """
    return struct.unpack('?', bool_bytes_string)[0]


def byte_2_int(byte_string, is_little_endian=False):
    """
    将byte（1个字节）转换成int。
    :param byte_string:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.unpack('<B', byte_string)[0]
    return struct.unpack('>B', byte_string)[0]


def word_2_int(word_byte_string, is_little_endian=False):
    """
    将word （2字节）转换成short.
    :param word_byte_string:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.unpack('<h', word_byte_string)[0]
    return struct.unpack('>h', word_byte_string)[0]


def bytes_2_ushort(ushort_bytes_string, is_little_endian=False):
    """
    将2字节的bytes串转换成 无符号short.
    :param ushort_bytes_string:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.unpack('<H', ushort_bytes_string)[0]
    return struct.unpack('>H', ushort_bytes_string)[0]


def dword_2_long(dword_bytes_string, is_little_endian=False):
    """
    将4字节的bytes串转换成unsigned long.
    :param dword_bytes_string:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.unpack('<L', dword_bytes_string)[0]
    return struct.unpack('>L', dword_bytes_string)[0]


def bytes_2_int(int_bytes_string, is_little_endian=False):
    """
    将4字节的bytes串转换成int。
    :param int_bytes_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<i', int_bytes_string)[0]
    # 大端数据返回
    return struct.unpack('>i', int_bytes_string)[0]


def bytes_2_long(long_bytes_string, is_little_endian=False):
    """
    将8字节的bytes串转换成int。
    :param long_bytes_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<q', long_bytes_string)[0]
    # 大端数据返回
    return struct.unpack('>q', long_bytes_string)[0]


def bytes_2_float(bytes_float_string, is_little_endian=False):
    """
    将4字节的bytes串转换成float.
    :param bytes_float_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<f', bytes_float_string)[0]
    # 大端数据返回
    return struct.unpack('>f', bytes_float_string)[0]


def bytes_2_double(bytes_double_string, is_little_endian=False):
    """
    将8字节的bytes串转换成float.
    :param bytes_double_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<d', bytes_double_string)[0]
    # 大端数据返回
    return struct.unpack('>d', bytes_double_string)[0]


def bytes_to_decimal_string(bytes_decimal_str, is_little_endian=False):
    """
    将bytes转换成10进制的字符串。
    :param bytes_decimal_str:
    :param is_little_endian:
    :return:
    """
    if not bytes_decimal_str.isdigit():
        raise Exception('bytes_decimal_str 不是数字字符串！')
        return
    length = len(bytes_decimal_str)
    tmp_list = [bytes_decimal_str[i:i+2] for i in range(length) if (i % 2 == 0)]
    hex_list = list()
    for byte_str in tmp_list:
        h_str = hex(int(byte_str))
        hex_list.append(h_str[2:].zfill(2))
    byte_str = bytes.fromhex(''.join(hex_list))
    # print(byte_str)
    return byte_str


def bytes_2_unsigned_int(bytes_string, is_little_endian=False):
    """
    将4字节的bytes转换成unsigned int。
    :param bytes_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<I', bytes_string)[0]
    # 大端数据返回
    return struct.unpack('>I', bytes_string)[0]


def bytes_2_unsigned_long(bytes_long_string,  is_little_endian=False):
    """
    将8字节的bytes转换成unsigned long long
    :param bytes_long_string:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.unpack('<Q', bytes_long_string)[0]
    # 大端数据返回
    return struct.unpack('>Q', bytes_long_string)[0]


def three_bytes_2_int(bytes_string,  is_little_endian=False):
    if is_little_endian:
        return int.from_bytes(bytes_string, byteorder="little")
    else:
        return int.from_bytes(bytes_string, byteorder='big')


def none_data_type(value, is_little_endian=False):
    """
    对非特定数据类型的处理
    :param value:
    :param  is_little_endian:
    :return:
    """
    print('是否是小端数据， ' + str(is_little_endian))
    print('输入参数有误，value =' + str(value))


global data_from_bytes_methods
data_from_bytes_methods = {"FLOATSTRING": bytes_2_float,
                         "HEXSTRING": bytes_2_hex_string,
                         "FLOATDOUBLE": bytes_2_double,
                         "FLOAT": bytes_2_float,
                         "BOOL": bytes_2_bool,
                         "STRING": bytes_2_string,
                         "BYTE": byte_2_int,
                         "WORD": word_2_int,
                         "USHORT": bytes_2_ushort,
                         "DWORD": dword_2_long,
                         "INT": bytes_2_int,
                         "LONG": bytes_2_long,
                         "BYTESDECIMAL": bytes_to_decimal_string,
                         "UNSIGNEDINT": bytes_2_unsigned_int,
                         "TIMESTAMP": bytes_2_unsigned_long,
                         "3BYTESINT": three_bytes_2_int,
                         }


def base_from_bytes(data_type, value, is_little_endian=False):
    """
    调用相应的方法，将特定数据转换成bytes。
    定长（byte、boolean、word、dword）的类型不需要传长度,变长(float、string)的需要传长度
    :param data_type:数据类型，值如：FLOAT，BOOL，BYTE，STRING，WORD，DWORD，INT.
    :param value:数据值
    :param is_little_endian:数据是否是小端。
    :return: hex字符串。
    """
    if data_type == b'':
        return b''
    base_value = data_from_bytes_methods.get(data_type, none_data_type)(value, is_little_endian=is_little_endian)
    return base_value


def get_bytes_length(data_type):
    """
    根据打包的数据类型返回bytes长度。
    :param data_type:
    :return:
    """
    if data_type == "FLOATSTRING":
        return 4
    if data_type == "HEXSTRING":
        return 16
    if data_type == "FLOATDOUBLE":
        return 8
    if data_type == "FLOAT":
        return 4
    if data_type == "BOOL":
        return 1
    if data_type == "BYTE":
        return 1
    if data_type == "WORD":
        return 2
    if data_type == "USHORT":
        return 2
    if data_type == "DWORD":
        return 4
    if data_type == "INT":
        return 4
    if data_type == "LONG":
        return 8
    if data_type == "BYTESDECIMAL":
        return 4
    if data_type == "UNSIGNEDINT":
        return 4
    if data_type == "TIMESTAMP":
        return 8
    if data_type == "3BYTESINT":
        return 3
    return 0


if __name__ == '__main__':
    pass
    # to_hex_str('FLOAT', 40.00875)
