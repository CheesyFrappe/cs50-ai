import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    ret_dict = {}

    for f in os.listdir(directory):
        path = os.path.sep.join([directory, f])
        ret_dict[f] = open(path).read()

    return ret_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    word_list = [word for word in words if word not in nltk.corpus.stopwords.words('english') and word not in string.punctuation]
        
    return word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_dict = {}
    total_docs = len(documents.keys())
    
    for list in documents.values():
        # eliminate duplicate words
        for word in set(list):
            try:
                idf_dict[word] += 1
            except KeyError:
                idf_dict[word] = 1
    
    for key, value in idf_dict.items():
        num_does_contain = value
        idf_dict[key] = math.log(total_docs / num_does_contain)

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranked_dict = {}

    for key, value in files.items():
        ranked_dict[key] = 0 
        for word in query:
            if word in value:
                ranked_dict[key] += idfs[word] * value.count(word)
    
    sorted_temp =[x[0] for x in sorted(ranked_dict.items(), key=lambda x: x[1], reverse= True)]

    return sorted_temp[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranked_dict = {}

    for key, value in sentences.items():
        rank = 0
        word_count = 0
        for word in query:
            if word in value:
                rank += idfs[word]
                word_count += value.count(word)
        if rank != 0 and word_count != 0:
            density = word_count / len(value)
            ranked_dict[key] = (rank, density)

    sorted_temp =[x[0] for x in sorted(ranked_dict.items(), key=lambda y: (y[1], y[1]), reverse= True)]

    return sorted_temp[:n]

if __name__ == "__main__":
    main()

"""
How do neurons connect in a neural network?
When was Python 3.0 released?
What are the types of supervised learning?
"""