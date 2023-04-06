'''
Copyright (c) 2023 Susanne Stole-Hentschel <sstolehe@ens-paris-saclay.fr>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import os
import imageio
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.realpath(__file__))

def plot_tracks(track_dict, ax=None, color='r', interp_fact=1):
    '''
    Function for plotting tracks

    Parameters:
    -----------
                input
                        track_dick              dictionary
                                                dictionary with track IDs als keys and an array containing the x and y positions of the tracks
                                                The axis are numbered according to the pixel position. 
                                                The x and y positions are given as list of indices.
                        ax                      plotting axis
                                                if desired a axis for plotting can be provided; default: None
                        color                   string
                                                color for plotting the tracks
                                                default: 'r'
                        interp_fact             int
                                                interpolation factor. If the tracks have been interpolated before defining the tracks the operation can be reversed so that 
                                                the plotted tracks match the initial grid. Default: 1
                output
                        ax                      plotting axis
                                                plotting axis used for plotting tracks
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(np.array(track_dict[0][1])/interp_fact, np.array(track_dict[0][0])/interp_fact, color=color)
    for i in range(1, len(track_dict)):
        ax.plot(np.array(track_dict[i][1])/interp_fact, np.array(track_dict[i][0])/interp_fact, color=color)
    ax.set_xticks([])
    ax.set_yticks([])
    return ax

def read_output_file(fn, min_track_length=10):
    ''''
    File that reads the defined tracks form the deverny edge detection program.
    The tracks are registered in a track ditionary if they exceed the provided min_track_length

    Parameters:
    -----------
                input   
                        fn                  string
                                            filename of the outputfile
                        min_track_length    int
                                            minimum allowed length of the track in number of points
                                            Shorter tracks are discarded
                output
                        track_dict          dictionary 
                                            definition of trackIDs and corresponding x and y positions
    '''
    tracklists = np.loadtxt(fn)
    track_dict = {}
    current_ID = 0
    this_track_x = []
    this_track_y = []

    for track in tracklists:
        if track[0]>-1:
            this_track_x.append(track[0])	
            this_track_y.append(track[1])
        else:
            if len(this_track_x)>min_track_length:
                track_dict[current_ID] = [this_track_x, this_track_y]
                current_ID += 1
            this_track_x = []
            this_track_y = []
    return track_dict

def write_non_interpol_output_file(track_dict, interp_fact):
    '''
    Generate an output file where interpolatated points are removed

    Parameters:
                    input
                        track_dick              dictionary
                                                dictionary with track IDs als keys and an array containing the x and y positions of the tracks
                                                The axis are numbered according to the pixel position. 
                                                The x and y positions are given as list of indices.
                        interp_fact             int
                                                interpolation factor. If the tracks have been interpolated before defining the tracks the operation can be reversed so that 
                                                the plotted tracks match the initial grid.             
    '''
    x_cords = []
    y_cords = []
    for key in track_dict.keys():
        this_track = track_dict[key]
        x_cords += this_track[0] + [-1]
        y_cords += this_track[1] + [-1]
    output = np.array([x_cords, y_cords]).T
    output /= interp_fact
    if interp_fact > 1:
        fn = 'output_inter.txt'
    else:
        fn = 'output.txt'
    np.savetxt(fn, output)

def plot_data(data, fig=None, ax=None):
    '''
    Plot data

    Parameters:
    ----------
                input
                            data            2d array
                                            containing data to be plotted
                            fig             matplotlib fig object
                                            provide if predefined; default: None
                            ax              matplotlib axis object
                                            provide if predefined; default: None
    '''
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(data.T, origin='lower')
    ax.set_xticks([])
    ax.set_yticks([])
    return fig, ax

def plot_data_and_tracks(data, track_dict, fig=None, ax=None, color='r', interp_fact=1):
    '''
    Plot data and superimpose tracks

    Parameters:
    -----------
                input
                            data            2d array
                                            containing data to be plotted
                            track_dick      dictionary
                                            dictionary with track IDs als keys and an array containing the x and y positions of the tracks
                                            The axis are numbered according to the pixel position. 
                                            The x and y positions are given as list of indices.
                            fig             matplotlib fig object
                                            provide if predefined; default: None
                            ax              matplotlib axis object
                                            provide if predefined; default: None
                            color           string
                                            color for plotting the tracks
                                            default: 'r'
                            interp_fact     int
                                            interpolation factor. If the tracks have been interpolated before defining the tracks the operation can be reversed so that 
                                            the plotted tracks match the initial grid. Default: 1
                output    
                            fig             matplotlib fig object
                                            reference to figure object that was used for plotting
                            ax              matplotlib axis object
                                            reference to axis object that was used for plotting                       
    '''
    if ax is None:
        fig, ax = plt.subplots()
    plot_data(data, fig=fig, ax=ax)
    plot_tracks(track_dict, ax, color=color, interp_fact=interp_fact)
    return fig, ax

