
def make_param_entries(model_name, prepend, feat_dict, cfg):

    if(model_name in cfg):
        for i, param in enumerate(cfg[model_name]):
            param_key = param.keys()[0]
            feat_dict[prepend + '__' + param_key] = \
                cfg[model_name][i][param_key]
    return feat_dict
