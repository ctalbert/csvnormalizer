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


def process_row(row, header_order=None):
    # header_order is an array of the field header keys
    norm_values = {}
    if DEBUG:
        print(row)

    try:
        norm_values['Timestamp'] = normalize_timestamp(row['Timestamp'])
        norm_values['Address'] = normalize_address(row['Address'])
        norm_values['ZIP'] = normalize_zip(row['ZIP'])
        norm_values['FullName'] = normalize_fullname(row['FullName'])
        norm_values['FooDuration'], norm_values['BarDuration'] = normalize_foobar(row['FooDuration'], row['BarDuration'])
        norm_values['TotalDuration'] = norm_values['FooDuration'] + norm_values['BarDuration']
        norm_values['Notes'] = normalize_notes(row['Notes'])

        if DEBUG:
            print(norm_values)

        # Output the row
        output = ','.join([str(norm_values[i]) for i in header_order])
        print(output, file=sys.stdout)

    except ValueError:
        print('Error: {} -- will skip this line'.format(sys.exc_info()), file=sys.stderr)

def main():

    # Get Data and process it 
    try:
        
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        inputreader = csv.DictReader(sys.stdin.readlines())
    except UnicodeDecodeError as err:
        print(sys.exc_info(), err.start, err.end, file=sys.stderr)
        sys.exit()

    # output the column headers 
    # TODO: feels like wrong level of abstraction, don't love doing this here
    print(','.join(inputreader.fieldnames), file=sys.stdout)
    for row in inputreader:
        process_row(row, header_order=inputreader.fieldnames)


if __name__ == '__main__':
    main()

