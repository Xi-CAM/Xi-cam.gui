# -*- coding: utf-8 -*-
from functools import WRAPPER_ASSIGNMENTS
from pyqtgraph import ImageView, InfiniteLine, mkPen, ScatterPlotItem, ImageItem, PlotItem
from qtpy.QtGui import QTransform, QPolygonF
from qtpy.QtWidgets import QLabel, QErrorMessage, QSizePolicy, QPushButton
from qtpy.QtCore import Qt, Signal, Slot, QSize, QPointF, QRectF
import numpy as np
# from pyFAI.geometry import Geometry
from xicam.gui.widgets.elidedlabel import ElidedLabel
from xicam.gui.widgets.ROI import BetterPolyLineROI
from xicam.core import msg
import enum


# from pyFAI import AzimuthalIntegrator


# NOTE: PyQt widget mixins have pitfalls; note #2 here: http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/

# NOTE: PyFAI geometry position vector is: x = up
#                                          y = right
#                                          z = beam

# TODO: Add notification when qgrid is very wrong

def q_from_angles(phi, alpha, wavelength):
    r = 2 * np.pi / wavelength
    qx = r * np.sin(phi) * np.cos(alpha)
    qy = r * np.cos(phi) * np.sin(alpha)
    qz = r * (np.cos(phi) * np.cos(alpha) - 1)

    return np.array([qx, qy, qz])


def alpha(x, y, z):
    return np.arctan2(y, z)


def phi(x, y, z):
    return np.arctan2(x, z)


class DisplayMode(enum.Enum):
    raw = enum.auto
    cake = enum.auto
    remesh = enum.auto


class PixelSpace(ImageView):
    def __init__(self, *args, **kwargs):
        # Add axes
        self.axesItem = PlotItem()
        self.axesItem.axes['left']['item'].setZValue(10)
        self.axesItem.axes['top']['item'].setZValue(10)
        if 'view' not in kwargs: kwargs['view'] = self.axesItem

        self._transform = QTransform()

        super(PixelSpace, self).__init__(*args, **kwargs)

        self.imageItem.sigImageChanged.connect(self.updateAxes)

    def transform(self, img=None):
        # Build Quads
        shape = np.squeeze(img).shape
        a = [(0, shape[0] - 1),
             (shape[1] - 1, shape[0] - 1),
             (shape[1] - 1, 0),
             (0, 0)]

        b = [(0, 0),
             (shape[1] - 1, 0),
             (shape[1] - 1, shape[0] - 1),
             (0, shape[0] - 1)]

        quad1 = QPolygonF()
        quad2 = QPolygonF()
        for p, q in zip(a, b):
            quad1.append(QPointF(*p))
            quad2.append(QPointF(*q))

        transform = QTransform()
        QTransform.quadToQuad(quad1, quad2, transform)

        for item in self.view.items:
            if isinstance(item, ImageItem):
                item.setTransform(transform)
        self._transform = transform
        return img, transform

    def setImage(self, img, *args, **kwargs):
        if img is None: return

        if not kwargs.get('transform', None):
            img, transform = self.transform(img)
            self.updateAxes()
            super(PixelSpace, self).setImage(img, *args, transform=transform, **kwargs)

        else:
            super(PixelSpace, self).setImage(img, *args, **kwargs)

    def setTransform(self):
        self.setImage(self.imageItem.image)  # this should loop back around to the respective transforms

    def updateAxes(self):
        self.axesItem.setLabel('bottom', u'x (px)')  # , units='s')
        self.axesItem.setLabel('left', u'z (px)')


class QSpace(PixelSpace):
    def __init__(self, *args, geometry=None, **kwargs):
        self.displaymode = DisplayMode.raw

        super(QSpace, self).__init__(*args, **kwargs)

        self._geometry = None  # type: AzimuthalIntegrator
        self.setGeometry(geometry)

    def setGeometry(self, geometry):
        if callable(geometry):
            geometry = geometry()
        self._geometry = geometry
        self.setTransform()


