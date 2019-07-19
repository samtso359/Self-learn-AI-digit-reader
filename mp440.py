from __future__ import division
import inspect
import sys
from pprint import pprint
import math
import operator
import copy
'''
Raise a "not defined" exception as a reminder 
'''
tempdata=[]
pd = {}  #prior distribution
counter = {} #to count how many times each label appears in the documents
cd = {} #number of time the pixel has value > 0 for the label
cd2 = {} #probability of that pixel has value > 0 for each label
jointprob = {} #a dictionary of all labels along with their probabilities
k=0.00000001

def _raise_not_defined():
    print "Method not implemented: %s" % inspect.stack()[1][3]
    sys.exit(1)


'''
Extract 'basic' features, i.e., whether a pixel is background or
forground (part of the digit) 
'''
def extract_basic_features(digit_data, width, height):
    features=[]

    # Your code starts here

    features = {}

    for i in range(height):
        for j in range(width):
            if(digit_data[i][j] == 0):
                features[(i,j)]=False
            else:
                features[(i,j)]=True

    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    # _raise_not_defined()

    return features


def recursiveCount(x, y, basic_feat, width, height, iter):
    if iter[(x, y)] == 1:
        return
    if basic_feat[(x,y)] == True:
        return
    iter[(x, y)] = 1
    if x > 0:
        recursiveCount(x - 1, y, basic_feat, width, height, iter)
    if x < width - 1:
        recursiveCount(x + 1, y, basic_feat, width, height,iter)
    if y > 0:
        recursiveCount(x, y - 1, basic_feat, width, height,iter)
    if y < height - 1:
        recursiveCount(x, y + 1, basic_feat, width, height,iter)

def boundaryOfDigit(data, width, height):
    (minx, miny, maxx, maxy) = (float("inf"), float("inf"), float("-inf"), float("-inf"))
    for x in range(height):
        for y in range(width):
          if data[x][y] >0:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    return (minx, miny, maxx, maxy)

def leftRatio(data, bound, numberOfdigitpixel):
    #print "running left ratio"
    minx = bound[0]
    miny = bound[1]
    maxx = bound[2]
    maxy = bound[3]
    leftPixels = 0
    #tempcount = 0
    #print "bound is: " + str(bound)
    #copys = copy.deepcopy(data)
    #for x in range(len(copys)):
    #    for y in range(len(copys[x])):
    #        copys[x][y] = 0

    for x in range(minx, maxx+1):
        for y in range(miny, int((miny+maxy)/2)):
            if data[x][y]>0:
                leftPixels+=1
                #copys[x][y] = data[x][y]
    #for i in range(len(copys)):
     #   print copys[i]
    #for x in range(len(copys)):
    #    for y in range(len(copys[x])):
    #        if copys[x][y]>0:
     #           tempcount += 1
    #print tempcount
    #print "number of pixel on the left: " + str(leftPixels)
    #print "ratio is: " + str(leftPixels / numberOfdigitpixel)
    return leftPixels/numberOfdigitpixel

def topRatio(data, bound, numberOfdigitpixel):
    #print "running top ratio"
    minx = bound[0]
    miny = bound[1]
    maxx = bound[2]
    maxy = bound[3]
    topPixels = 0
    #tempcount = 0
    #print "bound is: "+str(bound)
    #copys = copy.deepcopy(data)
    #for x in range(len(copys)):
    #    for y in range(len(copys[x])):
    #        copys[x][y] = 0
    for x in range(minx, int((minx+maxx)/2)):
        for y in range(miny, maxy+1):
            if data[x][y]>0:
                topPixels+=1
     #           copys[x][y] = data[x][y]
   # for i in range(len(copys)):
    #    print copys[i]
    #for x in range(len(copys)):
     #   for y in range(len(copys[x])):
     #       if copys[x][y]>0:
     #           tempcount += 1
    #print tempcount
    #print "number of pixel on the top: "+str(topPixels)
    #print "ratio is: "+ str(topPixels/numberOfdigitpixel)
    return topPixels/numberOfdigitpixel
