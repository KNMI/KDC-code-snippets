# KDC-code-snippets

Snippets for getting and using data from KNMI Data Center

## Python
The folder python contains the following snippets:
* `fetch radar.py` fetches the latest Volume data from the the radar in Herwijnen from [KNMI Data Center](https://data.knmi.nl/datasets/radar_volume_full_herwijnen/1.0) using ftp;
* `read radar.py` uses [wradlib](https://bitbucket.org/wradlib/wradlib) to plot the radar data;
* `fetch synop.py` fetches the latest synoptic observations from [KNMI Data Center](https://data.knmi.nl/datasets/Actuele10mindataKNMIstations/1) using ftp;
* `read synop.py` uses netCDF4 for python to read all values from the synoptic data;

## Web demo's

The folder `web` contains demo's for front-end code. You can view these online as well:

* [adaguc-openlayers](http://cdn.rawgit.com/KNMI/KDC-code-snippets/master/web/adaguc-openlayers/index.html)

## Contributing

When you have a nice and small demo related to the data in the KNMI Data Center and or its technologies you're welcome to contribute your demo. Please follow the default Github contribution steps:

1. Fork it ( https://github.com/[my-github-username]/KDC-code-snippets/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
