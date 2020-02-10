from qtpy.QtCore import QSettings
from qtpy.QtGui import QIcon

from xicam.core import msg
from xicam.plugins.settingsplugin import ParameterSettingsPlugin
from xicam.gui.static import path


class LoggingSettingsPlugin(ParameterSettingsPlugin):
    """Settings plugin for logging information and parameterization.
    """
    def __init__(self):

        def msg_levels(recommended=""):
            """Returns a dictionary mapping logging level names to their respective integer values.

            Parameters
            ----------
            recommended
                Optional string which will mark a logging level as recommended (for use in the list parameter)
                (default is "", which will not mark any levels).

            Returns
            -------
                Dictionary that maps log level names to their values, optionally with one name marked as recommended.

            """
            levels = dict()#{v: k for k, v in msg.levels.items()}
            for level, level_name in msg.levels.items():
                if recommended and recommended == level_name:
                    levels[level_name + " (recommended)"] = level
                else:
                    levels[level_name] = level
            return levels

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
                # Allow users to configure the default log level for the xicam logger's FileHandler
                dict(
                    name="File Log Level",
                    values=msg_levels(recommended="DEBUG"),
                    value="DEBUG",
                    type="list",
                    tip="Changes how much information is logged to the log file in 'Log Directory.'"
                ),
                # Allow users to configure the default log level for the xicam logger's StreamHandler
                dict(
                    name="Terminal Log Level",
                    values={v: k for k, v in msg.levels.items()},
                    value="DEBUG",
                    type="list",
                    tip="Changes how much information is logged to the system console / terminal.",
                ),
            ],
        )
        msg.file_handler.setLevel(self["File Log Level"])
        msg.stream_handler.setLevel(self["Terminal Log Level"])

    def apply(self):
        msg.file_handler.setLevel(self["File Log Level"])
        msg.stream_handler.setLevel(self["Terminal Log Level"])
        QSettings().setValue(msg.FILE_LOG_LEVEL_SETTINGS_NAME, self["File Log Level"])
        QSettings().setValue(msg.STREAM_LOG_LEVEL_SETTINGS_NAME, self["Terminal Log Level"])
