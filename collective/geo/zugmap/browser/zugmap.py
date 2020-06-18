from Products.Five.browser import BrowserView
import requests


class ZugMap(BrowserView):
    def __call__(self):
        js_string = '''
            function() {
                /* https://github.com/Safecast/GeoSense/blob/master/public/lib/openlayers/OpenLayers-2.13.1/tests/Layer/WMTS.html */
                /* https://github.com/Safecast/GeoSense/blob/19d4c01999a06c061a94f7d9a6c98d2916e44526/public-build/lib/openlayers/OpenLayers-2.13.1/tests/Layer/WMTS.html#L205-L214 */

                var html = `%s`;
                var doc = new OpenLayers.Format.XML().read(html);
                var obj = new OpenLayers.Format.WMTSCapabilities().read(doc);

                var wmts_layer = "zg.ortsplan";
                var url_template = obj.contents.layers.find(
                    x => x.identifier === wmts_layer
                ).resourceUrls[0].template;

                var layer = new OpenLayers.Layer.WMTS({
                    name: "Ortsplan des Kantons Zug",
                    requestEncoding: "REST",
                    url: url_template,
                    layer: wmts_layer,
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
