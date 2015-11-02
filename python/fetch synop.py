#ftp://anonymous@data.knmi.nl/download/Actuele10mindataKNMIstations/1/noversion/2015/11/02/KMDS__OPER_P___10M_OBS_L2.nc

import sys
from ftplib import FTP
from datetime import datetime, timedelta

# connect without a password
ftp = FTP('data.knmi.nl')
result = ftp.login('anonymous')
if result != '230 login accepted':
    print >> sys.stderr, 'login failed'
    sys.exit(1)

# get the date and time for 5 minutes ago
datetime = datetime.utcnow() - timedelta(minutes=5)
datetime = datetime - timedelta(minutes=datetime.minute % 5)

# path to the 5 minute radar dataset for date
path = (
    '/download/Actuele10mindataKNMIstations/1/noversion/'
    '{datetime.year}/{datetime.month:02d}/{datetime.day:02d}/'
).format(datetime=datetime)
print path

result = ftp.cwd(path)
if result != '250 CWD command successful':
    print 'directory {0} not found'.format(path)
    sys.exit(2)

filename = 'KMDS__OPER_P___10M_OBS_L2.nc'
result = ftp.retrbinary(
    'RETR {filename}'.format(filename=filename), open(filename, 'wb').write)
if not result.startswith('226'):
    print 'Failed to retrieve {filename}'.format(filename = filename)
    sys.exit(3)

ftp.quit()