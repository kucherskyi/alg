#!venv/bin/python

import random
import timeit



li = []

for i in xrange(10):
    li.append(random.randint(0, 100))

print "list : {}" .format(li)

# The Insertion Sort


def insertion(li):
    for i in range(1, len(li)):
        cur = li[i]
        pos = i
        while pos > 0 and li[pos - 1] > cur:
            li[pos] = li[pos - 1]
            pos = pos - 1
        li[pos] = cur
insertion(li)


# The Quick Sort
def quick(li):
    if not li:
        return []
    pivots = [x for x in li if x == li[0]]
    less = quick([x for x in li if x < li[0]])
    more = quick([x for x in li if x > li[0]])
    return less + pivots + more
quick(li)


# The Selection Sort
def selection(li):
    for enem in range(len(li) - 1, 0, -1):
        maxValue = 0
        for location in range(1, enem + 1):
            if li[location] > li[maxValue]:
                maxValue = location
        temp = li[enem]
        li[enem] = li[maxValue]
        li[maxValue] = temp
selection(li)


# The Merge Sort
def merges(li):
    if len(li) > 1:
        mid = len(li) // 2
        left = li[:mid]
        right = li[mid:]
        merges(left)
        merges(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                li[k] = left[i]
                i = i + 1
            else:
                li[k] = right[j]
                j = j + 1
            k = k + 1
        while i < len(left):
            li[k] = left[i]
            i = i + 1
            k = k + 1
        while j < len(right):
            li[k] = right[j]
            j = j + 1
            k = k + 1
merges(li)


print timeit.timeit(stmt="""
import random
li = []

for i in xrange(10):
  li.append(random.randint(0,100))
def insertion(li):
   for i in range(1,len(li)):

     cur = li[i]
     pos = i

     while pos>0 and li[pos-1]>cur:
         li[pos]=li[pos-1]
         pos = pos-1

     li[pos]=cur


insertion(li)


""", number=100000)

print timeit.timeit(stmt="""
import random
li = []

for i in xrange(10):
  li.append(random.randint(0,100))
def selection(li):
   for enem in range(len(li)-1,0,-1):
       maxValue=0
       for location in range(1,enem+1):
           if li[location]>li[maxValue]:
               maxValue = location

       temp = li[enem]
       li[enem] = li[maxValue]
       li[maxValue] = temp


selection(li)

""", number=100000)

print timeit.timeit(stmt="""
import random
li = []

for i in xrange(10):
  li.append(random.randint(0,100))
def merges(li):
    if len(li)>1:
        mid = len(li)//2
        left = li[:mid]
        right = li[mid:]

        merges(left)
        merges(right)

        i=0
        j=0
        k=0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                li[k]=left[i]
                i=i+1
            else:
                li[k]=right[j]
                j=j+1
            k=k+1

        while i < len(left):
            li[k]=left[i]
            i=i+1
            k=k+1

        while j < len(right):
            li[k]=right[j]
            j=j+1
            k=k+1

merges(li)

""", number=100000)

print timeit.timeit(stmt="""
import random
li = []

for i in xrange(10):
  li.append(random.randint(0,100))
def quick(li):
    if not li:
        return []

    pivots = [x for x in li if x == li[0]]
    less = quick([x for x in li if x < li[0]])
    more = quick([x for x in li if x > li[0]])
    return less + pivots + more

quick(li)

""", number=100000)
