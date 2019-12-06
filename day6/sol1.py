#!/usr/bin/env python
# coding: utf-8

# In[42]:


with open('input.txt') as inf:
    DATA = inf.read()

arcs = [l.split(')') for l in DATA.splitlines()]
reverse = dict(list(zip(*list(zip(*arcs))[::-1])))

def path(start):
    n = 0
    curr = start
    while curr != 'COM':
        curr = reverse[curr]
        n += 1
    return n

print(sum(path(s) for s in reverse.keys() | reverse.values()))


# In[ ]:




