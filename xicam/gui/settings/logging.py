from qtpy.QtGui import QIcon

from xicam.core import msg
from xicam.plugins.settingsplugin import ParameterSettingsPlugin
from xicam.gui.static import path


class LoggingSettingsPlugin(ParameterSettingsPlugin):
    """Settings plugin for logging information and parameterization.
    """
    def __init__(self):
        super(LoggingSettingsPlugin, self).__init__(
            QIcon(str(path("icons/ellipsis.png"))),
            "Logging",
            [
                # Show users where the log directory is, don't let them modify it though
                dict(
                    name="Log Directory",
                    value=msg.log_dir,
                    type='str',
                    readonly=True,
                    tip="Location where Xi-CAM writes its logs to."),
                # Allow users to configure the default log level for the xicam logger's StreamHandler
                dict(
                    name="Log Level",
                    values={v: k for k, v in msg.levels.items()},
                    value="DEBUG",
                    type="list",
                    tip="How much information to output to the printed log messages (DEBUG gives the most information).",
                ),
            ],
        )
        msg.stream_handler.setLevel(self["Log Level"])

    def apply(self):
        msg.stream_handler.setLevel(self["Log Level"])
