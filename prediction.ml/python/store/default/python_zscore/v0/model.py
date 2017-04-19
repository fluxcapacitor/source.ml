cat_mean = 0.0
cat_stdv = 0.0
dog_mean = 0.0
dog_stdv = 0.0

def train():
    print("Training model...")

    global cat_mean
    global cat_stdv
    global dog_mean
    global dog_stdv

    cat_mean = 0.1
    cat_stdv = 0.20
    dog_mean = 0.3
    dog_stdv = 0.40

    print("...Done!")

def predict(inputs):
    cat_affinity_score = sum([ d['weight'] * d['user_score'] for d in inputs if 'cat' in d['tags'] ])
    dog_affinity_score = sum([ d['weight'] * d['user_score'] for d in inputs if 'dog' in d['tags'] ])

    global cat_mean
    global cat_stdv
    global dog_mean
    global dog_stdv

    # create normalized z score for compare/classify
    cat_zscore = (cat_affinity_score - cat_mean)/cat_stdv
    dog_zscore = (dog_affinity_score - dog_mean)/dog_stdv

    # classify
    if abs(cat_zscore) > abs(dog_zscore):
        if cat_zscore >= 0:
            category = "cat_lover"
        else:
            category = "cat_hater"
    else:
        if dog_zscore >= 0:
            category = "dog_lover"
        else:
            category = "dog_hater"

    classification = {
        'category': category,
        'cat_affinity_score': cat_affinity_score,
        'dog_affinity_score': dog_affinity_score,
        'cat_zscore': cat_zscore,
        'cat_zscore': dog_zscore
    }

    return classification 
