Aplura REST Client Module
====

So, you need a REST Client? Let's make sure.
Does your input:
1. Need to be configurable via the UI?
1. Connect to an API?
1. Need Proxy Support?

If you answered yes to these questions, then you need a REST CLIENT! Lucky for you, we just happen to have one ready to go!

Files in this folder
----

- app_rc.py
    - This is a sample REST Client file.
- RESTClient.py
    - This is the RESTClient Class. Import it, and then instantiate a new object. See below for details!
- RESTClientTests.py
    - This contains the unit tests to validate the RESTClient class. You probably don't need to worry about it.
- README.md
    - You are reading it. Right now. In English. "What" ain't no language I've ever heard of!
    
So how do I use it?
-----

We are going to make some assumptions. 


RESTClient Instantiation
----
To use the RESTClient module, you need to extend the base class, and then instantiate it in your script. The constructor takes a JSON object to configure the client.


```python
class SampleRESTClient(RESTClient):
    def _build_url(self, endpoint):
        return "https://%s/%s" % (self._hostname, endpoint)
        
    def _call(self, endpoint, **kwargs):
        payload = self._payload(**kwargs)
        url = self._build_url(endpoint)
        return self._read(url, payload=payload)

    def get_incidents(self, **kwargs):
        return self._call("incidents", **kwargs)

RC = SampleRESTClient("myAppName", {
            "auth":
                {"type": "token",
                 "token": MI.get_config("token"),
                 "authorization_string": "%s"
                 },
            "proxy":
                {
                    "host": "localhost",
                    "port": "8080",
                    "useSSL" : False
                    "authentication":
                        {
                            "username": "username",
                            "password": "password"
                        }
                },
            "hostname": MI.get_config("hostname"),
            "verify_certificate": False
        })
```


Constructor Arguments
------
|JSON Object Parent | Key | Option | Description |
| --- | --- | --- | 
| root | auth |  `<object>` | This base object will define how authentication to the REST API is configured. |
| root | hostname | `<string>` | This is the hostname for the API |
| root | verify_certificate | `<boolean>` | This flag will either verify the SSL certificate, or ignore any errors in Certs, and just connect | 
| root | proxy | `<object>` | This object will configure proxy support. See the `proxy` settings below |
| auth| type | `token_url` | This type of authentication includes the token in the URL of the request. THIS NEEDS TO BE SET IN THE `_build_url` OVERRIDDEN METHOD!! |
| auth | type | `token` | This type of authentication will include the defined token in the `Authentication` header, formatted using the `authorization_string` setting.  |
| auth | token | `<string>` | This is the token to use with either `token` or `token_url` authentication types |
| auth | authorization_string | `<python_string>` | An authorization string for the header. The `%s` will be replaced with the token string. Example: `Bearer %s`
| proxy | host | `<string>` | This setting will tell the client which Proxy host to use. |
| proxy | port | `<string>` | This setting will tell the client which Proxy port to use. |
| proxy | useSSL | `<boolean>` | This setting will set the flag to either use SSL (https) or not use SSL (http) |
| proxy | authentication | `<object>` | If the proxy is authenticated, make sure to set this object. If not included, No Authentication will take place. |
| proxy:authentication | username | `<string>` | The username for the proxy |
| proxy:authentication | password | `<string>` | The password for the proxy |