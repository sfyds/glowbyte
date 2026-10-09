'''
Color detector, detects the colors, counts how many pixels are of said color then outputs a histogramm with that data 
For input, on a scale of 0 - 100 pick sensitivity to color varience: e.g. 100 EVERY color only differing by one digit in RGB is a different color. 50: colors can differ by  50% 
and still be considered the same. 


1. Load image and extact RGB pixels 
2. Count exact colors and calculate percentages 
3. Implement K-means clustering 
4. Create Matplotlib vizualisations 
5. test on data and put in output

'''

import numpy as np 
from PIL import Image 
import matplotlib.pyplot as plt 

import sys 

MAX_RGB_DISTANCE = np.sqrt(3) * 255  # distance from black (0,0,0) to white (255,255,255), used later for percentage distance between two colors



def load_pixels(path, max_size = 200):
    # Open the image
    pass

def main(): 
    # ask for input from user python colors.py file.png Sensitivity
    # So we expect three inputs 
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    sens = 80
    while True:
        raw = input("Sensitivity (default 80): ").strip()
        if not raw: 
            break 
        try: 
            sens = int(raw)
        except ValueError: 
            print("Sensitivity can only be a number between 0-100")
            continue
        if 0 <= sens <= 100: 
            break
        else:
            print("Sensitivity can only be a number between 0-100")


    inputfile = sys.argv[1]
    outputfile = "output_" + sys.argv[1]
    path = "input/" + inputfile 
    outpath = "output/" + outputfile

    





if __name__ == "__main__":
    main()