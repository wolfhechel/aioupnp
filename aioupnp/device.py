from .version import UPnPVersion20
from .description.device import DeviceDescription


class Device(object):
    """ Device class for implementing a UPnP device.

    In order to implement your own UPnP device you can either choose to
    inherit from this class or instantiate and set the properties.


    Attributes:
        version (:obj:`UPnPVersion`, required): UPnP device architecture version this device supports.
        device_type (str, required): The device type URI.
        friendly_name (str, required): A human friendly device name, control points use this
            for presentation purposes (i.e. when selecting device).
        manufacturer (str, required): Name of the manufacturer of this device.
        manufacturer_url (str): URL to the manufacturer website.

    Todo:
        * Finish describing all properties here
    """

    _config_id = 0

    version = UPnPVersion20

    device_type = None

    friendly_name = None

    manufacturer = None

    manufacturer_url = None

    model_description = None

    model_name = None

    model_number = None

    model_url = None

    serial_number = None

    device_uuid = None

    universal_product_code = None

    presentation_url = None

    services = None

    @property
    def unique_device_name(self):
        return 'uuid:' + self.device_uuid if self.device_uuid else None

    def description(self):
        description = DeviceDescription(self)

        return bytes(description)
