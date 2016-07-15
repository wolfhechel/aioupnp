from aioupnp.service import Service, StateVariable, Action


def describe_service():

    class ExampleService(Service):

        TestVariable = StateVariable('i3')

        AnotherTestVariable = StateVariable('string')

        @Action
        def GetTestVariable(self) -> (('TestVariable', TestVariable), ):
            pass

        @Action
        def SetTestVariable(self, TestVariable: TestVariable):
            pass

    def action_sets_is_action():
        @Action
        def TestMethod():
            pass

        assert TestMethod._is_action == True

    def action_sets_in_args():
        assert tuple(ExampleService.GetTestVariable.in_args.keys()) == tuple()
        assert tuple(ExampleService.SetTestVariable.in_args.keys()) == ('TestVariable',)

    def action_sets_out_args():
        assert tuple(ExampleService.GetTestVariable.out_args.keys()) == ('TestVariable',)
        assert tuple(ExampleService.SetTestVariable.out_args.keys()) == tuple()

    def state_variable_name_returns_name_from_instance():
        assert ExampleService.state_variable_name(ExampleService.TestVariable) == 'TestVariable'

    def service_state_table_is_initialized_on_service_definition():
        assert tuple(ExampleService.service_state_table.keys()) == ('TestVariable', 'AnotherTestVariable')

    def action_list_is_initialized_on_service_definition():
        assert tuple(ExampleService.action_list.keys()) == ('GetTestVariable', 'SetTestVariable')