"""
Example 3 for beamfpy library

demonstrates a 3D beamforming setup,

uses measured data in file 2008-05-16_11-36-00_468000.h5
calibration in file calib_06_05_2008.xml
microphone geometry in array_56.xml (part of beamfpy)


(c) Ennes Sarradj 2007-2010, all rights reserved
ennes.sarradj@gmx.de
"""

# imports from beamfpy
import beamfpy
from beamfpy import td_dir, L_p, TimeSamples, Calib, MicGeom, EigSpectra,\
RectGrid3D, BeamformerBase, BeamformerEig, BeamformerOrth, BeamformerCleansc

# other imports
from os import path
from numpy import mgrid, arange
from enthought.mayavi import mlab

#===============================================================================
# first, we define the data source, calibration and microphone geometry
#===============================================================================

t = TimeSamples(name=path.join(td_dir,'2008-05-16_11-36-00_468000.h5'))
cal = Calib(from_file=path.join(td_dir,'calib_06_05_2008.xml'))
m = MicGeom(from_file=path.join(\
    path.split(beamfpy.__file__)[0], 'xml', 'array_56.xml'))

#===============================================================================
# the 3D grid (very coarse to enable fast computation for this example)
#===============================================================================

g = RectGrid3D(x_min=-0.6, x_max=-0.0, y_min=-0.3, y_max=0.3, \
    z_min=0.48, z_max=0.88, increment=0.05)

#===============================================================================
# this provides the cross spectral matrix and defines the beamformer
# usually, another type of beamformer (e.g. CLEAN-SC) would be more appropriate
# to be really fast, we restrict ourselves to only 10 frequencies
# in the range 2000 - 6000 Hz (5*400 - 15*400)
#===============================================================================

f = EigSpectra(time_data=t, window='Hanning', overlap='50%', block_size=128, \
    ind_low=5, ind_high=15)
b = BeamformerBase(freq_data=f, grid=g, mpos=m, r_diag=True, c=346.04)

#===============================================================================
# reads the data, finds the maximum value (to properly scale the views)
#===============================================================================

map = b.synthetic(4000,1)
L1 = L_p(map)
mx = L1.max()

#===============================================================================
# print out the result integrated over an 3d-sector of the 3d map
#===============================================================================

print(L_p(b.integrate((-0.3,-0.1,0.58,-0.1,0.1,0.78)))[f.ind_low:f.ind_high])

#===============================================================================
# displays the 3d view
#===============================================================================

X,Y,Z = mgrid[g.x_min:g.x_max:1j*g.nxsteps,\
            g.y_min:g.y_max:1j*g.nysteps,\
            g.z_min:g.z_max:1j*g.nzsteps]
data = mlab.pipeline.scalar_field(X,Y,Z,L1)
mlab.pipeline.iso_surface(data,contours=arange(mx-10,mx,1).tolist(),vmin=mx-10,vmax=mx)

# uncomment one of the following lines to see a different visualization of 
# the data
#mlab.contour3d(X,Y,Z,L1,vmin=mx-5,vmax=mx,transparent=True)
#mlab.points3d(X,Y,Z,L1,vmin=mx-5,vmax=mx,transparent=True)

#===============================================================================
# adds some axes and enters the GUI main loop
#===============================================================================

mlab.axes()
mlab.show()

