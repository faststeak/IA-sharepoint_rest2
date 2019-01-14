import unittest


class UtilitiesTestCase(unittest.TestCase):
    def setUp(self):
        return True

    def _fail(self, step, function, message=None):
        return "action=failed step=%s function=%s message=\"%s\"" % (step, function, message)
