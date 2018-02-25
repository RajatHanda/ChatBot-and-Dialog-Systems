import sys
import re
import nltk
import random
from nltk.util import ngrams
from collections import Counter
from nltk.probability import FreqDist, MLEProbDist

lis = sys.argv
lis[1] = int(lis[1])
lis[2] = int(lis[2])
n = lis[1]
sent_num = lis[2]

def preprocess():
    global lis
    raw = b''
    if len(lis) < 4:
        print ("there are parameters missing")
        sys.exit ("there are parameters missing. Please re-execute with the correct params")
    for i in range (3,len(lis)):

        file = open(lis[i],"rb")
        raw += file.read()

    raw = raw.decode(encoding='utf-8')
    raw = raw.lower()

    #eliminating the new line markers
    raw = re.sub('\\r\\n','',raw.rstrip())
    return raw

def tokenize(raw):
    global lis
    # "n" holds the ngram value
    n = lis[1]
    
    #Tokanizing by sentence to add the boundary markers for each sentence 
    tokens = nltk.tokenize.sent_tokenize(raw)
    
    new_tokens = []
    
    #going through every sentence, tokenizing and inserting the boundary markers
    for i in range(len(tokens)):
        
        #tokanize every sentence
        w_tokens = nltk.tokenize.word_tokenize(tokens[i])

        if (len(w_tokens)  < n):
            #print ("this sentence is too short for our ngram: ", tokens[i])
            continue

        #inserting start and end markers to each tokenized sentence manually
        for i in range (n-1):
            
            w_tokens.append("<end>")
            w_tokens.insert(0, "<start>")
       
        
        new_tokens += w_tokens
    
    #bigram = ngrams(new_tokens,2)
    ngram = ngrams(new_tokens,n)       
    ngram_counter = Counter(ngram)
    
    if n == 1:
        return ngram_counter
    
    # Transforming the Counter dictionary to a dictionary of dictionaries for...
    #  ...the ease of use. the first n-1 items will be keys and the value is {nth item: value}
    token_dict = {}
    for key, value in ngram_counter.items():
        outer_key = key[:-1]
        if outer_key in token_dict.keys():
            token_dict[outer_key][key[-1]] = value
            continue
        #print ( outer_key, key[-1])
        token_dict[outer_key]= {key[-1]: value}
    return token_dict

# This function will generate the random sentences
def gen_sent(ngram):
    
    global lis
    
    # "n" contains the ngram number
    n = lis[1]
    #number of required sentences is stored in sent_num
    sent_num = lis[2]
    i = 0
    for  i in range (sent_num):
        j = True

        # we are using this window to go through the sentence with n-1 previous
        # words stored in the window
        window = []
        sent = ""
        for size in range (n-1):
            window.append('<start>')
        while j == True:
            tup_win = tuple(window)
            if tup_win not in ngram.keys():
                sys.exit("We don't have a start line")

            # FreqDist and MLEProbDist function will transform the frequencies to probabilities
            # by performing (item freq/ sum of frequencies)
            freq_dist = FreqDist(ngram[tup_win])

            #prob_dist.generate() will take in the freq-distance and generate a random token
            # according to the distribution
            prob_dist = MLEProbDist(freq_dist)
            next_w = prob_dist.generate()

            #the following condition is used to detect the end of line
            if (next_w =="." or next_w == "?" or next_w == "!"):
                j = False
                sent += next_w
                continue

            #We'd like to make sure the apostrophe token has no space before or after it...
            # ... as well as the begining of the line
            elif (next_w == "m" or next_w == "s" or next_w == "re" or next_w == "," 
                  or next_w == "’" or next_w == "ve" or next_w == "t" or tup_win[-1] == '<start>'):
                sent += next_w
            else:
                sent += " %s"%next_w
            
            #moving the window forward by popping and appending
            window.pop(0)
            window.append(next_w)

        print ("\nSentence %s:\n%s"%(i+1, sent))

def gen_unigram(ngram):
    i = 0
    
    for  i in range (sent_num):
        j = 0
        sent = ""
        new_dict = {}
        while j < 30:

            
            for key, value in ngram.items():
                if value > 10:
                    new_dict[key] = value
                    
                
            next_w = random.choice(list(new_dict.keys()))
            
            #the following condition is used to detect the end of line
            if (next_w =="." or next_w == "?" or next_w == "!"):
                j = 30
                sent += next_w
                continue

            #We'd like to make sure the apostrophe token has no space before or after it...
            # ... as well as the begining of the line
            elif (next_w == "m" or next_w == "s" or next_w == "re" or next_w == "," 
                  or next_w == "’" or next_w == "ve" or next_w == "t"):
                sent += next_w
            else:
                sent += " %s"%next_w
            j += 1
            if j == 30:
                sent += "."

        print ("\nSentence %s:\n%s"%(i+1, sent))

    return
    
def main():

    print ("This program generates random sentences based on an Ngram model\n", \
            "Command line settings: %s %s %s" %(lis[0], lis[1], lis[2]))

    raw = preprocess()

    ngram = tokenize(raw)

    if n == 1:
        gen_unigram(ngram)
        
    elif n > 1:
        gen_sent(ngram)
    
    else:
        sys.exit("the number for ngram was not appropriate")

if __name__ == "__main__":
    main()
    sys.exit(0)
#print (ngram_counter)