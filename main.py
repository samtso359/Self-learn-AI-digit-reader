import mp440 as mp
import time
import sys
import os
import random

DATA_WIDTH=28
DATA_HEIGHT=28
NUMBER_OF_TRAINING_EXAMPLES=5000
NUMBER_OF_VALIDATION_EXAMPLES=1000

ALL_TRAINING_IMAGES=[]
ALL_TRAINING_LABELS=[]
ALL_VALIDATION_IMAGES=[]
ALL_VALIDATION_LABELS=[]

'''
Convert ASC-II pixel into numerical data and vise versa

    - ' ' is converted to 0, which means it's part of the background
    - '#' is converted to 1, part of the image interior
    - '+' is converted to 2, part of the image exterios (i.e., edges)
    
'''
def _pixel_to_value(character):
    if(character == ' '):
        return 0
    elif(character == '#'):
        return 1
    elif(character == '+'):
        return 2    

def _value_to_pixel(value):
    if(value == 0):
        return ' '
    elif(value == 1):
        return '#'
    elif(value == 2):
        return '+'    

'''
Function for loading data and label files
'''
def _load_data_file(filename, n, width, height):
    fin = [l[:-1] for l in open(filename).readlines()]
    fin.reverse()
    items = []
    for i in range(n):
        data = []
        for j in range(height):
            row = map(_pixel_to_value, list(fin.pop()))
            data.append(row)
        items.append(data)
    return items
        
def _load_label_file(filename, n):
    fin = [l[:-1] for l in open(filename).readlines()]
    labels = []
    for i in range(n):
        labels.append(int(fin[i]))
    return labels

'''
Helper function for prting an image
'''
def _print_digit_image(data):
    for row in range(len(data)):
        print ''.join(map(_value_to_pixel, data[row]))
   

'''
Loading all data into a list of "pixels" with some edge information
'''
def _load_all_data():
    global ALL_TRAINING_IMAGES
    global ALL_TRAINING_LABELS
    global ALL_VALIDATION_IMAGES
    global ALL_VALIDATION_LABELS

    ALL_TRAINING_IMAGES = _load_data_file("digitdata/trainingimages",
        NUMBER_OF_TRAINING_EXAMPLES, DATA_WIDTH, DATA_HEIGHT)
    ALL_TRAINING_LABELS = _load_label_file("digitdata/traininglabels",
        NUMBER_OF_TRAINING_EXAMPLES)

    ALL_VALIDATION_IMAGES = _load_data_file("digitdata/validationimages",
        NUMBER_OF_VALIDATION_EXAMPLES, DATA_WIDTH, DATA_HEIGHT)
    ALL_VALIDATION_LABELS = _load_label_file("digitdata/validationlabels",
        NUMBER_OF_VALIDATION_EXAMPLES)

if __name__ == "__main__":
    start_time= time.time()
    # Load all data
    _load_all_data()

    # Pring a random traning example
    example_number = random.randint(0, NUMBER_OF_TRAINING_EXAMPLES)
    print "Printing digit example #" + str(example_number + 1) + " with label: " \
        + str(ALL_TRAINING_LABELS[example_number])
    _print_digit_image(ALL_TRAINING_IMAGES[example_number])
    print

    # Calling the basic feature extractor 
    features = mp.extract_basic_features(ALL_TRAINING_IMAGES[example_number],
        DATA_WIDTH, DATA_HEIGHT)
    #mp.extract_advanced_features(ALL_TRAINING_IMAGES[example_number],DATA_WIDTH, DATA_HEIGHT)
    #mp.extract_advanced_features(ALL_TRAINING_IMAGES[2075],DATA_WIDTH, DATA_HEIGHT)

    # Compute parameters for a Naive Bayes classifier using the basic feature
    # extractor 
    #mp.compute_statistics(ALL_TRAINING_IMAGES, ALL_TRAINING_LABELS, DATA_WIDTH,DATA_HEIGHT, mp.extract_basic_features)

    # Making predictions on validation data 
    #predicted_labels = mp.classify(ALL_VALIDATION_IMAGES, DATA_WIDTH, DATA_HEIGHT,mp.extract_basic_features)

    #with advance features
    #mp.compute_statistics(ALL_TRAINING_IMAGES, ALL_TRAINING_LABELS, DATA_WIDTH, DATA_HEIGHT, mp.extract_advanced_features)
    #predicted_labels = mp.classify(ALL_VALIDATION_IMAGES, DATA_WIDTH, DATA_HEIGHT, mp.extract_advanced_features)

    #with final features
    mp.compute_statistics(ALL_TRAINING_IMAGES, ALL_TRAINING_LABELS, DATA_WIDTH, DATA_HEIGHT, mp.extract_final_features)
    predicted_labels = mp.classify(ALL_VALIDATION_IMAGES, DATA_WIDTH, DATA_HEIGHT, mp.extract_final_features)
    correct_count = 0.0
    for ei in range(len(predicted_labels)):
        if(ALL_VALIDATION_LABELS[ei] == predicted_labels[ei]):
            correct_count += 1

    print "Correct prediction: " + str(correct_count/len(predicted_labels))
    print("--- %s seconds ---" % (time.time() - start_time))

    
