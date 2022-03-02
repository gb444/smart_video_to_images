#!/usr/bin/env python

from distutils.core import setup

setup(name='smart_video_to_images',
      version='1.0',
      description='A small GUI to take a video and convert it quickly to a series of images for photogramatry',
      author='Giles Barton-Owen',
      author_email='giles.bartonowen@gmail.com',
      url='https://github.com/gb444/smart_video_to_images',
      packages=['smart_video_to_images'],
      install_requires=[
          'opencv-python',
          'pysimplegui',
      ],
     )