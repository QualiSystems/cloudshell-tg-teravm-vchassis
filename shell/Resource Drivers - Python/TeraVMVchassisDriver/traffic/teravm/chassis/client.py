import httplib

import requests


class TeraVMClient(object):
    def __init__(self, address, user=None, password=None, scheme="https", port=443, verify_ssl=False):
        """
        :param str address: controller IP address
        :param str user: controller username
        :param str password: controller password
        :param str scheme: protocol (http|https)
        :param int port: controller port
        :param bool verify_ssl: whether SSL cert will be verified or not
        """
        self._base_url = "{}://{}:{}".format(scheme, address, port)
        # self._auth = HTTPBasicAuth(username=user, password=password)
        self._auth = None
        self._headers = {"Accept": "application/vnd.cobham.v1+json"}
        self._verify_ssl = verify_ssl

    def _do_get(self, path, raise_for_status=True, **kwargs):
        """Basic GET request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        resp = requests.get(url=url, auth=self._auth, headers=self._headers, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_post(self, path, raise_for_status=True, **kwargs):
        """Basic POST request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        resp = requests.post(url=url, auth=self._auth, headers=self._headers, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_put(self, path, raise_for_status=True, **kwargs):
        """Basic PUT request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        resp = requests.put(url=url, auth=self._auth, headers=self._headers, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def _do_delete(self, path, raise_for_status=True, **kwargs):
        """Basic DELETE request client method

        :param str path: path for the request
        :param dict kwargs: additional kwarg that would be passed to the requests lib
        :rtype: requests.Response
        """
        url = "{}/{}".format(self._base_url, path)
        kwargs.update({"verify": self._verify_ssl})
        resp = requests.delete(url=url, auth=self._auth, headers=self._headers, **kwargs)
        raise_for_status and resp.raise_for_status()
        return resp

    def check_if_service_is_deployed(self, logger):
        """

        :return:
        """
        try:
            resp = self._do_get(path="v1/legacy-ui/ui/index.html", raise_for_status=False)
        except requests.exceptions.ConnectionError:
            return False

        if resp.status_code == httplib.OK and "executive management ip" in resp.content.lower():
            return True

    def configure_executive_server(self, ip_addr):
        """"""
        data = {
            "executiveMachineIP": ip_addr
        }

        resp = self._do_post(path="v1/legacy-ui/application/settings/executive-ip", data=data)
        return resp

    def get_modules_info(self):
        """Get test modules and ports information

        :return:
        """
        response = self._do_get(path="v1/poolmanager/testModules")
        data = response.json()

        return data["testModules"]
