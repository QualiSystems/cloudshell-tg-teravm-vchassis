import re

# from traffic.teravm.controller import constants


class TrafficGeneratorControllerResource(object):
    def __init__(self, address=None, test_user=None, shell_name=None, attributes=None):
        """

        :param str address: IP address of the resource
        :param str shell_name: shell name
        :param str test_user: shell name
        :param dict[str, str] attributes: attributes of the resource
        """
        self.address = address
        self.test_user = test_user
        self.attributes = attributes or {}

        if shell_name:
            self.namespace_prefix = "{}.".format(shell_name)
        else:
            self.namespace_prefix = ""

    @property
    def user(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}User".format(self.namespace_prefix), None)

    @property
    def password(self):
        """

        :rtype: string
        """
        return self.attributes.get("{}Password".format(self.namespace_prefix), None)

    @property
    def cli_connection_type(self):
        """

        :rtype: str
        """
        return "SSH"
        # return self.attributes.get("{}CLI Connection Type".format(self.namespace_prefix), None)

    @property
    def cli_tcp_port(self):
        """

        :rtype: str
        """
        return 22
        # return self.attributes.get("{}CLI TCP Port".format(self.namespace_prefix), None)

    @property
    def sessions_concurrency_limit(self):
        """

        :rtype: float
        """
        return 1
        # return self.attributes.get("{}Sessions Concurrency Limit".format(self.namespace_prefix), 1)
    #
    # @property
    # def test_files_location(self):
    #     """
    #
    #     :rtype: float
    #     """
    #     return self.attributes.get("{}Test Files Location".format(self.namespace_prefix), "")

    # @staticmethod
    # def get_test_user(reservation_id):
    #     """Get valid test username based on reservation id
    #
    #     :param str reservation_id:
    #     :return:
    #     """
    #     return re.sub("[^0-9a-zA-Z]", "", reservation_id)[:32]

    # @staticmethod
    # def get_chassis_model(cs_api, reservation_id):
    #     """
    #
    #     :param cs_api:
    #     :param reservation_id:
    #     :return:
    #     """
    #     for resource in cs_api.GetReservationDetails(reservationId=reservation_id).ReservationDescription.Resources:
    #         if resource.ResourceModelName in constants.CHASSIS_MODELS:
    #             return resource
    #
    #     raise Exception("Unable to find {} model in the current reservation".format(constants.CHASSIS_MODELS))

    @classmethod
    def from_context(cls, context):
        """

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :return:
        """
        return cls(address=context.resource.address, attributes=dict(context.resource.attributes))

    # @classmethod
    # def create_from_chassis_resource(cls, context, cs_api):
    #     """Create an instance of TrafficGeneratorControllerResource from the given context
    #
    #     :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
    #     :param cs_api:
    #     :rtype: TrafficGeneratorControllerResource
    #     """
    #     reservation_id = context.reservation.reservation_id
    #     chassis_resource = cls.get_chassis_model(cs_api=cs_api, reservation_id=reservation_id)
    #     test_user = cls.get_test_user(reservation_id)
    #
    #     return cls(address=chassis_resource.FullAddress,
    #                test_user=test_user,
    #                attributes=dict(context.resource.attributes))
