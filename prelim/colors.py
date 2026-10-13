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
from PIL import Image, ImageOps
import matplotlib.pyplot as plt 

import sys 

MAX_RGB_DISTANCE = np.sqrt(3) * 255  # distance from black (0,0,0) to white (255,255,255), used later for percentage distance between two colors

# helper functions 

def distance(c1, c2): 
    # return the Euclidian distance between two RGB tuples , what this means is 
    # that RGB will be viewed at as a Cube, 3D inherently 
    # Use the formula: √((R₁−R₂)² + (G₁−G₂)² + (B₁−B₂)²)
    # distance((0,0,0), (255,255,255)) = 441.67
    r1, g1, b1 = c1
    r2, g2, b2 = c2 
    dist = np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) 
    return dist



# --- Load Image ---
def load_pixels(path, max_size = 200): #loads pixels, shrink it down to 200px per side at most, max 40k pixels at end
    # Open the image
    img = Image.open(path)
    # convert to RGB    
    img = img.convert("RGB")
    # shrink it with thumbnail, tuple width, height
    img.thumbnail((max_size, max_size))
    # Turn it into a NumPy Array 
    arr = np.array(img)
    return arr.reshape(-1, 3) # flattens into long list of pixels, each with 3 values 

# --- Count exact colors and calculate percentages --- 
def count_colors(pixels, step = 8): 
    colordict = {}  # so we're making a dict
        # count every color, make a table with each color and the amount it shows up in the image? 
    for pixel in pixels: 
        color = tuple(int(v) // step * step for v in pixel)# logs every pixel, kinda divides the colors into bytes instead of distinct colors
        colordict[color] = colordict.get(color, 0) + 1 
    return colordict


# we're looking at the most voted colors, these are centres we're looking at 
# from there we tolerate a certain variance of sensitivity as distance 
# those colors are summarised under the same centre 

#--- merge similar colors depending on sensitivity, already weight it here--- 
def merge_colors(counts, sens):
    newdict = {} 
    tolerance = MAX_RGB_DISTANCE * (1 - sens / 100)    
    order = sorted(counts, key = counts.get, reverse = True)
    # print (order[:5])
    # so for each pixel we run through the distance thing and return dist and 
    # check if it falls iwthin the treshold, if yes we add that vote / we take 
    # into consideration its weight to later evaluate the final color
    used = set()
    for center in order: 
        if center in used: 
            continue 
        total = 0 
        r_sum = g_sum = b_sum = 0
        for color in order: 
            if color not in used and distance(center, color) <= tolerance: 
                used.add(color)
                count = counts[color]
                total += count
                r, g, b = color # tuple unpacking
                r_sum += r * count 
                g_sum += g * count 
                b_sum += b * count
        avg = (round(r_sum/total), round(g_sum/total), round(b_sum/total))
        newdict[avg] = newdict.get(avg, 0) + total
    return newdict


def to_percentages(counts):
    #we look at how many pixels we have and which amount these pixels 
    # we're looking at now make up / the ones we voted for 
    # for this we look at newdict and its size and divide it for each center
    size = sum(counts.values() ) # gives us all pixels 
    perc = {}
    for color, count in counts.items(): 
        # we divide the count incounts through size 
        # then write it in perc 
        perc[color] = count / size * 100
    
    return perc








# ----------Histogram output instead CLI NOTE: later implementation should make
# groups on an image, not histogram, this is just for now 
# we're going to ignore colors under 1% btw
def histogram(percs, outpath):
    # keep only colors with at least 1%
    kept = [(color, p) for color, p in percs.items() if p >= 1]
    # largest first
    kept = sorted(kept, key=lambda item: item[1], reverse=True)

    # matplotlib wants 0-1 instead of 0-255 -> divide each channel by 255
    colors = [(r / 255, g / 255, b / 255) for (r, g, b), p in kept]
    heights = [p for color, p in kept]

    plt.bar(range(len(heights)), heights, color=colors, edgecolor="black")
    plt.ylabel("% of pixels")
    plt.title("Color distribution")

    labels = ["#%02x%02x%02x" % c for c, p in kept]
    plt.xticks(range(len(heights)), labels, rotation=90)
    plt.tight_layout()

    plt.savefig(outpath)
    plt.close()







def main(): 
    # ask for input from user python colors.py file.png Sensitivity
    # So we expect three inputs 
    
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    sens = 85
    while True:
        raw = input("Sensitivity 0-100 (default 85): ").strip()
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

    pixels = load_pixels(path)    
    counts = count_colors(pixels) #colordict with ALL colors
    newdict = merge_colors(counts, sens)
    
    # print(counts)
    # finalcolors = merge_colors(counts, sens)
    # print (newdict)

    percentages = to_percentages(newdict)
    print(percentages)

    histogram(percentages, outpath)

    





if __name__ == "__main__":
    main()