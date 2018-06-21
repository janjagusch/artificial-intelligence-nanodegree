import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """
    Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Likelihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # Iterate through test words.
    for test_word, (X, lengths) in test_set.get_all_Xlengths().items():
        # Store best score as in log likelihood.
        best_score = float("-Inf")
        # Store best guess based on log likelihood.
        best_guess = None
        probability_dict = {}
        # Iterate through trained words.
        for trained_word, model in models.items():
            try:
                # Score test word on trained word model.
                log_l = model.score(X, lengths)
                # Add log likelihood to dictionary.
                probability_dict[trained_word] = log_l
            except:
                probability_dict[trained_word] = float("-Inf")
            # If log_l is greater than best score, best_guess is trained word.
            if log_l > best_score:
                best_score = log_l
                best_guess = trained_word
        # Append probability dict and best guess.
        probabilities.append(probability_dict)
        guesses.append(best_guess)

    return probabilities, guesses