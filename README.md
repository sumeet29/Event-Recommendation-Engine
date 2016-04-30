
Event Recommendation Engine


        Jeevan Khetwani                        Sameer Sharma	                           Sumeet Agarwal
        jhkhetwa@ncsu.edu                     ssharm20@ncsu.edu 	                    sagarwa6@ncsu.edu


1	Background and Introduction

1.1	 Introduction
Rapid growth of social networking sites and large influx of social data collected from millions of users has made event recommendation one of the most sought after problem in data science. The sheer volume of event data generated on a social networking site and the inherent heterogeneous and incomplete nature of event data makes the problem of event recommendation challenging, but of great business value. A lot of work has been done in this field to achieve better accuracy, which in turn, can result in higher revenues and profits for the companies.

Our goal is to build a event recommendation system that can generate real-time recommendation with a good accuracy. We aim to develop a model that is robust enough to handle data from different sources parsed to some relevant features by data preprocessing.

1.2	Applications and Business value
Recommendation engines are subclasses of information filtering systems that aim to predict the preference or inclination of a user towards a product or service. Recommender systems have become ubiquitous in recent years and their applications can be found in many places.

Recommendation systems can be classified into two broad categories: Collaborative filtering and Content-based filtering models. Collaborative filtering takes advantage of user's past behavior as well as decisions made by similar users or friends of the user. Content-based filtering concentrates on similarities between products to make relevant recommendations. In this project, we followed a hybrid approach where we use both the above stated methods to make event recommendations for a user.

An efficient and accurate event recommendation is of great business value to digital advertising sites and other social media platforms and can be put into use in many other fields as explained below:

•	User-adaptive recommendation systems can take in account the historical information of the user and can make recommendations aligned to user’s past behaviour or recent preferences.
•	Event organizers can promote the event by targeting the right audience for the event and gain popularity by word of mouth.
•	Travel sites can send the specific emails and offers to the customers according to their interests and location.

1.3	The Dataset
We obtained the dataset for training and testing our model from the Event Recommendation Engine Challenge on Kaggle.com. This challenge concluded three years back and the dataset is available on the site for further explorations. Here is the brief description of the data provided.

There are six files in total: train.csv, test.csv, users.csv, user_friends.csv, events.csv and event_attendees.csv.

train.csv (user, event, invited, timestamp, interested, not_interested)
test.csv (user, event, invited, timestamp)
users.csv (user_id, locale, birthyear, gender, joinedAt, location,
          hometown, timezone)
events.csv (event_id, user_id, start_time, city, state, zip, country,
          lat, lng, c_1, c_2, ..., c_100, c_other)
user_friends.csv (user, friends)
event_attendees.csv (event, yes, maybe, invited, no)

Most of the files and their columns listed above are self explanatory apart from events.csv file. Event data contains 110 columns. The first nine columns are event_id, user_id, start_time, city, state, zip, country, latitude, and longitude. The last 101 columns contain the count of 100 most common words which appear in the description of the event and the last column have the count of other words which are not part of these 100 most common words.
One of the major challenge is the sheer amount of data presented to us. Data preprocessing and feature extraction is a critical step as we have to extract the most important features from this large amount of data. Another challenge is the large number of empty fields present in the events data and the non-structured nature of information given in columns like location.

2	Method

As mentioned earlier, we have 6 different csv files containing the data. We have taken the train.csv file (which has all the training data) as the main dataset with which we will train our model on. This dataset contains the userid and eventid fields. We use these fields to expand the rows in train.csv. In other words, what we are doing is that we are picking up a userid and eventid from the train.csv file, matching these ids to the respective ids stored in users.csv and events.csv, and then extracting the corresponding fields from those files and appending them to the corresponding row in train.csv. We tried to compress the all the columns in nine to ten features by using clustering and other data mining techniques.

2.1 	Data Preprocessing

The first challenge was to deal with the missing values. The values that were missing were mostly in the events.csv file, and their presence was not all that important. Hence, we substituted the missing values with ‘NA’ and went ahead with the other fields as usual.

The next challenge was the location field in users.csv. It was not very well formatted (format of the string was not consistent throughout). However, we also realized that user_city and user_country were relatively clean. Also, for our model, we felt that it was enough to know the user_city and user_country. Hence, we just extracted the user_city and user_country from the location field of users.csv.

2.2 	Feature Extraction

We extracted certain features from the dataset we believed were important to train our model. We started off with a list of about 20 features, and then decided on the nine most important ones and went ahead with those. These features are explained below.

