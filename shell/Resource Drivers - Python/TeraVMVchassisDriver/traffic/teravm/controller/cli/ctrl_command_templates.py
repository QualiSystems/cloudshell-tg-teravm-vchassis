from collections import OrderedDict

from cloudshell.cli.command_template.command_template import CommandTemplate

from traffic.teravm.controller.exceptions import TestGroupDoesNotExist


LICENSE_SERVER_PORT = 5053
LICENSE_SERVER_WEB_INTERFACE_PORT = 5054
DEFAULT_ERROR_MAP = OrderedDict((("ERROR:", "Error happens while executing CLI command"),
                                 ("Could not check out the required", "Failed to acquire teravm license")))


def raise_test_group_exception(session, logger):
    """

    :param cloudshell.cli.session.session.Session:
    :param logging.Logger logger:
    :return:
    """
    raise TestGroupDoesNotExist()


def prepare_error_map(error_map=None):
    """

    :param collections.OrderedDict error_map:
    :rtype: collections.OrderedDict
    """
    if error_map is None:
        error_map = OrderedDict()

    error_map.update(DEFAULT_ERROR_MAP)
    return error_map


DELETE_TEST_GROUP = CommandTemplate("deleteTestGroup {test_group_name} -u {user}",
                                    action_map=OrderedDict(((r"[Tt]est [Gg]roup.*does not exist",
                                                             raise_test_group_exception),)),
                                    error_map=prepare_error_map())

IMPORT_TEST_GROUP = CommandTemplate("importTestGroup // {test_group_file} -u {user}",
                                    error_map=prepare_error_map())

START_TEST_GROUP = CommandTemplate("startTestGroup {test_group_name} -u {user}",
                                   error_map=prepare_error_map(OrderedDict(
                                       ((r"[Tt]est [Gg]roup.*does not exist", "Test Group does not exist. Be sure "
                                                                              "that you have loaded configuration"),
                                        (r"[Ss]ystem is already running", "Test Group was already started")))))

STOP_TEST_GROUP = CommandTemplate("stopTestGroup {test_group_name} -u {user}",
                                  error_map=prepare_error_map(OrderedDict(
                                      ((r"Cannot stop [Tt]est [Gg]roup as it is not currently running",
                                        "Cannot stop Test Group as it is not currently running"),
                                       (r"[Tt]est [Gg]roup.*does not exist", "Test Group does not exist. Be sure that "
                                                                             "you have loaded configuration")))))


SAVE_RESULTS = CommandTemplate("saveTestGroupHistoricalDetailedResults {test_group_name} {destination_file} -u {user}",
                               error_map=prepare_error_map(OrderedDict(
                                   ((r"[Tt]est [Gg]roup.*does not exist", "Test Group does not exist. Be sure that "
                                                                          "you have loaded configuration"),
                                    (r"There is no current or last run", "There are no stats available for Export. "
                                                                         "Be sure that you have started tests")))))

CONFIGURE_LICENSE_SERVER = CommandTemplate("configureTvmLicensing LicenseServer {license_server_ip} %s %s"
                                           % (LICENSE_SERVER_PORT, LICENSE_SERVER_WEB_INTERFACE_PORT),
                                           error_map=prepare_error_map())

REMOVE_FILE = CommandTemplate("rm {file_name}")
