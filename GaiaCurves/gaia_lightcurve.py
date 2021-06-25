from astroquery import gaia
from astroquery.simbad import Simbad
from astroquery.gaia import Gaia
import requests
import matplotlib.pyplot as plt
import os

def gaia_id(obj_name):
    """ Get Gaia ID for an object
    
    Returns Gaia id for objects available in SIMBAD
    
    Args:
        obj_name (string): String. Reference name of objects available in the SIMBAD catalog that we need the Gaia ID for.

    Returns:
        String. Gives back the Gaia ID of the object. Returns empty string if Gaia ID could not be fetched.
    """
    list_id = Simbad.query_objectids(obj_name, cache=False)
    if list_id == None:
        print('Gaia ID not found for given object')
        return ''
    for i in list_id['ID']:
        if i[0:8] == "Gaia DR2":
            gaia_id = i
    return gaia_id[5:].split()[1]

def fetch_lightcurve_dr2(gaia_id, output_dir='../data/'):
    """ Fetch Gaia Lightcurve for a Gaia Source ID (of a variable star) from Gaia DR2 Data Link
    
    Returns path of csv file stored for given source
    
    Args:
        gaia_id (string): String. Gaia Source ID of the variable star you need to fetch the lightcurve from DR1 for
        [output_dir] (string): Optional. String. By default, the csv files for the lightcurves are stored in the subfolder data/. To change the default path, enter a new path for the folder to save the lightcurve

    Returns:
        String. Gives back the path/to/lightcurve/filename.csv where the lightcurve is stored. Returns empty string if no lightcurve is fetched.
    """
    url='https://gea.esac.esa.int/data-server/data?ID=Gaia+DR2+'+gaia_id+'&RETRIEVAL_TYPE=EPOCH_PHOTOMETRY&FORMAT=CSV'
    save_path=output_dir+gaia_id+'_data.csv'
    read_data = requests.get(url, allow_redirects=True)
    if(len(read_data.content)==0):
        print('Could not fetch lightcurve from DR2 for Gaia Source ID '+gaia_id)
        return '' 
    #assert len(read_data.content)!=0, 'Could not fetch lightcurve from DR2 for Gaia Source ID '+gaia_id
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 
    open(save_path, 'wb').write(read_data.content)
    return save_path


def fetch_lightcurve_dr1(gaia_id, output_dir='../data/'):
    """ Fetch Gaia Lightcurve for a Gaia Source ID (of a variable star) from Gaia DR1 Data Link
    
    Returns path of csv file stored for given source
    
    Args:
        gaia_id (string): String. Gaia Source ID of the variable star you need to fetch the lightcurve from DR1 for
        [output_dir] (string): Optional. String. By default, the csv files for the lightcurves are stored in the subfolder data/. To change the default path, enter a new path for the folder to save the lightcurve

    Returns:
        String. Gives back the path/to/lightcurve/filename.csv where the lightcurve is stored. Returns empty string if no lightcurve is fetched.
    """
    save_path=output_dir+gaia_id+'_data.csv'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 
    query = 'select solution_id, source_id, observation_time, g_flux, g_flux_error, g_magnitude, \
            2.5/log(10)* g_flux_error/ g_flux AS g_magnitude_error, rejected_by_variability_processing AS rejected \
            FROM gaiadr1.phot_variable_time_series_gfov \
            WHERE source_id='+ gaia_id
    dr1_job = Gaia.launch_job_async(query, output_file=save_path, output_format='csv', dump_to_file=True)
    print('Loading DR1 lightcurve')
    while(dr1_job.is_finished()!=True):
        pass
    if(len(dr1_job.get_results())==0):
        os.remove(save_path)
        print('Could not fetch lightcurve from DR1 for Gaia Source ID '+gaia_id)
        return ''    
    #assert len(dr1_job.get_results())!=0, 'Could not fetch lightcurve from DR1 for Gaia Source ID '+gaia_id
    print('Loaded DR1 lightcurve')
    return save_path