import folium
import tempfile
import dtcc_io as io
from pathlib import Path

def view(citymodel_pb):
    tmp_geojson = tempfile.NamedTemporaryFile(suffix=".geojson",delete=False)
    outpath = Path(tmp_geojson.name)
    io.save_citymodel(citymodel_pb, outpath)
    bounds = io.citymodel.building_bounds(outpath)
    print(bounds)
    m = folium.Map()
    m.fit_bounds([(bounds[1],bounds[0]),(bounds[3],bounds[2])])
    
    with open(outpath, "r") as f:
        cm_geojson = f.read()
    cm_layers =  folium.GeoJson(cm_geojson).add_child(folium.GeoJsonPopup(fields=['id','height','error'],aliases=['UUID','Height','Error']))  
    m.add_child(cm_layers)
    tmp_geojson.close()
    outpath_dir = outpath.parent
    outpath.unlink()
    try:
        outpath_dir.rmdir()
    except OSError:
        pass


    return m



