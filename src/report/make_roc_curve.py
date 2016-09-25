from sklearn.cross_validation import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle
from src.utils.get_time_stamp import get_time_stamp
from sklearn.grid_search import GridSearchCV


def make_roc_curve(pipeline, X, y, train_frac, subject, cfg):
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=train_frac,
                                                        random_state=1,
                                                        stratify=y)
    grid_search = GridSearchCV(pipeline, {}, scoring=cfg['scoring'],
                               verbose=10)
    grid_search.fit(X_train, y_train)
    y_pred_class = grid_search.predict(X_test)
    y_pred_prob = grid_search.predict_proba(X_test)[:, 1]
    acc_score = metrics.accuracy_score(y_test, y_pred_class)
    print(acc_score)
    conf_mat = metrics.confusion_matrix(y_test, y_pred_class)
    print(conf_mat)
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_prob)
    roc_auc = metrics.auc(fpr, tpr)

    # method I: plt

    plt.title(subject + '\nReceiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    fig_dir = cfg['fig_dir']
    plt.savefig(fig_dir + '/roc_curve_' + subject.lower() +
                '_' + get_time_stamp() + '.png')
    results_save = (grid_search, X_test, y_test, acc_score, conf_mat,
                    y_pred_class, y_pred_prob)
    pickle.dump(results_save, open(fig_dir + '/split_data_' + subject.lower() +
                                   '_' + get_time_stamp() + '.p', 'wb'))
