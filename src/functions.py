'''
Created on Sep 18, 2014

@author: Andre
'''
import math
from functools import reduce


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
