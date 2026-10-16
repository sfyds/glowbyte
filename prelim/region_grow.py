''' 
Using the code from colors.py we'll take the found colors that have been generated 
and put them back into the original image using seed growing. 

For this the algorithm looks as follows: 
1. we find a center with the main colors we have / the closest color in the entire 
picture and grow the region from there, for this we need a given sensitivity.
    1.1 we repeat this process until we have all centres covered in the image

2. we repeat this process with all given colors
3. if gaps are left open, we lower the sensitivity and grow the closest color 
into those gaps 



The difference for this is that we can't just load pixels as a list, we need 
neighbours of centres


We compare the pixel we're looking at in comparison to the original centre (seed pixel) 
+ 
keeping the sensitivity and maximum distance between each color in the palette in mind 
is crucial for this step 
'''
from collections import deque 

import colors # we're using the previously made code for this
import numpy
from PIL import Image 
import sys




# first algorithm should be from finding the colors we'll use, we'll just use 
# the automatic sensitivity 85 for a good middle ground 
SENS = 85




# load image as 2D, we need neighbours so no flattening
def load_image_2d(path, max_size = 200): #loads pixels, shrink it down to 200px per side at most, max 40k pixels at end
    # Open the image
    img = Image.open(path)
    # convert to RGB    
    img = img.convert("RGB")
    # shrink it with thumbnail, tuple width, height
    img.thumbnail((max_size, max_size))
    return numpy.array(img).astype(int)



# Algorithmus: 
# im img durch alle pixel gehen, die pixel die von der farbe noch in der toleranz sind werden 
# als seed markiert
# Label gibt an ob die farbe schon vergeben ist oder nicht, es müssen pixel übersprungen
# werden die schon einer farbe zugewiesen sind in z.B. palette[].
# somit hat z.b. palette[0] automatisch Vorrang im Vergleich zu palette[1]. 
# 
# Also ersten. :  
def find_seed(img, labels, color, tolerance):
    pass            # None, wenn nichts nah genug ist





def main(): 
    if len(sys.argv) != 2:
        sys.exit("Usage: python region_grow.py image.png")

    sens = SENS 
    inputfile = sys.argv[1]
    path = "input/" + inputfile
    outpath = "output/regions_" + inputfile


    while True:
        raw = input(f"Sensitivity 0-100 (default {SENS}): ").strip()
        if not raw:
            break
        try:
            sens = int(raw)
        except ValueError:
            print("Sensitivity can only be a number between 0-100")
            continue
        if 0 <= sens <= 100:
            break
        print("Sensitivity can only be a number between 0-100")



    # load img 
    img = load_image_2d(path)

    # Get color palllette from colors.py with 
    # load_pixels -> count_colors -> merge_colors -> to_percentages 
    percs = colors.to_percentages(colors.merge_colors(colors.count_colors(colors.load_pixels(path)), sens))
    # atp we have the main colors and we go through all of the colors we want to 
    # for this ig we should now mark the seeds

    # convert percs into a palette 
    palette = get_palette(percs)
    print(palette)
    # we got the color palette, now we search through the image to find proper seeds
    tolerance = colors.MAX_RGB_DISTANCE * (1 - sens / 100)
    labels = numpy.full(img.shape[:2], -1)   # -1 = frei, sonst Index der Palettenfarbe

    for index, color in enumerate(palette): 
        seed = find_seed(img, labels, color, tolerance)
        print(index, color, seed)
    

# helper functions 
def get_palette(percs, min_percent=1):
    ranked = sorted(percs.items(), key=lambda item: item[1], reverse=True)
    return [color for color, p in ranked if p >= min_percent]



if __name__ == "__main__":
    main()