class EwaldCorrected(QSpace):
    def setDisplayMode(self, mode):
        self.displaymode = mode
        self.setTransform()

    def transform(self, img):
        if not self._geometry: return super(QSpace, self).transform(img)  # Do pixel space transform when not calibrated

        from camsaxs import remesh_bbox
        img, q_x, q_z = remesh_bbox.remesh(np.squeeze(img), self._geometry, reflection=False, alphai=None)

        # Build Quads
        shape = img.shape
        a = 0, shape[0] - 1
        b = shape[1] - 1, shape[0] - 1
        c = shape[1] - 1, 0
        d = 0, 0

        quad1 = QPolygonF()
        quad2 = QPolygonF()
        for p, q in zip([a, b, c, d], [a, b, c, d]):  # the zip does the flip :P
            quad1.append(QPointF(*p))
            quad2.append(QPointF(q_x[q[::-1]], q_z[q[::-1]]))

        transform = QTransform()
        QTransform.quadToQuad(quad1, quad2, transform)

        for item in self.view.items:
            if isinstance(item, ImageItem):
                item.setTransform(transform)
        self._transform = transform

        return img, self._transform

    def setImage(self, img, *args, **kwargs):
        if img is None: return

        if self._geometry:
            img, transform = self.transform(img)
            self.axesItem.setLabel('bottom', u'q_x (Å⁻¹)')  # , units='s')
            self.axesItem.setLabel('left', u'q_z (Å⁻¹)')
            super(QSpace, self).setImage(img, *args, transform=transform, **kwargs)

        else:
            super(QSpace, self).setImage(img, *args, **kwargs)


class CenterMarker(QSpace):

    def __init__(self, *args, **kwargs):
        self.centerplot = ScatterPlotItem(brush='r')
        self.centerplot.setZValue(100)

        super(CenterMarker, self).__init__(*args, **kwargs)

        self.addItem(self.centerplot)
        self.drawCenter()

    def drawCenter(self):
        try:
            fit2d = self._geometry.getFit2D()
        except (TypeError, AttributeError):
            pass
        else:
            x = 0  # fit2d['centerX']
            y = 0  # fit2d['centerY']
            self.centerplot.setData(x=[x], y=[y])

    def setGeometry(self, geometry):
        super(CenterMarker, self).setGeometry(geometry)
        self.drawCenter()


class Crosshair(ImageView):
    def __init__(self, *args, **kwargs):
        super(Crosshair, self).__init__(*args, **kwargs)
        linepen = mkPen('#FFA500')
        self._vline = InfiniteLine((0, 0), angle=90, movable=False, pen=linepen)
        self._hline = InfiniteLine((0, 0), angle=0, movable=False, pen=linepen)

        self._vline.setVisible(False)
        self._hline.setVisible(False)

        self.addItem(self._vline)
        self.addItem(self._hline)

        self.scene.sigMouseMoved.connect(self.moveCrosshair)

    def moveCrosshair(self, pos):
        if self.view.getViewBox().sceneBoundingRect().contains(pos):
            mousePoint = self.view.getViewBox().mapSceneToView(pos)
            x, y = mousePoint.x(), mousePoint.y()

            if self.imageItem.mapRectToView(self.imageItem.boundingRect()).contains(mousePoint):  # within bounds
                self._vline.setPos(x)
                self._hline.setPos(y)
                self._hline.setVisible(True)
                self._vline.setVisible(True)
            else:
                self._hline.setVisible(False)
                self._vline.setVisible(False)


