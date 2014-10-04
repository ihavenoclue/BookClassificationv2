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
from numpy import arange,array,ones,linalg
import functions #own package defined in another python file "functions.py"
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import random


###########################################################################
###################### IMPORT AND CLEAN DATA ##############################
###########################################################################

#Define minimum number of characters in a string for it to be considered for training
minstring=300
#Define number of common words wanted for training
numComWords=20
path='C:/Users/Andre/Dropbox/Books/'
#path='C:/Users/lsaloumi/Dropbox/Books/'

#Final table with all features from all books. This will be the input for the training
allFeatures=[]

#Extract most common words in english
os.chdir(path)
comWords = open("lemma.num")
comWords = comWords.read().split("\n")[:-1]
comWords =[row.split(" ")[2] for row in comWords][0:numComWords]

#Authors available for training
authorList=[pathi.split("/")[-1] for pathi in [x[0] for x in os.walk(path)][1:]]

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
            
            ################################
            ### EXTRACT CHAPTER FEATURES####
            ################################
            
            ##Extract common word features
            chFeatures=[word for word in comWords]
            tmp2=text1.lower()
            for c in string.punctuation:
                tmp2= tmp2.replace(c,"")
            tmp2=tmp2.split(" ")
            
            chFeatures=[tmp2.count(word)/len(tmp2) for word in comWords]
            
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
            #Feature3: average number of unique words "per word" 
            avgDifWords=round(len(uniquelist)/len(wordlist),4)
            
            #bookFeaturesi.append([avgSentLength,varSentLength,avgDifWords,len(tmp)])
            bookFeaturesi.append(chFeatures)
        authorFeatures.append(bookFeaturesi)
    
    allFeatures.append(authorFeatures)

############################################################################################
###################### VISUALIZE DATA / CHECK INCONSISTENCIES ##############################
############################################################################################

#Compare features for 2 books

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

#Compare features for one author against all others
author1=0
author2=4

#First 3 features
X,Y,Z=[],[],[]

for author in [i for i in range(len(authorList))]:
    X.append([row[0] for row in reduce(lambda x,y: x+y,allFeatures[author])])
    Y.append([row[1] for row in reduce(lambda x,y: x+y,allFeatures[author])])
    Z.append([row[2] for row in reduce(lambda x,y: x+y,allFeatures[author])])

#XYZ[0] is the first feature for all authors. XYZ[0][0] represents is the 1st feature for the 1st author
XYZ=[]   
tmp=[]
for j in [j for j in range(numComWords)]:
    for author in [i for i in range(len(authorList))]:
        tmp.append([row[j] for row in reduce(lambda x,y: x+y,allFeatures[author])])
    XYZ.append(tmp)
    tmp=[]


#===============================================================================
##XYZ[0] is all the features for the 1st author. XYZ[0][0] represents is the 1st feature for the 1st author
# XYZ=[]   
# tmp=[]
# for author in [i for i in range(len(authorList))]:
#     for j in [j for j in range(numComWords)]:
#         tmp.append([row[j] for row in reduce(lambda x,y: x+y,allFeatures[author])])
#     XYZ.append(tmp)
#     tmp=[]
#===============================================================================

plt.scatter(reduce(lambda x,y: x+y,[X[r] for r in range(len(authorList)) if r!=author1]),reduce(lambda x,y: x+y,[Y[r] for r in range(len(authorList)) if r!=author1]),color="blue")
#plt.scatter(X[author2],Y[author2],color="blue")
plt.scatter(X[author1],Y[author1],color="red")

plt.show()

#################################################################
###################### TRAIN MODEL ##############################
#################################################################

#############################
### Simple linear model #####
#############################
#Vectors of error for each author "isolation"
Ein=[]
Eout=[]
#Define index of training points (chapters) for each client
indexes=[0]+functions.cumulative_sum([len(XYZ[0][r]) for r in range(len(authorList))])
#Total number of training points (all authors)
lAll=indexes[-1]

for author1 in range(len(authorList)):
    
    #Create shuffle index to create validation sets
    shuffled=list(range(lAll))
    random.shuffle(shuffled)
    #Number of training points for the isolated author
    lX=indexes[author1 + 1]
    
    #X matrix for the linear regression ( X[0[] is the feature value for all training points)
    xi= array([reduce(lambda x,y: x+y, XYZ[r]) for r in range(numComWords)])
    A = np.vstack((xi, ones(lAll)))
    
    #Y vector where training points for the isolated author are set to 0
    y=list(ones(lAll))
    y[indexes[author1]:indexes[author1+1]]=[-1 for i in range(indexes[author1+1]-indexes[author1])]
    y=array(y)
    
    #Get linear regression coefficients
    w = linalg.lstsq(A.T,y)[0] # obtaining the parameters
    
    #Derive Ein for the author
    ystar=[np.dot(A.T[i],w.T) for i in range(lAll)]
    error=[elem/math.fabs(elem) for elem in ystar ]+y
    
    Ein.append(len([1 for i in error if i==0])/lAll)

