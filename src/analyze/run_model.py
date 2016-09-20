from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from src.wrangle.make_params import make_param_entries

import datetime
import pickle


def create_model(feat_un, model_name, feat_grid, cfg):

    pipeline, param_dict = make_pipeline(feat_un, model_name, feat_grid, cfg)

    scoring = cfg['scoring']
    verbose = cfg['verbose']
    folds = cfg['folds']
    grid_search = GridSearchCV(pipeline, cv=folds, param_grid=param_dict,
                               scoring=scoring, verbose=verbose)
    return grid_search


def make_pipeline(feat_un, model_name, feat_dict, cfg):

    if (model_name == 'logistic_regression'):
        model = LogisticRegression(C=1e9, penalty='l1')

    elif (model_name == 'svc'):
        model = SVC()

    elif (model_name == 'naive_bayes'):
        model = MultinomialNB()

    feat_dict = make_param_entries(model_name, 'model', feat_dict, cfg)
    pipe = Pipeline(steps=[('features', feat_un), ('model', model)])

    return pipe, feat_dict


def run_model(model, X, y, sub, cfg):

    model.fit(X, y)

    if cfg['save_model']:
        save_result(model, X, y, sub, cfg)

    return model


def save_result(obj, X, y, sub, cfg):

    file_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    if(cfg['also_save_data']):

        save_string = cfg['model_dir'] + 'data_model_' + sub + '_' + \
            file_time + '.p'
        saved_obj = (obj, X, y)
        pickle.dump(saved_obj, open(save_string, 'wb'))

    save_string = cfg['model_dir'] + 'model_' + sub + '_' + file_time + '.p'
    pickle.dump(obj, open(save_string, 'wb'))


def get_y_probs(fit_mod, X):

    return fit_mod.predict_proba(X)[:, 1]