class PixelCoordinates(PixelSpace):
    def __init__(self, *args, **kwargs):
        super(PixelCoordinates, self).__init__(*args, **kwargs)

        self._coordslabel = QLabel(u"<div style='font-size:12pt;background-color:#111111; "
                                   u"text-overflow: ellipsis; width:100%;'>&nbsp;</div>")

        # def sizeHint():
        #     sizehint = QSize(self.ui.graphicsView.width()-10, self._coordslabel.height())
        #     return sizehint
        # self._coordslabel.sizeHint = sizeHint
        self._coordslabel.setSizePolicy(QSizePolicy.Ignored,
                                        QSizePolicy.Ignored)  # TODO: set sizehint to take from parent, not text
        self.ui.gridLayout.addWidget(self._coordslabel, 2, 0, 1, 1, alignment=Qt.AlignHCenter)

        self.scene.sigMouseMoved.connect(self.displayCoordinates)

    def displayCoordinates(self, pos):
        if self.view.sceneBoundingRect().contains(pos):
            mousePoint = self.view.getViewBox().mapSceneToView(pos)
            pos = QPointF(mousePoint.x(), mousePoint.y())

            if self.imageItem.mapRectToView(self.imageItem.boundingRect()).contains(mousePoint):  # within bounds
                # angstrom=QChar(0x00B5)
                pxpos = self.imageItem.mapFromView(pos)

                self.formatCoordinates(pxpos, pos)
            else:
                self._coordslabel.setText(u"<div style='font-size:12pt;background-color:#111111;'>&nbsp;</div>")

    def formatCoordinates(self, pxpos, pos):
        """
        when the mouse is moved in the viewer, recalculate coordinates
        """

        try:
            I = self.imageItem.image[int(pxpos.y()), int(pxpos.x())]
        except IndexError:
            I = 0

        self._coordslabel.setText(f"<div style='font-size: 12pt;background-color:#111111; "
                                  f"text-overflow: ellipsis; width:100%;'>"
                                  f"x={pxpos.x():0.1f}, "
                                  f"<span style=''>y={self.imageItem.image.shape[0] - pxpos.y():0.1f}</span>, "
                                  f"<span style=''>I={I:0.0f}</span></div>")


class QCoordinates(QSpace):
    def formatCoordinates(self, pxpos, pos):
        """
        when the mouse is moved in the viewer, recalculate coordinates
        """

        try:
            I = self.imageItem.image[int(pxpos.y()), int(pxpos.x())]
        except IndexError:
            I = 0
        self._coordslabel.setText(f"<div style='font-size: 12pt;background-color:#111111; "
                                  f"text-overflow: ellipsis; width:100%;'>"
                                  f"x={pxpos.x():0.1f}, "
                                  f"<span style=''>y={self.imageItem.image.shape[0] - pxpos.y():0.1f}</span>, "
                                  f"<span style=''>I={I:0.0f}</span>, "
                                  f"q={np.sqrt(pos.x() ** 2 + pos.y() ** 2):0.3f} \u212B\u207B\u00B9, "
                                  f"q<sub>z</sub>={pos.y():0.3f} \u212B\u207B\u00B9, "
                                  f"q<sub>\u2225</sub>={pos.x():0.3f} \u212B\u207B\u00B9, "
                                  f"d={2 * np.pi / np.sqrt(pos.x() ** 2 + pos.y() ** 2) * 10:0.3f} nm, "
                                  f"\u03B8={np.rad2deg(np.arctan2(pos.y(), pos.x())):.2f}&#176;</div>")


class BetterButtons(ImageView):
    def __init__(self, *args, **kwargs):
        super(BetterButtons, self).__init__(*args, **kwargs)

        # Setup axes reset button
        self.resetAxesBtn = QPushButton('Reset Axes')
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resetAxesBtn.sizePolicy().hasHeightForWidth())
        self.resetAxesBtn.setSizePolicy(sizePolicy)
        self.resetAxesBtn.setObjectName("resetAxes")
        self.ui.gridLayout.addWidget(self.resetAxesBtn, 2, 1, 1, 1)
        self.resetAxesBtn.clicked.connect(self.autoRange)

        # Setup LUT reset button
        self.resetLUTBtn = QPushButton('Reset LUT')
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resetLUTBtn.sizePolicy().hasHeightForWidth())
        # self.resetLUTBtn.setSizePolicy(sizePolicy)
        # self.resetLUTBtn.setObjectName("resetLUTBtn")
        self.ui.gridLayout.addWidget(self.resetLUTBtn, 2, 2, 1, 1)
        self.resetLUTBtn.clicked.connect(self.autoLevels)

        # Hide ROI button and rearrange
        self.ui.roiBtn.setParent(None)
        self.ui.menuBtn.setParent(None)
        # self.ui.gridLayout.addWidget(self.ui.menuBtn, 1, 1, 1, 1)
        self.ui.gridLayout.addWidget(self.ui.graphicsView, 0, 0, 2, 1)


