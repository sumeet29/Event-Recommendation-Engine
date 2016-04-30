from sklearn.cluster import KMeans
from pandas import DataFrame
import pandas as pd

na = ['None', ' ', 'NA', '']
path = "data/events.csv"
output_path = "data/cluster_events.csv"
events = pd.read_csv(path, header=0, na_values=na)
events_id = events.ix[:, 0]
events_keywords = events.ix[:, 10:] 


kmeans = KMeans(n_clusters = 50, max_iter = 40, n_init = 4)
clusters = DataFrame(kmeans.fit_predict(events_keywords))
result = pd.concat([events_id, clusters], axis=1, join='inner', )
result.columns = ['event_id', 'cluster']
result.to_csv(output_path, na_rep = 'NA', header = True, index = False)
