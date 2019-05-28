from __future__ import division

from collections import Counter

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


from ..tools.utils import is_numpy


class CountEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, min_count=0, nan_value=-1, copy=True):
        self.min_count = min_count
        self.nan_value = nan_value
        self.copy = copy
        self.counts = {}

    def fit(self, x):
        self.counts = {}
        if len(x.shape) == 1:
            x = x.reshape(-1, 1)
        ncols = x.shape[1]
        is_np = is_numpy(x)

        for i in range(ncols):
            if is_np:
                cnt = dict(Counter(x[:, i]))
            else:
                cnt = x.iloc[:, i].value_counts().to_dict()
            if self.min_count > 0:
                cnt = dict((k, self.nan_value if v < self.min_count else v) for k, v in cnt.items())
            self.counts.update({i: cnt})
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
            cnt = self.counts[i]
            if is_np:
                k, v = np.array(list(zip(*sorted(cnt.items()))))
                ix = np.digitize(x[:, i], k, right=True)
                x[:, i] = v[ix]
            else:
                x.iloc[:, i].replace(cnt, inplace=True)
        return x