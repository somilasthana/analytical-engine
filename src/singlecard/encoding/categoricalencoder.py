from __future__ import division


import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder


from ..tools.utils import is_numpy


class CategoryEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, min_count=0, first_category=1, copy=True):
        self.min_count = min_count
        self.first_category = first_category
        self.copy = copy
        self.encoders = {}
        self.ive = None

    def fit(self, x):
        self.encoders = {}
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        ncols = x.shape[1]
        is_np = is_numpy(x)

        #if self.min_count > 0:
        #    self.ive = InfrequentValueEncoder(threshold=self.min_count, value=np.finfo(float).min)
        #    x = self.ive.fit_transform(x)

        for i in range(ncols):
            if is_np:
                enc = LabelEncoder().fit(x[:, i])
            else:
                enc = LabelEncoder().fit(x.iloc[:, i])
            self.encoders.update({i: enc})
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

        if self.ive is not None:
            x = self.ive.transform(x)

        for i in range(ncols):
            enc = self.encoders[i]
            if is_np:
                x[:, i] = enc.transform(x[:, i]) + self.first_category
            else:
                x.iloc[:, i] = enc.transform(x.iloc[:, i]) + self.first_category
        return x
