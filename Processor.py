import json
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

class DataProcessor:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.features = self.data.iloc[:, :-1]
        self.labels = self.data.iloc[:, -1]
        self.feature_nums=len(self.data.iloc[0,:])
        self.label_nums=len(set(self.data.iloc[:,-1]))
        self.has_none = 1 if np.any(self.features.isnull()) else 0
        self.f_mean = np.mean(self.features, axis=0)
        self.f_max = np.max(self.features, axis=0)
        self.f_min = np.min(self.features, axis=0)
        self.f_std = np.std(self.features, axis=0)

    def data_statistics(self):
        msg = {
            "has_none": self.has_none,
            "f_mean": list(self.f_mean),
            "f_max": list(self.f_max),
            "f_min": list(self.f_min),
            "f_std": list(self.f_std)
        }
        return json.dumps(msg, ensure_ascii=False)

    def minmax(self):
        return (self.features - self.f_min) / (self.f_max - self.f_min + 1e-15)

    def standardization(self):
        return (self.features - self.f_mean) / (self.f_std + 1e-15)

    def fill(self,fill):
        temp_features = self.features
        fill_val = None
        if self.has_none:
            for column in list(temp_features.columns[temp_features.isnull().sum() > 0]):
                if fill == "mean":
                    fill_val = temp_features[column].mean()
                elif fill == "max":
                    fill_val = temp_features[column].max()
                elif fill == "min":
                    fill_val = temp_features[column].min()
                elif fill == "zero":
                    fill_val = 0
                temp_features[column].fillna(fill_val, inplace=True)
            return temp_features

    def pca(self, fn, fill="mean"):
        temp_features = self.features
        fill_val = None
        if self.has_none:
            for column in list(temp_features.columns[temp_features.isnull().sum() > 0]):
                if fill == "mean":
                    fill_val = temp_features[column].mean()
                elif fill == "max":
                    fill_val = temp_features[column].max()
                elif fill == "min":
                    fill_val = temp_features[column].min()
                elif fill == "zero":
                    fill_val = 0
                temp_features[column].fillna(fill_val, inplace=True)
        p = PCA(n_components=fn)
        p.fit(temp_features)
        pca_x = p.transform(temp_features)
        contribution = p.explained_variance_ratio_
        return pca_x, contribution
