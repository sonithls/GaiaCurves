from astroquery.simbad import Simbad

def gaia_id(Obj_name):
    """ Returns Gaia id for objects available in SIMBAD"""
    list_id = Simbad.query_objectids(Obj_name, cache=False)
    for i in list_id['ID']:
        if i[0:8] == "Gaia DR2":
            print (i)
            gaia_id = i
    return gaia_id[5:]