'''
Extract advanced features that you will come up with 
'''
def extract_advanced_features(digit_data, width, height):
    features=[]
    # Your code starts here
    basic_feat = extract_basic_features(digit_data, width,height)
    features = {}
    emptyPixel =0
    occupiedPixel = 0
    outterCount = 0
    #zeroCount = 0
    iter ={}
    #tempdata =[[0 for x in range(height)] for y in range(width)]
    boundary = boundaryOfDigit(digit_data, width, height) #(minx, miny, maxx, maxy)


    for x in range(height):
        for y in range(width):
            iter[(x,y)] = 0

    recursiveCount(0, 0, basic_feat, width, height, iter)
    #pprint(iter)
    for key, value in iter.iteritems():
        #print key
        if value == 1:
            outterCount+=1

    for key, value in basic_feat.iteritems():
        if value == False:
            emptyPixel +=1
        else:
            occupiedPixel +=1
    #for i in range(len(digit_data)):
       # print digit_data[i]
    #print outterCount
    #print emptyPixel
    #print occupiedPixel
    if(outterCount/emptyPixel)<0.981:
        basic_feat["loop"] = True
        #print "has loop"
    else:
        basic_feat["loop"] = False

    topratios = topRatio(digit_data, boundary, occupiedPixel)
    if(topratios)>0.6:
        basic_feat["topHeavy"] = True
        basic_feat["bottomHeavy"] = False
        #print "is top heavy"
    elif(topratios)<0.4:
        basic_feat["topHeavy"] = False
        basic_feat["bottomHeavy"] = True
        #print "is bottom heavy"
    elif (topratios)<=0.6 and (topratios)>=0.4:
        basic_feat["topHeavy"] = False
        basic_feat["bottomHeavy"] = False
        #print "top and bottom are balanced"


    leftratios = leftRatio(digit_data, boundary, occupiedPixel)
    if (leftratios) > 0.6:
        basic_feat["leftHeavy"] = True
        #print "is left heavy"
        basic_feat["rightHeavy"] = False
    elif (leftratios)<0.4:
        basic_feat["leftHeavy"] = False
        #print "is right heavy"
        basic_feat["rightHeavy"] = True
    elif (leftratios)<=0.6 and (leftratios)>= 0.4:
        basic_feat["rightHeavy"] = False
        basic_feat["leftHeavy"] = False
        #print "left and right are balanced"
    for key in basic_feat.keys():
        if isinstance(key, tuple):
            del basic_feat[key]

    features = basic_feat
    #pprint(features)
   # pprint(features)
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    #_raise_not_defined()
    return features

'''
Extract the final features that you would like to use
'''
def extract_final_features(digit_data, width, height):
    features=[]
    # Your code starts here 
    basic_feat = extract_basic_features(digit_data, width, height)
    features = {}
    emptyPixel = 0
    occupiedPixel = 0
    outterCount = 0
    # zeroCount = 0
    iter = {}
    # tempdata =[[0 for x in range(height)] for y in range(width)]
    boundary = boundaryOfDigit(digit_data, width, height)  # (minx, miny, maxx, maxy)

    for x in range(height):
        for y in range(width):
            iter[(x, y)] = 0

    recursiveCount(0, 0, basic_feat, width, height, iter)
    # pprint(iter)
    for key, value in iter.iteritems():
        # print key
        if value == 1:
            outterCount += 1

    for key, value in basic_feat.iteritems():
        if value == False:
            emptyPixel += 1
        else:
            occupiedPixel += 1
    # for i in range(len(digit_data)):
    # print digit_data[i]
    # print outterCount
    # print emptyPixel
    # print occupiedPixel
    if (outterCount / emptyPixel) < 0.981:
        basic_feat["loop"] = True
        # print "has loop"
    else:
        basic_feat["loop"] = False

    topratios = topRatio(digit_data, boundary, occupiedPixel)
    if (topratios) > 0.6:
        basic_feat["topHeavy"] = True
        basic_feat["bottomHeavy"] = False
        # print "is top heavy"
    elif (topratios) < 0.4:
        basic_feat["topHeavy"] = False
        basic_feat["bottomHeavy"] = True
        # print "is bottom heavy"
    elif (topratios) <= 0.6 and (topratios) >= 0.4:
        basic_feat["topHeavy"] = False
        basic_feat["bottomHeavy"] = False
        # print "top and bottom are balanced"

    leftratios = leftRatio(digit_data, boundary, occupiedPixel)
    if (leftratios) > 0.6:
        basic_feat["leftHeavy"] = True
        # print "is left heavy"
        basic_feat["rightHeavy"] = False
    elif (leftratios) < 0.4:
        basic_feat["leftHeavy"] = False
        # print "is right heavy"
        basic_feat["rightHeavy"] = True
    elif (leftratios) <= 0.6 and (leftratios) >= 0.4:
        basic_feat["rightHeavy"] = False
        basic_feat["leftHeavy"] = False
        # print "left and right are balanced"

    features = basic_feat
    # Your code ends here 

    return features

