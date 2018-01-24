from datetime import datetime
from datetime import timedelta
import time

from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_cli
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from traffic.teravm.controller.configuration_attributes_structure import TrafficGeneratorControllerResource


from traffic.teravm.chassis.client import TeraVMClient
from traffic.teravm.deployment.runners.configuration_runner import TeraVMConfigurationRunner

ASSOCIATED_MODELS = ["TeraVM Module"]
ATTR_NUMBER_OF_PORTS = "Number of Ports"
ATTR_OWNER_CHASSIS = "Virtual Traffic Generator Chassis"
EXC_ATTRIBUTE_NOT_FOUND = "Expected resource model {0} to have attribute '{1}' but did not find it"
SSH_SESSION_POOL = 1
SERVICE_STARTING_TIMEOUT = 30 * 60


class TeraVMVchassisDriver(ResourceDriverInterface):
    def __init__(self):
        """ Constructor must be without arguments, it is created with reflection at run time """
        self._cli = None

    def initialize(self, context):
        """

        :param InitCommandContext context: the context the command runs on
        """
        self._cli = get_cli(SSH_SESSION_POOL)
        return "Finished initializing"

    def configure_device_command(self, context, resource_cache):
        """Configure Virtual Chassis

        :param ResourceCommandContext context: the context the command runs on
        :type resource_cache: str
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Configure device command started')

        with ErrorHandlingContext(logger):
            # tvm_client = TeraVMClient(address=resource_config.address, port=int(resource_config.port))
            tvm_api_client = TeraVMClient(address=context.resource.address)
            timeout_time = datetime.now() + timedelta(seconds=SERVICE_STARTING_TIMEOUT)

            while not tvm_api_client.check_if_service_is_deployed():
                if datetime.now() > timeout_time:
                    raise Exception("TeraVM Controller service haven't been started within {} minute(s)"
                                    .format(SERVICE_STARTING_TIMEOUT/60))

                time.sleep(10)

            executive_server_ip = "192.168.42.193"

            tvm_api_client.configure_executive_server(executive_server_ip)

            license_server_ip = "192.168.122.244"

            cs_api = get_api(context)

            resource_config = TrafficGeneratorControllerResource.from_context(context=context)

            configuration_operations = TeraVMConfigurationRunner(resource_config=resource_config,
                                                                 cli=self._cli,
                                                                 cs_api=cs_api,
                                                                 logger=logger)

            configuration_operations.configure_license_server(license_server_ip=license_server_ip)

    def get_inventory(self, context):
        """Discovers the resource structure and attributes.

        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Get Inventory command started')

        return AutoLoadDetails([], [])

    def cleanup(self):
        """ Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """

        pass


if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = '192.168.42.158'

    user = 'cli'
    password = 'diversifEye'
    port = 443
    scheme = "https"
    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'TVM Chassis'
    context.resource.fullname = 'TeraVM Chassis'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = 'b18fb3d1-5f08-4002-9cf2-c519ac3edfa6'
    context.resource.attributes = {}
    context.resource.attributes['User'] = user
    context.resource.attributes['Password'] = password
    context.resource.address = address

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.48"

    dr = TeraVMVchassisDriver()


    with mock.patch('__main__.get_api') as get_api:
        get_api.return_value = type('api', (object,), {
            'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        dr.initialize(context)

        # out = dr.get_inventory(context)
        #
        # for xx in out.resources:
        #     print xx.__dict__
        #

        out = dr.configure_device_command(context, "")

        print(out)