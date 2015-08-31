__author__ = 'GTK'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

# from PyQt4.QtNetwork import *
# from PyQt4.QtXml import *
# from PyQt4.Qsci import *
import sys
import os

# Import our GUI
from shapeviewer_gui import Ui_MainWindow


# Environment variable QGISHOME must be set to the install directory
# before running the application
qgis_prefix = os.getenv("QGISHOME")


class ShapeViewer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.layers = []

        QMainWindow.__init__(self)

        # Required by Qt4 to initialize the UI
        self.setupUi(self)

        # Set the title for the app
        self.setWindowTitle("ShapeViewer")

        # Create the map canvas
        self.canvas = QgsMapCanvas()
        self.canvas.useImageToRender(False)
        self.canvas.show()

        # Lay our widgets out in the main window using a
        # vertical box layout
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        self.actionAddLayer = QAction(QIcon(
            "(qgis_prefix + ""/apps/Python27/Lib/site-packages/matplotlib-1.3.1-py2.7-win-amd64.egg/matplotlib/mpl-data/images/hand.png"),
                                      "Add Layer", self.frame)
        self.connect(self.actionAddLayer, SIGNAL("activated()"), self.addLayer)

        self.actionZoomIn = QAction(QIcon("(qgis_prefix + ""/zoom_to_rect.png"), "Zoom In", self.frame)
        self.connect(self.actionZoomIn, SIGNAL("activated()"), self.zoomIn)

        self.actionAggiungi = QAction(QIcon("(qgis_prefix + ""/zoom_to_rect.png"), "Aggiungi", self.frame)
        self.connect(self.actionAggiungi, SIGNAL("activated()"), self.aggiungi)

        self.toolbar = self.addToolBar("Map")
        # Add the actions to the toolbar
        self.toolbar.addAction(self.actionAddLayer)
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionAggiungi)
        # self.toolbar.addAction(self.actionZoomOut);
        # self.toolbar.addAction(self.actionPan);
        # self.toolbar.addAction(self.actionZoomFull);

        # Create the map tools
        # self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)  # false = in
        # self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out


        # layout is set - open a layer
        # Add an OGR layer to the map
        # file = QFileDialog.getOpenFileName(self,
        #               "Open Shapefile", ".", "Shapefiles (*.shp)")
        # fileInfo = QFileInfo(file)

        # Add the layer
        layer = QgsVectorLayer("C:/OSGeo4W64/APP/world_borders.shp", "world borders", "ogr")
        layer2 = QgsVectorLayer("C:/OSGeo4W64/APP/cities.shp", "cities", "ogr")

        QgsApplication.initQgis()
        # Show setting of parameters
        print QgsApplication.showSettings()

        if not layer.isValid():
            return

        # Change the color of the layer to gray
        # symbols = layer.renderer().symbols()
        # ymbol = symbols[0]
        # ymbol.setFillColor(QColor.fromRgb(192,192,192))

        # Add layer to the registry
        # QgsMapLayerRegistry.instance().addMapLayers([layer,layer2])

        QgsMapLayerRegistry.instance().addMapLayers([layer, layer2])

        # Set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())

        # Set up the map canvas layer set
        cl = QgsMapCanvasLayer(layer)
        cl2 = QgsMapCanvasLayer(layer2)
        self.layers = [cl2, cl]
        self.canvas.setLayerSet(self.layers)
        allLayers = self.canvas.layers()
        for i in allLayers: print i.name()

        # urlWithParams = 'url=http://vmap0.tiles.osgeo.org/wms/vmap0&format=image/png&layers=basic&styles='
        # layer = QgsRasterLayer(urlWithParams, 'MA-ALUS', 'wms')

        # QgsMapLayerRegistry.instance().addMapLayer(layer)

        self.canvas.setExtent(layer.extent())

        # Set up the map canvas layer set
        cl = QgsMapCanvasLayer(layer)
        cl2 = QgsMapCanvasLayer(layer2)
        self.layers = [cl2, cl]
        self.canvas.setLayerSet(self.layers)
        allLayers = self.canvas.layers()
        for i in allLayers: print i.name()
        # for field in layer2.pendingFields():
        # print field.name(), field.typeName()
        # layer.select(1)
        # print(layer.getFeatures().next())
        # print(layer.selectedFeaturesIds())
        # selected_features = layer.selectedFeatures()
        # for i in selected_features:
        # print(i.feature['CAT'])

        # iter = layer.getFeatures()
        # for feature in iter:
        # retrieve every feature with its geometry and attributes
        # fetch geometry
        # geom = feature.geometry()
        # print "Feature ID %d: " % feature.id()
        # print feature.attributes()

        # self.canvas.zoomScale(100000000)

        self.layer = layer2  # For MapTips
        self.layer.setDisplayField('NAME')
        self.createMapTips()

        symbols = layer2.rendererV2()
        print "Type:", symbols.type()

        symbol = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color': 'red'})
        layer2.rendererV2().setSymbol(symbol)
        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView()
        self.view.setModel(self.model)
        self.LegendDock = QDockWidget("Layers", self)
        self.LegendDock.setObjectName("layers")
        self.LegendDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.view)
        self.LegendDock.setContentsMargins(9, 9, 9, 9)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.LegendDock)
        # symbols = layer.rendererV2().symbols()
        # symbol = symbols[0]
        # symbol.setColor(QColor.fromRgb(50,250,250))

        # fetch attributes
        # attrs = feature.attributes()
        # print attrs
        # attrs is a list. It contains all the attribute values of this feature
        # print attrs

        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        # result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.sticazzi)

        self.canvas.setMapTool(self.clickTool)
        self.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.sticazzi)

    def sticazzi(self, point, button):
        print(QgsPoint(point.x(), point.y()))
        print(self.layer.dataProvider().capabilitiesString())

        caps = self.layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.AddFeatures:
            feat = QgsFeature(self.layer.pendingFields())
            feat.setAttribute(0, 'hello')
            feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(point.x(), point.y())))
            (res, outFeats) = self.layer.dataProvider().addFeatures([feat])
            self.canvas.refresh()

    def createMapTips(self):
        """ Create MapTips on the map """
        self.timerMapTips = QTimer(self.canvas)
        self.mapTip = QgsMapTip()
        self.connect(self.canvas, SIGNAL("xyCoordinates(const QgsPoint&)"),
                     self.mapTipXYChanged)
        self.connect(self.timerMapTips, SIGNAL("timeout()"),
                     self.showMapTip)

    def mapTipXYChanged(self, p):
        """ SLOT. Initialize the Timer to show MapTips on the map """
        if self.canvas.underMouse():  # Only if mouse is over the map
            # Here you could check if your custom MapTips button is active or sth
            self.lastMapPosition = QgsPoint(p.x(), p.y())
            self.mapTip.clear(self.canvas)
            self.timerMapTips.start(750)  # time in milliseconds

    def showMapTip(self):
        """ SLOT. Show  MapTips on the map """
        self.timerMapTips.stop()

        if self.canvas.underMouse():
            # Here you could check if your custom MapTips button is active or sth
            pointQgs = self.lastMapPosition
            pointQt = self.canvas.mouseLastXY()
            print("pointqgs:", pointQgs, " - pointqt: ", pointQt)
            self.mapTip.showMapTip(self.layer, pointQgs, pointQt,
                                   self.canvas)

    def addLayer(self):
        file = QFileDialog.getOpenFileName(self, "Open Shapefile", ".", "Shapefiles (*.shp)")
        fileInfo = QFileInfo(file)

        # Add the layer
        layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")

        if not layer.isValid():
            return

        # Change the color of the layer to gray
        symbols = layer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QColor.fromRgb(192, 192, 192))

        # Add layer to the registry
        QgsMapLayerRegistry.instance().addMapLayer(layer);

        # print(QgsMapCanvas.layers())
        # Set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())

        # Set up the map canvas layer set
        cl = QgsMapCanvasLayer(layer)
        # layers = [cl]
        # self.layers = self.canvas.mapRenderer().layerSet()
        self.layers.insert(0, QgsMapCanvasLayer(layer))
        self.canvas.setLayerSet(self.layers)

    # Set the map tool to zoom in
    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def aggiungi(self):
        # self.canvas.setMapTool(self.toolZoomIn)
        print("faicose")


        # geom = QgsGeometry()
        # feat = QgsFeature()
        # feat.setGeometry(geom.fromPoint(QgsPoint(12, 13)))
        # feat.setAttributes(['i', 'line'])
        # layer = QgsVectorLayer("C:/OSGeo4W64/APP/cities.shp", "cities", "ogr")
        # layer.addFeature(feat)

    # Set the map tool to zoom out
    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    # Set the map tool to
    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    # Zoom to full extent of layer
    def zoomFull(self):
        self.canvas.zoomFullExtent()


def main(argv):
    # create Qt application
    app = QApplication(argv)

    # Initialize qgis libraries
    QgsApplication.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
    QgsApplication.initQgis()

    # create main window
    wnd = ShapeViewer()
    # Move the app window to upper left
    wnd.move(100, 100)
    wnd.show()

    # run!
    retval = app.exec_()

    # exit
    QgsApplication.exitQgis()
    sys.exit(retval)


if __name__ == "__main__":
    main(sys.argv)
