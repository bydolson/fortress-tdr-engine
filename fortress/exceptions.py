"""Custom exceptions used by fortress

Error handling in fortress is done via exceptions. In this file we define a
variety of exceptions.

There is FortressError which every other exception should subclass so that it is
distinguished from other kind of exceptions not raised explicitly by fortress code.

The rule of thumb is that there should be as many exceptions are there are
errors. Feel free to create a new exception when an existing one doesn't quite
fit the purpose.

All exceptions should be named CamelCase and always use the Error suffix.
"""

import traceback


class FortressError(Exception):
    """All custom fortress exceptions should subclass this one.

    When printed, this class will always print its default message plus
    the message provided during exception initialization, if provided.

    """
    msg = "Fortress Error"
    code = -1

    def __init__(self, msg=None, exc=None):
        if exc is None and isinstance(msg, Exception):
            msg, exc = repr(msg), msg
        self.orig_exc = exc if isinstance(exc, Exception) else None
        self.orig_traceback = traceback.format_exc()
        msg = "%s: %s" % (self.msg, msg) if msg is not None else self.msg
        super(FortressError, self).__init__(msg)


class ModuleLoadError(FortressError):
    msg = "Error loading module"
    code = 1


class DetectorNotFoundError(FortressError):
    msg = "Anomaly detector not found"
    code = 2


class TimefieldNotFoundError(FortressError):
    msg = "Timefield not found in data"
    code = 3


class SensorsNotFoundError(FortressError):
    msg = "Selected sensors not found in data"
    code = 4


class mongoConnectionError(FortressError):
    msg = "Cannot connect to mongo"
    code = 5


class KibanaConfigNotFoundError(FortressError):
    msg = "Kibana config index not found in mongo"
    code = 6
