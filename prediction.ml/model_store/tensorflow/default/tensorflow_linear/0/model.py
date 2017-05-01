import dill as pickle

class Predictor():
    def __init__(self, cat_mean, cat_stdv, dog_mean, dog_stdv):
        self.cat_mean = cat_mean
        self.cat_stdv = cat_stdv
        self.dog_mean = dog_mean
        self.dog_stdv = dog_stdv

    def setup_model():
        pass

    def teardown_model():
        pass
 
    def setup_request(inputs):
        pass

    def teardown_request(outputs):
        pass

    def predict(self, inputs):
        cat_affinity_score = sum([ d['weight'] * d['user_score'] for d in inputs if 'cat' in d['tags'] ])
        dog_affinity_score = sum([ d['weight'] * d['user_score'] for d in inputs if 'dog' in d['tags'] ])

        # create normalized z score for compare/classify
        cat_zscore = (cat_affinity_score - self.cat_mean)/self.cat_stdv
        dog_zscore = (dog_affinity_score - self.dog_mean)/self.dog_stdv

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

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('model_pkl_filename')
    args = parser.parse_args()
    model_pkl_filename = args.model_pkl_filename

    print("Training model...")
    cat_mean = 0.1
    cat_stdv = 0.20
    dog_mean = 0.3
    dog_stdv = 0.40
    print("...Done!")

    print("Pickling model to '%s'..." % model_pkl_filename)
    predictor = Predictor(cat_mean, cat_stdv, dog_mean, dog_stdv)
    with open(model_pkl_filename, 'wb') as model_pkl_file:
        pickle.dump(predictor, model_pkl_file)
    print("...Done!")
