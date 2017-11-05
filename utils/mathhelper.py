#!/mnt/sda1/opkg/usr/bin/python
# #encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import itertools
'''
http://blog.csdn.net/mad1989/article/details/9150157
'''

def GetPermu(lists,n=2):
    #lists=['a','b','c','d','e']     5*4
    #[('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'a'), ('b', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'a'), ('c', 'b'), ('c', 'd'), ('c', 'e'), ('d', 'a'), ('d', 'b'), ('d', 'c'), ('d', 'e'), ('e', 'a'), ('e', 'b'), ('e', 'c'), ('e', 'd')]
    nlists=list(itertools.permutations(lists,n))
    return nlists

def GetCombi(lists,n=2):
    #lists=['a','b','c','d','e']     5*4/2*1  no order
    nlists=list(itertools.combinations(lists,n))
    return nlists

