#!/usr/bin/env python
# coding: utf-8

# In[8]:


PATTERN = 0, 1, 0, -1


# In[9]:


from itertools import repeat, chain, islice, cycle, tee

def pat(n):
    base = chain.from_iterable(repeat(d, n + 1) for d in PATTERN)
    return islice(cycle(base), 1, None)

def pi(l, m):
    return sum(x * y for x, y in zip(l, m))

def fft_step(s):
    res = [abs(pi(s, pat(n))) % 10 for n in range(len(s))]
    return res

def fft(s, n):
    s = list(map(int, s))
    for _ in range(n):
        s = fft_step(s)
    return ''.join(map(str, s))


# In[10]:


pi([9, 8, 7, 6, 5], cycle([1,2,3])) ==  9*1 + 8*2 + 7*3 + 6*1 + 5*2


# In[11]:


fft_step(list(map(int, '12345678'))) == [4, 8, 2, 2, 6, 1, 5, 8]


# In[12]:


fft_step(list(map(int, '48226158'))) == [3, 4, 0, 4, 0, 4, 3, 8]


# In[13]:


fft('80871224585914546619083218645595', 100)


# In[14]:


IN = '59718730609456731351293131043954182702121108074562978243742884161871544398977055503320958653307507508966449714414337735187580549358362555889812919496045724040642138706110661041990885362374435198119936583163910712480088609327792784217885605021161016819501165393890652993818130542242768441596060007838133531024988331598293657823801146846652173678159937295632636340994166521987674402071483406418370292035144241585262551324299766286455164775266890428904814988362921594953203336562273760946178800473700853809323954113201123479775212494228741821718730597221148998454224256326346654873824296052279974200167736410629219931381311353792034748731880630444730593'


# In[39]:


get_ipython().run_line_magic('time', 'x = fft(IN, 1)')


# In[26]:


def skip(l, n):
    for i, e in enumerate(l, 1):
        if i == 1 or i % n == 0: continue
        yield e    

class SV:
    def __init__(self, sv, start = None, stop = None, step = None, skip = None):
        self.start = start
        self.stop = stop
        self.step = step
        self.skip = skip
        if isinstance(sv, SV):
            self.sv = sv
        else:
            self.sv = None
            self.list = sv[:]
    def __iter__(self):
        if self.skip is not None:
            return skip(
                iter(self.list) if self.sv is None else iter(self.sv),
                self.skip
            )
        return islice(
            iter(self.list) if self.sv is None else iter(self.sv),
            self.start, self.stop, self.step
        )


# In[31]:


s = SV(list(range(20)), 1)
t = SV(s, 1, None, 2)
u = SV(t, None, 2)
v = SV(t, skip = 3)
z = SV(v, skip = 2)
list(s), list(t), list(u), list(v), list(z)


# In[49]:


def pos(l, n):
    print(n, l)
    if n == 1:
        return '({})-({})'.format('+'.join(map(str, l[::4])), '+'.join(map(str,l[2::4])))
    if n % 2 == 0:
        return pos(l[1::2], n // 2) + '+' + pos(l[2::2], n // 2)
    else:
        a, b = [], []
        for i, e in enumerate(l, 1):
            (a if i % n == 0 else b).append(e)
        #print(a,b[1:])
        #print(l[(n-1)::n], list(skip(l, n)))
        return pos(a, 1) + '+' + pos(b[1:], n - 1)    


# In[53]:


pos(list(range(1, 200)), 200)


# In[34]:


def nfft(l, n):
    #print(n, list(l))
    if n == 1:
        return sum(SV(l, 0, None, 4)) - sum(SV(l, 2, None, 4))
    if n % 2 == 0:
        return (
            nfft(SV(l, 1, None, 2), n // 2) + 
            nfft(SV(l, 2, None, 2), n // 2)
        )
    else:
        return (
            nfft(SV(l, n - 1, None, n), 1) +
            nfft(SV(l, skip = n), n - 1)
        )


# In[35]:


def anfft(s):
    res = []
    l = list(map(int, s))
    for n in range(1, 1 + len(s)):
        res.append(abs(nfft(SV(l), n)) % 10)
    return ''.join(map(str, res))

def canfft(s, n):
    for _ in range(n):
        s = anfft(s)
    return s


# In[38]:


get_ipython().run_line_magic('time', 'x = canfft(IN, 1)')


# In[43]:


l = list(range(1000000))


# In[45]:


get_ipython().run_line_magic('time', 'll = list(skip(l, 3))')


# In[ ]:




