#!/usr/bin/env python3

import os, sys
import glob
import shutil

if __name__ == '__main__':
    names = ['chess', 'fire', 'heads', 'office', 'pumpkin', 'redkitchen', 'stairs']
    shutil.rmtree('copy')
    os.mkdir('copy')
    for name in names:
        files = glob.glob(os.path.join(name, '*.ply'))
        files.sort(key=lambda x: int(''.join(filter(str.isdigit,x))))
        print(name, end=', ')
        print(files[-1])
        shutil.copy2(files[-1], os.path.join('copy', name + str(len(files)) + '.ply'))
