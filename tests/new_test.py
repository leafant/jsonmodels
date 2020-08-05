
import struct
import time
import uuid

import uuid as uuid

from tests import rcu_distinguish_objects_model
from tests.rcu_distinguish_objects_model import TargetObject, RcuDistinguishObjects


def create_rcu_distinguish_obj(device_type, Longitude, Latitude, p_x, p_y, p_w, p_h, xr, yr, v, length,
                               width, hei, s, heading=0, l=0, c=2, uuid_str=None):
    tem_obj = TargetObject()
    if not uuid_str:
        uuid_str = str(uuid.uuid4()).replace('-', '')
    tem_obj.uuid = uuid_str
    tem_obj.C = c
    if device_type == 30634:
        tem_obj.P_x = p_x
        tem_obj.P_y = p_y
        tem_obj.P_w = p_w
        tem_obj.P_h = p_h
    elif device_type == 30635:
        tem_obj.P_x = -1
        tem_obj.P_y = -1
        tem_obj.P_w = -1
        tem_obj.P_h = -1
    else:
        print('The device type is wrong!')
        return
    tem_obj.L = l
    tem_obj.Xr = xr
    tem_obj.Yr = yr
    tem_obj.V = v
    tem_obj.longitude = Longitude
    tem_obj.Latitude = Latitude
    tem_obj.length = length
    tem_obj.width = width
    tem_obj.hei = hei
    tem_obj.S = s
    tem_obj.heading = heading
    return tem_obj


def assemble_single_rcu_perception_object_result2(rcu_distinguish_object, is_little_end=False, timestamp=None):
    """
    参考1.5.1 RCU侧检测目标结果（上报）-0x05。结果来源于摄像头或雷达。
    :param rcu_distinguish_object：
    :param is_little_end:
    :param timestamp:
    :return:
    """
    if not isinstance(rcu_distinguish_object, RcuDistinguishObjects):
        return
    if not timestamp:
        t = time.time()
        rcu_distinguish_object.timestamp = int(round(t * 1000))

    bytes_time = rcu_distinguish_object.get_field('timestamp').byte_value
    check_code = rcu_distinguish_object.get_field('checkCode').byte_value

    if rcu_distinguish_object.deviceId.isdigit():
        device_id = rcu_distinguish_object.get_field('deviceId').byte_value
    else:
        print('当前device不是数字字符串')
        return

    f_name = 'targets'
    if hasattr(rcu_distinguish_object, f_name):
        targets = getattr(rcu_distinguish_object, f_name)

    tmp_bytes_list = list()
    if isinstance(targets, list):
        for target in targets:
            uuid = target.get_field('uuid').byte_value
            C = target.get_field('C').byte_value
            P_x = target.get_field('P_x').byte_value
            P_y = target.get_field('P_y').byte_value
            P_w = target.get_field('P_w').byte_value
            P_h = target.get_field('P_h').byte_value
            L = target.get_field('L').byte_value
            Xr = target.get_field('Xr').byte_value
            Yr = target.get_field('Yr').byte_value
            V = target.get_field('V').byte_value
            longitude = target.get_field('longitude').byte_value
            Latitude = target.get_field('Latitude').byte_value
            length = target.get_field('length').byte_value
            width = target.get_field('width').byte_value
            hei = target.get_field('hei').byte_value
            S = target.get_field('S').byte_value
            heading = target.get_field('heading').byte_value
            tmp_bytes_list.append(uuid + C + P_x + P_y + P_w + P_h + L + Xr + Yr + V + longitude + Latitude + length + width
                                  + hei + S + heading)
    else:
        print('WARNING！！！！识别列表中信息是空！！！！！')

    if is_little_end:
        length_hex = struct.pack('<H', 59*len(targets))
    else:
        length_hex = struct.pack('>H', 59*len(targets))

    device_type = rcu_distinguish_object.get_field('deviceType').byte_value
    rcu_id = rcu_distinguish_object.get_field('rcuId').byte_value
    tmp_bytes = device_type + rcu_id + device_id + length_hex + b''.join(tmp_bytes_list) + bytes_time + check_code
    # print(str(tmp_bytes))
    return tmp_bytes


def test():
    """
    :return:
    """
    dis_objects = rcu_distinguish_objects_model.rcu_distinguish_objects
    c = dis_objects.targets
    dis_objects.load_from_json_file()

    dis_objects.deviceType = 30634
    dis_objects.rcuId = "2019A10000D3"
    dis_objects.deviceId = "3402000000132000000005"

    a = dis_objects.rcuId
    b = dis_objects.get_field_bytes('deviceId')
    c = dis_objects.targets[0].get_field_bytes('Latitude')
    print("a={}".format(a))
    print("b={}".format(b))
    print("c={}".format(c))


def test_rcu_data_to_queue():
    """
    将即将上报的rcu识别数据放入临时列表中。
    :return:
    """
    dis_objects = rcu_distinguish_objects_model.rcu_distinguish_objects
    dis_objects.load_from_json_file()
    dis_objects.targets.clear()
    uuid_s = str(uuid.uuid4()).replace('-', '')

    dis_objects.deviceType = 30635
    dis_objects.rcuId = "2019A10000D3"
    dis_objects.deviceId = "3402000000132000000005"
    # "3402000000132000000005"

    # 根据设备（摄像头和雷达）的数量，一一生成所属设备的识别结果。
    tem_obj = create_rcu_distinguish_obj(device_type=dis_objects.deviceType,
                                         Longitude=116.1234567,
                                         Latitude=30.123456,
                                         c=2, p_x=2, p_y=2, p_w=2, p_h=2,
                                         xr=100,
                                         yr=100,
                                         v=11.11 * 100,
                                         length=500,
                                         width=300,
                                         hei=160,
                                         l=0,
                                         s=0,
                                         heading=34.12,
                                         uuid_str=uuid_s)

    t = time.time()
    now_time = int(round(t * 1000))
    dis_objects.timestamp = now_time
    print('原始数据时间：{0}'.format(now_time))
    dis_objects.targets.append(tem_obj)
    tcp_rcu_payload = assemble_single_rcu_perception_object_result2(dis_objects, is_little_end=True)
    print(tcp_rcu_payload)
