# -*- coding: utf-8 -*-
#================================================
# 
# scrapAPOD.py
# 
# Python script to scrap pictures from NASA's Astronomy Picture of the Day (APOD) website.
#
# Written by: Matheus Inoue, 2018, Federal University of ABC (UFABC)
#=================================================

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import glob




def downloadPicture(linkPic, picName):
    b = requests.get(linkPic)
    soup = BeautifulSoup(b.text, 'lxml')
    
    try:
        picSuffix = soup.find('img')['src']
        fileExt = re.findall('\.([\w\d]+)', picSuffix)[-1]
        linkJPG = linkPreffix + picSuffix
        print('Downloading the picture for {} from {} =D'.format(re.findall('\d{4}_\d{2}_\d{2}',picName)[0], linkPic))
        c = requests.get(linkJPG)
        
        file = open('pics//'+picName+'.'+fileExt,'wb') 
        file.write(bytes(c.content))
        file.close() 
    except:
        print('The file for {} is not a picture file =('.format(re.findall('\d{4}_\d{2}_\d{2}',picName)[0]))




link = 'https://apod.nasa.gov/apod/archivepix.html'
linkPreffix = 'https://apod.nasa.gov/apod/'

a = requests.get(link)
soup = BeautifulSoup(a.text, 'lxml')

boldText = soup.find('b')

regexDate = re.findall('\d{4} \w+ \d{1,2}:[^\n]+', str(boldText))


listJPGfiles = glob.glob('pics\*.jpg')
setPicsStored = set(os.path.basename(f)[:-4] for f in listJPGfiles)    

nPics = input('From '+str(len(regexDate))+' pictures of the day, how many do you want to download, starting from newest images?\n:')
    
for day in regexDate[:int(nPics)]:
    soupDay = BeautifulSoup(day, 'lxml')
    linkSuffix = soupDay.find('a')['href']
    date = re.findall('\d{4} \w+ \d{1,2}', day)[0]
    date = datetime.strftime(datetime.strptime(date, '%Y %B %d'), '%Y_%m_%d')
    
    picTitle = soupDay.find('a').text
    picName = date+' - '+picTitle.replace(':', ' -')
    
    if picName not in setPicsStored:
        linkPic = linkPreffix+linkSuffix
        downloadPicture(linkPic, picName)
    else:
        continue

    
   