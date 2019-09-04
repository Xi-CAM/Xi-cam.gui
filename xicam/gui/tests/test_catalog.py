from qtpy.QtWidgets import QLabel
from xicam.plugins import GUIPlugin, GUILayout
from pyqtgraph import ImageView


class TestPlugin(GUIPlugin):
    name = 'catalogtest'

    def __init__(self):
        self.imageview = ImageView()

        self.stages = {'Stage 1': GUILayout(self.imageview), }

        super(TestPlugin, self).__init__()

    def appendCatalog(self, runcatalog, **kwargs):
        print(runcatalog)

    def appendHeader(self):
        ...
