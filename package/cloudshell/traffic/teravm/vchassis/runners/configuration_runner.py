from cloudshell.traffic.teravm.cli.ctrl_handler import TeraVMControllerCliHandler

from cloudshell.traffic.teravm.vchassis.flows.configure_license_server_flow import TeraVMConfigureLicenseServerFlow


class TeraVMConfigurationRunner(object):
    def __init__(self, cli, cs_api, resource_config, logger):
        """

        :param cloudshell.cli.cli.CLI cli: CLI object
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api: cloudshell API object
        :param traffic.teravm.controller.configuration_attributes_structure.TrafficGeneratorControllerResource resource_config:
        :param logging.Logger logger:
        """
        self._cli = cli
        self._cs_api = cs_api
        self._resource_config = resource_config
        self._logger = logger

    @property
    def cli_handler(self):
        """

        :rtype: TeraVMControllerCliHandler
        """
        return TeraVMControllerCliHandler(self._cli,
                                          self._resource_config,
                                          self._logger,
                                          self._cs_api)

    @property
    def configure_license_server_flow(self):
        """

        :rtype: TeraVMLoadConfigurationFlow
        """
        return TeraVMConfigureLicenseServerFlow(cli_handler=self.cli_handler,
                                                resource_config=self._resource_config,
                                                cs_api=self._cs_api,
                                                logger=self._logger)

    def configure_license_server(self, license_server_ip):
        """

        :param str license_server_ip:
        """
        return self.configure_license_server_flow.execute_flow(license_server_ip)
