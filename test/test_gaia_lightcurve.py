import pytest
import pandas as pd
from GaiaCurves import gaia_lightcurve as gc


def test_gaia_id():
	""" 
	Unit test to evaluate the correctness of the gaia_id() function
	"""
	fetched_id=gc.gaia_id('NQ Dra')
	assert fetched_id=='2154100169676165120', 'Incorrect ID returned for NQ Dra, Check function'

def test_gaia_id_null():
	""" 
	Unit test to evaluate the correctness of the gaia_id() function using a expected null output 
	"""
	fetched_id=gc.gaia_id('gibberish')
	assert fetched_id=='', 'An ID returned when not expected. Check function'

def test_fetch_lightcurve_dr2():
	""" 
	Unit test to evaluate the correctness of the fetch_lightcurve_dr2() function
	"""
	save_path=gc.fetch_lightcurve_dr2('2154100169676165120')
	lc=pd.read_csv(save_path)
	print(len(lc))
	assert len(lc) == 84, "Unexpected length of the Lightcurve fetched from DR2, check function"


def test_fetch_lightcurve_dr1():
	""" 
	Unit test to evaluate the correctness of the fetch_lightcurve_dr1() function
	"""
	save_path=gc.fetch_lightcurve_dr1('5284240582308398080')
	lc=pd.read_csv(save_path)
	print(len(lc))
	assert len(lc)==144, "Unexpected length of the Lightcurve fetched from DR1, check function"

def test_fetch_curves():
	""" 
	Unit test to evaluate the correctness of the fetch_curves() function
	"""
	table=gc.fetch_curves(['NQ Dra', 'gibberish'])
	match_table={'NQ Dra': {'ID': '2154100169676165120', 'pathname': '../data/2154100169676165120_data_dr2.csv', 'source': 'DR2'}, 'gibberish': {'ID': 'N/A', 'pathname': 'N/A', 'source': 'N/A'}}
	assert table==match_table, "Unexpected results received, check function"

def test_end_to_end():
	""" 
	End-to-end test to evaluate the correctness of the gaia_lightcurve module
	"""
	table=gc.fetch_curves(['OGLE LMC570.29.005418'], ignore='DR2')
	abs_lc=pd.read_csv(table['OGLE LMC570.29.005418']['pathname'])
	test_lc=pd.read_csv('test/end_to_end_test.csv')
	assert abs_lc['observation_time'].all()==test_lc['observation_time'].all(), "Time from ground truth does not match, check module"
	assert abs_lc['g_magnitude'].all()==test_lc['g_magnitude'].all(), "Magnitude from ground truth does not match, check module"
