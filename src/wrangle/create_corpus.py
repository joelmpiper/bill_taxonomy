from gensim import corpora, models
import pandas as pd
from textblob import TextBlob
from gensim.parsing.preprocessing import STOPWORDS


def real_corpus(train_title, train_text):

    # get titles
    title_tokens = tokenize(train_title)

    # get full_text
    text_tokens = tokenize(train_text)

    # directory to store the relevant data
    base_dir = '/Users/Joel/Desktop/Insight/data/'

    text_dict = corpora.Dictionary(text_tokens)
    title_dict = corpora.Dictionary(title_tokens)

    text_dict.save(base_dir + 'text.dict')
    title_dict.save(base_dir + 'title.dict')

    text_corpus = [text_dict.doc2bow(t) for t in text_tokens]
    title_corpus = [title_dict.doc2bow(t) for t in title_tokens]

    corpora.MmCorpus.serialize(base_dir + 'text_cor.mm', text_corpus)
    corpora.MmCorpus.serialize(base_dir + 'title_cor.mm', title_corpus)

    return title_corpus, text_corpus


def create_corpora(train_title, train_text):

    # directory to store the relevant data
    base_dir = '/Users/Joel/Desktop/Insight/data/'

    text_dict = corpora.Dictionary.load(base_dir + 'text.dict')
    title_dict = corpora.Dictionary.load(base_dir + 'title.dict')

    text_corpus = corpora.MmCorpus(base_dir + 'text_cor.mm')
    title_corpus = corpora.MmCorpus(base_dir + 'title_cor.mm')

    tfidf_text = models.TfidfModel(text_corpus)
    tfidf_text.save(base_dir + 'tfidf_full_txt.mdl')

    tfidf_title = models.TfidfModel(title_corpus)
    tfidf_title.save(base_dir + 'tfidf_title.mdl')

    title_lda = models.LdaModel(title_corpus, id2word=title_dict,
                                num_topics=2)
    title_lda.save(base_dir + 'lda_title.mdl')

    text_lda = models.LdaModel(text_corpus, id2word=text_dict, num_topics=2)
    text_lda.save(base_dir + 'lda_text.mdl')

    return (title_corpus, text_corpus, tfidf_title, tfidf_text, title_lda,
            text_lda)


def tokenize(texts):

    results = [unicode(text, 'utf-8').lower() for text in texts]
    tests = [TextBlob(word) for word in results]
    return [[word.lemmatize() for word in test.words
             if word not in STOPWORDS] for test in tests]
