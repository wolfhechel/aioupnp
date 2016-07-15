import pytest

from aioupnp.service import Service, StateVariable, Action
from aioupnp.device import Device


class BasicService(Service):

    service_id = 'urn:upnp-org:serviceId:BasicService'

    service_type = 'urn:schemas-upnp-org:service:BasicService:1'

    TestVariable = StateVariable('i4', allowed_values=[1, 2, 3], default_value=1)

    AnotherTestVariable = StateVariable('string', send_events=False, multicast=True)

    @Action
    def GetTestVariable(self) -> (('TestVariable', TestVariable),):
        pass

    @Action
    def SetTestVariable(self, TestVariable: TestVariable):
        pass


class BasicDevice(Device):

    device_type = 'urn:schemas-upnp-org:device:Basic:1.0'

    friendly_name = 'TestDevice'

    manufacturer = 'aioupnp'

    model_name = 'test'

    device_uuid = '00000000-0000-0000-0000-000000000000'

    services = (
        BasicService,
    )

    __service_instances = None

    def __init__(self):
        self.__service_instances = {}

        for service in self.services:
            self.__service_instances[service.service_type] = service(self)

    def get_service(self, service_type):
        return self.__service_instances.get(service_type, None)


@pytest.fixture
def basic_device():
    return BasicDevice()