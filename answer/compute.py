import nltk
import sys
import os
import operator
import string
import numpy as np
import pickle

FILE_MATCHES = 1
SENTENCE_MATCHES = 1
INITIATE = False
NEW_FILE = False

def main(ques):
    # files from sever side
    curr_dir = os.path.dirname(os.path.realpath(__file__))  # current directory name
    corpus = os.path.join(curr_dir, 'corpus')
    saved_data = os.path.join(curr_dir, 'saved_data')
    saved_file_path = os.path.join(saved_data, 'data.pkl')      # saved files path.pkl
    saved_words_path = os.path.join(saved_data, 'data_words.pkl')   # saved words path.pkl
    saved_fileIDFs_path = os.path.join(saved_data, 'data_file_idfs.pkl')   # saved file idfs path.pkl
    saved_queries_path = os.path.join(saved_data, 'data_queries.pkl')       # saved queries path.pkl

    """
    file dictionary when initiate the file ,
    when more files added, 
    when no files added
    """
    if INITIATE:                                           # whole calculation
        saved_dict = dict()
        files = initiate_files(saved_file_path, corpus, saved_dict)
    elif NEW_FILE:                                          # added some calculation
        files = add_more_files(saved_file_path, corpus)
    else:                                                   # direct retrieve
        saved_file = open(saved_file_path, "rb")
        files = pickle.load(saved_file)
        saved_file.close()

    """
    file words dictionary when initiate the file,
    when more files added
    when no files added
    """
    if INITIATE:                   # whole calculation
        file_words = {
            filename: tokenize(files[filename])
            for filename in files
        }
        a_file = open(saved_words_path, "wb")
        pickle.dump(file_words, a_file)
        a_file.close()
    elif NEW_FILE:                # added some calculation
        a_file = open(saved_words_path, "rb")
        file_words = pickle.load(a_file)
        a_file.close()

        for filename in files:
            if filename not in file_words:
                file_words[filename] = tokenize(files[filename])

        a_file = open(saved_words_path, "wb")
        pickle.dump(file_words, a_file)
        a_file.close()
    else:                          # direct retrieve
        a_file = open(saved_words_path, "rb")
        file_words = pickle.load(a_file)
        a_file.close()

    """file idf dictionary when initiate or add files, 
       no files added"""
    if INITIATE or NEW_FILE:
        file_idfs = compute_idfs(file_words)           # do whole Calculate IDF values across files
        a_file = open(saved_fileIDFs_path, "wb")
        pickle.dump(file_idfs, a_file)
        a_file.close()
    else:
        a_file = open(saved_fileIDFs_path, "rb")       # direct retrieve the words idf file
        file_idfs = pickle.load(a_file)
        a_file.close()

    # query or the question
    query = set(tokenize(ques))

    if len(query) == 0:
        return "PLEASE , ADD A QUESTION WITH CONTENT WORDS"

    """
    if already asked query
    """
    if INITIATE != True:
        a_file = open(saved_queries_path, "rb")
        saved_query = pickle.load(a_file)
        if repr(query) in saved_query:
            # print("already done", saved_query[repr(query)])
            return saved_query[repr(query)]
        a_file.close()

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
    total_match = ""
    for match in matches:
        total_match += match
        # print(match)

    """
    query dictionary for initiate,
    for new queries
    """
    if INITIATE:
        saved_query =dict()                 # add the starting query dict to file
        saved_query[repr(query)] = total_match
        a_file = open(saved_queries_path, "wb")
        pickle.dump(saved_query, a_file)
        a_file.close()
    else:
        a_file = open(saved_queries_path, "rb")  # add queries to file
        saved_query = pickle.load(a_file)
        saved_query[repr(query)] = total_match
        a_file.close()

        a_file = open(saved_queries_path, "wb")
        pickle.dump(saved_query, a_file)
        a_file.close()

    return total_match

"""
Make a new file for saved files
"""
def initiate_files(saved_file_path, corpus, saved_dict):
    files = add_files(corpus, saved_dict)

    saved_file = open(saved_file_path, "wb")
    pickle.dump(files, saved_file)
    saved_file.close()

    return files

"""
add more files into the saved files 
"""
def add_more_files(saved_file_path, corpus):
    saved_files = open(saved_file_path, "rb")
    saved_dict = pickle.load(saved_files)
    saved_files.close()

    files = add_files(corpus, saved_dict)
    saved_files = open(saved_file_path, "wb")
    pickle.dump(files, saved_files)
    saved_files.close()

    return files

def add_files(directory, saved_dict):
    """
    Given an dicrectory name, and a already existing files directory
    return a dictionary with new files and existing files
    """
    """dictionary  key(file name) --> value(string of content)"""
    files = os.listdir(directory)

    for file in files:
        if file not in saved_dict:
            content = ""
            with open(os.path.join(directory, file), encoding="utf-8") as f:
                content += f.read()  # .replace("\n", " ")

            saved_dict[file] = content

    return saved_dict

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []

    document = document.lower()
    document = nltk.word_tokenize(document)

    # print(nltk.corpus.stopwords.words("english"))
    for word in document:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            words.append(word)

    return words
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    """idf value of each word"""
    total_docs = len(documents)
    words_idf = dict()

    for document in documents:  # for all documents
        for word in documents[document]:

            # already not calculated
            if word not in words_idf:

                # how many document contain this word
                present_in = 1
                for doc in documents:
                    if doc != document and word in documents[doc]:
                        present_in += 1

                        # idf value using log e
                words_idf[word] = np.log(total_docs / present_in)

    return words_idf
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    """best match file"""
    files_rank = dict()

    for file in files:  # for each file calc file score
        file_score = 0
        # for each word in query
        for word in query:
            # if enter wrong spelling
            if word in idfs:
                TF = files[file].count(word)
                idf = idfs[word]
                file_score += TF * idf

        files_rank[file] = file_score

        # list of top n files
    best_files = [k for k, v in sorted(files_rank.items(), key=operator.itemgetter(1), reverse=True)[:n]]

    return best_files
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    """best match passage"""
    """matching word measure"""
    sentence_rank = dict()

    for sentence in sentences:  # for each sentence
        sentence_score = 0

        # matching word measure
        for word in query:
            if word in sentences[sentence]:
                sentence_score += idfs[word]

        sentence_rank[sentence] = sentence_score

    # top n sentences acc matching word measure
    best_sentences = [k for k, v in sorted(sentence_rank.items(), key=operator.itemgetter(1), reverse=True)[:n]]

    """query term density"""
    query_density = dict()
    for sentence in sentences:  # for each sentece
        QTDensity = 0
        # calc query term density
        for word in query:
            if word in sentences[sentence]:
                QTDensity += 1
        QTDensity /= len(sentences[sentence])

        query_density[sentence] = QTDensity

        # if equal word measure and less term density swap
    for j in range(n):
        for i in range(n - 1):
            if sentence_rank[best_sentences[i]] == sentence_rank[best_sentences[i + 1]] and query_density[
                best_sentences[i]] < query_density[best_sentences[i + 1]]:
                best_sentences[i], best_sentences[i + 1] = best_sentences[i + 1], best_sentences[i]

    return best_sentences
    # raise NotImplementedError


#if __name__ == "__main__":
#   main()
