from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from numpy import unravel_index
import math
import sys
import argparse


def fourier_transform(image_path, scale, color_scheme='nipy_spectral'):
    # алгоритм
    # посчитать расстояние от центра до первых максимумов (если они не паралельны оси х, применить теорему Пифагора) - обозначим X
    # посчитать по пропорции сколько X составляет в лин/px (центр картинки = 0, края картинки = 0.5 лин/px) - обозначим Y
    # посмотреть в ZEN чему равен 1 px - обозначим Z (в мкм)
    # формула = Z/Y = период
    try:
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        raise FileNotFoundError("File %s has not been found!" % image_path)

    data = np.asarray(img.getdata()).reshape(img.size)
    fft = np.fft.fft2(data)
    for i in range(-4, 4, 1):
        for n in range(-4, 4, 1):
            fft[i, n] = 0

    plt.imshow(np.abs(np.fft.fftshift(fft)), color_scheme)
    # сolor scheme - nipy_spectral, gist_stern, gist_ncar, gnuplot...
    plt.show()

    fft = np.abs(np.fft.fftshift(fft))
    index_of_max = unravel_index(fft.argmax(), fft.shape)
    print("--------------------------Supporting information--------------------------")
    print("Indices of maximum = %s" % str(index_of_max))
    first_katet = index_of_max[0] - fft.shape[0] / 2
    print("Length of first side of right triangle [px] = %s" % str(first_katet))
    second_katet = index_of_max[1] - fft.shape[1] / 2
    print("Length of second side of right triangle [px] = %s" % str(second_katet))
    gipotenusa = math.sqrt(first_katet * first_katet + second_katet * second_katet)
    print("Distance from central maximum to first maximum [px] = %s" % str(gipotenusa))
    gipotenusa_in_line_per_pix = gipotenusa * 0.5 / (len(fft) / 2)
    print("Distance from central maximum to first maximum [line/px] = %s" % str(gipotenusa_in_line_per_pix))
    period = scale / gipotenusa_in_line_per_pix
    print("--------------------------Supporting information--------------------------\n")
    print("Period [mkm] = %s" % str(period))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="path to the image")
    parser.add_argument("scale", help="μm per pixel", type=float)
    parser.add_argument("--color_schema", default='nipy_spectral',
                        help="color scheme to use. See https://matplotlib.org/stable/tutorials/colors/colormaps.html")
    args = parser.parse_args()
    fourier_transform(args.image_path, args.scale, args.color_schema)