class PolygonROI(ImageView):
    def __init__(self, *args, **kwargs):
        super(PolygonROI, self).__init__(*args, **kwargs)
        rect = self.imageItem.boundingRect()  # type: QRectF
        positions = [(rect.bottomLeft().x(), rect.bottomLeft().y()),
                     (rect.bottomRight().x(), rect.bottomRight().y()),
                     (rect.topRight().x(), rect.topRight().y()),
                     (rect.topLeft().x(), rect.topLeft().y())]
        self._roiItem = BetterPolyLineROI(positions=positions, closed=True, scaleSnap=True, translateSnap=True)
        self.addItem(self._roiItem)

    def poly_mask(self, shape=None, ):
        if not shape: shape = self.imageItem.image.shape
        # return self._roiItem.renderShapeMask(*shape)
        result, mapped = self._roiItem.getArrayRegion(np.ones_like(self.imageItem.image), self.imageItem, returnMappedCoords=True)

        # TODO -- move this code to own function and test
        # Pad result mask rect into bounding rect of mask and image
        floorX = np.floor(mapped[0]).astype(int)
        floorY = np.floor(mapped[1]).astype(int)

        # TODO TEMP
        from matplotlib import pyplot as plt

        plt.figure('image (origin=lower)')
        plt.imshow(self.imageItem.image, origin='lower')

        plt.figure('initial result (origin=lower)')
        plt.imshow(result, origin='lower')
        # plt.figure('floor(mapped[0]')
        # plt.imshow(floorX)
        # plt.figure('floor(mapped[1]')
        # plt.imshow(floorY)
        # END TODO TEMP

        # Return empty mask if ROI bounding box does not intersect image bounding box
        resultRect = QRectF(QPointF(np.min(floorX), np.min(floorY)), QPointF(np.max(floorX), np.max(floorY)))
        if not self._intersectsImage(resultRect):
            return np.zeros(shape)

        width = self.imageItem.width()
        height = self.imageItem.height()
        roiMinX = np.min(floorX)
        roiMaxX = np.max(floorX)
        roiMinY = np.min(floorY)
        roiMaxY = np.max(floorY)
        maxX = max(roiMaxX, width - 1)
        minX = min(roiMinX, 0)
        maxY = max(roiMaxY, height - 1)
        minY = min(roiMinY, 0)

        # bounding_box_height = maxY - minY
        # bounding_box_width = maxX - minX

        # Any negative values where the mask dimension outside of the image indicates 0 padding
        yBefore = int(minY)
        yBeforePadding = int(abs(np.min(floorY)))
        if yBefore < 0:
            yBeforePadding = 0

        yAfter = int(height - maxY - 1)
        yAfterPadding = int(height - abs(np.max(floorY)) - 1)
        if yAfter < 0:
            yAfterPadding = 0

        xBefore = int(minX)
        xBeforePadding = int(abs(np.min(floorX)))
        if xBefore < 0:
            xBeforePadding = 0

        xAfter = int(width - maxX - 1)
        xAfterPadding = int(width - abs(np.max(floorX)) - 1)
        if xAfter < 0:
            xAfterPadding = 0

        # assert(y_after_offset - y_before_offset + 1 == height)
        # assert(x_after_offset - x_before_offset + 1 == width)

        bounding_box = np.pad(result, ((xAfterPadding, xBeforePadding), (yAfterPadding, yBeforePadding)), 'constant')

        plt.figure('bounding_box, origin="lower"')
        plt.imshow(bounding_box, origin='lower')

        # Trim off mask that does not intersect with the image
        rowSliceLower = int(abs(xBefore))
        rowSliceUpper = width - xBefore
        colSliceLower = int(abs(yBefore))
        colSliceUpper = height - yBefore
        trimmed = bounding_box[rowSliceLower:rowSliceUpper, colSliceLower:colSliceUpper]
        # trimmed[roiMinX:roiMaxX+1, roiMinY:roiMaxY+1]
        # TODO TEMP
        plt.figure(f'trimmed, origin="lower"; slice -- {rowSliceLower}:{rowSliceUpper}, {colSliceLower}:{colSliceUpper}')
        plt.imshow(trimmed, origin='lower')
        plt.show()
        # END TODO TEMP
        return trimmed


    def _intersectsImage(self, roiRect : QRectF):
        return self.imageItem.boundingRect().intersects(roiRect)

        # if ((x_coord[0] >= 0 or x_coord[0] <= width) or (x_coord[1] >= 0 or x_coord[1] <= width)) \
        #     and ((y_coord[0] >= 0 or y_coord[1] <= height) or (y_coord[1] >= 0 or y_coord[1] >= height)):
        #     return True
        # return False


