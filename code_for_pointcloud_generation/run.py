#!/usr/bin/env python3

import os, sys
import glob
import numpy as np
import cv2
import shutil
import code

if __name__ == '__main__':
    names = ['chess', 'fire', 'heads', 'office', 'pumpkin', 'redkitchen', 'stairs']
    pts1 = np.array([[0, 0], [640, 0], [0, 480]], dtype=np.float32)
    pts2 = np.array([[22, 22], [22 + 580, 22], [22, 22 + 435]], dtype=np.float32)
    M = cv2.getAffineTransform(pts1,pts2)
    for name in names:
        orig_path = os.path.abspath('../' + name + '/seq-01')
        shutil.rmtree(name)
        os.mkdir(name)
        path_depth = sorted(glob.glob(os.path.join(orig_path, '*.depth.png')))
        path_rgb = sorted(glob.glob(os.path.join(orig_path, '*.color.png')))

        for file in path_rgb:
            file_out = os.path.join(name, os.path.basename(file).replace('color', 'rgb'))
            shutil.copy2(file, file_out)

        for file in path_depth:
            img = cv2.imread(file, cv2.IMREAD_ANYDEPTH)
            img[img == 65535] = 0
            img = cv2.warpAffine(img, M, (640, 480), flags=cv2.INTER_NEAREST)
            #cv2.imshow('img', img)
            #cv2.waitKey(1000)
            file_out = os.path.join(name, os.path.basename(file))
            cv2.imwrite(file_out, img)
        print(name + ' Finish copy!')
        os.system('build/merge ' + os.path.abspath(name) + ' > ' + name + '.log &')
