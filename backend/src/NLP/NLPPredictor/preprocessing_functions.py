# Importing Libraries
import unidecode
import re
import nltk
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.data
from nltk.stem import PorterStemmer, SnowballStemmer
import contractions
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string

nltk.download('stopwords')
nltk.download('punkt')


def remove_newlines_tabs(text):
    """
    This function will remove all the occurrences of newlines, tabs, and combinations like: \\n, \\.

    arguments:
        input_text: "text" of type "String".

    return:
        value: "text" after removal of newlines, tabs, \\n, \\ characters.

    Example:
        Input : This is her \\ first day at this place.\n Please,\t Be nice to her.\\n
        Output : This is her first day at this place. Please, Be nice to her.
    """
    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    formatted_text = text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\\', ' ').replace('. com',
                                                                                                               '.com')
    return formatted_text


def strip_html_tags(text):
    """
    This function will remove all the occurrences of html tags from the text.

    arguments:
        input_text: "text" of type "String".

    return:
        value: "text" after removal of html tags.

    Example:
        Input : This is a nice place to live. <IMG>
        Output : This is a nice place to live.
    """
    # Initiating BeautifulSoup object soup.
    soup = BeautifulSoup(text, "html.parser")
    # Get all the text other than html tags.
    stripped_text = soup.get_text(separator=" ")
    return stripped_text


def remove_links(text):
    """
    This function will remove all occurrences of links.

    arguments:
        text: A string containing the text.

    return:
        The input text after removal of all types of links.
    """
    # Removing all occurrences of links that start with https or http and end with various TLDs
    text_without_links = re.sub(r'https?://\S+?\.\w{2,3}\S*', '', text)

    # Remove all the occurrences of text that ends with .com
    text_without_com = re.sub(r"\ [A-Za-z]*\.com", " ", text_without_links)

    return text_without_com


def remove_whitespace(text):
    """ This function will remove
        extra whitespaces from the text
    arguments:
        input_text: "text" of type "String".

    return:
        value: "text" after extra whitespaces removed .

    Example:
        Input : How   are   you   doing   ?
        Output : How are you doing ?
    """
    pattern = re.compile(r'\s+')
    without_whitespace = re.sub(pattern, ' ', text)
    # There are some instances where there is no space after '?' & ')',
    # So I am replacing these with one space so that It will not consider two words as one token.
    text = without_whitespace.replace('?', ' ? ').replace(')', ') ')
    return text


# Code for text lowercasing
def lower_casing_text(text):
    """
    The function will convert text into lower case.

    arguments:
         input_text: "text" of type "String".

    return:
         value: text in lowercase

    Example:
        Input : The World is Full of Surprises!
        Output : the world is full of surprises!
    """
    # Convert text to lower case
    # lower() - It converts all uppercase letters of given string to lowercase.
    text = text.lower()
    return text


# Code for removing repeated characters and punctuations
def reducing_incorrect_character_repetition(text):
    """
    This Function will reduce repetition to two characters
    for alphabets and to one character for punctuations.

    arguments:
         input_text: "text" of type "String".

    return:
        value: Finally formatted text with alphabets repeating to
        two characters & punctuations limited to one repeatition

    Example:
        Input : Realllllllllyyyyy,        Greeeeaaaatttt   !!!!?....;;;;:)
        Output : Reallyy, Greeaatt !?.;:)
    """
    # Pattern matching for all case alphabets
    pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)

    # Limiting all the  repetition to two characters.
    formatted_text = pattern_alpha.sub(r"\1\1", text)

    # Pattern matching for all the punctuations that can occur
    pattern_punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')

    # Limiting punctuations in previously formatted string to only one.
    combined_formatted = pattern_punct.sub(r'\1', formatted_text)

    # The below statement is replacing repetition of spaces that occur more than two times with that of one occurrence.
    final_formatted = re.sub(' {2,}', ' ', combined_formatted)
    return final_formatted


# The code for expanding contraction words
def expand_contractions(text):
    """
    expand shortened words to the actual form.
    e.g. don't to do not

    arguments:
        input_text: "text" of type "String".

    return:
        value: Text with expanded form of shortened words.

    Example:
        Input : ain't, aren't, can't, cause, can't've
        Output :  is not, are not, cannot, because, cannot have
    """
    # Add special abbreviations not covered by the package
    contractions.add('e.g.', 'exempli gratia')
    contractions.add('i.e.', 'id est')
    contractions.add('etc.', 'et cetera')
    contractions.add('Art.', 'Article')

    # Expand contractions
    text = contractions.fix(text)

    # Replace ’s at a words end with s
    # text = text.replace("’s", "s")

    return text


# The code for removing special characters
def removing_special_characters(text):
    """
    Removing all the special characters except the one that is passed within
    the regex to match, as they have imp meaning in the text provided.


    arguments:
         input_text: "text" of type "String".

    return:
        value: Text with removed special characters that don't require.

    Example:
        Input : Hello, K-a-j-a-l. Thi*s is $100.05 : the payment that you will receive! (Is this okay?)
        Output :  Hello, Kajal. This is $100.05 : the payment that you will receive! Is this okay?
    """
    # The formatted text after removing not necessary punctuations.
    formatted_text = re.sub(r"[^a-zA-Z0-9$%.?!§äöüÄÖÜ]+", ' ', text)
    # The above regex expression provides a necessary set of punctuations that are frequent in this particular dataset.
    return formatted_text


# The code for removing stopwords
stopwords = stopwords.words('english')
set_stopwords = set(stopwords)


# user's is transformed into user and 's
# id stays as id
def removing_stopwords_nltk(text):
    """
    This function will remove stopwords which doesn't add much meaning to a sentence
    & they can be removed safely without compromising meaning of the sentence.

    arguments:
         input_text: "text" of type "String".

    return:
        value: Text after omitted all stopwords.

    Example:
        Input : This is Kajal from delhi who came here to study.
        Output : ["'This", 'Kajal', 'delhi', 'came', 'study', '.', "'"]
    """
    # Text without stopwords
    no_stopwords = [word for word in word_tokenize(text) if word.lower() not in set_stopwords]

    # Convert list of tokens_without_stopwords to String type.
    words_string = ' '.join(no_stopwords)
    return words_string


def manual_words_to_sentences(word_list):
    """
    This function converts a list of words into a list of sentences.

    Arguments:
        word_list: A list of words.

    Returns:
        sentence_list: A list of sentences.
    """
    sentence_list = []
    current_sentence = []

    for word in word_list:
        current_sentence.append(word)

        # Check if the word ends with a period, question mark, or exclamation mark
        if word.endswith('.') or word.endswith('?') or word.endswith('!'):
            # Accessing the last element
            last_element = current_sentence[-1]

            # Removing the last character
            modified_element = last_element[:-1]

            # Updating the last element in the list
            current_sentence[-1] = modified_element

            # Add the list to the sentence list
            sentence_list.append(current_sentence)

            current_sentence = []

    return sentence_list


def automatic_words_to_sentences(word_list):
    """
    This function converts a list of words into a list of sentences.

    Arguments:
        word_list: A list of words.

    Returns:
        sentence_list: A list of sentences.
    """
    text = ' '.join(word_list)

    sentences = sent_tokenize(text)

    split_sentences = [sentence.split() for sentence in sentences]

    # Translator to remove punctuation
    translator = str.maketrans('', '', string.punctuation)

    cleaned_sentences = [sentence[:-1] + [sentence[-1].translate(translator)] for sentence in split_sentences]

    return cleaned_sentences
