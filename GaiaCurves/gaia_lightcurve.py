from astroquery.simbad import Simbad
from astroquery.gaia import Gaia
import requests
import matplotlib.pyplot as plt
import os
import warnings
import pandas as pd

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
    save_path=output_dir+gaia_id+'_data_dr2.csv'
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
    """ Fetch Gaia Lightcurve for a Gaia Source ID (of a variable star) from Gaia DR1 Table (phot_variable_time_series_gfov)
    
    Returns path of csv file stored for given source
    
    Args:
        gaia_id (string): String. Gaia Source ID of the variable star you need to fetch the lightcurve from DR1 for
        [output_dir] (string): Optional. String. By default, the csv files for the lightcurves are stored in the folder ../data/. To change the default path, enter a new path for the folder to save the lightcurve

    Returns:
        String. Gives back the path/to/lightcurve/filename.csv where the lightcurve is stored. Returns empty string if no lightcurve is fetched.
    """
    save_path=output_dir+gaia_id+'_data_dr1.csv'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 
    query = 'select solution_id, source_id, observation_time, g_flux, g_flux_error, g_magnitude, \
            2.5/log(10)* g_flux_error/ g_flux AS g_magnitude_error, rejected_by_variability_processing AS rejected \
            FROM gaiadr1.phot_variable_time_series_gfov \
            WHERE source_id='+ gaia_id
    dr1_job = Gaia.launch_job_async(query, output_file=save_path, output_format='csv', dump_to_file=True)
    #print('Loading DR1 lightcurve')
    while(dr1_job.is_finished()!=True):
        pass
    if(len(dr1_job.get_results())==0):
        os.remove(save_path)
        print('Could not fetch lightcurve from DR1 for Gaia Source ID '+gaia_id)
        return ''    
    #assert len(dr1_job.get_results())!=0, 'Could not fetch lightcurve from DR1 for Gaia Source ID '+gaia_id
    #print('Loaded DR1 lightcurve')
    return save_path

def fetch_curves(starList, output_dir='../data/', ignore=None, ):
    """ Fetch Gaia Lightcurves for a list of variable stars from Gaia DR2 and DR1 Sources
    
    Returns a dictionary of Gaia IDs, saved photometric CSV paths, and sources for all the given variable star names
    
    Args:
        starList (list): List of strings. Variable star names (Cepheids and RRLyrae stars) to fetch lightcurves from Gaia  
        [output_dir](string): Optional. String. By default, the csv files for the lightcurves are stored in the folder ../data/. To change the default path, enter a new path for the folder to save the lightcurve
        [ignore] (string): Optional. String. Takes values None, DR1 and DR2. By default, the lightcurves are downloaded from both DR2 and DR1. To change ignore a source, specify DR1 or DR2.

    Returns:
        Dictionary. Gives back the path/to/lightcurve/filename.csv as pathname, Gaia ID as id, and DR1 or DR2 as source for star names as Keys.
    """
    assert len(starList)>=1, "Add atleast one star to the list to search for light curves"
    ids=[]
    pathnames=[]
    sources=[]
    id=''
    pathname=''
    source=''
    for i, star in enumerate(starList):
        id=gaia_id(star)
        if(id!=''):
            if(ignore!='DR2'):
                pathname=fetch_lightcurve_dr2(id, output_dir)
                source='DR2'
            elif(ignore!='DR1' and pathname==''):
                pathname=fetch_lightcurve_dr1(id, output_dir)
                source='DR1'
            if(pathname!=''):
                ids.append(id)
                pathnames.append(pathname)
                sources.append(source)
            else:
                ids.append(id)
                pathnames.append('N/A')
                sources.append('N/A')
        else:
            ids.append('N/A')
            pathnames.append('N/A')
            sources.append('N/A')
    results={}
    for i, star in enumerate(starList):
        results[star] = {'ID':ids[i], 'pathname':pathnames[i], 'source':sources[i]}
    return results

def plot_lightcurve(csv_path, star, id):
    """ Plot the Gaia light curve for a given .csv file generated by fetch_curves function.
    
    Args:
        csv_path (string): String. Path to the generated .csv file. 
        star (string): String. Takes the star name for visualization
        id (string): String. Takes the Gaia ID for the star for visualization

    Returns:
        None   
    """
    df = pd.read_csv(csv_path)

    if csv_path.endswith('dr1.csv'):
        y_upper = df.g_magnitude.max()
        y_lower = df.g_magnitude.min()
        
        plt.figure(1, (8, 6))
        plt.scatter(df.observation_time, df.g_magnitude, s=50, c='green', edgecolors='black', alpha=0.6, label='G')
        plt.errorbar(df.observation_time, df.g_magnitude, df.g_magnitude_error, c='green', ls='')
        plt.legend()
        plt.ylim(y_lower-0.5, y_upper+0.5)
        plt.gca().invert_yaxis()
        plt.xlabel("Observation Time [Barycentric JD in TCB - 2455197.5 (day)]", size=11)
        plt.ylabel("Mag", size=11)
        plt.title(r'Light curve for DR1 source ' + ' '+ star + ' (Gaia ID: '+ id + ')', size=12)
        plt.show()

    elif csv_path.endswith('dr2.csv'):
        df_G = df.loc[df['band'] == 'G']
        df_BP = df.loc[df['band'] == 'BP']
        df_RP = df.loc[df['band'] == 'RP']

        y_upper = max(df_G.mag.max(), df_BP.mag.max(), df_RP.mag.max())
        y_lower = min(df_G.mag.min(), df_BP.mag.min(), df_RP.mag.min())

        plt.figure(1, (8, 6))
        plt.scatter(df_G.time, df_G.mag, s=50, c='green', edgecolors='black', alpha=0.6, label='G')
        plt.plot(df_G.time, df_G.mag, c='green', lw=0.1)
        plt.scatter(df_BP.time, df_BP.mag, s=50, c='blue', edgecolors='black', alpha=0.6, label='BP')
        plt.plot(df_BP.time, df_BP.mag, c='blue', lw=0.1)
        plt.scatter(df_RP.time, df_RP.mag, s=50, c='red', edgecolors='black', alpha=0.6, label='RP')
        plt.plot(df_RP.time, df_RP.mag, c='red', lw=0.1)
        plt.legend()
        plt.ylim(y_lower-0.5, y_upper+0.5)
        plt.gca().invert_yaxis()
        plt.xlabel("Time [Barycentric JD in TCB - 2455197.5 (day)]", size=11)
        plt.ylabel("Mag", size=11)
        plt.title(r'Light curve for DR2 source' + ' ' + star + ' (Gaia ID: '+ id + ')', size=12)
        plt.show()

    else:
        print('Valid .csv not found.')

warnings.filterwarnings("ignore")
