from __future__ import division


import numpy as np
from scipy.stats import norm
from sklearn.base import BaseEstimator, TransformerMixin
from statsmodels.distributions import ECDF
from ..tools.utils import is_numpy


class PercentileEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, apply_ppf=False, copy=True):
        self.ppf = lambda x: norm.ppf(x * .998 + .001) if apply_ppf else x
        self.copy = copy
        self.ecdfs = {}

    def fit(self, x):
        self.ecdfs = {}
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        ncols = x.shape[1]
        is_np = is_numpy(x)

        for i in range(ncols):
            self.ecdfs.update({i: ECDF(x[:, i] if is_np else x.iloc[:, i].values)})
        return self

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)

    def transform(self, x):
        if self.copy:
            x = x.copy()
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        ncols = x.shape[1]
        is_np = is_numpy(x)

        for i in range(ncols):
            ecdf = self.ecdfs[i]
            if is_np:
                x[:, i] = self.ppf(ecdf(x[:, i]))
            else:
                x.iloc[:, i] = self.ppf(ecdf(x.iloc[:, i]))
        return x