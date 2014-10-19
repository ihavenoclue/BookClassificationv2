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
from sklearn import metrics
from sklearn import datasets
from sklearn import svm
from sklearn import cross_validation
from sklearn.cross_validation import *
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
#import scipy

###########################################################################
###################### IMPORT AND CLEAN DATA ##############################
###########################################################################
#Define minimum number of characters in a string for it to be considered for training
minstring=300
#Define number of common words wanted for training
numComWords=200
path='C:/Users/Andre/Dropbox/Books/Training/'
pathValidation='C:/Users/Andre/Dropbox/Books/Validation/'
#path='C:/Users/lsaloumi/Dropbox/Books/Training/'
#pathValidation='C:/Users/lsaloumi/Dropbox/Books/Validation/'
#Final table with all features from all books. This will be the input for the training
trainFeatures=[]
testFeatures=[]
#Extract most common words in english
os.chdir(path)
comWords = open("lemma.num")
comWords = comWords.read().split("\n")[:-1]
comWords =[row.split(" ")[2] for row in comWords][0:numComWords]
#Authors available for training
authorList=[pathi.split("/")[-1] for pathi in [x[0] for x in os.walk(path)][1:]]
testList=[pathi.split("/")[-1] for pathi in [x[0] for x in os.walk(pathValidation)][1:]]
nauthors=len(authorList)

#Loop through all the folders present in path
for pathi in [x[0] for x in os.walk(path)][1:]+[x[0] for x in os.walk(pathValidation)][1:]:
    
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
            tmp=functions.extractFeatures(book,ch,minstring,comWords)
            if tmp==False:
                continue
            bookFeaturesi.append(tmp)
        authorFeatures.append(bookFeaturesi)
    if path in pathi:
        trainFeatures.append(authorFeatures)
    if pathValidation in pathi:
        testFeatures.append(authorFeatures)
        

############################################################################################
###################### VISUALIZE DATA / CHECK INCONSISTENCIES ##############################
############################################################################################

#trainMatrix[0] is the first feature for all authors. trainMatrix[0][0] represents is the 1st feature for the 1st author
trainMatrix=[]   
tmp=[]
for j in [j for j in range(numComWords)]:
    for author in [i for i in range(nauthors)]:
        tmp.append([row[j] for row in reduce(lambda x,y: x+y,trainFeatures[author])])
    trainMatrix.append(tmp)
    tmp=[]

testMatrix=[]   
tmp=[]
for j in [j for j in range(numComWords)]:
    for author in [i for i in range(len(testList))]:
        tmp.append([row[j] for row in reduce(lambda x,y: x+y,testFeatures[author])])
    testMatrix.append(tmp)
    tmp=[]



#################################################################
###################### TRAIN MODEL ##############################
#################################################################

#############################
### Simple linear model #####
#############################

#Vectors of error for each author "isolation"
Ein=[]
Eout=[]
#list of linear regression model coefficients for each aithor vs all others
W=[]
#how many buckets do we want to separate the data in for validation ?
nbuckets=20
#Define index of training points (chapters) for each client
indexes=[0]+functions.cumulative_sum([len(trainMatrix[0][r]) for r in range(nauthors)])
#Total number of training points (all authors)
lAll=indexes[-1]


for author1 in range(nauthors):
    
    #Create shuffle index to create validation sets
    shuffled=list(range(lAll))
    random.shuffle(shuffled)
    shuffled=functions.chunks(shuffled,math.ceil(lAll/nbuckets))
    #Number of training points for the isolated author
    lX=indexes[author1 + 1]
    
    #X matrix for the linear regression ( X[0[] is the feature value for all training points)
    xi= array([reduce(lambda x,y: x+y, trainMatrix[r]) for r in range(numComWords)])
    A = np.vstack((xi, ones(lAll)))
    
    #Y vector where training points for the isolated author are set to -1
    y=list(ones(lAll))
    y[indexes[author1]:indexes[author1+1]]=[-1 for i in range(indexes[author1+1]-indexes[author1])]
    y=array(y)
    
    
    #Derive Eout for our model
    ierror=[]
    for bucket in range(len(shuffled)):
        restindex=[i for i in range(lAll) if i not in shuffled[bucket]]
        Atest=A.T[restindex]
        ytest=y[restindex]
        wtest = linalg.lstsq(Atest,ytest)[0]
        
        Aval=A.T[shuffled[bucket]]
        yval=y[shuffled[bucket]]
        ystar=np.dot(Aval,wtest.T)
        ydiff=[elem/math.fabs(elem) for elem in ystar ]+yval
        ierror.append(len([1 for i in ydiff if i==0])/len(shuffled[bucket]))
    Eout.append(np.mean(ierror))
        
        
    #Get linear regression coefficients
    w = linalg.lstsq(A.T,y)[0] # obtaining the parameters
    W.append(w)
    #Derive Ein for the author
    ystar=np.dot(A.T,w.T)
    error=[elem/math.fabs(elem) for elem in ystar ]+y
    
    Ein.append(len([1 for i in error if i==0])/lAll)