•	The first feature which we intuitively decided was very important was ‘is user invited’. It is obvious that if a user was invited, the probability of him attending the event increases. It was pretty straightforward to extract.
•	The next two features are pretty much similar- ‘is user in event city’ and ‘is user in event country’, with the first one obviously having a higher weightage in our model than the second.
•	The next feature is called ‘is user a friend of creator’. The probability of a user going to an event increases if the event creator is a friend of the user. We extracted this feature from the user-friends.csv dataset.
•	The next feature is a very important feature. It is called ‘time difference between notification and event start’. We figured that if a user gets a notification about the event well in advance, he has a higher chance of attending it.
•	The next feature is called ‘number of people interested/not-interested/maybe-interested/not-attending the event’. This feature indicates the popularity of the event. The more popular the event, higher is the chance of a user attending it.
•	The next feature is pretty similar to the previous one. It is called ‘number of friends interested/not-interested/maybe-interested/not-attending the event’. If more friends are attending the event, naturally the user has a higher chance of attending the event.
•	The next feature is called ‘event cluster by topic’. The events.csv file has the frequencies of common words for each event. These events are hence clustered by these words. We have used k-means algorithm for clustering these events.
•	The next feature is called ‘user cluster by community’. This feature was the toughest to extract. We form the user clusters based on their network of friends. Since this thing could be better modeled as a graph, we use community detection to form the user clusters.

2.3 	Techniques Used

Community Detection
The users are related by friendship. This social relation can be captured in a graph framework, where nodes represent users and connections represent some social relation. Then finding clusters in graph becomes a problem of community detection.


We have used Structure-Attribute Clustering Algorithm SAC1, which uses Newman’s modularity function based on structural similarity to detect communities. The algorithm implemented is shown in above figure. Initially each node is assigned to different community. In each iteration, a node is assigned to remaining communities and gain in modularity is calculated. The node is assigned to community with the highest gain. This is done for all the nodes.  Then, all the nodes with same community are reduced to a single node and the process is repeated until no node changes community. We have used igraph package in python to implement community detection.

Clustering of events
The similarity of events is calculated based on the frequency of common terms given in events description data. We have used K-means algorithm to cluster similar events. The k-means is implemented using memory-efficient method big kmeans (package biganalytics) with maximum initial number of clusters.

2.4 	Data Models and Classification

We have used binary logistic regression and random forest to train the model.
In binary logistic regression, binary response variable is related to a set of explanatory variables. It predict probabilities of each class (interested or not interested) of response variable for a given value of set of explanatory variables and classify into class with higher probability.
Random Forest is an ensemble learning method that operates by constructing a multitude of decision trees at training time and predicts the class (interested or not-interested) for test data that is the mode of classes of individual decision trees. It avoids the problem of overfitting and creates a model with low variance by taking average. Random Forest model is flexible enough to accommodate and take care of null and empty values which is of great importance for the data we have in hand.

3	Experiment and Results
3.1	Base model and results

Till date, we have extracted and used nine features to build model for logistic regression and obtained accuracy of around 0.40. We have implemented k-means clustering for the events to reduce 101 columns in the events.csv to one feature. We have also implemented base version of the community detection and need to build on that to achieve higher accuracy rates.

3.2 	Random Forest and Ensemble Models (Under Construction)
3.3 	Validation (Under Construction)

4	Conclusion and future work

We have completed data preprocessing and feature extraction. We have completed the framework for our project that can be tweaked to accommodate future enhancements with minimalistic changes. We have achieved an accuracy rate of 0.4 using the base logistic model.

We are currently working on community detection, which together with other features and event clustering will make model more accurate. We also plan to use random forest that will further improve accuracy. Also, we plan to use Principal Component Analysis (PCA) to extract important features and compare them with features we have obtained manually. We plan to build an ensemble model using multiple classifiers to build upon and increase accuracy of our model. If time allows we also plan to test our model on new dataset obtained from other sources to test the robustness of our recommendation engine.

5	References
[1]  Kaggle Event recommendation challenge: https://www.kaggle.com/c/event-recommendation-engine-challenge

[2]  Sample solution description by Sujit Pal: http://sujitpal.blogspot.com/2013/02/my-solution-to-kaggle-event.html

[3] Augusto Q. Macedo, Leandro B. Marinho and Rodrygo L. T. Santos: Context-Aware Event Recommendation in Event-based Social Networks

[4] Zhi Qiao, Peng Zhang, Chuan Zhou, Yanan Cao1, Li Guo and Yanchun Zhang: Event Recommendation in Event-Based Social Networks
