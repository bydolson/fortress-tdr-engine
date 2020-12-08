import os
import sys
import streamlit as st
import pandas as pd
from scipy.io import loadmat
import pymongo
import warnings

warnings.filterwarnings("ignore")
import numpy as np
from numpy import percentile
import matplotlib.pyplot as plt
import matplotlib.font_manager

from pyod.models.hbos import HBOS

client = pymongo.MongoClient("localhost", 27017)
db = client.fortress

n_samples = st.slider('Number of samples', 200, 1000, step=200)
outliers_fraction = st.slider('Outliers percent', 0.05, 0.25, step=0.05)
clusters_separation = [0]

# Compare given detectors under given settings
# Initialize the data
xx, yy = np.meshgrid(np.linspace(-7, 7, 100), np.linspace(-7, 7, 100))
n_inliers = int((1. - outliers_fraction) * n_samples)
n_outliers = int(outliers_fraction * n_samples)

ground_truth = np.zeros(n_samples, dtype=int)
ground_truth[-n_outliers:] = 1

# initialize a set of detectors for LSCP
detector_list = [LOF(n_neighbors=5), LOF(n_neighbors=10), LOF(n_neighbors=15),
                 LOF(n_neighbors=20), LOF(n_neighbors=25), LOF(n_neighbors=30),
                 LOF(n_neighbors=35), LOF(n_neighbors=40), LOF(n_neighbors=45),
                 LOF(n_neighbors=50)]

# Show the statics of the data
st.write(f'Number of inliers: {n_inliers} , Number of outliers: {n_outliers}')

#IF not already done, convert mat files into csv files
def convert_mat_to_csv(list):
    data_path = os.path.join(current_dir,'data')
    for m_file in list:
        mat_file = os.path.join(data_path, m_file)
        mat = scipy.io.loadmat(mat_file)
        mat = {k:v for k, v in mat.items() if k[0] != '_'}
        data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()})
        save_path = os.path.join(os.path.join(current_dir, 'csv_data'), f'{m_file}.csv')
        data.to_csv(save_path, index = None)

current_dir = os.getcwd()
mat_data = os.listdir(os.path.join(current_dir,'data'))
csv_folder = os.path.join(os.path.join(current_dir, 'csv_data'))
if not len(os.listdir(csv_folder)):
    convert_mat_to_csv(mat_data)

random_state = 42
# Define nine outlier detection tools to be compared
classifiers = {
    '(HBOS) Histogram-base Outlier Detection': HBOS(
        contamination=outliers_fraction)
}


def predict_for_classifier(classifier_name):
  for i, offset in enumerate(clusters_separation):
    np.random.seed(42)
    # Data generation
    X1 = 0.3 * np.random.randn(n_inliers // 2, 2) - offset
    X2 = 0.3 * np.random.randn(n_inliers // 2, 2) + offset
    X = np.r_[X1, X2]
    # Add outliers
    X = np.r_[X, np.random.uniform(low=-6, high=6, size=(n_outliers, 2))]

  clf_name = classifier_name
  clf = classifiers[classifier_name]

  # fit the data and tag outliers
  clf.fit(X)
  scores_pred = clf.decision_function(X) * -1
  y_pred = clf.predict(X)
  threshold = percentile(scores_pred, 100 * outliers_fraction)
  n_errors = (y_pred != ground_truth).sum()
  # plot the levels lines and the points

  Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
  Z = Z.reshape(xx.shape)
  subplot = plt.subplot(3, 4, i + 1)
  subplot.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
                         cmap=plt.cm.Blues_r)
  a = subplot.contour(xx, yy, Z, levels=[threshold],
                            linewidths=2, colors='red')
  subplot.contourf(xx, yy, Z, levels=[threshold, Z.max()],
                         colors='orange')
  b = subplot.scatter(X[:-n_outliers, 0], X[:-n_outliers, 1], c='white',
                            s=20, edgecolor='k')
  c = subplot.scatter(X[-n_outliers:, 0], X[-n_outliers:, 1], c='black',
                            s=20, edgecolor='k')
  subplot.axis('tight')
  subplot.legend(
            [a.collections[0], b, c],
            ['learned decision function', 'true inliers', 'true outliers'],
            prop=matplotlib.font_manager.FontProperties(size=10),
            loc='lower right')
  subplot.set_xlabel("%s (errors: %d)" % (clf_name, n_errors))
  subplot.set_xlim((-7, 7))
  subplot.set_ylim((-7, 7))
  st.subheader("Outlier detection")
  st.pyplot(fig)

if classifier_name:
  predict_for_classifier(classifier_name)
