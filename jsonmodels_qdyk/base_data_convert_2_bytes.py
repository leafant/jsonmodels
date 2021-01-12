# coding:utf-8

# 文件信息：将各种数据转换成hex字符串
# 创建时间：2019-8-16
# 作者：郭晓野/guoxiaoye@tusvn.com

# 修改日志
# 时间/作者/描述
import struct


def string_2_bytes(string_value, is_little_endian=False):
    """
    将string转换成bytes
    :param string_value:
    :param is_little_endian:
    :return:
    """
    b = bytes(string_value, encoding='utf-8')
    # str_temp = ''
    # for c in string_value:
    #     int_c = ord(c)
    #     s16 = '{0:02x}'.format(int_c)
    #     str_temp = str_temp + s16

    # if is_little_endian:
    #     return struct.pack('<p', string_value)
    # return struct.pack('>p', string_value)
    # return bytes.fromhex(str_temp)
    return b


def hex_string_2_bytes(hex_string_value, is_little_endian=False):
    return bytes.fromhex(hex_string_value)


def float_string_2_bytes(float_value, is_little_endian=False):
    """
    将float转换成hex串
    :param float_value:
    :param is_little_endian:
    :return:
    """
    return string_2_bytes(str(float_value), is_little_endian)


def bool_2_bytes(bool_value, is_little_endian=False):
    """
    将bool转换成hex串
    :param bool_value:
    :param is_little_endian:
    :return:
    """
    return struct.pack('?', bool_value)


def byte_2_bytes(word_value, is_little_endian=False):
    """
    将word转换成2字节的bytes串。
    :param word_value:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.pack('<B', word_value)
    return struct.pack('>B', word_value)


def word_2_bytes(word_value, is_little_endian=False):
    """
    将word转换成2字节的bytes串。即将short转换成bytes.
    :param word_value:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.pack('<h', word_value)
    return struct.pack('>h', word_value)


def ushort_2_bytes(ushort_value, is_little_endian=False):
    """
    将word转换成2字节的bytes串。即将short转换成bytes.
    :param ushort_value:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.pack('<H', ushort_value)
    return struct.pack('>H', ushort_value)


def dword_2_bytes(dword_value, is_little_endian=False):
    """
    将dword转换成4字节的bytes串
    :param dword_value:
    :param is_little_endian:
    :return:
    """
    if is_little_endian:
        return struct.pack('<L', dword_value)
    return struct.pack('>L', dword_value)


def int_2_bytes(int_value, is_little_endian=False):
    """
    将int转换成4字节的bytes串。
    :param int_value:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<i', int_value)
    # 大端数据返回
    return struct.pack('>i', int_value)


def long_2_bytes(long_value, is_little_endian=False):
    """
    将int转换成4字节的bytes串。
    :param int_value:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<q', long_value)
    # 大端数据返回
    return struct.pack('>q', long_value)


def float_2_bytes(f, is_little_endian=False):
    """

    :param f:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<f', f)
    # 大端数据返回
    return struct.pack('>f', f)


def double_2_bytes(d, is_little_endian=False):
    """

    :param d:
    :param is_little_endian:
    :return:
    """
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<d', d)
    # 大端数据返回
    return struct.pack('>d', d)


def bytes_to_decimal_bytes(bytes_decimal_str, is_little_endian=False):
    """

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


def unsigned_int_2_bytes(value, is_little_endian=False):
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<I', value)
    # 大端数据返回
    return struct.pack('>I', value)


def unsigned_long_2_bytes(value,  is_little_endian=False):
    # 小端数据返回
    if is_little_endian:
        return struct.pack('<Q', value)
    # 大端数据返回
    return struct.pack('>Q', value)


def three_bytes_2_int(value,  is_little_endian=False):
    if is_little_endian:
        return value.to_bytes(3, "little")
    else:
        return value.to_bytes(3, "big")


def none_data_type(value, is_little_endian=False):
    """
    对非特定数据类型的处理
    :param value:
    :param  is_little_endian:
    :return:
    """
    print('是否是小端数据， ' + str(is_little_endian))
    print('输入参数有误，value =' + str(value))


global data_to_bytes_methods
data_to_bytes_methods = {"FLOATSTRING": float_string_2_bytes,
                         "HEXSTRING": hex_string_2_bytes,
                         "FLOATDOUBLE": double_2_bytes,
                         "FLOAT": float_2_bytes,
                         "BOOL": bool_2_bytes,
                         "STRING": string_2_bytes,
                         "BYTE": byte_2_bytes,
                         "WORD": word_2_bytes,
                         "USHORT": ushort_2_bytes,
                         "DWORD": dword_2_bytes,
                         "INT": int_2_bytes,
                         "LONG": long_2_bytes,
                         "BYTESDECIMAL": bytes_to_decimal_bytes,
                         "UNSIGNEDINT": unsigned_int_2_bytes,
                         "TIMESTAMP": unsigned_long_2_bytes,
                         "3BYTESINT": three_bytes_2_int,
                         }


def base_to_bytes(data_type, value, is_little_endian=False):
    """
    调用相应的方法，将特定数据转换成bytes。
    定长（byte、boolean、word、dword）的类型不需要传长度,变长(float、string)的需要传长度
    :param data_type:数据类型，值如：FLOAT，BOOL，BYTE，STRING，WORD，DWORD，INT.
    :param value:数据值
    :param is_little_endian:数据是否是小端。
    :return: hex字符串。
    """
    bytes_str = data_to_bytes_methods.get(data_type, none_data_type)(value, is_little_endian=is_little_endian)
    return bytes_str


if __name__ == '__main__':
    pass
    # to_hex_str('FLOAT', 40.00875)
