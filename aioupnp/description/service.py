import io
import xml.etree.ElementTree as ET


class ServiceDescription(object):
    """ Device Description Template construction class.

    Constructs an ElementTree from a Device which is later used
    to encode the device template.
    """

    root = None

    _device = None

    def __init__(self, device, service):
        self._device = device
        self._service = service

        self._construct_elements()

    def _construct_elements(self):
        self.root = ET.Element('scpd', attrib={
            'xmlns': 'urn:schemas-upnp-org:service-1-0',
            'configId': str(self._device._config_id)
        })

        self.root.append(self._spec_version_element())

        action_list = self._action_list_element()

        if action_list:
            self.root.append(action_list)

        self.root.append(self._service_state_table_element())

    def _spec_version_element(self):
        spec_version = ET.Element('specVersion')

        ET.SubElement(spec_version,
                      'major').text = str(self._device.version.major)

        ET.SubElement(spec_version,
                      'minor').text = str(self._device.version.minor)

        return spec_version

    def _add_arguments_to_argument_list(self,
                                        argument_list,
                                        arg_dict,
                                        direction):
        for (argument_name, state_variable) in arg_dict.items():
            argument = ET.SubElement(argument_list, 'argument')
            ET.SubElement(argument, 'name').text = argument_name
            ET.SubElement(argument, 'direction').text = direction

            state_variable_name = self._service.state_variable_name(
                state_variable
            )

            ET.SubElement(
                argument,
                'relatedStateVariable'
            ).text = state_variable_name

    def _action_element(self, name, action):
        action_el = ET.Element('action')

        ET.SubElement(action_el, 'name').text = name

        if action.out_args or action.in_args:
            argument_list = ET.SubElement(action_el, 'argumentList')

            self._add_arguments_to_argument_list(
                argument_list,
                action.in_args,
                'in'
            )

            self._add_arguments_to_argument_list(
                argument_list,
                action.out_args,
                'out'
            )

        return action_el

    def _action_list_element(self):
        if self._service.action_list:
            action_list = ET.Element('actionList')

            for (name, method) in self._service.action_list.items():
                action_list.append(
                    self._action_element(name, method)
                )
        else:
            action_list = None

        return action_list

    def _state_variable_element(self, name, state_variable):
        attribs = {}

        if state_variable.send_events is not None:
            attribs['sendEvents'] = '1' if state_variable.send_events else '0'

        if state_variable.multicast is not None:
            attribs['multicast'] = '1' if state_variable.multicast else '0'

        state_variable_el = ET.Element('stateVariable', attrib=attribs)

        ET.SubElement(state_variable_el, 'name').text = name

        ET.SubElement(
            state_variable_el,
            'dataType'
        ).text = state_variable.data_type

        if state_variable.default_value is not None:
            ET.SubElement(
                state_variable_el,
                'defaultValue'
            ).text = str(state_variable.default_value)

        if state_variable.allowed_values:
            allowed_value_list = ET.SubElement(
                state_variable_el,
                'allowedValueList'
            )

            for value in state_variable.allowed_values:
                ET.SubElement(
                    allowed_value_list,
                    'allowedValue'
                ).text = str(value)

        # TODO: Add allowedValueRange

        return state_variable_el

    def _service_state_table_element(self):
        service_state_table = ET.Element('serviceStateTable')

        for (name, variable) in self._service.service_state_table.items():
            service_state_table.append(
                self._state_variable_element(name, variable)
            )

        return service_state_table

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
