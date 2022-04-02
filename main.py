from pprint import pprint
import numpy
#from sympy import Sum
from Parser import Parser
import util
import os
import pathlib
import math
from textblob import TextBlob as tb
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='query')
    parser.add_argument('--query', default='')
    parser.add_argument('--type', default='')
    return parser

class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None


    def __init__(self, documents=[]):
        self.documentVectors=[]
        self.parser = Parser()
        if(len(documents)>0):
            self.build(documents)

    def build(self,documents):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        #self.documentVectors = [self.makeVector(document) for document in documents]

        type_ = int(args.type)
        if type_ == 1:
             self.documentVectors = [self.TFWeightingVector(document) for document in documents]
        elif type_ == 2:
             self.documentVectors = [self.TFWeightingVector(document) for document in documents]
        elif type_ == 3:
            self.documentVectors = [self.TF_IDFWeightingVector(document) for document in documents]
        else:
            self.documentVectors = [self.TF_IDFWeightingVector(document) for document in documents]
       
        #print(documents)
        #print(self.vectorKeywordIndex)
        #print(self.documentVectors)


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def TFWeightingVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
            #tf = vector[self.vectorKeywordIndex[word]] / len(wordList)
        return vector 


    def TF_IDFWeightingVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        vectorlen = sum(vector)
        TFVector = [x / vectorlen for x in vector]      
        return TFVector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        #query = self.makeVector(" ".join(termList))
        """ convert query string into a term Frequency vector """
        type_ = int(args.type)
        if type_ == 1:
            query = self.TFWeightingVector(" ".join(termList))
        elif type_ == 2:
            query = self.TFWeightingVector(" ".join(termList))
        elif type_ == 3:
            query = self.TF_IDFWeightingVector(" ".join(termList))
        else:
            query = self.TF_IDFWeightingVector(" ".join(termList))
        
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        type_ = int(args.type)
        if type_ == 1:
            ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        elif type_ == 2:
            ratings = [util.euclidean(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        elif type_ == 3:
            ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        else:
            ratings = [util.euclidean(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)

        #ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        type_ = int(args.type)
        if type_ == 1:
            ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        elif type_ == 2:
            ratings = [util.euclidean(queryVector, documentVector) for documentVector in self.documentVectors]
        elif type_ == 3:
            ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        else:
            ratings = [util.euclidean(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings = [util.euclidean(queryVector, documentVector) for documentVector in self.documentVectors]

        #ratings.sort(reverse=True)
        return ratings

    def tf(self,word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(self,word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self,word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))

    def tfidf(self,word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)


if __name__ == '__main__':
     
     #get query
     parser = get_parser()
     args = parser.parse_args()
     type_ = args.type
     print('query: ' + args.query)
     print('type: ' + args.type)
     
     #test data
     """      documents = ["The cat in the hat disabled",
                  "A cat is a fine pet ponies cat.",
                  "Dogs and cats make good good good pets pets.",
                  "I haven't got a hat."]
     """
     # Define the location of the directory
     path =r"Vector Space Model/EnglishNews"
     # Change the directory
     os.chdir(path)
     documentsName = []
     documents = []
     # Iterate over all the files in the directory
     for file in os.listdir():
          if file.endswith('.txt'):
          # Create the filepath of particular file
              file_path =f"{path}/{file}"
              with open(file_path, 'r', encoding='utf-8') as file:
                  filename = pathlib.Path(file_path).stem
                  documentsName.append(filename)
                  documents.append(file.read())
     #print(documents)
     vectorSpace = VectorSpace(documents)
     
     score = vectorSpace.search([args.query])

     #print(score)
     # 反向排序
     sort_index = numpy.argsort(score)[::-1]
     print(sort_index)
     for index in sort_index[:10]:
          print(documentsName[index],score[index])

    #print(vectorSpace.search(["Trump Biden Taiwan China"]))


###################################################
