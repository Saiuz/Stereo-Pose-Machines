#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: produce-data-dir.py


import glob, cv2
import numpy as np
import sys, os

from tensorpack.utils.fs import mkdir_p
from runner import get_runner, get_parallel_runner
from model import colorize
from calibr import load_camera_from_calibr


if __name__ == '__main__':
    dir = sys.argv[1]
    undistdir = sys.argv[2]
    outdir = sys.argv[3]
    mkdir_p(undistdir)
    mkdir_p(outdir)
    runner, _ = get_runner('../data/cpm.npy' )

    C0, C1, d0, d1 = load_camera_from_calibr('../calibr-1211/camchain-homeyihuaDesktopCPM3D_kalibrfinal3.yaml')
    for f in sorted(glob.glob(os.path.join(dir, '*.jpg'))):
        im = cv2.imread(f, cv2.IMREAD_COLOR)

        im = cv2.undistort(im, C0.K, d0)


        cv2.imwrite(os.path.join(undistdir, os.path.basename(f)), im)

        im = cv2.resize(im, (368, 368))
        out = runner(im)
        np.save(os.path.join(outdir, os.path.basename(f)), out)

        #viz = colorize(im, out[:,:,:-1].sum(axis=2))
        #cv2.imshow("", viz/255.0)
        #cv2.waitKey()
        print f

