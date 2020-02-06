from collections import OrderedDict
from qtpy.QtGui import QIcon

from xicam.core.msg import log_dir
from xicam.plugins.settingsplugin import ParameterSettingsPlugin
from xicam.gui.static import path


class LoggingSettingsPlugin(ParameterSettingsPlugin):
    def __init__(self):
        super(LoggingSettingsPlugin, self).__init__(
            QIcon(str(path("icons/ellipsis.png"))),
            "Logging",
            [
                dict(
                    name="Log Directory",
                    value=log_dir,
                    type="text",
                    readonly=True,
                    tip="Location where Xi-CAM writes its log files."
                ),
            ],
        )
