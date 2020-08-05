# coding:utf-8

# 文件信息：RCU 摄像头识别结果上报结构。
# 创建时间：2019-8-27
# 作者：郭晓野/guoxiaoye@tusvn.com

# 修改日志
# 时间/作者/描述
import os
from jsonmodels_qdyk import models, fields


class TargetObject(models.Base):
    uuid = fields.StringField(pack_to_type='HEXSTRING')
    C = fields.IntField(min_value=0, max_value=255, pack_to_type='BYTE')
    P_x = fields.IntField(default_value=0, pack_to_type='WORD', is_little_endian=True)
    P_y = fields.IntField(default_value=0, pack_to_type='WORD', is_little_endian=True)
    P_w = fields.IntField(default_value=0, pack_to_type='WORD', is_little_endian=True)
    P_h = fields.IntField(default_value=0, pack_to_type='WORD', is_little_endian=True)
    L = fields.IntField(min_value=0, max_value=255, pack_to_type='BYTE')
    Xr = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    Yr = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    V = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    longitude = fields.FloatField(default_value=0, pack_to_type='FLOATDOUBLE', is_little_endian=True)
    Latitude = fields.FloatField(default_value=0, pack_to_type='FLOATDOUBLE', is_little_endian=True)
    length = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    width = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    hei = fields.IntField(default_value=0, pack_to_type='USHORT', is_little_endian=True)
    S = fields.IntField(min_value=0, max_value=255, pack_to_type='BYTE')
    heading = fields.FloatField(default_value=0, pack_to_type='FLOAT', is_little_endian=True)


class RcuDistinguishObjects(models.Base):
    """
    上行RCU数据结构。
    """
    deviceType = fields.IntField(required=True, default_value=30634, pack_to_type='USHORT', is_little_endian=True)
    # 使用通讯网卡MAC地址作为rcuId
    rcuId = fields.StringField(required=True, pack_to_type='HEXSTRING')
    deviceId = fields.StringField(required=True, pack_to_type='BYTESDECIMAL')
    timestamp = fields.IntField(pack_to_type='LONG', is_little_endian=True)
    targets = fields.ListField([TargetObject], pack_to_type='List')
    checkCode = fields.IntField(default_value=11111, pack_to_type='USHORT', is_little_endian=True)





rcu_distinguish_objects = RcuDistinguishObjects(json_file=os.path.sep.join([os.path.abspath(os.path.dirname(__file__)),
                                                                                 'rcu_distinguish_objects_model.json']))




