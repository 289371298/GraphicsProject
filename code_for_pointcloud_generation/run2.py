#!/usr/bin/env python3

import os, sys
import glob
import numpy as np
import cv2
import shutil
import code

if __name__ == '__main__':
    names = ['capture']
    pts1 = np.array([[0, 0], [320, 0], [0, 240]], dtype=np.float32)
    pts2 = np.array([[10, 8], [10 + 304, 8], [10, 8 + 228]], dtype=np.float32)
    M = cv2.getAffineTransform(pts1,pts2)
    for name in names:
        orig_path = os.path.abspath('../' + name)
        shutil.rmtree(name)
        os.mkdir(name)
        path_depth = sorted(glob.glob(os.path.join(orig_path, '*.depth.png')))
        path_rgb = sorted(glob.glob(os.path.join(orig_path, '*.rgb.png')))

        for file in path_rgb:
            file_out = os.path.join(name, os.path.basename(file).replace('color', 'rgb'))
            shutil.copy2(file, file_out)

        for file in path_depth:
            img = cv2.imread(file, cv2.IMREAD_ANYDEPTH)
            img[img == 65535] = 0
            img = cv2.warpAffine(img, M, (320, 240), flags=cv2.INTER_NEAREST)
            #cv2.imshow('img', img)
            #cv2.waitKey(1000)
            file_out = os.path.join(name, os.path.basename(file))
            cv2.imwrite(file_out, img)
        print(name + ' Finish copy!')
        os.system('build/merge ' + os.path.abspath(name))
