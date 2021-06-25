from setuptools import setup, find_packages, Extension
import numpy


def get_requires():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs


setup(
    name='GaiaCurves',
    version='1.0.0',
    description='GaiaCurves! Light curves of variable stars from Gaia',
    url='https://github.com/sonithls/GaiaCurves',
    author='',
    author_email='',
    license='MIT',
    packages=find_packages(),
    include_dirs=[numpy.get_include()],
    include_package_data = True,
    zip_safe=False,
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. 
        'Programming Language :: Python :: 3.7',
        ],
    keywords='Gaia Lightcurve',
    install_requires=get_requires()
    )