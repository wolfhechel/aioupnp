from .conftest import BasicDevice, BasicService


def describe_device():

    def get_service_returns_instance_of_service_type():
        device = BasicDevice()

        assert isinstance(device.get_service(BasicService.service_type), BasicService)