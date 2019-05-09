import logging
import json,os
import glob
import pickle 
import gensim
from gensim import corpora
import pyLDAvis.gensim
import nltk
from nltk.tokenize import RegexpTokenizer   
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk import word_tokenize
import azure.functions as func
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService

# Application Settings #
PUNKT_SENTENCE_TOKENIZER_BLOBURL = os.environ.get('NltkPunktSentenceTokenizer')
STOPWORDS_ENGLIST_SET_BLOBURL = os.environ.get('NltkStopWords')
GUTENBERG_BLOB_ACCOUNT_NAME = os.environ.get('GutenbergBlobAccountName')
GUTENBERG_BLOB_ACCOUNT_KEY = os.environ.get('GutenbergBlobAccountKey')

_treebank_word_tokenizer = TreebankWordTokenizer()
_nltk_stopwords = nltk.data.load(STOPWORDS_ENGLIST_SET_BLOBURL).split('\n')
_nltk_tokenizer = nltk.data.load(PUNKT_SENTENCE_TOKENIZER_BLOBURL)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        container_name = req_body.get('container_name')
#        container_models = container_name + "models"
        container_models = "ldamodel"

    _nltk_stopwords.append("could")
    _nltk_stopwords.append("would")
    _nltk_stopwords.append("still")
    _nltk_stopwords.append("shall")

    # List Blobs in the container
    block_blob_service = BlockBlobService(account_name=GUTENBERG_BLOB_ACCOUNT_NAME, 
                                          account_key=GUTENBERG_BLOB_ACCOUNT_KEY) 
    logging.info("\nList blobs in the container")
    generator = block_blob_service.list_blobs(container_name)
    data = []
    doc_map = {}
    doc_id = 1
    for blob in generator:
        logging.info("\t Blob name: " + blob.name)
        readblob = block_blob_service.get_blob_to_bytes(container_name, # name of the container
                                                        blob.name)
        doc_map[doc_id] = blob.name
        blob_content  = str(readblob.content)
        raw = blob_content.replace('\n','').replace('\r','').replace('\r\n','')
        cleaned_raw = raw.replace('\\r\\n','')
        data.append(cleaned_raw)
        doc_id += 1
                
    token_data = []
    for doc in data:
        tokens = prepare_text_for_lda(doc)
        token_data.append(tokens)
    pickled_token_data = pickle.dumps(token_data) 
    pickled_docmap = pickle.dumps(doc_map)
    block_blob_service.create_blob_from_bytes(container_models, "token_data" + container_name, pickled_token_data)
    block_blob_service.create_blob_from_bytes(container_models, "docmap" + container_name, pickled_docmap)


    dictionary = corpora.Dictionary(token_data)
    corpus = [dictionary.doc2bow(text) for text in token_data]

    num_topics = req_body.get('num_topics')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word=dictionary, passes=15)

    lda_blob_url = "https://" + "gutenbergbooks" + ".blob.core.windows.net/" + container_models + "/" + "ldamodel.html"
    settings = ContentSettings(content_type='text/html')
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    p_data = pyLDAvis.prepared_data_to_html(vis)
    block_blob_service.create_blob_from_text(container_models, 'ldamodel.html', p_data)
    block_blob_service.set_blob_properties(container_models, 'ldamodel.html', content_settings=settings)
    if container_name:
        return func.HttpResponse(lda_blob_url)
    else:
        return func.HttpResponse(
             "Please pass a dataset name",
             status_code=400
        )


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    en_stop = set(_nltk_stopwords)

    tokens = custom_nltk_tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    
    # TODO: find another lemmatizer. https://github.com/nltk/nltk/issues/2127 raised on NLTK
    # tokens = [get_lemma(token) for token in tokens]
    return tokens

'''
    Tokenizes used TreeBank Tokenizer and PunktSentence Tokenizer.
    Customized from NLTK as ntlk data load automatically loads english tokenizer from 
    nltk_data path. We want to load this from a Azure Blob.
    nltk_tokenizer variable in this method preloads the PunktSentenceTokenizer for English
    from Azure blob
    Returns:
    Tokenized text
'''

def custom_nltk_tokenize(text,language='english', preserve_line=False):
        sentences = [text] if preserve_line else _nltk_tokenizer.tokenize(text, language)
        return [token for sent in sentences
            for token in _treebank_word_tokenizer.tokenize(sent)]
