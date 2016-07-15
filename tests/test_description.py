import os
from lxml import etree
import pytest

from .conftest import BasicService


def load_data_file(*args):
    return os.path.join(
        os.path.dirname(__file__),
        *args
    )


def validate_xml(xml_string, schema_path):
    doc = etree.parse(load_data_file(schema_path))
    schema = etree.XMLSchema(doc)

    schema.assertValid(etree.XML(xml_string))


def describe_device_description():

    def description_fails_on_missing_required_element(basic_device):
        basic_device.device_uuid = None

        with pytest.raises(ValueError):
            basic_device.description()

    def description_validates_against_schema(basic_device):
        validate_xml(basic_device.description(), 'schemas/device-1-0.xsd')

    def service_list_contains_device_services(basic_device):
        description = etree.fromstring(basic_device.description())

        assert description.xpath(
            '//d:serviceList/d:service/d:serviceId[1]/text()',
        namespaces={
            'd': 'urn:schemas-upnp-org:device-1-0'
        }) == [BasicService.service_id]


def describe_service_description():

    def service_state_table_ordered(basic_device):
        service = basic_device.get_service(BasicService.service_type)

        description = etree.fromstring(service.description())

        assert description.xpath(
            '//d:serviceStateTable/d:stateVariable/d:name/text()',
            namespaces={
                'd': 'urn:schemas-upnp-org:service-1-0'
            }) == ['TestVariable', 'AnotherTestVariable']

    def action_list_is_ordered(basic_device):
        service = basic_device.get_service(BasicService.service_type)

        description = etree.fromstring(service.description())

        assert description.xpath(
            '//d:actionList/d:action/d:name/text()',
            namespaces={
                'd': 'urn:schemas-upnp-org:service-1-0'
            }) == ['GetTestVariable', 'SetTestVariable']

    def action_list_includes_arguments(basic_device):
        service = basic_device.get_service(BasicService.service_type)

        description = etree.fromstring(service.description())

        assert description.xpath(
            '//d:actionList/d:action[1]/d:argumentList/d:argument[1]/*/text()',
            namespaces={
                'd': 'urn:schemas-upnp-org:service-1-0'
            }) == ['TestVariable', 'out', 'TestVariable']

        assert description.xpath(
            '//d:actionList/d:action[2]/d:argumentList/d:argument[1]/*/text()',
            namespaces={
                'd': 'urn:schemas-upnp-org:service-1-0'
            }) == ['TestVariable', 'in', 'TestVariable']

    def description_validates_against_schema(basic_device):
        service = basic_device.get_service(BasicService.service_type)

        validate_xml(service.description(), 'schemas/service-1-0.xsd')