import string
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from src.wrangle.make_params import make_param_entries
from sklearn.decomposition import LatentDirichletAllocation
import re

wordnet_lemmatizer = WordNetLemmatizer()


def lemmatize_tokens(tokens, lemma):
    lemmatized = []
    for item in tokens:
        lemmatized.append(lemma.lemmatize(item))
    return lemmatized


def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    text = "".join([ch for ch in text if ch not in string.digits])
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    tokens = word_tokenize(text)
    lemmas = lemmatize_tokens(tokens, wordnet_lemmatizer)
    return lemmas


def my_preproc_text(bill_tuple):
    text = bill_tuple[1].lower()
    revised = " ".join([t for t in text.split() if len(t) > 3])
    return revised


def my_preproc_title(bill_tuple):
    title = bill_tuple[0].lower()
    revised = " ".join([t for t in title.split() if len(t) > 3])
    return revised


def make_tfidf_title_features():
    tfidf_title = TfidfVectorizer(stop_words='english', tokenizer=tokenize,
                                  preprocessor=my_preproc_title,
                                  ngram_range=(1, 3), min_df=10, max_df=0.4)
    return tfidf_title


def make_tfidf_text_features():
    tfidf_text = TfidfVectorizer(stop_words='english', tokenizer=tokenize,
                                 preprocessor=my_preproc_text,
                                 ngram_range=(1, 2), min_df=10, max_df=0.4)
    return tfidf_text


def make_tf_title_features():
    tf_title = CountVectorizer(stop_words='english', tokenizer=tokenize,
                               preprocessor=my_preproc_title,
                               ngram_range=(1, 3), min_df=10, max_df=0.4)
    return tf_title


def make_tf_text_features():
    tf_text = CountVectorizer(stop_words='english', tokenizer=tokenize,
                              preprocessor=my_preproc_text, ngram_range=(1, 2),
                              min_df=10, max_df=0.4)

    return tf_text


def make_lda_text_features(feat_dict, cfg):

    lda_tf_text = make_tf_text_features()
    lda_model_text = LatentDirichletAllocation(n_topics=100, max_iter=5,
                                               learning_method='online',
                                               learning_offset=50.,
                                               random_state=0)
    lda_text = Pipeline(steps=[('lda_tf_text', lda_tf_text),
                               ('lda_model_text', lda_model_text)])

    feat_dict = make_param_entries('lda_tf_text',
                                   "features__lda_text__lda_tf_text",
                                   feat_dict, cfg)
    feat_dict = make_param_entries('lda_model_text',
                                   "features__lda_text__lda_model_text",
                                   feat_dict, cfg)
    return lda_text, feat_dict


def make_lda_title_features(feat_dict, cfg):

    lda_tf_title = make_tf_title_features()
    lda_model_title = LatentDirichletAllocation(n_topics=100, max_iter=5,
                                                learning_method='online',
                                                learning_offset=50.,
                                                random_state=0)
    lda_title = Pipeline(steps=[('lda_tf_title', lda_tf_title),
                                ('lda_model_title', lda_model_title)])

    feat_dict = make_param_entries('lda_tf_title',
                                   "features__lda_title__lda_tf_title",
                                   feat_dict, cfg)
    feat_dict = make_param_entries('lda_model_title',
                                   "features__lda_title__lda_model_title",
                                   feat_dict, cfg)
    return lda_title, feat_dict


def make_feat_union(pipe_feats, cfg):

    feat_un = []
    feat_dict = {}
    feat_vec = None
    for feat in pipe_feats:
        if (feat == 'tf_text'):
            feat_vec = make_tf_text_features()

        if (feat == 'tf_title'):
            feat_vec = make_tf_title_features()

        if (feat == 'tfidf_text'):
            feat_vec = make_tfidf_text_features()

        if (feat == 'tfidf_title'):
            feat_vec = make_tfidf_title_features()

        if (feat == 'lda_text'):
            feat_vec, feat_dict = make_lda_text_features(feat_dict, cfg)

        if (feat == 'lda_title'):
            feat_vec, feat_dict = make_lda_title_features(feat_dict, cfg)

        feat_un.append((feat, feat_vec))
        feat_dict = make_param_entries(feat, "features__" + feat, feat_dict,
                                       cfg)

    return FeatureUnion(feat_un), feat_dict


def make_x_values(bills):

    bill_cols = bills[['bill_name', 'bill_text']]
    return [tuple(x) for x in bill_cols.values]


def make_y_values(bills, subjects, name):

    sub_bills = subjects[subjects['subject'] == name]
    bills[name.lower()] = 0
    bills.ix[bills['bill_num'].isin(sub_bills['bill_num']), name.lower()] = 1
    return bills[name.lower()]
