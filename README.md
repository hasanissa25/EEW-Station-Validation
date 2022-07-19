# Station Verification of Data Quality with Ispaq
This program is designed to run IRIS's System for Portable Assessment of Quality (ISPAQ) to gather statistics about data quality new Stations for the Earthquake Early Warning system.


Note: ispaq can be very resource intensive. During testing with a 6 channel station over a 10 day period, it was observed to use almost 2 GB of RAM. If ispaq seems to end abruptly without any visible error, it may have been stopped by oom_killer.

# Install Instructions for Centos 7/8
First you must install ispaq as a package.

Install the required packages with Yum.

```
    sudo yum install -y epel-release

    sudo yum install -y python3 python3-pip git
```

For Centos 8 only, some of the rependancy packages for R are missing from the yum repository, so install using dnf.

```
    sudo dnf --enablerepo=powertools install openblas-devel
    
    sudo dnf --enablerepo=powertools install texinfo-tex
```

Install the rest of the required packages

```
    sudo yum install -y python3-devel libcurl-devel libxml2-devel R
```

Clone custom version of ISPAQ from Bitbucket. This version of ISPAQ has modifications to allow it to function more effectively in the Verification Facility. For a list of changes, read the Customizations section in the [README](http://bitbucket.seismo.nrcan.gc.ca/users/jgosset/repos/ispaq/browse/README.md) file.

```
    mkdir ispaq

    git clone http://bitbucket.seismo.nrcan.gc.ca/scm/~jgosset/ispaq.git
```

Install required python packages with pip. 

```
    pip3 install numpy==1.19.5 pandas==0.25.3 obspy==1.2.2 rpy2==3.1.0 --user
```

Install ispaq 

```
    pip3 install ./ispaq/ --user

    ispaq -I
```
If prompted to create a user namespace: yes

Once ISPAQ is installed, the Station Verification package can be downloaded, configured and installed.

```
    mkdir stationverification

    git clone http://bitbucket.seismo.nrcan.gc.ca/users/jgosset/repos/station-validation
```
Default config files will be located in the package at ./stationverification/data and can be modified pre-installation, or copies can be made to override the default. Configuration files will be covered in the next section.

Once any required configuration is complete, install the package.
```
    pip3 install ./station_validation
```

# Configuration
Within ./stationverification/data there is a few default config files that can be modified before install or used as templates for config files to be used at runtime.

### eew_preferences.txt
The preference file used by ISPAQ. The file is self-documenting, and additional information can be found in the ISPAQ [README](http://bitbucket.seismo.nrcan.gc.ca/users/jgosset/repos/ispaq/browse/README.md) file. An instance of this file is configured automatically at run time. The only option that should be changed would be the list of metrics in the line starting with 'eew_test'.

### config.ini
This file contains preferences for the stationverification cmdline tools. The first section in this file, [thresholds], contains the thresholds for the possible metrics that the script can check. The comments in the file describe the specific scope of each threshold.

The second section of this file, [nagios], describes preferences for the cmdline tool _pushtonagios_ which is used to push results to a Nagios Server's nrdp API to populate. The preferences in this section include __nagios__, the url for the Nagios NRDP api, __token__, the API token to send with the push request, and __metrics__, a list of metrics for which to try and push results to Nagios.

### stationTXX6.conf
This is a sample Station Config file. When running the _stationverification_ cmdline tool, a station config file must be used to generate station Metadata and response information for ISPAQ. The sample included contains metadata for test station TXX6, and must be modified for the intended station.

The main section of this file is the [metadata] section, which contains network and stations codes, coordinates, install date and a list of channels the station has. This information is used to determine the target station for populate a temporary station xml file for ISPAQ to use.

There should also be an additional section for each channel in the list from the previous section. For each, the sample rate is required, as well as one of two options for instrument response. The first option is to specify the [NRL](https://docs.obspy.org/master/packages/obspy.clients.nrl.html) __sensor_keys__ and __datalogger_keys__. These keys are used to retrieve response information from the Nominal Response Library. The keys represent the configuration of the datalogger and instrument used for the specific channel, and the order of the keys and what they represent can differ from device to device. To determine the keys for a device it's recommended to explore the [NRL](http://ds.iris.edu/NRL/) archive. The second option for instruments that don't have response information in the NRL is to specify a __response_path__. Instruments like the Guralp Fortimus allow you to download the response file directly from the device itself, and this should be the absolute path to the specific RESP file corresponding to the channel.
If using the --FDSNWS option to use an FDSN Web Service for metadata, the channel-specific sections are not required. 

# Usage

This package contained three command line tools that are described here.

## stationverification
```
usage: stationverification [-h] -c STATIONCONFIG -d STARTDATE -e ENDDATE
                           [-i ISPAQLOCATION] [-M METRICS]
                           [-P PREFERENCE_FILE] [-L LOGFILE] [-v]
                           [-t THRESHOLDS] [-l HDF5] [-f FDSNWS]
                           [-o OUTPUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  -c STATIONCONFIG, --stationconfig STATIONCONFIG
                        Path to the file that contains station information.
  -d STARTDATE, --startdate STARTDATE
                        The first date of the verification period. Must be in
                        YYYY-MM-DD format
  -e ENDDATE, --enddate ENDDATE
                        The end of the verification period. Data will be
                        tested for each day from the start date up to but not
                        including the end date. Must be in YYYY-MM-DD format.
  -i ISPAQLOCATION, --ispaqlocation ISPAQLOCATION
                        Specifies the path or alias for the ispaq cmdline
                        tool. Default: ispaq
  -M METRICS, --metrics METRICS
                        Select the group of metrics from the ispaq preference
                        file to run with. Default: eew_test
  -P PREFERENCE_FILE, --preference_file PREFERENCE_FILE
                        Overrides the default ispaq config file.
  -L LOGFILE, --logfile LOGFILE
                        To log to a file instead of stdout, specify the
                        filename.
  -v, --verbose         Sets logging level to DEBUG.
  -t THRESHOLDS, --thresholds THRESHOLDS
                        Overrides the default config file.
  -l HDF5, --HDF5 HDF5  The directory containing HDF5 sniffwave archive.
                        Default: /data/sniffwave
  -f FDSNWS, --fdsnws FDSNWS
                        FDSN webservice URL to use. If not specified, then
                        --stationconfig must be specified to generate station
                        metadata for Ispaq
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Output directory to store results in. If none is
                        specified, the current directory is used.
```
Typical usage with only the required arguments might look something like
```
stationverification -d 2021-07-10 -e 2021-07-12 -c ../stationTXX6.conf
```
Dates should be in the YYYY-MM-DD format.

Ispaq will generate metrics for dates up to but not including the end date.
Latency metrics are generated from HDF5 files created by the [pysniffwave](http://bitbucket.seismo.nrcan.gc.ca/projects/EEW/repos/pysniffwave/browse) utility, and SOH metrics are generated by reading the miniseed files representing the SOH channels.

Once metrics are generated from ispaq, the results will be parsed and compared to the configured thresholds. The results are packaged in JSON format, which is stored in a tarball with the generated PSD plots under the name NETWORK.STATION_STARDATE-ENDATE_validation.tgz.

## dailyverification

```
usage: dailyverification [-h] [-i ISPAQLOCATION] [-P PREFERENCE_FILE]
                         [-L LOGFILE] [-v] [-t THRESHOLDS] [-l HDF5]
                         [-a ARCHIVE] [-f FDSNWS] [-o OUTPUTDIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -i ISPAQLOCATION, --ispaqlocation ISPAQLOCATION
                        If ispaq is not installed as a package, specify the
                        location of run_ispaq.py Default: ispaq
  -P PREFERENCE_FILE, --preference_file PREFERENCE_FILE
                        Declare what ISPAQ preference file to use when running
                        ISPAQ. Default is eew_preferences.txt. Default:
                        /home/jgosset/.local/lib/python3.7/site-
                        packages/stationverification/data/eew_preferences.txt
  -L LOGFILE, --logfile LOGFILE
                        To log to a file instead of stdout, specify the
                        filename.
  -v, --verbose         Sets logging level to DEBUG
  -t THRESHOLDS, --thresholds THRESHOLDS
                        The path to the preference file containing the
                        thresholds to test the metrics against. Default:
                        /home/jgosset/.local/lib/python3.7/site-
                        packages/stationverification/data/config.ini
  -l HDF5, --HDF5 HDF5  The directory containing HDF5 sniffwave files.
                        Default: /data/sniffwave
  -a ARCHIVE, --archive ARCHIVE
                        The path to the miniseed archive. Default:
                        /data/miniseed
  -f FDSNWS, --fdsnws FDSNWS
                        Specity a FDSNWS to use for waveform data instead of a
                        miniseed archive.
  -o OUTPUTDIRECTORY, --outputdirectory OUTPUTDIRECTORY
                        The directory to archive daily verification reports.
                        Default: ./dailyverification
```
This specialized tool will do a one-day verification for the previous day on every station in the archive. The purpose of these daily verifications is so that the results can be pushed to nagios to be used as services. It uses a dummy stationxml file for metadata that should allow for any station in the XX, CN or QW network, so no station config files are required to generate metadata. It only performs checks of basic stats so no response information is required. A json will be generated for each station and stored in the outputdirectory, in a year/month/day supdirectory structure.

## pushtonagios
```
usage: pushtonagios [-h] [-a ARCHIVEPATH] [-n NAGIOSURL] [-t TOKEN]
                    [-c NAGIOS_CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -a ARCHIVEPATH, --archivepath ARCHIVEPATH
                        The path to the archived verification reports.
  -n NAGIOSURL, --nagiosurl NAGIOSURL
                        Overrides the default URL for the Nagios nrdp server
                        to push results to. Defaults are stored in config.ini
  -t TOKEN, --token TOKEN
                        Overrides the Nagios API token in config.ini.
  -c NAGIOS_CONFIG, --nagios_config NAGIOS_CONFIG
                        Override the default config file.
```
This tool pushes the results of the previous day's __dailyverification__. It uses code from the [seismic-digitizer-soh](http://bitbucket.seismo.nrcan.gc.ca/projects/NAG/repos/seismic-digitizer-soh/browse) package to interface with Nagios. The code was copied to stationverification/nagios so that that package would not be a requirement for this one.
This tool should be set up along side the __dailyverification__ tool as cron jobs.
```
* 1 * * * /home/jgosset/.local/bin/dailyverification -o /data/dailyverifications/
* 2 * * * /home/jgosset/.local/bin/pushtonagios -a /data/dailyverifications/
```