print("Number of features used: ",numComWords)
#print("Ein=",[round(elem,5) for elem in Ein])
print("Eout=",[1-math.ceil(elem*10000)/10000 for elem in Eout])
print("mean(Eout)=",1-math.ceil(array(Eout).mean()*10000)/10000)

#test our model
#Define index of training points (chapters) for each client
indexestest=[0]+functions.cumulative_sum([len(testMatrix[0][r]) for r in range(len(testList))])

for author1 in range(len(testList)):
    xitest= array([reduce(lambda x,y: x+y, testMatrix[r]) for r in range(numComWords)]).T
    xitest=xitest[indexestest[author1]:indexestest[author1+1]].T
    Atest = np.vstack((xitest, ones(len(xitest.T))))
    error=[]
    for w in W:
        ytest=np.dot(Atest.T,w.T)
        error.append(sum([1 for i in ytest if i<0]))
    print("Predicted author is ",authorList[error.index(max(error))])
    print("Real author was",testList[author1])
    print(error)


################################
### Support Vector machine #####
################################

#Vectors of error for each author "isolation"
Ein=[]
Eout=[]
#how many buckets do we want to separate the data in for validation ?
nbuckets=20
#Define index of training points (chapters) for each client
indexes=[0]+functions.cumulative_sum([len(trainMatrix[0][r]) for r in range(nauthors)])
#Total number of training points (all authors)
lAll=indexes[-1]

#X matrix for the linear regression ( X[0] is the feature value for all training points)
x= array([reduce(lambda x,y: x+y, trainMatrix[r]) for r in range(numComWords)])


for author1 in range(nauthors):
    
    #Number of training points for the isolated author
    lX=indexes[author1 + 1]
    #Y vector where training points for the isolated author are set to 0
    y=list(ones(lAll))
    y[indexes[author1]:indexes[author1+1]]=[-1 for i in range(indexes[author1+1]-indexes[author1])]
    y=array(y)
    #Derive Ein for the author
    clf = svm.SVC(C=100,kernel='linear')
    scores = cross_validation.cross_val_score(estimator=clf, X=x.T, y=y,cv=cross_validation.StratifiedKFold(y,20,shuffle=True))
    Eout.append(scores.mean())
    tmp=clf.fit(x.T,y)
    Ein.append(clf.score(x.T, y))
    print("Author ",authorList[author1]," is done. ")


print("Number of features used: ",numComWords)
print("Ein=",[math.ceil(elem*10000)/10000 for elem in Ein])
print("Eout=",[math.ceil(elem*10000)/10000 for elem in Eout])


#Multi-Classification
X = x.T
Y = np.repeat(list(range(nauthors)),[len(trainMatrix[0][r]) for r in range(nauthors)])
np.savetxt("C:/Users/Andre/Desktop/featuresmatrix.csv", X, delimiter=",")
np.savetxt("C:/Users/Andre/Desktop/authors.csv", Y, delimiter=",")

clf = svm.SVC(C=100,kernel='linear') #SVC uses a one-against-one classification system
lin_clf=svm.LinearSVC(C=100) #linearSVC uses a one-against-all classification system
scores = cross_validation.cross_val_score(estimator=clf, X=X, y=Y,cv=cross_validation.StratifiedKFold(y,20,shuffle=True))
lin_scores = cross_validation.cross_val_score(estimator=lin_clf, X=X, y=Y,cv=cross_validation.StratifiedKFold(y,20,shuffle=True))
clf.fit(X, Y)
lin_clf.fit(X, Y)


#parameter estimation using grid-search with cross-validation

# Split the dataset in two equal parts
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.1, random_state=0)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000,10000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000,10000,100000]},
                     {'kernel': ['poly'], 'C': [100, 1000,10000,100000],'degree':[1,100]}]

#scores = ['precision', 'recall', 'accuracy']
score='accuracy'

print("# Tuning hyper-parameters for %s" % score)
print()

clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=cross_validation.StratifiedKFold(y_train,20,shuffle=True), scoring=score)
clf.fit(X_train, y_train)

print("Best parameters set found on development set:")
print()
print(clf.best_estimator_)
print()
print("Grid scores on development set:")
print()
for params, mean_score, scores in clf.grid_scores_:
    print("%0.3f (+/-%0.03f) for %r"
          % (mean_score, scores.std() / 2, params))

print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
y_true, y_pred = y_test, clf.predict(X_test)
target_names = authorList
print(classification_report(y_true, y_pred,target_names=target_names))
print()
