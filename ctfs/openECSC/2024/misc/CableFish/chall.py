#!/usr/bin/env python3

import os
import subprocess
import time

flag = os.getenv('FLAG', 'openECSC{redacted}')

def filter_traffic(filter):
    filter = filter[:50]
    sanitized_filter = f'(({filter}) and (not frame contains "flag_placeholder"))'
    p1 = subprocess.Popen(['tshark', '-r', '/home/user/capture.pcapng', '-Y', sanitized_filter, '-T', 'fields', '-e', 'tcp.payload'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()

    if stderr != b'':
        return sanitized_filter, stderr.decode(), 'err'

    res = []
    for line in stdout.split(b'\n'):
        if line != b'':
            p2 = subprocess.Popen(['xxd', '-r', '-p'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(os.devnull, 'wb'))
            stdout, _ = p2.communicate(input=line)
            p3 = subprocess.Popen(['xxd', '-c', '32'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(os.devnull, 'wb'))
            stdout, _ = p3.communicate(input=stdout)
            res.append(stdout.decode().replace('flag_placeholder', flag))

    return sanitized_filter, res, 'ok'

if __name__ == '__main__':
    banner = '''
                                            ,@@
                                        @@@/  @@
                                     @@      &@
                                   @@        @*
                                 ,@          @*
                                ,@           @@
                                @,            @.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


                         ,,        ,,                    ,,           ,,
       .g8"""bgd        *MM      `7MM         `7MM"""YMM db         `7MM
     .dP'     `M         MM        MM           MM    `7              MM
     dM'       ` ,6"Yb.  MM,dMMb.  MM  .gP"Ya   MM   d `7MM  ,pP"Ybd  MMpMMMb.
     MM         8)   MM  MM    `Mb MM ,M'   Yb  MM""MM   MM  8I   `"  MM    MM
     MM.         ,pm9MM  MM     M8 MM 8M""""""  MM   Y   MM  `YMMMa.  MM    MM
     `Mb.     ,'8M   MM  MM.   ,M9 MM YM.    ,  MM       MM  L.   I8  MM    MM
       `"bmmmd' `Moo9^Yo.P^YbmdP'.JMML.`Mbmmd'.JMML.   .JMML.M9mmmP'.JMML  JMML.

'''
    print(banner)
    filter = input('Please, specify your filter: ')
    print("Loading, please wait...")
    sanitized_filter, res, status = filter_traffic(filter)
    print(f'Evaluating the filter: {sanitized_filter}')
    print()
    output = ''
    if status == 'err':
        output = f'ERROR: {res}'
    else:
        for line in res:
            for l in line.strip().split('\n'):
                output += l[91:]
    print(output)
    print('\nEnd of the results. Bye!')