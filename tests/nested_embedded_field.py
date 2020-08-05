# coding:utf-8

# 文件信息：动态地图 道路变更信息。
# 创建时间：2018-7-3
# 作者：郭晓野/guoxiaoye@tusvn.com
# 修改日志
# 时间/作者/描述

import os

from jsonmodels_qdyk import models, fields, errors, validators


class Node(models.Base):
    vendor = fields.StringField(required=True, pack_to_type='STRING')
    nodeId = fields.IntField(min_value=0, max_value=9999999, pack_to_type='WORD')
    junctionId = fields.StringField(required=True, pack_to_type='STRING')


class StructPosition(models.Base):
    longitude = fields.FloatField(min_value=10.0000001, max_value=199.999999, pack_to_type='FLOATDOUBLE')
    latitude = fields.FloatField(min_value=0.000001, max_value=89.999999, pack_to_type='FLOATDOUBLE')
    altitude = fields.FloatField(min_value=0.000001, max_value=99999999999.9, pack_to_type='FLOATDOUBLE')
    pdop_accuracy = fields.FloatField(min_value=0.01, max_value=99.99, pack_to_type='FLOATDOUBLE')
    hdop_accuracy = fields.FloatField(min_value=0.01, max_value=99.99, pack_to_type='FLOATDOUBLE')
    vdop_accuracy = fields.FloatField(min_value=0.01, max_value=99.99, pack_to_type='FLOATDOUBLE')


class StructMapNode(models.Base):
    node = fields.EmbeddedField(Node, required=True)
    position = fields.EmbeddedField(StructPosition)


class StructMapRoadUpstream(models.Base):
    vendor = fields.StringField(required=True, pack_to_type='STRING')
    roadId = fields.IntField(required=True, pack_to_type='WORD')
    startNode = fields.EmbeddedField(StructMapNode)
    endNode = fields.EmbeddedField(StructMapNode)
    startPosition = fields.EmbeddedField(StructPosition)
    endPosition = fields.EmbeddedField(StructPosition)


class StructConflictRoad(models.Base):
    conflictType = fields.IntField(required=True, pack_to_type='WORD')
    roadId = fields.IntField(required=True, pack_to_type='WORD')
    startPosition = fields.EmbeddedField(StructPosition, required=True)
    endPosition = fields.EmbeddedField(StructPosition, required=True)
    snapshots = fields.IntField(required=True, pack_to_type='WORD')
    proprietary = fields.WeakKeyDictionary()
    confidence = fields.FloatField(required=True, pack_to_type='FLOAT')
    timestamp = fields.IntField(required=True, pack_to_type='LONG')


class VehicleRoadChangeMessage(models.Base):
    """
    上报车运行事件message。
    """
    vehicleId = fields.IntField(required=True, pack_to_type='WORD')
    vendor = fields.EmbeddedField(StructMapRoadUpstream, required=True)
    conflictRoads = fields.ListField([StructConflictRoad], required=True)


class DM0105RpadChangeModel(models.Base):
    reptDataType = fields.StringField(required=True, pack_to_type='STRING')
    message = fields.ListField([VehicleRoadChangeMessage])


class VehicleRoadChangeMessage(models.Base):
    """
    上报车运行事件message。
    """
    vehicleId = fields.IntField(required=True, pack_to_type='WORD')
    vendor = fields.StringField(required=False, pack_to_type="STRING")
    conflictRoads = fields.ListField([StructConflictRoad], required=True)


class DM0105RpadChangeModel(models.Base):
    reptDataType = fields.StringField(required=True, pack_to_type="STRING")
    message = fields.ListField([VehicleRoadChangeMessage])


dm05changemodel = DM0105RpadChangeModel(json_file=os.path.sep.join([os.path.abspath(os.path.dirname(__file__)),
                                                                                 'nested_embedded_field.json']))


if __name__ == '__main__':

    test = dm05changemodel
    dm05changemodel.load_from_json_file()
    f = dm05changemodel.get_field_bytes('reptDataType')
    print(test.message)



