#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[1]:


import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!


# ## Extracting Zip FIles into read mode

# In[2]:


import os
#os.mkdir('small_zip') #directory will be made only once
local_zip='readonly/small_img.zip'
zip_ref=zipfile.ZipFile(local_zip,'r')
zip_ref.extractall('small_img')
zip_ref.close()


#os.mkdir('images') #directory will be made only once
local_zip = 'readonly/images.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('images')
zip_ref.close()


# ## Generating a Global list

# In[3]:



#list that contains the images names
plist=os.listdir('small_img')

Global_list=[]
for pname in plist:
    local_list=[] 
    
    #local list = [ page_name , tesseract_text ] 
    
    local_list.append(pname)
    img = Image.open('small_img/'+pname)
    
    local_list.append(pytesseract.image_to_string(img).replace('-\n',''))

    Global_list.append(local_list)


# ## Function to look for faces
# 

# In[4]:


def func_search(text,folder):
    for local_list in Global_list:
        if text in local_list[1]:
            print('Results found in file',local_list[0])
            
            try:
                img = Image.open(str(folder+local_list[0]))
                faces = (face_cascade.detectMultiScale(np.array(img),1.35,4)).tolist()
                #storing the bounding boxes of all faces detected in each image of iteration
                faces_in_each = []
                
                for x,y,w,h in faces:
                    faces_in_each.append(img.crop((x,y,x+w,y+h)))
                      #modifying local data structure in each iteration to sotre PIL Image of each face
                      #display((img.crop((x,y,x+w,y+h))).resize((110,110)))
                
                contact_sheet = Image.new(img.mode, (550,110*int(np.ceil(len(faces_in_each)/5))))
                 #contact sheet modification to display each iteration's result
                x = 0
                y = 0

                for face in faces_in_each:
                    face.thumbnail((110,110))
                    #using HINT 4
                    contact_sheet.paste(face, (x, y))
                    
                    if x+110 == contact_sheet.width:
                        x=0
                        y=y+110
                    else:
                        x=x+110
                        
                display(contact_sheet)
            except:
                print('NO faces FOUND!')


# ## Testing

# In[5]:


func_search("Christopher",'small_img/')


# ## Repeating process for Images.zip

# In[6]:



#list that contains the images names
plist=os.listdir('images')

Global_list=[]
for pname in plist:
    local_list=[] 
    
    #local list = [ page_name , tesseract_text ] 
    
    local_list.append(pname)
    img = Image.open('images/'+pname)
    
    local_list.append(pytesseract.image_to_string(img).replace('-\n',''))

    Global_list.append(local_list)


# ## Testing

# In[7]:


func_search(text="Mark",folder='images/')


# In[ ]:





# In[ ]:




