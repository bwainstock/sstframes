"""Takes sst file as input and increments output timestamp by 1 frame"""

import csv
import glob
import os
import re
import sys


def parse_sst(filename):
    """Reads in lines of sst file and modified timestamps"""

    print(filename)
    with open(filename) as input_file:
        orig_lines = csv.reader(input_file, delimiter='\t')
        output_filename = '.'.join([filename[:-4], 'son'])
        with open(output_filename, 'a') as output_file:
            for line in orig_lines:
                if not re.match('\d{4}', line[0]):
                    output_file.write(line[0])
                else:
                    validate_timecodes(line)
                    modified_line = increment_line(line)
                    output_file.write('\t'.join(modified_line))
                output_file.write('\r\n')


def validate_timecodes(timestamp):
    """Parses NTSC SMPTE timecodes and increments by one frame"""

    sub_num, in_timecode, out_timecode, _ = timestamp
    max_ff = 29
    max_mm = max_ss = 59

    _, in_mm, in_ss, in_ff = [int(x) for x in in_timecode.split(':')]
    _, out_mm, out_ss, out_ff = [int(x) for x in out_timecode.split(':')]

    if (in_ff > max_ff) or (out_ff > max_ff):
        error_msg = 'frames ({})'.format(sub_num)
    elif (in_ss > max_ss) or (out_ss > max_ss):
        error_msg = 'seconds ({})'.format(sub_num)
    elif (in_mm > max_mm) or (out_mm > max_mm):
        error_msg = 'minutes ({})'.format(sub_num)
    else:
        error_msg = ''

    if error_msg:
        sys.exit('-'.join(['Bad timestamp format', error_msg]))


def increment_line(timestamp):
    """Parses NTSC SMPTE timecodes and increments by one frame"""

    sub_num, in_timecode, out_timecode, graphics_filename = timestamp
    max_ff = 29
    max_mm = max_ss = 59

    out_hh, out_mm, out_ss, out_ff = [int(x) for x in out_timecode.split(':')]
    if out_ff < max_ff:
        out_ff += 1
    else:
        out_ff = 0
        if out_ss < max_ss:
            out_ss += 1
        else:
            out_ss = 0
            if out_mm < max_mm:
                out_mm += 1
            else:
                out_mm = 0
                out_hh += 1
    out_timecode_fields = (out_hh, out_mm, out_ss, out_ff)
    mod_out_timecode = ['{0:02d}'.format(field) for field in out_timecode_fields]
    mod_out_timecode = ':'.join(mod_out_timecode)
    return [sub_num, in_timecode, mod_out_timecode, graphics_filename]


def main():
    """Reads filenames, parses files, and outputs new files"""

    filenames = glob.glob('*.sst')
    for filename in filenames:
        parse_sst(filename)

if __name__ == '__main__':
    main()
