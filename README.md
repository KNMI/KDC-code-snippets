# KDC-code-snippets
Snippets for getting and using data from KNMI Data Center

## Python
The folder python contains the following snippets:
* `fetch radar.py` fetches the latest Volume data from the De Bilt radar from [KNMI Data Center](https://data.knmi.nl/portal/KNMI-DataCentre.html#term=volume&dataset-name=radar_volume_debilt&dataset-version=2.0) using ftp;
* `read radar.py` uses [wradlib](https://bitbucket.org/wradlib/wradlib) to plot the radar data;
* `fetch synop.py` fetches the latest synoptic observations from [KNMI Data Center](https://data.knmi.nl/portal/KNMI-DataCentre.html#term=synoptic&dataset-name=Actuele10mindataKNMIstations&dataset-version=1) using ftp;
* `read synop.py` uses netCDF4 for python to read all values from the synoptic data;