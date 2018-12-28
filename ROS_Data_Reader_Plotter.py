#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 12:38:43 2018

Caleb G. Pan
University of Montana
Numerical Terradynamic Simulations Group (NTSG)
Missoula, MT, USA
email: caleb.pan@mso.umt.edu

THIS SCRIPT PROVIDES THE BASIC GDAL TOOLS TO EXTRACT INFORMATION FROM ROS DATA.
INFORMATION INCLUDE; PROJECTION, GEOTRANSFORM, AND SHAPE (ROWS/COLS). ALSO,
A SIMPLE PLOT IS CREATED TO VISUALIZE THE DATA. PLEASE NOTE, THE SHAPE OF THESE 
DATA ARE NOT EXACT TO ALASKA, THIS IS BECAUSE OF THE 24KM INVERSE BUFFER 
APPLIED TO SCREEN OUT WATER CONTAMINATED PIXELS. TWO SMALL CIRCLES CAN BE 
OBSERVED IN THE ALASKA PLOT, ONE IN THE SOUTHEAST AND ANOTHER IN THE SOUTHWEST 
- THESE ARE MASKED LAKES.

THE ROS DATA RECORD IS ARCHIVED AT THE OAK RIDGE NATIONAL LABORATORY AND CAN
BE ACCESSED HERE: https://daac.ornl.gov/ABOVE/guides/Rain-on-Snow_Data.html
"""
#==============================================================================
# IMPORT THE NECESSARY LIBRARIES
#==============================================================================
import gdal
import numpy as np
import matplotlib.pyplot as plt
#==============================================================================
# INSERT THE FILE DIRECTORY OF THE FILE OF INTEREST
#==============================================================================

inputfile = '/Users/calebpan/Dropbox/ROSAlaska/AMSR_ROS_SUM_A_6km_NDJFM_WY2004_v1.tif'

#==============================================================================
# USING GDAL BINDINGS, OPEN THE FILE AND EXTRACT THE BAND. THE BAND IS THEN
# CONVERTED TO AN ARRAY. VALUES LESS THAN ZERO ARE SET TO NP.NAN BECAUSE THESE 
# ARE THE VALUES THAT EXIST OUTSIDE OF THE ALASKA BOUNDARIES 
# (WHICH ARE SET TO -9999)
#==============================================================================

opentif = gdal.Open(inputfile, gdal.GDT_Int16)
band = opentif.GetRasterBand(1)
array = band.ReadAsArray().astype(np.float64) #set array to float 
array[array<0] = np.nan

#==============================================================================
# EXTRACT THE PROJECTION, GEOTRANSFORM AND SHAPE OF THE ROS DATA
#==============================================================================

prj = opentif.GetProjection()
geo = opentif.GetGeoTransform()
shape = np.shape(array)

print 'Projection', prj
print 'GeoTransform', geo
print 'Array Shape (rows/columns)', shape

#==============================================================================
# GET MIN, MAX, AND MEAN VALUES OF ROS EVENTS ACROSS ALASKA
#==============================================================================

ROSmin = np.nanmin(array)
ROSmax = np.nanmax(array)
ROSmean = np.nanmean(array)

print 'Min: ', ROSmin, ' Max: ', ROSmax, ' Mean: ', ROSmean

"""

VISUALIZE ROS DATA

"""
#==============================================================================
# CONTOUR HERE IS USED TO DEFINE THE BOUNDARIES OF THE ROS DATA
#==============================================================================

contourband = opentif.GetRasterBand(1)
contourarray = contourband.ReadAsArray()
contour = contourarray>=0

#==============================================================================
# SET PLOT EXTENT VARIABLES
# FROM 'info' LOWER LEFT COORDINATES ARE EXTRACTED AND CONVERTED TO DECIMAL 
# DEGREES. THESE COORDINATES ARE USED TO CONVERT THE PLOT FROM ROWS/COLUMNS 
# TO LAT/LONG THERE WILL LIKELY BE DISTORTION IN THE LAT/LONG LABELS.
#==============================================================================

info = gdal.Info(opentif)
longll = -168.20750000
latll = 53.34969444
cs = 0.048
extent = [longll, longll+ shape[1] * cs, latll, latll + shape[0] * cs]

#==============================================================================
# PLOT THE ROS ARRAY
#==============================================================================

fig, ax = plt.subplots()
cmap = plt.cm.YlOrRd #designate the color ramp to display ROS images
outline = ax.contour(contour,extent, colors = 'k', origin='upper',\
                     linewidths = 0.075)
sums = ax.imshow(array, extent = extent,cmap = cmap)
ax.grid(linestyle = '-.')
ax.set_ylabel('Latitude [dd]')
ax.set_xlabel('Longitude [dd]')

cb = fig.colorbar(sums,orientation = 'vertical')
cb.set_label('Total ROS events pixel $^-$$^1$')
plt.show()
