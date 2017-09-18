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
    '/download/radar_volume_full_herwijnen/1.0/noversion/'
    '{datetime.year}/{datetime.month:02d}/{datetime.day:02d}/'
).format(datetime=datetime)
print path

result = ftp.cwd(path)
if result != '250 CWD command successful':
    print 'directory {0} not found'.format(path)
    sys.exit(2)

# get the filename for the latest one
# filenames for this particular dataset always follow the same structure
# 'RAD_NL60_VOL_NA_{hour}{minute}.h5'
# where minute is in 5 minute increments
# there is a slight delay before we release the data, so get the file from
# 10 minutes ago

filename = 'RAD_NL62_VOL_NA_{hour:02d}{minute:02d}.h5'.format(
    hour=datetime.hour, minute=datetime.minute)
print filename
result = ftp.retrbinary(
    'RETR {filename}'.format(filename=filename), open(filename, 'wb').write)
if not result.startswith('226'):
    print 'Failed to retrieve {filename}'.format(filename = filename)
    sys.exit(3)

# or get the latest file by listing the directory contents
ls_result = []
result = ftp.retrlines('LIST', ls_result.append)
if not result.startswith('226'):
    print 'Failed to retrieve list'
    sys.exit(3)

# and taking the name of the last file
filename = ' '.join(ls_result[-1].split()[8:])
print filename

result = ftp.retrbinary(
    'RETR {filename}'.format(filename=filename), open(filename, 'wb').write)
if not result.startswith('226'):
    print 'Failed to retrieve {filename}'.format(filename = filename)
    sys.exit(3)

ftp.quit()
