from collections import OrderedDict

from .description.service import ServiceDescription


def Action(func):
    func.out_args = OrderedDict(func.__annotations__.pop('return', ()))
    func.in_args = OrderedDict(func.__annotations__)
    func._is_action = True

    return func


class StateVariable(object):

    data_type = None

    send_events = None

    multicast = None

    allowed_values = None

    default_value = None

    def __init__(self,
                 data_type,
                 send_events=None,
                 multicast=None,
                 allowed_values=None,
                 default_value=None):

        self.data_type = data_type
        self.send_events = send_events
        self.multicast = multicast
        self.allowed_values = allowed_values or []
        self.default_value = default_value


class ServiceType(type):

    def __prepare__(name, bases, **kwargs):
        return OrderedDict()

    @staticmethod
    def _lookup_service_state_table(__dict__):
        service_state_table = OrderedDict()

        for (attr_name, attr_value) in __dict__.items():
            if isinstance(attr_value, StateVariable):
                service_state_table[attr_name] = attr_value

        return service_state_table

    @staticmethod
    def _lookup_action_list(__dict__):
        action_list = OrderedDict()

        for (attr_name, attr_value) in __dict__.items():
            if (callable(attr_value)
                    and getattr(attr_value, '_is_action', False)):
                action_list[attr_name] = attr_value

        return action_list

    def __new__(mcs, name, bases, __dict__):
        __dict__['service_state_table'] = mcs._lookup_service_state_table(
            __dict__
        )
        __dict__['action_list'] = mcs._lookup_action_list(__dict__)

        return super().__new__(mcs, name, bases, __dict__)


class Service(object, metaclass=ServiceType):

    service_id = None

    service_type = None

    service_state_table = None

    action_list = None

    __device = None

    def __init__(self, device):
        self.__device = device

    def description(self):
        return bytes(ServiceDescription(self.__device, self))

    @classmethod
    def state_variable_name(cls, state_variable):
        return next(
            name for name, variable
            in cls.service_state_table.items()
            if variable == state_variable
        )
