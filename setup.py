from setuptools import setup
from setuptools import find_packages
import versioneer


setup(
    name='stationverification',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='This package is used to check data quality from EEW Stations',
    author='Jonathan Gosset, Hasan Issa',
    author_email='jonathan.gosset@canada.ca, Hasan.issa@nrcan-rncan.gc.ca',
    packages=find_packages(exclude=('tests')),
    package_data={
        'stationverification': [
            'data/*.txt',
            'data/*.ini',
            'data/*.jar',
            'data/*.xml'
        ]
    },
    install_requires=[
        'tables',
        'pandas==0.25.3',
        'obspy==1.2.2',
        'rpy2==3.1.0',
        'rdflib',
        'boto3',
        'numpy==1.19.5',
        'arrow',
        "pydantic",
        "Jinja2"
    ],
    extras_require={
        'dev': [
            'pytest'
        ]
    },
    entry_points={
        'console_scripts': [
            'stationverification = \
                stationverification.bin.stationverification:main',
            'stationverificationlatency = \
                stationverification.bin.stationverification_latency:main',
            'stationverificationCN = \
                stationverification.bin.stationverification_CN:main',
            'uploadreport = \
                stationverification.bin.upload_report_to_gitlab:main',
            'fetchStationXml = \
                stationverification.bin.fetch_station_xml:main',
            # These will not work with the current version of
            # stationverification, they will need refactoring
            # 'dailyverification = \
            #     stationverification.bin.dailyverification:main',
            # 'pushtonagios = \
            #     stationverification.bin.pushtonagios:main'
        ]
    }
)
