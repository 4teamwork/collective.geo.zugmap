from Products.Five.browser import BrowserView
import requests


class ZugMapBase(BrowserView):

    def __init__(self, context, request):
        super(ZugMapBase, self).__init__(context, request)
        self.name = ""
        self.layer = ""
        self.style = ""
        self.matrixSet = ""

    def __call__(self):
        return self._get_layer_js()

    def _get_layer_js(self):
        js_string = '''
            function() {
                var name = `%s`;
                var layer = `%s`;
                var style = `%s`;
                var matrixSet = `%s`;
                var html = `%s`;

                var doc = new OpenLayers.Format.XML().read(html);
                var obj = new OpenLayers.Format.WMTSCapabilities().read(doc);

                var url_template = obj.contents.layers.find(
                    x => x.identifier === layer
                ).resourceUrls[0].template;

                var layer = new OpenLayers.Layer.WMTS({
                    name: name,
                    requestEncoding: "REST",
                    url: url_template,
                    layer: layer,
                    style: style,
                    matrixSet: matrixSet,
                    format: "image/png",
                    matrixIds: obj.contents.tileMatrixSets["zg"].matrixIds,
                    projection: new OpenLayers.Projection("EPSG:2056"),
                    tileSize: new OpenLayers.Size(512, 512),
                    'attribution': '<span style="color: white; background-color: #333;">Quelle: GIS Kanton Zug</span>'
                });

                return layer;
            }
            ''' % (self.name, self.layer, self.style, self.matrixSet, self._get_capabilities())
        return js_string

    def _get_capabilities(self):
        url = "https://services.geo.zg.ch/tc/wmts/1.0.0/WMTSCapabilities.xml"
        response = requests.get(url)
        return response.text


class ZugMapOrtsplan(ZugMapBase):
    def __init__(self, context, request):
        super(ZugMapOrtsplan, self).__init__(context, request)
        self.name = "Ortsplan des Kantons Zug"
        self.layer = "zg.ortsplan"
        self.style = "default"
        self.matrixSet = "zg"


class ZugMapOrthoPlus(ZugMapBase):
    def __init__(self, context, request):
        super(ZugMapOrthoPlus, self).__init__(context, request)
        self.name = "LuftbildPLUS"
        self.layer = "zg.luftbildplus"
        self.style = "default"
        self.matrixSet = "zg"
