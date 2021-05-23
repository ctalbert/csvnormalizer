import sys
import csv
import re
from datetime import datetime, time
from zoneinfo import ZoneInfo

DEBUG=0

def normalize_timestamp(ts):
    # Convert to EST
    # Get into RFC3339 format
    dt_pst = datetime.strptime(ts, '%m/%d/%y %I:%M:%S %p').replace(tzinfo=ZoneInfo('America/Los_Angeles'))
    dt_est = dt_pst.astimezone(ZoneInfo('America/New_York'))
    
    return dt_est.isoformat()

def normalize_address(addr):
    return '"' + addr + '"'

def normalize_zip(zip):
    # TODO: Should this throw if it's not 5 digits?
    z = zip
    if len(zip) < 5:
        zeros_to_add = 5 - len(zip)
        z = '0'*zeros_to_add + zip
    
    return z

def normalize_fullname(fname):
    return fname.upper()

def normalize_foobar(f, b):
    def calcsecs (timestr):
        m = re.match('(\d+)\:(\d+)\:(\d+\.\d+)', timestr)
        secs = int(m.group(1)) * 3600 # hours -> sec
        secs += int(m.group(2)) * 60 # min -> sec
        secs += float(m.group(3))
        return secs

    fsec = calcsecs(f)
    bsec = calcsecs(b)
    return fsec, bsec

def normalize_notes(notes):

    return '"' + notes + '"'


def process_row(row):
    if DEBUG:
        print(row)

    try:
        norm_timestamp = normalize_timestamp(row['Timestamp'])
        norm_address = normalize_address(row['Address'])
        norm_zip = normalize_zip(row['ZIP'])
        norm_fullname = normalize_fullname(row['FullName'])
        norm_foo, norm_bar = normalize_foobar(row['FooDuration'], row['BarDuration'])
        norm_total = norm_foo + norm_bar
        norm_notes = normalize_notes(row['Notes'])

        if DEBUG:
            print('Timestamp: {}, Address: {}, zip: {}, fullname: {}, foo: {}, bar: {}, total: {}, notes: {}'.format(
                norm_timestamp, norm_address, norm_zip, norm_fullname, norm_foo, norm_bar, norm_total, norm_notes))

        print('{}, {}, {}, {}, {}. {}. {}. {}'.format(norm_timestamp, norm_address, norm_zip, norm_fullname, norm_foo, norm_bar, norm_total, norm_notes),
            file=sys.stdout)

    except ValueError:
        print('Error: {} -- will skip this line'.format(sys.exc_info()), file=sys.stderr)

def main():

    # Get Data and process it
    # TODO: handle differently named rows, different orders (should be handled by DictReader)
 
    try:
        
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        inputreader = csv.DictReader(sys.stdin.readlines())
    except UnicodeDecodeError as err:
        print(sys.exc_info(), err.start, err.end, file=sys.stderr)
        sys.exit()

    # output the column headers
    print(','.join(inputreader.fieldnames), file=sys.stdout)
    for row in inputreader:
        process_row(row)


if __name__ == '__main__':
    main()

