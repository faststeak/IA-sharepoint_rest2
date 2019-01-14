Aplura Modular Input Module
====

So, you need a Modular Input? Let's make sure.
Does your input:
1. Need to be configurable via the UI?
1. Have multiple inputs with different sources?
1. Run on a Heavy Forwarder?

If you answered yes to these questions, then you need a Modular Input! Lucky for you, we just happen to have one ready to go!

Files in this folder
----

- app_mi.py
    - This is a sample Modular Input file. The name of this file MUST match the name of the stanza in the `inputs.conf.spec`. 
- inputs.conf.spec
    - This is a sample `inputs.conf.spec` file for  you to use. Place it in `$APP_HOME/README` and edit the parameters to what you need.
- ModularInput.py
    - This is the ModularInput Class. Import it, and then instantiate a new object. See below for details!
- ModularInputTests.py
    - This contains the unit tests to validate the ModularInput class. You probably don't need to worry about it.
- README.md
    - You are reading it. Right now. In English. "What" ain't no language I've ever heard of!
    
So how do I use it?
-----

We are going to make some assumptions. 

PROXY SUPPORT
------

If Proxy Support using the RESTClient module is required, add an input "proxy_id" to the `inputs.conf.spec` and use the utilities to pull the proxy configuration.


Modular Input Methods
----

| Method Name | Arguments | Description |
| --- | --- | --- | 
| thise | none | that |