import wradlib
import glob
import numpy
import datetime
import re

files = glob.glob('*.h5')

h5file = wradlib.io.read_generic_hdf5(files[-1])

elevations = []

# what is the altitude of the radar?
sitecoords = (h5file['radar1']['attrs']['radar_location'][0], h5file['radar1']['attrs']['radar_location'][1], 0)

# define your cartesian reference system
projstr = wradlib.georef.create_projstr("utm",zone=32, hemisphere="north")
proj = wradlib.georef.proj4_to_osr(projstr)

# containers to hold Cartesian bin coordinates and data
xyz, data = numpy.array([]).reshape((-1,3)), numpy.array([])

for i in range(14):
        elevation = h5file['scan{i}'.format(i=i+1)]['attrs']['scan_elevation']
        elevations.append(elevation)
        # get the scan metadata for each elevation
        # where = raw["dataset%d/where"%(i+1)]
        # what  = raw["dataset%d/data1/what"%(i+1)]

        # define arrays of polar coordinate arrays (azimuth and range)
        # az = np.arange(0.,360.,360./where["nrays"])
        nrays = h5file['scan{i}'.format(i=i+1)]['attrs']['scan_number_azim']
        az = numpy.arange(0.,360.,360./nrays)
        # r  = np.arange(where["rstart"], where["rstart"]+where["nbins"]*where["rscale"], where["rscale"])
        rstart = 0.0
        nbins = h5file['scan{i}'.format(i=i+1)]['attrs']['scan_number_range']
        rscale = h5file['scan{i}'.format(i=i+1)]['attrs']['scan_range_bin']
        r  = numpy.arange(rstart, rstart + nbins*rscale, rscale)

        # derive 3-D Cartesian coordinate tuples
        xyz_ = wradlib.vpr.volcoords_from_polar(sitecoords, elevation, az, r, proj)

        # get the scan data for this elevation
        #   here, you can do all the processing on the 2-D polar level
        #   e.g. clutter elimination, attenuation correction, ...

        # parse gain and offset from calibration formula string
        match = re.match(
                'GEO=(\d+\.\d*)\*PV\+(-\d+\.\d*)',
                h5file['scan{i}/calibration'.format(i=i+1)]['attrs']['calibration_Z_formulas'][0]
        )
        gain = float(match.group(1))
        offset = float(match.group(2))
        data_ = offset + gain * h5file['scan{i}/scan_Z_data'.format(i=i+1)]['data']

        # transfer to containers
        xyz, data = numpy.vstack( (xyz, xyz_) ), numpy.append(data, data_.ravel())

# generate 3-D Cartesian target grid coordinates
maxrange  = 200000
minelev   = elevations[0]
maxelev   = elevations[-1]
maxalt    = 5000.
horiz_res = 2000.
vert_res  = 250.
trgxyz, trgshape = wradlib.vpr.make_3D_grid(sitecoords, proj, maxrange, maxalt, horiz_res, vert_res)

# interpolate to Cartesian 3-D volume grid
tstart = datetime.datetime.now()
gridder = wradlib.vpr.CAPPI(xyz, trgxyz, trgshape, maxrange, minelev, maxelev)
vol = numpy.ma.masked_invalid( gridder(data).reshape(trgshape) )
print "3-D interpolation took:", datetime.datetime.now() - tstart

# diagnostic plot
trgx = trgxyz[:,0].reshape(trgshape)[0,0,:]
trgy = trgxyz[:,1].reshape(trgshape)[0,:,0]
trgz = trgxyz[:,2].reshape(trgshape)[:,0,0]
wradlib.vis.plot_max_plan_and_vert(trgx, trgy, trgz, vol, unit="dBZH", levels=range(-32,60))

# print h5file.keys()
# print h5file['radar1']['attrs']['radar_location']
# print h5file['geographic']
# print h5file['scan1/scan_Z_data']['data'].size
# print h5file['scan1/scan_Z_data']['data'][0].size
# print h5file['scan1/scan_Z_data']['data'][0]