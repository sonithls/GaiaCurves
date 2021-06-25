import pytest
import pandas as pd
from GaiaCurves import gaia_lightcurve

def test_gaia_id():
	""" 
	Unit test to evaluates the correctness of the gaia_id() function
	"""
	fetched_id=gaia_lightcurve.gaia_id('NQ Dra')
	assert fetched_id=='2154100169676165120', 'Incorrect ID returned for NQ Dra, Check function'

def test_gaia_id_null():
	""" 
	Unit test to evaluates the correctness of the gaia_id() function using a expected null output 
	"""
	fetched_id=gaia_lightcurve.gaia_id('gibberish')
	assert fetched_id=='', 'An ID returned when not expected. Check function'

def test_fetch_lightcurve_dr2():
	""" 
	Unit test to evaluates the correctness of the fetch_lightcurve_dr2() function
	"""
	save_path=gaia_lightcurve.fetch_lightcurve_dr2('2154100169676165120')
	lc=pd.read_csv(save_path)
	print(len(lc))
	assert len(lc)==84, "Unexpected length of the Lightcurve fetched from DR2, check function"

def test_fetch_lightcurve_dr1():
	""" 
	Unit test to evaluates the correctness of the fetch_lightcurve_dr1() function
	"""
	save_path=gaia_lightcurve.fetch_lightcurve_dr1('5284240582308398080')
	lc=pd.read_csv(save_path)
	print(len(lc))
	assert len(lc)==144, "Unexpected length of the Lightcurve fetched from DR1, check function"