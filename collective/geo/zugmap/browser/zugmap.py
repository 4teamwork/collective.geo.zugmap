from Products.Five.browser import BrowserView
import requests


class ZugMap(BrowserView):
    def __call__(self):
        js_string = '''
            function() {
                var html = `%s`;
                var doc = new OpenLayers.Format.XML().read(html);
                var obj = new OpenLayers.Format.WMTSCapabilities().read(doc);

                /* https://github.com/Safecast/GeoSense/blob/master/public/lib/openlayers/OpenLayers-2.13.1/tests/Layer/WMTS.html */
                var layer = new OpenLayers.Layer.WMTS({
                    name: "Ortsplan des Kantons Zug",
                    requestEncoding: "REST",
                    url: "https://services.geo.zg.ch/tc/wmts",
                    layer: "zg.ortsplan",
                    style: "default",
                    matrixSet: "zg",
                    format: "image/png",
                    matrixIds: obj.contents.tileMatrixSets["zg"].matrixIds,
                    'attribution': '<span style="color: white; background-color: #333;">Quelle: GIS Kanton Zug</span>'
                });

                return layer;
            }
            ''' % (self._get_capabilities())
        return js_string

    def _get_capabilities(self):
        url = "https://services.geo.zg.ch/tc/wmts/1.0.0/WMTSCapabilities.xml"
        response = requests.get(url)
        return response.text
