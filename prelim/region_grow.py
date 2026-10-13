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

import colors # we're using the previously made code for this