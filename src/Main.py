'''
Created on Aug 5, 2014

@author: lsaloumi
'''

import epub
import os
from functools import reduce
from bs4 import BeautifulSoup
import string
import numpy as np
import functions #own package defined in another python file "functions.py"
import matplotlib.pyplot as plt
from matplotlib import cm


###########################################################################
###################### IMPORT AND CLEAN DATA ##############################
###########################################################################

#Define minimum number of characters in a string for it to be considered for training
minstring=50

#Final table with all features from all books. This will be the input for the training
allFeatures=[]

path='C:/Users/Andre/Dropbox/Books/'

#Loop through all the folders present in path
for pathi in [x[0] for x in os.walk(path)][1:]:
    
    authorFeatures=[]
    #Get all epub books from the current directory
    books=[file for file in os.listdir(pathi) if file.endswith(".epub")]
    os.chdir(pathi)
    #Loop on all books from that directory
    for bookName in books:

        #Open the epub book as an object thanks to the epub package
        book = epub.open_epub(bookName)
        
        #Get all chapters "names" from the book
        chapterNames = [book.get_item(item_id).href for item_id, linear in book.opf.spine.itemrefs]
        chapterNames = [ch for ch in chapterNames if ch[:2]=='ch']
        
        bookFeaturesi=[]
        #Loop on the chapter in current book
        for ch in chapterNames:

            #Read the chapter from epub file as a string
            text = book.read_item(ch).decode("utf-8")
            
            #Convert to BS text for html processing
            soup = BeautifulSoup(text)

            #Remove all the html tags from the string
            for tag in soup.find_all('strong'):
                tag.replaceWith('')
            text1=soup.get_text()

            #If only one sentence or less, skip to next chapter
            if len(text1.split("."))==1:
                print("Skipping "+ch+" in "+bookName)
                print("Reason: only one sentence \""+text1)
                continue
            
            #Delete the first Chapter strings that are annoying
            text1=functions.cleanup(text1)
            text1=functions.cleanup(text1)
            
            text1 = text1.replace('\n', ' ')
            
            #If string is too short, don't consider it for training
            if len(text1)<minstring:
                print("Skipping "+ch+" in "+bookName+ " : less than "+str(minstring)+" characters \""+text1+"\"")
                continue
            #text1 = text1.replace('\\', '')
            
            ### EXTRACT CHAPTER FEATURES
            ## average sentence length
            tmp=text1.split(".")
            
            
            tmp=[len(sentence.split()) for sentence in tmp]
            #Feature1: average sentence length
            avgSentLength= round(reduce(lambda x, y: x + y, tmp) / len(tmp),2)
            #Feature2: sentence length standard deviation
            varSentLength=round(functions.stddv(tmp),2)
            
            tmp2=text1.lower()
            for c in string.punctuation:
                tmp2= tmp2.replace(c,"")
            
            wordlist=tmp2.split()
            uniquelist=list(set(wordlist))
            #Feature3: aveage number of unique words "per word" 
            avgDifWords=round(len(uniquelist)/len(wordlist),4)
            
            bookFeaturesi.append([avgSentLength,varSentLength,avgDifWords,len(tmp)])
        
        authorFeatures.append(bookFeaturesi)
    
    allFeatures.append(authorFeatures)

############################################################################################
###################### VISUALIZE DATA / CHECK INCONSISTENCIES ##############################
############################################################################################

x1=[row[0] for row in allFeatures[1][1]]
y1=[row[1] for row in allFeatures[1][1]]
z1=[row[2] for row in allFeatures[1][1]]

x2=[row[0] for row in allFeatures[2][1]]
y2=[row[1] for row in allFeatures[2][1]]
z2=[row[2] for row in allFeatures[2][1]]

plt.scatter(x1,y1,color="red")
plt.scatter(x2,y2,color="blue")

plt.scatter(x1,z1,color="red")
plt.scatter(x2,z2,color="blue")
plt.show()





