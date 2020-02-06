from collections import OrderedDict
from qtpy.QtCore import Qt
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
                    tip="Location where Xi-CAM writes its log files.",
                ),
            ],
        )

    @property
    def widget(self):
        tree = super(LoggingSettingsPlugin, self).widget
        log_dir_param = tree.findItems("Log Directory", Qt.MatchContains | Qt.MatchRecursive)
        if log_dir_param:
            log_dir_param = log_dir_param[0]
            log_dir_param.textBox.setText("blah")
        return tree

