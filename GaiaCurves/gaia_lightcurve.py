from astroquery.simbad import Simbad

def gaia_id(obj_name):
    """ Get Gaia ID for an object
    
    Returns Gaia id for objects available in SIMBAD
    
    Args:
        obj_name (string): String. Reference name of objects available in the SIMBAD catalog
        that we need the Gaia ID for.

    Returns:
        String. Gives back the Gaia ID of the object
    """
    list_id = Simbad.query_objectids(Obj_name, cache=False)
    for i in list_id['ID']:
        if i[0:8] == "Gaia DR2":
            print (i)
            gaia_id = i
    return gaia_id[5:]


def gaia_fetch(obj_id):
    