'''
Compupte the parameters including the prior and and all the P(x_i|y). Note
that the features to be used must be computed using the passed in method
feature_extractor, which takes in a single digit data along with the width
and height of the image. For example, the method extract_basic_features
defined above is a function than be passed in as a feature_extractor
implementation.

The percentage parameter controls what percentage of the example data
should be used for training. 
'''
def compute_statistics(data, label, width, height, feature_extractor, percentage=100.0):

    #counting how many times each label appears in the file, and save it to the dictionary pd
    global pd
    global jointprob
    global counter
    global cd2

    for num in range(10):
        pd[num]=0
        jointprob[num]=0
    for i in range(int(len(data)*(percentage/100))):
        pd[label[i]] +=1

    counter=pd.copy()

    #initualizing the cd list with every pixel and label
    for i in range(10):
        for h in range(height):
            for w in range(width):
                cd[(h, w), i] = 0

    #for every pixel (i, j) in each label, count how many times that pixel has a value
    for alldata in range(int(len(data)*(percentage/100))):
        feats = feature_extractor(data[alldata],width,height)
        for key,value in feats.iteritems() :
            if value == True and isinstance(key, tuple):        #changes
                cd[key, label[alldata]] +=1

    #pprint(cd)

    cd2 = cd.copy()
    #calculate the log of probability of each label
    for i in range(len(pd)):
        pd[i] =pd[i]/len(label)
        pd[i] = math.log(pd[i], 10)
    #for key, value in cd2.iteritems():
    #    jointprob[key[1]] = math.log(float(cd[key]+k)/float((counter[key[1]]+k)))
            #jointprob[key[1]]

    #for i in range(len(jointprob)):
    #    jointprob[i] = jointprob[i]+pd[i]
        #print (-1)*math.log(float(cd[key]+k)/float(counter[key[1]]+k))
    #pprint(jointprob)

    for key, value in cd2.iteritems():
        cd2[key] = cd2[key]/counter[key[1]]
    #pprint(pd)

    #pprint(cd)
    #pprint(cd2)
    # Your code starts here
    # You should remove _raise_not_defined() after you complete your code
    # Your code ends here 
    #_raise_not_defined()

'''
For the given features for a single digit image, compute the class 
'''
def compute_class(features):
    predicted = -1

    # Your code starts here
    #_raise_not_defined()
    global k
    #pprint(cd2)
    for i in range(len(jointprob)):
        jointprob[i] = pd[i]
        for key,value in features.iteritems():
            if value == True and isinstance(key, tuple) : #changes
                #print "is true"
                #print cd2[key,i]+k
                #print key
                jointprob[i] += math.log(cd2[key,i]+k,10)
                #jointprob[i] += cd2[key,i]
            elif value == False and isinstance(key, tuple) :
                #print key
                #print "is false"
                #print 1-cd2[key,i]+k
                jointprob[i] += math.log(1-cd2[key,i]+k,10)
                #jointprob[i] += 1-cd2[key,i]


    #pprint(jointprob)

    # g = 7 #great increase
    # f = 5       #medium flat amount
    # s = 3       #small change

    g = 13       #13
    f = 11      #11
    s = 1
    if 'loop' in features:
        if features['loop'] == True:            #how much probability increase do we want to give
            jointprob[0] += g
            jointprob[4] += s          #give 4 only a little, some people don't write 4 with loop
            jointprob[6] += f
            jointprob[8] += f
            jointprob[9] += f
        else:
            jointprob[1] += f
            jointprob[2] += f
            jointprob[3] += f
            jointprob[5] += f
            jointprob[7] += f
        if features['topHeavy'] == True:
            jointprob[9] += f
            jointprob[7] += f
        if features['bottomHeavy'] == True:
            jointprob[4] += f
            jointprob[6] += f
            jointprob[5] += s
        if features['rightHeavy'] == True:
            jointprob[9] += f
            jointprob[7] += f
            jointprob[3] += f
            jointprob[4] += f
            #jointprob[5] += s
        if features['leftHeavy'] == True:
            jointprob[6] += f
    pprint(jointprob)
    predicted = max(jointprob.iteritems(), key=operator.itemgetter(1))[0]
    #print predicted
    #exit()
    # Your code ends here 

    print "predicted is: "+str(predicted)+"\n=============================================================================="

    return predicted

'''
Compute joint probaility for all the classes and make predictions for a list
of data
'''
def classify(data, width, height, feature_extractor):

    predicted=[]
    #_raise_not_defined()
    # Your code starts here

    for i in range(len(data)):
        for j in range(len(data[i])):
            print data[i][j]

        temp = compute_class(feature_extractor(data[i], width, height))
        predicted.append(temp)
        #print predicted
        #exit()



    return predicted







        
    
