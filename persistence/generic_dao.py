from .abstract_dao import AbstractDAO


class GenericDAO(AbstractDAO):
    def __init__(self, entity_class):
        super().__init__(entity_class.__name__.lower())
        self.__entity_type = entity_class

    def insert(self, obj):
        if isinstance(obj, self.__entity_type) and obj is not None:
            super().insert(self.get_obj_key(obj), obj)

    def update(self, key, obj):
        if isinstance(obj, self.__entity_type) and obj is not None:
            super().update(key, self.get_obj_key(obj), obj)
            return obj

    def get_obj_key(self, obj):
        if hasattr(obj, "cpf"):
            return obj.cpf
        elif hasattr(obj, "identificador"):
            return obj.identificador
        elif hasattr(obj, "numero_chip"):
            return obj.numero_chip

        return obj.animal.numero_chip
