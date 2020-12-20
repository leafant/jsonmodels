# add by gloria
# date 2020-12-20
from jsonmodels_qdyk.models import Base


class ModelsFactory(object):
    """
    工厂类：通过数据类型和版本号，返回特定json model 的实例。
    """
    @staticmethod
    def get_json_data_model(data_type, data_version):
        json_models_base_classes = Base.__subclasses__()
        for model_class in json_models_base_classes:
            if model_class.data_type == data_type and model_class.data_version == data_version:
                return model_class()
            else:
                print('!!!WARNING:没有找到匹配的数据类型和其对应版本！')
