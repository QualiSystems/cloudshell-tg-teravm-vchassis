from cloudshell.devices.standards.traffic.virtual.chassis.configuration_attributes_structure import \
    TrafficGeneratorVChassisResource


class TeraVMTrafficGeneratorVChassisResource(TrafficGeneratorVChassisResource):

    @property
    def api_user(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}API User".format(self.namespace_prefix), None)

    @property
    def api_password(self):
        """

        :rtype: string
        """
        return self.attributes.get("{}API Password".format(self.namespace_prefix), None)

    @property
    def tvm_comms_network(self):
        """TeraVM Comms Network Name

        :rtype: str
        """
        return self.attributes.get("{}TVM Comms Network".format(self.namespace_prefix), None)

    @property
    def tvm_mgmt_network(self):
        """TeraVM MGMT Network Name

        :rtype: str
        """
        return self.attributes.get("{}TVM MGMT Network".format(self.namespace_prefix), None)

    @property
    def executive_server(self):
        """TeraVM Executive Server IP

        :rtype: str
        """
        return self.attributes.get("{}Executive Server".format(self.namespace_prefix), None)
