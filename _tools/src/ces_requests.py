import requests as r
import json
from urllib.parse import urlencode
from envelope import Envelope

def query_ces_dados(envelope : Envelope) -> dict:

    geometry = {
        "spatialReference" : {"latestWkid" : 29192, "wkid" : 29182},
        "xmin":envelope.left,
        "ymin":envelope.bottom,
        "xmax":envelope.right,
        "ymax":envelope.top
    }

    q_params = {
        "extent":{"spatialReference":{"latestWkid":29192,"wkid":29182},
                  "xmin":envelope.left,
                  "ymin":envelope.bottom,
                  "xmax":envelope.right,
                  "ymax":envelope.top},
                  "mode":"view",
                  "originPosition":"upperLeft",
                  "tolerance":1.1943285669555674}

    payload = {
        'where' : '1=1',
        'outFields' : '*',
        "f": "json",
        "outSR" : 29182,
        "geometry": json.dumps(geometry),
        "maxRecordCountFactor":3,
        "quantizationParameters" : json.dumps(q_params),
        "resultType" : "tile",
        "spatialRel":"esriSpatialRelIntersects",
        "geometryType" : "esriGeometryEnvelope",
        "inSR" : 29182,
    }

    url = "https://www.copel.com/cesweb/proxy.jsp?https://www.copel.com/arcgis/rest/services/CES/CES_Dados/MapServer/0/query?"
    request_url = url + urlencode(payload)

    request = r.get(request_url, timeout=20)

    try:
        query_as_json = json.loads(request.text)
    except:
        return "-> could not parse response to json format"

    return query_as_json

def query_ces_postes_transf(envelope : Envelope) -> dict:

    geometry = {
        "spatialReference" : {"latestWkid" : 29192, "wkid" : 29182},
        "xmin":envelope.left,
        "ymin":envelope.bottom,
        "xmax":envelope.right,
        "ymax":envelope.top
    }

    q_params = {
        "extent":{"spatialReference":{"latestWkid":29192,"wkid":29182},
                  "xmin":envelope.left,
                  "ymin":envelope.bottom,
                  "xmax":envelope.right,
                  "ymax":envelope.top},
                  "mode":"view",
                  "originPosition":"upperLeft",
                  "tolerance":1.1943285669555674}

    payload = {
        'where' : '1=1',
        'outFields' : '*',
        "f": "json",
        "outSR" : 29182,
        "geometry": json.dumps(geometry),
        "maxRecordCountFactor":3,
        "quantizationParameters" : json.dumps(q_params),
        "resultType" : "tile",
        "spatialRel":"esriSpatialRelIntersects",
        "geometryType" : "esriGeometryEnvelope",
        "inSR" : 29182
    }

    url = "https://www.copel.com/cesweb/proxy.jsp?https://www.copel.com/arcgis/rest/services/CES/postes_transferencia/MapServer/0/query?"
    request_url = url + urlencode(payload)

    try:
        request = r.get(request_url, timeout=10)
        #print(request.status_code)
        query_as_json = json.loads(request.text)
        return query_as_json
    except:
        return {'error' : "-> could not finish the request"}
    
if __name__ == "__main__":

    envelope = Envelope(7181139.263564575,7180780.964994488,669682.0867694629,669145.8332428999)
    response = query_ces_dados(envelope)
    with open('ces_response.txt', "w") as file:
        file.write(json.dumps(response))

