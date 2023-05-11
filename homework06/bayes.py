import pickle
from collections import Counter, defaultdict

import nltk
import numpy as np
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

nltk.download('wordnet')
# 9019138755980861
# 0.5376794258373205
class NaiveBayesClassifier:
    def __init__(self, alpha=0.05):
        self.word_probabilities = defaultdict(Counter)
        self.class_probabilities = defaultdict()
        self.alpha = alpha
        self.labels = set()
        self.words = Counter()
        self.word_dict = dict()
        self.label_dict = dict()

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        class_counts = Counter(y)
        total_count = len(y)
        self.labels = set(y)
        self.class_probabilities = {label: count / total_count for label, count in class_counts.items()}
        for doc, label in zip(X, y):
            for word in wordpunct_tokenize(doc):
                # stemmed = ps.stem(word)
                stemmed = lemmatizer.lemmatize(word)
                self.words[stemmed] += 1
                self.word_probabilities[label][stemmed] += 1
        count_labels = {}
        for label in self.labels:
            count_labels[label] = sum(self.word_probabilities[label].values())
        for word in self.words:
            for label in self.labels:
                self.word_probabilities[label][word] = (self.word_probabilities[label][word] + self.alpha) / (
                    count_labels[label] + self.alpha * len(self.words)
                )

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predictions = []
        ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        c = 0
        for doc in X:
            scores = {label: np.log(prob) for label, prob in self.class_probabilities.items()}
            for word in wordpunct_tokenize(doc):
                for label, word_probs in self.word_probabilities.items():
                    # if word_probs[ps.stem(word)] != 0:
                    #     scores[label] += np.log(word_probs[ps.stem(word)])
                    if word_probs[lemmatizer.lemmatize(word)] != 0:
                        scores[label] += np.log(word_probs[lemmatizer.lemmatize(word)])

            predicted_label = max(scores, key=scores.get)
            predictions.append(predicted_label)
        return predictions

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        correct = 0
        total = len(y_test)
        predictions = self.predict(X_test)
        for prediction, true_label in zip(predictions, y_test):
            if prediction == true_label:
                correct += 1
        return correct / total

    def save(self, path):
        """Save model to path"""

        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        """Load model from path"""

        with open(path, "rb") as f:
            return pickle.load(f)
