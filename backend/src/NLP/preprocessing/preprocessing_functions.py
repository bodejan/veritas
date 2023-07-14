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


# Code for accented characters removal
def accented_characters_removal(text):
    # this is a docstring
    """
    The function will remove accented characters from the
    text contained within the Dataset.

    arguments:
        input_text: "text" of type "String".

    return:
        value: "text" with removed accented characters.

    Example:
    Input : Málaga, àéêöhello
    Output : Malaga, aeeohello
    """
    # Remove accented characters from text using unidecode.
    # Unidecode() - It takes unicode data & tries to represent it as ASCII characters.
    text = unidecode.unidecode(text)
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
    """expand shortened words to the actual form.
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
    """Removing all the special characters except the one that is passed within
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
    formatted_text = re.sub(r"[^a-zA-Z0-9$%.?!()§]+", ' ', text)
    # The above regex expression provides a necessary set of punctuations that are frequent in this particular dataset.
    return formatted_text


# The code for removing stopwords
stopwords = stopwords.words('english')
set_stopwords = set(stopwords)


# user's is transformed into user and 's
# id stays as id
def removing_stopwords_nltk(text):
    """This function will remove stopwords which doesn't add much meaning to a sentence
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


# user's is transformed into user
# id is sometimes turned into d
# performs lemmatization
def removing_stopwords_spacy(text, nlp):
    """This function will remove stopwords that don't add much meaning to a sentence
       and can be safely removed without compromising the meaning of the sentence.

    Arguments:
        text: Input text of type str.

    Returns:
        words_string: Text after removing all stopwords as a single string.

    Example:
        Input : "This is Kajal from Delhi who came here to study."
        Output: "Kajal Delhi came study ."
    """
    # Tokenize the input text using spaCy
    doc = nlp(text)

    # Remove stopwords from the list of tokens
    no_stopwords = [token.text for token in doc if token.text.lower() not in STOP_WORDS]

    # Convert the list of tokens without stopwords back to a string
    words_string = ' '.join(no_stopwords)

    return words_string


# The code for spelling corrections
def spelling_correction(text):
    """
    This function will correct spellings.

    arguments:
         input_text: "text" of type "String".

    return:
        value: Text after corrected spellings.

    Example:
    Input : This is Oberois from Dlhi who came heree to studdy.
    Output : This is Oberoi from Delhi who came here to study.
    """
    # Check for spellings in English language
    spell = Speller(lang='en')
    corrected_text = spell(text)
    return corrected_text


# The code for lemmatization
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()


def lemmatization(text, v_or_n):
    """This function converts word to their root words (verb or noun) without explicitely cut down as done in stemming.

    arguments:
         input_text: "text" of type "String".
         v_or_n: 'v' for verb or 'n' for noun of type "String".

    return:
        value: Text having root words only, no tense form, no plural forms

    Example (for verbs):
    Input : text reduced
    Output :  text reduce
    """
    # Converting words to their root forms
    lemma = [lemmatizer.lemmatize(w, v_or_n) for w in w_tokenizer.tokenize(text)]
    return lemma


# The Porter stemming algorithm might perform better than the Snowball stemming algorithm in some cases
def porter_stemming(text):
    """This function performs stemming on the given text using the Porter stemming algorithm.

    Arguments:
        text: A string representing the input text to be stemmed.

    Returns:
        stemmed_text: The stemmed text after applying the stemming algorithm.
    """
    # Initialize the Porter stemmer
    stemmer = PorterStemmer()

    # Tokenize the text into individual words
    words = nltk.word_tokenize(text)

    # Apply stemming to each word in the text
    stemmed_words = [stemmer.stem(word) for word in words]

    return stemmed_words


# The Snowball stemming algorithm is an improved version of the Porter stemming algorithm
def snowball_stemming(text, language='english'):
    """This function performs stemming on the given text using the Snowball stemming algorithm.

    Arguments:
        text: A string representing the input text to be stemmed.
        language: (optional) A string representing the language used for stemming. Defaults to 'english'.

    Returns:
        stemmed_text: The stemmed text after applying the Snowball stemming algorithm.
    """
    # Initialize the Snowball stemmer
    stemmer = SnowballStemmer(language)

    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Tokenize each sentence into words
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    # Apply stemming to each word in each sentence
    stemmed_sentences = []
    for sentence in tokenized_sentences:
        stemmed_words = [stemmer.stem(word) for word in sentence]
        stemmed_sentences.append(stemmed_words)

    # Flatten the list of stemmed words
    stemmed_words = [word for sentence in stemmed_sentences for word in sentence]

    return stemmed_words


def manual_words_to_sentences(word_list):
    """This function converts a list of words into a list of sentences.

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
            # Add the list to the sentence list
            sentence_list.append(current_sentence[:-1])
            current_sentence = []

    return sentence_list


def automatic_words_to_sentences(word_list):
    """This function converts a list of words into a list of sentences.

    Arguments:
        word_list: A list of words.

    Returns:
        sentence_list: A list of sentences.
    """
    text = ' '.join(word_list)

    sentences = sent_tokenize(text)

    return sentences
