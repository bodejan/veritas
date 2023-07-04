import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
import pickle
import keras
from keras_preprocessing.sequence import pad_sequences


def preprocess_nlp(text):
    """

    :param text: plain text
    :return:  preprocessed text
    """
    text = text.replace("\n", ". ")
    # tokenize the text
    tokens = word_tokenize(text.lower())
    # remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    # remove special chars and punctuation
    tokens = [t for t in tokens if t.isalnum()]
    # Remove numbers
    tokens = [t for t in tokens if not t.isdigit()]
    # join the tokens back into a string
    return ' '.join(tokens)


def process_split_words(text):
    """

    :param text: plain text
    :return: array of tokenized words
    """
    result = []
    #nltk.download('punkt', quiet=True)  # Download the necessary tokenizer data
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = sentence.split()
        result.append(words)
    return result

def predictor(text):
    """

    :return: dictionary with frequency of each class appears in the given text
    :param text: plain text
    """
    result = process_split_words(text)
    # Load the tokenizer
    # Try abs path if it does not work 
    with open('/app/NLP/NLPPredictor/tokenizer.pkl', 'rb') as f:
    #with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    sequences = tokenizer.texts_to_sequences(result)
    pad_rev = pad_sequences(sequences, maxlen=102, padding='post')
    # Try abs path if it does not work
    lstm_model = keras.models.load_model('/app/NLP/NLPPredictor/Bidirectional_LSTM_Model.h5')
    #lstm_model = keras.models.load_model('Bidirectional_LSTM_Model.h5')
    preds = lstm_model.predict(pad_rev)
    classes = []

    for pred in preds:
        if pred[np.argmax(pred)] > 0.5:
            classes.append(np.argmax(pred))

    result = {}
    mapping = ['Data Recipients', 'Safeguards Copy', 'Processing Purpose',
               'Data Categories', 'Source of Data', 'Right to Erase',
               'Right to Restrict', 'Right to Access', 'Right to Object',
               'Withdraw Consent', 'Right to Portability', 'Profiling',
               'Controller Contact', 'Provision Requirement',
               'Storage Period', 'Lodge Complaint', 'DPO Contact',
               'Adequacy Decision']
    for cat in mapping:
        result[cat] = 0
    for c in classes:
        result[mapping[c]] = 1
    return result


if __name__ == '__main__':
    #preds = process_split_words("sd asd awd  awfawf  saffaw. awda awd s d wad ? adwuidandnwda adina dawd, awdjajwd.")
    preds = predictor("We may provide our analysis and certain non-personal information to third parties who may in turn use this information to provide advertisements tailored to your interests. We seek to maintain the integrity and security of your Personal Information. In order to improve guest online and mobile shopping experiences, help with fraud identification. These contracts give your personal data the same protection it has in the EEA. We may share some or all of your personal data with our affiliates.")
    print(preds)
