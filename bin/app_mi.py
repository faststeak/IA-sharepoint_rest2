import logging as logger

from Utilities import KennyLoggins
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path

from ModularInput import ModularInput

__author__ = 'ksmith'

_MI_APP_NAME = '_LONG_NAME_ Modular Input'
_APP_NAME = '_BASE_APP_'

_SPLUNK_HOME = make_splunkhome_path([""])

kl = KennyLoggins()
log = kl.get_logger(_APP_NAME, "modularinput", logger.INFO)

class _BASE_APP_ModularInput(ModularInput):
    def __init__(self, **kwargs):
        ModularInput.__init__(self, **kwargs)

    def _validate_arguments(self, val_data):
        """
        :param val_data: The data that requires validation.
        :return:
        RAISE an error if the arguments do not validate correctly. The default is just "True".
        """
        return True


MI = _BASE_APP_ModularInput(app_name=_APP_NAME, scheme={
    "title": "_LONG_NAME_",
    "description": "_LONG_DESC_",
    "args": [
        {"name": "hostname",
         "description": "description",
         "title": "Title",
         "required": False
         }
    ]
})


def run():
    MI.start()
    try:
        # DO SOMETHING! ANYTHING!!!
        MI.log.info("Not Instantiated")

        # Maybe pull some stuff from an API?
        # from _BASE_APP__API import _BASE_APP__API
        # apiObject = _BASE_APP__API(api_version="v1")

        # Need a checkpoint? Have a key, if no value, current time that the checkpoint was loaded will be used.
        # MI.get_checkpoint("my_key")
        # do stuff with checkpoint
        # MI.set_checkpoint("my_key")
        # OR MI.set_checkpoint("my_key",value) where value = "now" (for now), or any thing else that can be used.....

        # How to event?
        # Like This: MI.print_event("some pig")

        # Array of Objects to print?
        # Like This: MI.print_multiple_events( [ "object_1", "object_2" ] )


    except Exception, e:
        MI.print_error(e)
    MI.stop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            MI.scheme()
        elif sys.argv[1] == "--validate-arguments":
            MI.validate_arguments()
        elif sys.argv[1] == "--test":
            print 'No tests for the scheme present'
        else:
            print 'You giveth weird arguments'
    else:
        run()

    sys.exit(0)
