#!/usr/bin/env python
#coding=utf-8
# translate word into id in documents
from __future__ import print_function
import sys


w2id = {}

def indexFile(pt, res_pt):
    print('index file: '+str(pt))
    wf = open(res_pt, 'w')
    for l in open(pt):
        ws = l.strip().split()
        wids = list()
        for w in ws:
            if w in w2id:
                wids.append(w2id[w])
            else:
                wids.append("0")
        print(' '.join(map(str, wids)), file=wf)
    print('write file: '+str(res_pt))


def loadDict(vocab_file):
    vf = open(vocab_file, 'r')
    for l in vf:
        id, word = l.split()
        w2id[word] = id
    print(len(w2id))
    vf.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python %s <doc_pt> <dwid_pt> <voca_pt>' % sys.argv[0])
        print('\tdoc_pt    input docs to be indexed, each line is a doc with the format "word word ..."')
        print('\tdwid_pt   output docs after indexing, each line is a doc with the format "wordId wordId..."')
        print('\tvoca_pt   input vocabulary file, each line is a word with the format "wordId    word"')
        exit(1)
        
    doc_pt = sys.argv[1]
    dwid_pt = sys.argv[2]
    voca_pt = sys.argv[3]
    loadDict(voca_pt)
    indexFile(doc_pt, dwid_pt)
    print('n(w)='+str(len(w2id)))
