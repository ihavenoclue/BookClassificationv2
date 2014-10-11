'''
Created on Sep 18, 2014

@author: Andre
'''
import math
from functools import reduce
from bs4 import BeautifulSoup
import string

def stddv(mylist):
    '''This derives the standard deviation of the numbers in the list
    '''
    avg= reduce(lambda x, y: x + y, mylist) / len(mylist)
    stddv=0
    for number in mylist:
        stddv=stddv+(number-avg)**2
    stddv=math.sqrt(stddv/(len(mylist)-1))
    return stddv

def cumulative_sum(L):
    CL = []
    csum = 0
    for x in L:
        csum += x
        CL.append(csum)
    return CL

def chunks(list, n):
    if n < 1:
        n = 1
    return [list[i:i + n] for i in range(0, len(list), n)]

def cleanup(mystring):
    '''This cleans up leading strings from an epub string if an expression is repeated twice in the same configuration in the beginning.
        For example, if myword="Chapter ", "Chapter I. ChapterI." or "Chapter IChapter I" will be removed because the same pattern with myword is repeated twice.
    '''
    cnt=0
    while cnt==0:
        cnt=1
        if len(mystring)>1:
            myword=mystring.split(' ', 1)[0]
            if myword in mystring.split(' ',1)[1]:
                if mystring[0:mystring.index(myword,1)]==mystring[mystring.index(myword,1):mystring.index(myword,1)*2]:
                    mystring=mystring[mystring.index(myword,1)*2:]
                    cnt=0
    return(mystring)

def extractFeatures(book,ch,minstring,comWords):
    text = book.read_item(ch).decode("utf-8")
    
    #Convert to BS text for html processing
    soup = BeautifulSoup(text)
    
    #Remove all the html tags from the string
    for tag in soup.find_all('strong'):
        tag.replaceWith('')
    text1=soup.get_text()
    
    #If only one sentence or less, skip to next chapter
    if len(text1.split("."))==1:
        #print("Skipping "+ch+" in "+bookName)
        #print("Reason: only one sentence \""+text1)
        return(False)
    
    #Delete the first Chapter strings that are annoying
    text1=cleanup(text1)
    text1=cleanup(text1)
    
    text1 = text1.replace('\n', ' ')
    
    #If string is too short, don't consider it for training
    if len(text1)<minstring:
        #print("Skipping "+ch+" in "+bookName+ " : less than "+str(minstring)+" characters \""+text1+"\"")
        return(False)
    
    ################################
    ### EXTRACT CHAPTER FEATURES####
    ################################
    
    ##Extract common word features
    tmp2=text1.lower()
    for c in string.punctuation:
        tmp2= tmp2.replace(c,"")
    tmp2=tmp2.split(" ")
    
    chFeatures=[tmp2.count(word)/len(tmp2) for word in comWords]
    
    ## average sentence length
    #tmp=text1.split(".")
    #tmp=[len(sentence.split()) for sentence in tmp]
    ##Feature1: average sentence length
    #avgSentLength= round(reduce(lambda x, y: x + y, tmp) / len(tmp),2)
    #Feature2: sentence length standard deviation
    #varSentLength=round(stddv(tmp),2)
    
    #tmp2=text1.lower()
    #for c in string.punctuation:
    #    tmp2= tmp2.replace(c,"")
    
    #wordlist=tmp2.split()
    #uniquelist=list(set(wordlist))
    ##Feature3: average number of unique words "per word" 
    #avgDifWords=round(len(uniquelist)/len(wordlist),4)
    
    #bookFeaturesi.append([avgSentLength,varSentLength,avgDifWords,len(tmp)])
    return(chFeatures)


