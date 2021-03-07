from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, \
    load_robot_execution_failures
from tsfresh import extract_features, extract_relevant_features, select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import ComprehensiveFCParameters

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt

download_robot_execution_failures()
df, y = load_robot_execution_failures()
print(df.head())

df[df.id == 3][['time', 'F_x', 'F_y', 'F_z', 'T_x', 'T_y', 'T_z']].plot(x='time', title='Success example (id 3)', figsize=(12, 6))
df[df.id == 20][['time', 'F_x', 'F_y', 'F_z', 'T_x', 'T_y', 'T_z']].plot(x='time', title='Failure example (id 20)', figsize=(12, 6))
# plt.show()

# extract features: for each robot execution (which is our id) and for each of the measured sensor values (F_* and T_*)
# tsfresh will result in a single row for each id and will calculate the features for each columns (we call them "kind") separately

extraction_settings = ComprehensiveFCParameters()
X = extract_features(df, column_id='id', column_sort='time',
                     default_fc_parameters=extraction_settings,
                     # we impute = remove all NaN features automatically
                     impute_function=impute)
# features survive the feature selection given this target
X_filtered = select_features(X, y)

print(X_filtered.head())

X_full_train, X_full_test, y_train, y_test = train_test_split(X, y, test_size=.4)
X_filtered_train, X_filtered_test = X_full_train[X_filtered.columns], X_full_test[X_filtered.columns]

# Compared to using all features 
classifier_full = DecisionTreeClassifier()
classifier_full.fit(X_full_train, y_train)
print(classification_report(y_test, classifier_full.predict(X_full_test)))

# Compared to using only the relevant features, achieves better classification performance with less data
classifier_filtered = DecisionTreeClassifier()
classifier_filtered.fit(X_filtered_train, y_train)
print(classification_report(y_test, classifier_filtered.predict(X_filtered_test)))

# list of selected features
X_filtered_2 = extract_relevant_features(df, y, column_id='id', column_sort='time',
                                         default_fc_parameters=extraction_settings)
print(X_filtered_2.head())
