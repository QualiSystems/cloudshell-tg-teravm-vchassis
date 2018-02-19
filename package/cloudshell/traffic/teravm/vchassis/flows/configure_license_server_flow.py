from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor

from cloudshell.traffic.teravm.cli import ctrl_command_templates


class TeraVMConfigureLicenseServerFlow(object):
    def __init__(self, cli_handler, resource_config, cs_api, logger):
        """

        :param traffic.teravm.controller.cli.ctrl_handler.TeraVMControllerCliHandler cli_handler:
        :param traffic.teravm.controller.configuration_attributes_structure.TrafficGeneratorControllerResource resource_config:
        :param logging.Logger logger:
        """
        self._cli_handler = cli_handler
        self._resource_config = resource_config
        self._cs_api = cs_api
        self._logger = logger

    def execute_flow(self, license_server_ip):
        """

        :param str license_server_ip:
        :return:
        """
        with self._cli_handler.get_cli_service(self._cli_handler.cli_mode) as cli_session:
            command = CommandTemplateExecutor(cli_service=cli_session,
                                              command_template=ctrl_command_templates.CONFIGURE_LICENSE_SERVER)

            command.execute_command(license_server_ip=license_server_ip)
