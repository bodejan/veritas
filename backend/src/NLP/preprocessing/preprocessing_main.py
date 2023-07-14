from preprocessing import preprocessing_functions
import csv
from NLPPredictor import predictor

"""
Performs text preprocessing operations based on the provided parameters.

Parameters:
- functions (list): A list of strings specifying the preprocessing functions to apply. They are executed depending on the order that they are stated in the list. Available options are:
    - 'remove_newlines_tabs': Removes newlines and tabs from the text.
    - 'strip_html_tags': Strips HTML tags from the text.
    - 'remove_links': Removes links from the text.
    - 'remove_whitespace': Removes whitespace from the text.
    - 'accented_characters_removal': Removes accented characters from the text.
    - 'lower_casing_text': Converts the text to lowercase.
    - 'reducing_incorrect_character_repetition': Reduces incorrect character repetition in the text.
    - 'expand_contractions': Expands contractions in the text.
    - 'removing_special_characters': Removes special characters from the text.
    - 'removing_stopwords_nltk': Removes stopwords using NLTK library.
    - 'removing_stopwords_spacy': Removes stopwords using spaCy library.
    - 'spelling_correction': Corrects spelling errors in the text.
    - 'lemmatization': Performs lemmatization on the text. Requires additional parameter 'v_or_n' to specify 'v' (verb) or 'n' (noun).
    - 'porter_stemming': Performs Porter stemming on the text.
    - 'snowball_stemming': Performs Snowball stemming on the text.

- text (str): The input text to preprocess (default: empty string).
- v_or_n (str): Optional parameter for 'lemmatization' function. Specifies whether to perform lemmatization for verbs ('v') or nouns ('n').
                Raises a ValueError if an invalid value is provided (default: empty string).
- words_or_sentences (str): Optional parameter specifying the output format. Available options are:
    - 'w': Returns the preprocessed text as words.
    - 's': Returns the preprocessed text as sentences.
    Raises a ValueError if an invalid value is provided (default: empty string).

Returns:
- output_text (str): The preprocessed text based on the specified parameters.

Raises:
- ValueError: If an invalid value is provided for 'v_or_n' or 'words_or_sentences' parameters.

Usage example:
```python
functions = ['lower_casing_text', 'remove_stopwords_nltk']
text = "Hello, this is an example text."
v_or_n = 'n'
words_or_sentences = 's'
preprocessed_text = function_caller(functions, text, v_or_n, words_or_sentences)
print(preprocessed_text)
```
"""
def function_caller(nlp=None, functions=None, text="", v_or_n="", words_or_sentences=""):
    output_text = text

    for parameter in functions:
        # yes
        if parameter == 'remove_newlines_tabs':
            output_text = preprocessing_functions.remove_newlines_tabs(output_text)
        # yes
        elif parameter == 'strip_html_tags':
            output_text = preprocessing_functions.strip_html_tags(output_text)
        # yes
        elif parameter == 'remove_links':
            output_text = preprocessing_functions.remove_links(output_text)
        # yes
        elif parameter == 'remove_whitespace':
            output_text = preprocessing_functions.remove_whitespace(output_text)
        # no
        elif parameter == 'accented_characters_removal':
            output_text = preprocessing_functions.accented_characters_removal(output_text)
        # yes
        elif parameter == 'reducing_incorrect_character_repetition':
            output_text = preprocessing_functions.reducing_incorrect_character_repetition(output_text)
        # yes
        elif parameter == 'expand_contractions':
            output_text = preprocessing_functions.expand_contractions(output_text)
        # no
        elif parameter == 'spelling_correction':
            output_text = preprocessing_functions.spelling_correction(output_text)
        elif parameter == 'lower_casing_text':
            output_text = preprocessing_functions.lower_casing_text(output_text)
        elif parameter == 'removing_special_characters':
            output_text = preprocessing_functions.removing_special_characters(output_text)
        elif parameter == 'removing_stopwords_nltk':
            output_text = preprocessing_functions.removing_stopwords_nltk(output_text)
        elif parameter == 'removing_stopwords_spacy':
            output_text = preprocessing_functions.removing_stopwords_spacy(output_text, nlp)
        elif parameter == 'lemmatization':
            if v_or_n is not None and v_or_n in ['v', 'n']:
                output_text = preprocessing_functions.lemmatization(output_text, v_or_n)
            else:
                raise ValueError("Invalid value for v_or_n. Only 'v' or 'n' is allowed. 'v' stands for verb and 'n' stands for Noun.")
        elif parameter == 'porter_stemming':
            output_text = preprocessing_functions.porter_stemming(output_text)
            output_text = output_text
        elif parameter == 'snowball_stemming':
            output_text = preprocessing_functions.snowball_stemming(output_text)

    if isinstance(output_text, str):
        output_text = output_text.split()

    if words_or_sentences is not None and words_or_sentences in ['s']:
        output_text = preprocessing_functions.manual_words_to_sentences(output_text)
    elif words_or_sentences is not None and words_or_sentences in ['w']:
        pass
    else:
        raise ValueError("Invalid value for words_or_sentences. Only 'w' or 's' is allowed. 'w' stands for words and 's' stands for sentences.")

    # remove empty list entries
    output_text = list(filter(None, output_text))

    return output_text


def save_list_as_csv_manual(data_list, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in data_list:
            writer.writerow(item)


def save_list_as_csv_automatic(data_list, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write each sentence as a row in the CSV file
        for sentence in data_list:
            writer.writerow([sentence])


def main(file_path):
    # Open the file in read mode
    file = open(file_path, "r", encoding="utf-8")

    # Read the entire content of the file
    input_text = file.read()

    text = NLPPredictor.predictor(input_text)

        # function_caller(None,
        #                    ["remove_newlines_tabs", "remove_links", "remove_whitespace", "lower_casing_text",
        #                     "reducing_incorrect_character_repetition", "expand_contractions",
        #                     "removing_special_characters"],
        #                    text=input_text,
        #                    v_or_n='n',
        #                    words_or_sentences='s')

    if type(text) == list:
        save_list_as_csv_manual(text, 'output.csv')
    elif type(text) == str:
        # Specify the file path where you want to save the text file
        file_path = "output.txt"

        # Open the file in write mode
        with open(file_path, "w") as file:
            # Write the data to the file
            file.write(text)


if __name__ == '__main__':
    main("example_policy.txt")