def process_track_finding(input_data, input, interp_fact, sigma, l, h, min_track_length):
    '''
    process track finding

    Parameters:
    -----------
                input
                        input_data              2d array
                                                data for which tracks should be found read from the input image
                        input                   string
                                                referring to input image
                        interp_fact             int
                                                interpolation factor to be used if interpolation is applied
                        sigma                   float
                                                Value for Gaussian smoothing during edge tracking
                        l                       int
                                                lower threshold for edge tracking
                        h                       int 
                                                higher threshold for edge tracking
                        min_track_length        int
                                                number of points that a valid track should at least contain
                output
                        number_of_tracks        int
                                                number of valid tracks found
    '''

    # convert image for devernay, keep original
    input_copy = input[:-4]+'_copy'+ input[-4:]
    input_pgm = input[:-4]+'_copy.pgm'
    os.system(f'cp {input} {input_copy}')
    os.system(f'convert {input_copy} {input_pgm}')

    # run devernay algorithm for determining edges
    loc_devernay = os.path.join(ROOT, 'devernay_1.0_modified')
    os.system(f'{loc_devernay}/devernay {input_pgm} -t output_intermediate.txt -s {sigma} -l {l} -h {h}')

    # read the output file of the tracks
    track_dict = read_output_file('output_intermediate.txt', min_track_length=min_track_length)
    write_non_interpol_output_file(track_dict, interp_fact)

    # generate output images
    number_of_tracks = len(track_dict.keys())
    if number_of_tracks>0:
        plot_data_and_tracks(input_data, track_dict, interp_fact=interp_fact)
        plt.savefig(f'output.pdf', bbox_inches='tight')
        plot_tracks(track_dict, color='k', )
        plt.savefig(f'tracks.pdf', bbox_inches='tight')
    else:
        plot_data(input_data)
        plt.savefig(f'output.pdf', bbox_inches='tight')
    if input_copy==input_pgm:
        os.system(f'rm {input_copy}')
    else:
        os.system(f'rm {input_copy} {input_pgm}')
    return number_of_tracks

def main(input, interp, interp_method, interp_fact, sigma, l, h, min_track_length):
    '''
    Access point of the program; saves the input image as svg, reads it into a data array.
    Program is started. If wanted, interpolation is applied before proceeding to the edge tracking

    Parameters:
    -----------
                input
                        input               string
                                            input image
                        interp              bool
                                            indicating if interpolation should be applied
                        interp_method       string
                                            provides interpolation method possible choices are summarized the interpolation module
                                            some examples are: 'bilinear', 'fourier', 'bicubic', 'bspiline2', 'omoms3', 'nearest', 'lanczos3')
                        interp_fact         int
                                            interpolation factor to be used if interpolation is applied
                        sigma               float
                                            Value for Gaussian smoothing during edge tracking
                        l                   int
                                            lower threshold for edge tracking
                        h                   int 
                                            higher threshold for edge tracking
                        min_track_length    int
                                            number of points that a valid track should at least contain     
    '''

    # save input image
    input_data = imageio.imread(input)
    plot_data(input_data)
    plt.savefig(f'input.pdf', bbox_inches='tight')
    if not interp:
        interp_fact = 1

    if interp:
        loc_linterp = os.path.join(ROOT, 'linterp-src')
        input_png = input[:-4] + '_converted.png' 
        os.system(f'convert {input} {input_png}')
        input_inter = input[:-4] + '_inter.png'
        os.system(f'{loc_linterp}/linterp {input_png} {input_inter} -m {interp_method} -x {interp_fact}')
        number_of_tracks = process_track_finding(input_data, input_inter, interp_fact, sigma, l, h, min_track_length)
        os.system(f'rm {input_png}')
    
    else:
        number_of_tracks = process_track_finding(input_data, input, 1, sigma, l, h, min_track_length)
    os.system('rm output_intermediate.txt')

    print("The number of tracks found is: ", number_of_tracks)
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--interp", type=str, default=False, required=False)
    parser.add_argument("--interp_method", type=str, required=False)
    parser.add_argument("--interp_fact", type=int, required=False)
    parser.add_argument("--sigma", type=float, default=1, required=False)
    parser.add_argument("--l", type=float, default=8, required=False)
    parser.add_argument("--h", type=float, default=12, required=False)
    parser.add_argument("--min_track_length", type=int, default=10, required=False)

    args = parser.parse_args()
    main(args.input, args.interp, args.interp_method, args.interp_fact, args.sigma, args.l, args.h, args.min_track_length)
