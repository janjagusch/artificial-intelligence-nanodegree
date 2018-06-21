import math
import warnings
import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    Base class for model selection (strategy design pattern).
    '''


    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose


    def calculate_score(self, model):
        pass

    def get_component_range(self):
        """Returns range between min_n_components and max_n_components."""
        return range(self.min_n_components, self.max_n_components + 1)


    def select(self):
        """Selects best model, based on DIC score."""

        # Ignore deprecation warning.
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Stores best score found.
        best_score = float('-Inf')
        # Stores best model found.
        best_model = None
        # If no exception occurs, return best model.
        try:
            for n_components in self.get_component_range():
                hmm_model = self.base_model(n_components)
                score = self.calculate_score(hmm_model)
                if score > best_score:
                    best_model = hmm_model
                    best_score = score
            return best_model
        # If exception occurs, return constant model.
        except:
            return self.base_model(self.n_constant)


    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """
    Select the model with value self.n_constant.
    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ Select the model with the lowest Bayesian Information Criterion(BIC) score.

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def calculate_score(self, model):
        """Calculates score, based on BIC metric."""

        # Calculate log likelihood of model.
        log_l = model.score(self.X, self.lengths)
        # Calculate penalty factor.
        n_params = model.n_components ** 2 + 2 * model.n_components * model.n_features - 1
        # Calculate score.
        score = -2 * log_l + n_params * math.log(model.n_components)
        return score


class SelectorDIC(ModelSelector):
    """
    Select best model based on Discriminative Information Criterion
    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    """

    def calculate_score(self, model):
        """Calculates score, based on DIC metric."""

        scores = []
        # Iterate though word list.
        for word, (X, lengths) in self.hwords.items():
            # If word is not target word, add likelihood to scores.
            if word != self.this_word:
                scores.append(model.score(X, lengths))
        # Subtract likelihood of target word from average likelihood of other words.
        score = model.score(self.X, self.lengths) - np.mean(scores)
        return score


class SelectorCV(ModelSelector):
    """Select best model based on average log Likelihood of cross-validation folds."""

    def calculate_score(self, model):
        """
        Calculate the average log likelihood of cross-validation folds using the KFold class
        :return: tuple of the mean likelihood and the model with the respective score
        """

        # Define number of splits as 2.
        scores = []
        split_method = KFold(n_splits=2)

        # Iterate through samples of training and testing.
        for train_idx, test_idx in split_method.split(self.sequences):
            self.X, self.lengths = combine_sequences(train_idx, self.sequences)
            X, l = combine_sequences(test_idx, self.sequences)
            scores.append(model.score(X, l))
        return np.mean(scores), model
