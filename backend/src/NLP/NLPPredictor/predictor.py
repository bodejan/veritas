import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim
import pickle
import keras
from keras_preprocessing.sequence import pad_sequences
from src.NLP.NLPPredictor.preprocessing_functions import *
import csv


def preprocess_nlp(text):
    """
    Preprocesses the given text for natural language processing (NLP) tasks.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        csv: A list of sentences, where each sentence is a list of words.

    Example:
        >>> text = "This is a sample text."
        >>> preprocess_nlp(text)
        [['this', 'is', 'a', 'sample', 'text']]
    """
    output_text = remove_newlines_tabs(text)
    output_text = strip_html_tags(output_text)
    output_text = remove_links(output_text)
    output_text = expand_contractions(output_text)
    output_text = remove_whitespace(output_text)
    output_text = reducing_incorrect_character_repetition(output_text)
    output_text = lower_casing_text(output_text)
    output_text = removing_special_characters(output_text)

    # string to list of strings
    if isinstance(output_text, str):
        output_text = output_text.split()

    # turn a list of words into a list of sentences where each sentence is a list of words
    output_list = manual_words_to_sentences(output_text)

    # remove empty list entries
    output_list = list(filter(None, output_list))

    return output_list


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
    with open('/app/src/NLP/NLPPredictor/f_tokenizer.pkl', 'rb') as f:
    #with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    sequences = tokenizer.texts_to_sequences(result)
    pad_rev = pad_sequences(sequences, maxlen=192, padding='post')
    # Try abs path if it does not work
    lstm_model = keras.models.load_model('/app/src/NLP/NLPPredictor/f_bi_lstm_model.h5')
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


def save_list_as_csv(data_list, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write each sentence as a row in the CSV file
        for elem in data_list:
            writer.writerow(elem)


def text_file_to_csv_file(file_path):
    # Open the file in read mode
    file = open(file_path, "r", encoding="utf-8")

    # Read the entire content of the file
    input_text = file.read()

    text = preprocess_nlp(input_text)

    save_list_as_csv(text, 'output.csv')


if __name__ == '__main__':
    text_file_to_csv_file("example_policy.txt")
    # preds = process_split_words("sd asd awd  awfawf  saffaw. awda awd s d wad ? adwuidandnwda adina dawd, awdjajwd.")
    # preds = predictor("We may provide our analysis and certain non-personal information to third parties who may in turn use this information to provide advertisements tailored to your interests. We seek to maintain the integrity and security of your Personal Information. In order to improve guest online and mobile shopping experiences, help with fraud identification. These contracts give your personal data the same protection it has in the EEA. We may share some or all of your personal data with our affiliates.")
    # print(preds)
