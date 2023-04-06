The wave tracking algorithm
============================

Version 1.0 - April 2023
Susanne Stola-Hentschel


Introduction
------------

This algorithm defines wave tracks in two dimensional 
wave data, typically images of waves over time and range.
The work is described in the article :

  Tracking the Evolution of Ocean Waves"
  by Susanne Stole-Hentschel,
  Image Processing On Line, 2023. XXX


Files
-----
README.txt		    	- This file
COPYING       			- GNU AFFERO GENERAL PUBLIC LICENSE Version 3
requirements.txt		- requirements for installing installation and usage
main.py				- Main program in python provides an interface to the c-codes
	
devernay_1.0_modified/*		- Folder containing edge detection code with its own README

linterp-src/*			- Folder containing linterp-src code with its own README



Compiling
---------

Before using the code at least the devernay_1.0_modified code must be compiled inside it's folder.
All necessary information is contained in the README file of that folder.

For making use of the interpolation, the linterp-src code must also be compiled. 
It requires the following libraries: FFTW, JPE, PNG, TIFF. 
For installation please refer to the README file in the folder


Running the Command Line Interface
----------------------------------
The basic commmand line is:

python main.py --input testPNG.png

Additional options are
--sigma 		<value for the Gaussian filtering, default 1>
--l     		<lower threshold for edge detection, default 8>
--h     		<higher threshold for edge detection, default 12>
--min_track_length 	<minimum valid track length, default 10>
--interp 		<boolean indicating of interpolation should be used, default:False>
--interp_method 	<interpolation method, a choice of possible options is
			'bilinear', 'fourier', 'bicubic', 'bspiline2', 
			'omoms3', 'nearest', 'lanczos3'>
  			more information on the interpolation options are documented
			in the linterp-src folder.
--interp_fact 		<interpolation factor by which the number of points are increased 			
			in each direction>


The program shows three images: the original, the original with the tracks superimposed and an image of the tracks. All three are saved to file as <input.pdf>, <output.pdf> and <tracks.pdf>. 
The position of the tracks from the edge detection algorithm is also available in <output.txt> or <output_inter.txt> if the data has been interpolated.
If interpolation was used, the interpolation file is available as well with <_inter> added to the name.


Copyright and License
---------------------

Copyright (c) 2023 Susanne Stole-Hentschel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


