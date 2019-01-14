import logging as logger

from Utilities import KennyLoggins
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path

from RESTClient import RESTClient

__author__ = 'ksmith'

_MI_APP_NAME = '_LONG_NAME_ REST Client Example'
_APP_NAME = '_BASE_APP_'

_SPLUNK_HOME = make_splunkhome_path([""])

kl = KennyLoggins()
log = kl.get_logger(_APP_NAME, "restclient", logger.INFO)

class _BASE_APP_RESTClient(RESTClient):
    # this must be updated to build the URL for the REST API
    # Example: Hostname = google.com, Endpoint = Maps, kwargs = { "query" : "blah" }
    # Returns: https://google.com/Maps?query=blah
    def _build_url(self, endpoint, **kwargs):
        kwargs = {"apikey": self.get_token()}
        self._log.info(kwargs)
        arguments = "?%s" % (urllib.urlencode(kwargs))
        return "https://%s/1/current.json%s" % (self._hostname, arguments)

    # For each action that you need to perform, read a url in this style.
    def some_pig(self, **kwargs):
        url = self._build_url("endpoint", **kwargs)
        self._log.info("URL: %s" % url)
        return self._read(url)


RC = _BASE_APP_RESTClient(_APP_NAME, {
    "auth":
        {"type": "token_url",
         "token": "<insert_token>"
         },
    "hostname": "api.meh.com",
    "verify_certificate": False
}

                          )


def run():
    try:
        # DO SOMETHING! ANYTHING!!!
        # RC._log.info("Not Instantiated")

        # Basic Auth
        # auth_type = basic
        # auth_username = <string>
        # auth_password = <string>

        # Token Auth
        # auth_type = token
        # auth_token = <string>
        # auth_authorization_string = "Bearer %s"

        # Token URL Auth (the token is in the url, not in the header)
        # auth_type = token_url
        # auth_token = <string>

        # Output Type
        # output_type = json, <string>
        # Any thing else just returns the response

        # Version
        # version = api_version // This is what is used in the sample _build_url function

        # Call a function to get stuff
        result = RC.some_pig()
        RC._log.info(result)

    except Exception, e:
        RC._log.error(e)


if __name__ == '__main__':
    run()
    sys.exit(0)
