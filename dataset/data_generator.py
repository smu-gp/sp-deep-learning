
# coding: utf-8

# In[1]:


#!/usr/bin/env python
#-*-coding:cp949-*-

import glob
import io
import os
import random

import numpy
from PIL import Image, ImageFont, ImageDraw
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter




# Default data paths.
DEFAULT_LABEL_FILE ='./labels/2350-common-hangul.txt'
DEFAULT_FONTS_DIR ='./fonts/'
DEFAULT_OUTPUT_DIR_IMAGE = './image-data'
DEFAULT_OUTPUT_DIR_XML='./xml'
# Number of random distortion images to generate per font and character.
DISTORTION_COUNT = 3

# Width and height of the resulting image.
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500



def elastic_distort(image, alpha, sigma):
  """Perform elastic distortion on an image.
  Here, alpha refers to the scaling factor that controls the intensity of the
  deformation. The sigma variable refers to the Gaussian filter standard
  deviation.
  """
  random_state = numpy.random.RandomState(None)
  shape = image.shape
  dx = gaussian_filter((random_state.rand(*shape) * 2 - 1),sigma, mode="constant") * alpha
  dy = gaussian_filter((random_state.rand(*shape) * 2 - 1),sigma, mode="constant") * alpha
  x, y = numpy.meshgrid(numpy.arange(shape[0]), numpy.arange(shape[1]))
  indices = numpy.reshape(y+dy, (-1, 1)), numpy.reshape(x+dx, (-1, 1))
  return map_coordinates(image, indices, order=1).reshape(shape)
  """Generate Hangul image files.
  This will take in the passed in labels file and will generate several
  images using the font files provided in the font directory. The font
  directory is expected to be populated with *.ttf (True Type Font) files.
  The generated images will be stored in the given output directory. Image
  paths will have their corresponding labels listed in a CSV file.
  """
    
    
    
label_file = DEFAULT_LABEL_FILE
img_output_dir = DEFAULT_OUTPUT_DIR_IMAGE
xml_output_dir = DEFAULT_OUTPUT_DIR_XML
fonts_dir = DEFAULT_FONTS_DIR

with io.open(label_file, 'r', encoding='utf-8') as f:
  labels = f.read().splitlines()
image_dir = os.path.join(img_output_dir, 'hangul-images')
xml_dir = os.path.join(xml_output_dir,'hangul-annotation')
if not os.path.exists(image_dir):
  os.makedirs(os.path.join(image_dir))

if not os.path.exists(xml_output_dir):
  os.makedirs(os.path.join(xml_dir))
# Get a list of the fonts.
fonts = glob.glob(os.path.join(fonts_dir, '*.ttf'))


total_count = 0
prev_count = 0

for character in labels:
  if len(character) == 2 :
    ncharacter = character[1]
    character = ncharacter+""
    # Print image count roughly every 5000 images.
  if total_count - prev_count > 5000:
    print("no error")
    prev_count = total_count
    print('{} images generated...'.format(total_count))
  for font in fonts:
    fontpoint = numpy.random.randint(15,40)
    get_x = numpy.random.randint(0,450)
    get_y = numpy.random.randint(0,450)
    total_count += 1
    image = Image.new('L', (IMAGE_WIDTH, IMAGE_HEIGHT), color=0)
    font = ImageFont.truetype(font, fontpoint)
    drawing = ImageDraw.Draw(image)
    w, h = drawing.textsize(character, font=font)
    #drawing.text(get_x, get_y ,character,fill=(255),font=font)
    drawing.text((get_x, get_y),character,fill=(255),font=font)
    file_string = 'hangul_{}.jpeg'.format(total_count)
    file_path = os.path.join(image_dir, file_string)
    image.save(file_path, 'JPEG')
        

    for i in range(DISTORTION_COUNT):
      total_count += 1
      file_string = 'hangul_{}.jpeg'.format(total_count)
      file_path = os.path.join(image_dir, file_string)
      arr = numpy.array(image)
      distorted_array = elastic_distort(arr, alpha=random.randint(30, 36),sigma=random.randint(5, 6))
      distorted_image = Image.fromarray(distorted_array)
      distorted_image.save(file_path, 'JPEG')    
      xml_file_string = 'hangul_{}.xml'.format(total_count) 
      xml_file_path = os.path.join(xml_dir,xml_file_string)           
      f1 = open('frame.txt','r',encoding='utf8')
      f2 = open(xml_file_path,'w',encoding='utf8')
      lines = f1.readlines()
      for i in range(0,len(lines)):
        if "<folder>" in lines[i]:
          lines[i] = lines[i].replace("<folder>","<folder>"+str(img_output_dir))
        if "<filename>" in lines[i]:
          lines[i]=lines[i].replace("<filename>","<filename>"+str(file_string))
        if "<width>" in lines[i] :
          lines[i]=lines[i].replace("<width>","<width>"+str(w))
        if "<height>" in lines[i] :
          lines[i]=lines[i].replace("<height>","<height>"+str(h))
        if "<name>" in lines[i] :
          lines[i]=lines[i].replace("<name>","<name>"+ str(character))
        if "<xmin>" in lines[i] :
          lines[i]=lines[i].replace("<xmin>","<xmin>"+str(get_x))
        if "<ymin>" in lines[i] :
          lines[i]=lines[i].replace("<ymin>","<ymin>"+str(get_y))
        if "<xmax>" in lines[i] :
          lines[i]=lines[i].replace("<xmax>","<xmax>"+str(get_x+w))
        if "<ymax>" in lines[i] :
          lines[i]=lines[i].replace("<ymax>","<ymax>"+str(get_y+h))
            
      f2.writelines(lines)        

      f1.close()

      f2.close()
            
print('Finished generating {} images.'.format(total_count))






