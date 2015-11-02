from netCDF4 import Dataset
import glob

files = glob.glob('*.nc')

rootgrp = Dataset(files[-1], 'r', format='NETCDF4')
print rootgrp

for name, variable in rootgrp.variables.items():
	if variable.size < 45:
		print name, variable

for i in range(46):
	print '======'
	for name, variable in rootgrp.variables.items():
		if variable.size < 45:
			continue
		if 'units' in variable.__dict__:
			print '{name}: {value} {units} | {long_name}'.format(name=name, value=variable[i], units = variable.__dict__['units'], long_name = variable.__dict__['long_name'])
		else:
			print '{name}: {value}'.format(name=name, value=variable[i])

rootgrp.close()