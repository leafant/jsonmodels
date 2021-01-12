
import json
import six

from jsonmodels_qdyk import base_data_from_bytes
from . import parsers, errors
from .fields import BaseField, ListField, EmbeddedField
from .errors import ValidationError


class JsonmodelMeta(type):

    def __new__(cls, name, bases, attributes):
        cls.validate_fields(attributes)
        return super(cls, cls).__new__(cls, name, bases, attributes)

    @staticmethod
    def validate_fields(attributes):
        fields = {
            key: value for key, value in attributes.items()
            if isinstance(value, BaseField)
        }
        taken_names = set()
        for name, field in fields.items():
            structue_name = field.structue_name(name)
            if structue_name in taken_names:
                raise ValueError('Name taken', structue_name, name)
            taken_names.add(structue_name)


class Base(six.with_metaclass(JsonmodelMeta, object)):

    """Base class for all models."""
    # 协议中的数据类型和数据版本
    data_type = None
    data_version = None
    json_data_file = None
    
    def __init__(self, json_file=None, length=None, **kwargs):
        self._cache_key = _CacheKey()
        self.populate(**kwargs)
        self.json_file = json_file
        self.load_default_values()
        self.length = length

    def populate(self, **values):
        """Populate values to fields. Skip non-existing."""
        values = values.copy()
        fields = list(self.iterate_with_name())
        for _, structure_name, field in fields:
            if structure_name in values:
                field.__set__(self, values.pop(structure_name))
        for name, _, field in fields:
            if name in values:
                field.__set__(self, values.pop(name))

    def get_field(self, field_name):
        """Get field associated with given attribute."""
        for attr_name, field in self:
            if field_name == attr_name:
                return field

        raise errors.FieldNotFound('Field not found', field_name)

    # add by gloria
    def get_field_by_sequence(self, sequence_index):
        """Get field associated with given sequence_index."""
        for attr_name, field in enumerate(self):
            if sequence_index == field[1].sequence:
                return field

        raise errors.FieldNotFound('Field not found', sequence_index)

    # add by gloria
    def set_field_by_sequence(self, sequence_index, value):
        """Get field associated with given sequence_index."""
        for attr_name, field in self:
            if sequence_index == field.sequence:
                setattr(self, field[0], value)

        raise errors.FieldNotFound('Field not found', sequence_index)

    def __iter__(self):
        """Iterate through fields and values."""
        for name, field in self.iterate_over_fields():
            yield name, field

    def validate(self):
        """Explicitly validate all the fields."""
        for name, field in self:
            try:
                field.validate_for_object(self)
            except ValidationError as error:
                raise ValidationError(
                    "Error for field '{name}'.".format(name=name),
                    error,
                )

    @classmethod
    def iterate_over_fields(cls):
        """Iterate through fields as `(attribute_name, field_instance)`."""
        for attr in dir(cls):
            clsattr = getattr(cls, attr)
            if isinstance(clsattr, BaseField):
                yield attr, clsattr

    @classmethod
    def iterate_with_name(cls):
        """Iterate over fields, but also give `structure_name`.

        Format is `(attribute_name, structue_name, field_instance)`.
        Structure name is name under which value is seen in structure and
        schema (in primitives) and only there.
        """
        for attr_name, field in cls.iterate_over_fields():
            structure_name = field.structue_name(attr_name)
            yield attr_name, structure_name, field

    def to_struct(self):
        """Cast model to Python structure."""
        return parsers.to_struct(self)

    @classmethod
    def to_json_schema(cls):
        """Generate JSON schema for model."""
        return parsers.to_json_schema(cls)

    # add by gloria
    def load_json_model(self, json_dict):
        """
        for loading self parameters.
        :param json_dict: json dictionary data.
        :return: None
        """
        if not isinstance(self, Base):
            raise Exception('The parameter item is not a json model')
        if not json_dict:
            raise Exception('The parameter json_dict is None')
        if not isinstance(json_dict, dict):
            raise Exception('The parameter json_dict is not a json dict!')

        for attr, field in enumerate(self):
            # 如果对象本身有默认值，将使用类中的值。如果json文件中有值，将以json文件中的值为主。
            if field[0] not in json_dict.keys() or json_dict[field[0]] == "":
                if field[1].default_value is not None:
                    setattr(self, field[0], field[1].default_value)
                else:
                    print('This attribute:{} not been set default value both in model class and json file.'.format(field))
            else:
                # 若属性是列表类型
                if type(field[1]) is ListField:
                    # 如果列表是空列表
                    if len(json_dict[field[0]]) == 0:
                        setattr(self, field[0], [])
                        continue
                    # 如果是值类型的数组：
                    if (isinstance(json_dict[field[0]][0], int) or isinstance(json_dict[field[0]][0], float)
                            or isinstance(json_dict[field[0]][0], str)):
                        setattr(self, field[0], json_dict[field[0]])
                        continue
                    item_type = field[1].items_types[0]
                    list_obj_list = list()
                    for list_obj in json_dict[field[0]]:
                        obj_item = item_type()
                        obj_item.load_json_model(list_obj)
                        list_obj_list.append(obj_item)
                    setattr(self, field[0], list_obj_list)
                    continue
                # 若属性是model类型
                if type(field[1]) is EmbeddedField:
                    obj_item_type = field[1].types[0]
                    obj_item = obj_item_type()
                    obj_item.load_json_model(json_dict[field[0]])
                    setattr(self, field[0], obj_item)
                    # print('field:{} is a Embedded Field'.format(field))
                    continue
                # 其余则属性是值类型的
                else:
                    setattr(self, field[0], json_dict[field[0]])
                    # print('field:{} is a value Field'.format(field))

    # add by gloria
    def load_default_values(self):
        """
        loading the default values for all fields.
        :return: None
        """
        if not isinstance(self, Base):
            raise Exception('The parameter item is not a json model')

        for attr, field in enumerate(self):
            # 具有默认值。
            if field[1].default_value is not None:
                setattr(self, field[0], field[1].default_value)
            else:
                # 若属性是列表类型
                if type(field[1]) is ListField:
                    item_type = field[1].items_types
                    tem_list = list()
                    for i, list_obj in enumerate(item_type):
                        obj_item = list_obj()
                        obj_item.load_default_values()
                        tem_list.append(obj_item)
                    setattr(self, field[0], tem_list)
                    # print('load_default_values, field: {} is a ListField'.format(field))
                    continue
                # 若属性是model类型
                if type(field[1]) is EmbeddedField:
                    obj_item_type = field[1].types[0]
                    obj_item = obj_item_type()
                    obj_item.load_default_values()
                    setattr(self, field[0], obj_item)
                    # print('load_default_values, field:{} is a Embedded Field'.format(field))
                    continue
                # 其余值类型的，但没有默认值
                # else:
                #     print('!!!Warning, load_default_values, please set default value for field: {}'.format(field))

    # add by gloria
    def get_field_bytes(self, field_name):
        """
        获得属性值的bytes串
        :param field_name:
        :return:
        """
        for attr_name, field in self:
            if field_name == attr_name:
                return field.bytes_str(self)

    # add by gloria
    def get_obj_bytes(self):
        """
        将model中的所有属性，转换成一个长bytes。
        :return:
        """
        # 用于存放各个按顺序的field对应的bytes。
        temp_bytes_dict = dict()
        temp_bytes = b''
        for attr, field in enumerate(self):
            # 判断是否有依赖的field
            depended_field = field[1].depending_field
            if depended_field:
                depend = getattr(self, depended_field)
                # 如果依赖的数据项的值是0或空，则此数据项将被排除。
                if (not depend) or depend < 1:
                    temp_bytes_dict[field[1].sequence] = b''
                    continue

            # 如果属性是列表
            if type(field[1]) is ListField:
                brother_classes = Base.__subclasses__()
                list_items = getattr(self, field[0])
                if len(list_items) == 0:
                    temp_bytes_dict[field[1].sequence] = b''
                # 如果列表中只是值属性,非json model属性
                elif field[1].pack_to_type != 'LIST' and type(list_items[0]) not in brother_classes:
                    temp_bytes_dict[field[1].sequence] = field[1].byte_value
                # 如果列表中的内容是jsonmodel 属性。
                else:
                    tmp_bytes_list = list()
                    for item in list_items:
                        # 如果列表属性是json 对象时，
                        tmp_bytes_list.append(item.get_obj_bytes())

                    temp_bytes_dict[field[1].sequence] = b''.join(tmp_bytes_list)
            # 如果属性是嵌入jsonmodel自定义对象
            elif type(field[1]) is EmbeddedField:
                embeded_field = getattr(self, field[0])
                temp_bytes_dict[field[1].sequence] = embeded_field.get_obj_bytes()
            # 如果属性是普通field对象
            elif field[1].pack_to_type:
                # print('开始处理filed:' + str(field[0]))
                temp_bytes_dict[field[1].sequence] = field[1].byte_value
            else:
                print('!!!Warning: field:{} packe_to_type is none!'.format(field[0]))
        dict_length = len(temp_bytes_dict)
        i = 0
        while i < dict_length:
            temp_bytes += temp_bytes_dict[i]
            i += 1
        return temp_bytes

    # @classmethod
    # def obj_to_bytes(cls, model_obj):
    #     """
    #     将model中的field 根据值一一转成bytes。
    #     :return:
    #     """
    #     for attr, field in enumerate(model_obj):
    #         # 如果属性是对象列表或值列表
    #         if type(field[1]) is ListField:
    #             continue
    #         # 如果属性是嵌入自定义对象
    #         elif type(field[1]) is EmbeddedField:
    #             continue
    #         # 如果属性是普通field对象
    #         elif field[1].pack_to_type is not None:
    #             # print('开始处理filed:' + str(field[0]))
    #             BaseField.to_bytes(cls, field[1], model_obj._cache_key)
    #
    #         else:
    #             raise Exception('the attribute pack_to_type is none.')

    # add by gloria
    def load_from_json_file(self):
        """
        从json文件中加载属性。
        :return:
        """
        if self.json_data_file:
            json_file_name = self.json_data_file
        elif self.json_file:
            json_file_name = self.json_file
        else:
            print('没有初始化json file')
        with open(json_file_name, "r", encoding='UTF-8') as f:
            t = json.load(f)
        return self.load_json_model(t)

    @classmethod
    # add by gloria
    def get_json_data_model(cls, data_type, data_version):
        """
        给定协议中特定数据类型和版本号，返回其对应的jsonmodel 实例。
        :param data_type:
        :param data_version:
        :return:
        """
        json_models_base_classes = cls.__subclasses__()
        for model_class in json_models_base_classes:
            if model_class.data_type == data_type and model_class.data_version == data_version:
                return model_class()

        print('!!!WARNING:没有找到匹配的数据类型和其对应版本！')
        raise Exception('ERROR：没有找到匹配的数据类型和其对应版本！')

    @classmethod
    def load_model_from_bytes(cls, data_type, data_version, bytes_str):
        """
        给定协议中特定数据类型和版本号，以及bytes string，返回解析后的json字典。
        :param data_type: 协议中规定的数据类别
        :param data_version:协议中规定的数据版本号
        :param bytes_str: bytes字符串
        :return: 跟协议数据结构一致的json字典。
        """
        target_json_model_instance = cls.get_json_data_model(data_type, data_version)
        cls.load_from_bytes(target_json_model_instance, bytes_str)
        return target_json_model_instance.to_struct()

    @classmethod
    # add by gloria
    def load_from_bytes(cls, target_json_model_instance, bytes_str):
        """
        给定目标json model实例及bytes strng，返回解析后的json model实例。
        :param target_json_model_instance: 协议中规定的数据类别
        :param bytes_str: bytes字符串
        :return: 跟协议数据结构一致的json字典。
        """
        if len(bytes_str) <= 0:
            print('WARNING: The input parameters length is 0!')
            return None
        if target_json_model_instance.length:
            if len(bytes_str) < target_json_model_instance.length:
                print('WARNING: 输入bytes的长度小于即将被解析对象的最小长度!')
                return None
        index = 0
        i = 0
        attr_dict = dict(enumerate(target_json_model_instance))
        while i < len(attr_dict):
            field_attr = target_json_model_instance.get_field_by_sequence(i)
            pack_data_type = field_attr[1].pack_to_type
            byte_length = field_attr[1].byte_length
            # 若属性是列表类型
            if type(field_attr[1]) is ListField:
                fields_list = list()
                known_length = None
                # 如果有依赖项，则说明是不定长列表，按列表指定长度一一解析。
                if field_attr[1].depending_field:
                    # 所依赖元素的值，就是列表的长度，获得列表长度
                    depending_field_name = field_attr[1].depending_field
                    depending_field = target_json_model_instance.get_field(depending_field_name)

                    if isinstance(depending_field.value, int):
                        known_length = depending_field.value
                else:
                    # 如果是定长列表，且列表里的元素都是同一类型。
                    items_types = field_attr[1].items_types
                    items_length = base_data_from_bytes.get_bytes_length(items_types)
                    if items_length == 0:
                        raise Exception('ERROR：列表元素的数据类型不是有效的数值类型！！！，field:{}'.format(field_attr[0]))
                    items_num = byte_length / items_length
                    if isinstance(items_num, int):
                        for j in range(items_num):
                            start_cursor = index + j * items_length
                            tmp_bytes = bytes_str[start_cursor:start_cursor + items_length]
                            tmp_value = base_data_from_bytes.base_from_bytes(items_types, tmp_bytes)
                            fields_list.append(tmp_value)
                    else:
                        raise Exception('ERROR：列表的总长度，与列表类型和元素长度不匹配！,field:{}'.format(field_attr[0]))
                # 如果列表是空列表
                if known_length and known_length == 0:
                    setattr(target_json_model_instance, field_attr[0], [])

                elif known_length and known_length > 0:
                    expected_byte_length = known_length * byte_length
                    if len(bytes_str[index:]) < expected_byte_length:
                        print('ERROR：剩余字节长度小于期望长度！field:{}, sequence'.format(field_attr[0], field_attr[1].sequence))
                        raise Exception('ERROR：剩余字节长度小于期望长度！')
                    counter = known_length
                    while counter > 0:

                        temp_model_bytes = bytes_str[index:index + byte_length]
                        index += byte_length
                        # 如果列表中的元素是Base model类的数组：
                        if issubclass(field_attr[1].items_types[0], Base):
                            obj_item_model_instance = field_attr[1].items_types[0]()
                            obj_item_model_instance.load_from_bytes(obj_item_model_instance, temp_model_bytes)
                            fields_list.append(obj_item_model_instance)
                        else:
                            raise Exception('ERROR：未能识别的json model 类型，field ={}'.format(field_attr[0]))
                        counter -= 1
                    setattr(target_json_model_instance, field_attr[0], fields_list)
                else:
                    print('ERROR：未指定列表元素的数量,或数量是负值，length ={}'.format(known_length))
                    raise Exception('ERROR：未指定列表元素的数量，length ={}'.format(known_length))

            # 若属性是model类型
            elif type(field_attr[1]) is EmbeddedField:
                byte_str = bytes_str[index:index + byte_length]
                tep_value = field_attr[1].load_from_bytes(byte_str)
                setattr(target_json_model_instance, field_attr[0], tep_value)
            # 其余则属性是值类型的
            else:
                byte_str = bytes_str[index:index + byte_length]

                value = base_data_from_bytes.base_from_bytes(pack_data_type, byte_str)
                setattr(target_json_model_instance, field_attr[0], value)
            index += byte_length
            i += 1

    def __repr__(self):
        attrs = {}
        for name, _ in self:
            try:
                attr = getattr(self, name)
                if attr is not None:
                    attrs[name] = repr(attr)
            except ValidationError:
                pass

        return '{class_name}({fields})'.format(
            class_name=self.__class__.__name__,
            fields=', '.join(
                '{0[0]}={0[1]}'.format(x) for x in sorted(attrs.items())
            ),
        )

    def __str__(self):
        return '{name} object'.format(name=self.__class__.__name__)

    def __setattr__(self, name, value):
        try:
            return super(Base, self).__setattr__(name, value)
        except ValidationError as error:
            raise ValidationError(
                "Error for field '{name}'.".format(name=name),
                error
            )

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        for name, _ in self.iterate_over_fields():
            try:
                our = getattr(self, name)
            except errors.ValidationError:
                our = None

            try:
                their = getattr(other, name)
            except errors.ValidationError:
                their = None

            if our != their:
                return False

        return True

    def __ne__(self, other):
        return not (self == other)


class _CacheKey(object):
    """Object to identify model in memory."""
