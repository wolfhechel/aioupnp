import io
import xml.etree.ElementTree as ET


class DeviceDescription(object):
    """ Device Description Template construction class.

    Constructs an ElementTree from a Device which is later used
    to encode the device template.
    """

    root = None

    _device = None

    ELEMENT_MAP = (
        ('deviceType', 'device_type'),
        ('friendlyName', 'friendly_name'),
        ('manufacturer', 'manufacturer'),
        ('manufacturerURL', 'manufacturer_url'),
        ('modelDescription', 'model_description'),
        ('modelName', 'model_name'),
        ('modelNumber', 'model_number'),
        ('modelURL', 'model_url'),
        ('serialNumber', 'serial_number'),
        ('UDN', 'unique_device_name'),
        ('UPC', 'universal_product_code')
    )

    REQUIRED_ELEMENTS = (
        'deviceType',
        'friendlyName',
        'manufacturer',
        'modelName',
        'UDN'
    )

    def __init__(self, device):
        self._device = device

        self._construct_elements()

    def _construct_elements(self):
        self.root = ET.Element('root', attrib={
            'xmlns': 'urn:schemas-upnp-org:device-1-0',
            'configId': str(self._device._config_id)
        })

        self.root.append(self._spec_version_element())
        self.root.append(self._device_element())

    def _spec_version_element(self):
        spec_version = ET.Element('specVersion')

        ET.SubElement(spec_version,
                      'major').text = str(self._device.version.major)

        ET.SubElement(spec_version,
                      'minor').text = str(self._device.version.minor)

        return spec_version

    def _device_element(self):
        device = ET.Element('device')

        for (tag_name, attr_name) in self.ELEMENT_MAP:
            value = getattr(self._device, attr_name)

            if value is not None:
                ET.SubElement(device, tag_name).text = str(value)
            else:
                if tag_name in self.REQUIRED_ELEMENTS:
                    raise ValueError(
                        'Attribute %s cannot be empty' % attr_name
                    )

        icon_list = self._icon_list_element()

        if icon_list:
            device.append(icon_list)

        service_list = self._service_list_element()

        if service_list:
            device.append(service_list)

        return device

    def _icon_list_element(self):
        """
        Constructs the iconList element.

        :todo: Create the Icon specification for Device.

        :return: None
        """
        return None

    def _service_element(self, service):
        service_element = ET.Element('service')

        ET.SubElement(service_element,
                      'serviceType').text = service.service_type

        ET.SubElement(service_element,
                      'serviceId').text = service.service_id

        # TODO: Add real URL's for services here
        ET.SubElement(service_element, 'SCPDURL').text = ''
        ET.SubElement(service_element, 'controlURL').text = ''
        ET.SubElement(service_element, 'eventSubURL').text = ''

        return service_element

    def _service_list_element(self):
        """
        Constructs the serviceList element.

        :todo: Add service specification to device.

        :return: None
        """
        if self._device.services:
            service_list = ET.Element('serviceList')

            for service in self._device.services:
                service_list.append(self._service_element(service))
        else:
            service_list = None

        return service_list

    def __str__(self):
        return self.__bytes__().decode('utf-8')

    def __bytes__(self):
        """
        Encodes the ElementTree into a UTF-8 encoded bytestring.

        :return: bytes
        """
        stream = io.BytesIO()

        ET.ElementTree(self.root).write(stream,
                                        'utf-8',
                                        short_empty_elements=True,
                                        xml_declaration=True)

        return stream.getvalue()
