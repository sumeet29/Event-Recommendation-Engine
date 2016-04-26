from pandas import DataFrame
import csv, sys
import pandas as pd
from dateutil.parser import parse

na = ['None', ' ', 'NA', '']

def loadTrainingData(path):
    # Columns: user, event, invited, timestamp, interested, not_interested
    training_data = pd.read_csv(path, header=0, na_values=na)
    return training_data

def expandUsers(training_data):
    # Columns: user_id, locale, birthyear, gender, joinedAt, location, timezone
    unique_users = set(training_data['user'])
    with open('data/users.csv', 'r') as users:
        reader = csv.reader(users)
        user_headers = reader.next()
        user_headers = ["user", "user_locale", "user_birthyear", "user_gender", "user_joinedAt", "user_location", "user_timezone"]
        user_data = [[int(row[0])] + row[1:] for row in reader if int(row[0]) in unique_users]
    users = DataFrame(user_data, columns = user_headers)
    return pd.merge(training_data, users)

def expandEvents(training_data):
    # Columns: event_id,user_id,start_time,city,state,zip,country,lat,lng,c_1, ... c_100, c_other
    unique_events = set(training_data['event'])
    with open('data/events.csv', 'r') as events:
        reader = csv.reader(events)
        event_headers = reader.next()
        event_headers = ['event', 'admin'] + ["event_header_"+ i for i in event_headers[2:]]
        event_data = [[int(row[0])] + row[1:] for row in reader if int(row[0]) in unique_events]
    events = DataFrame(event_data, columns = event_headers)
    return pd.merge(training_data, events)

def findFriends(training_data):
    unique_users = set(training_data['user'])
    with open('data/user_friends.csv', 'r') as friends_data:
        reader = csv.reader(friends_data)
        reader.next()
        user_friends = dict([[int(user), set([int(user)]+[int(f) for f in friends.split(' ')])]
                             for (user, friends) in reader
                             if int(user) in unique_users])
    return user_friends

def toIntList(str):
    return [] if not str else map(int, str.split(' '))

def eventAttendees(training_data):
    unique_events = set(training_data['event'])
    with open('data/event_attendees.csv', 'r') as attendee:
        reader = csv.reader(attendee)
        reader.next()
        attendee_headers = ['interested_users', 'maybe_users', 'invited_users', 'notinterested_users']
        event_attendees = {}
        for (event, interested_users, maybe_users, invited_users, notinterested_users) in reader:
            if int(event) in unique_events:
                event_attendees[int(event)] = dict(zip(
                    attendee_headers,
                    [toIntList(interested_users),
                    toIntList(maybe_users),
                    toIntList(invited_users),
                    toIntList(notinterested_users)]
                ))
    return event_attendees

def addAttendeesInfo(training_data):
    unique_events = set(training_data['event'])
    attendance_headers=['event','event_interested_ratio','event_maybe_ratio','event_invited_ratio','event_no_ratio']
    with open('data/event_attendees.csv','r') as attendees:
        reader=csv.reader(attendees)
        reader.next()
        attendees_data=[]
        for(event_id, interested_users, maybe_users, invited_users, notinterested_users) in reader:
            if int(event_id) in unique_events:
                (interested_users, maybe_users, invited_users, notinterested_users) = \
                    [interested_users.split(' '), maybe_users.split(' '), invited_users.split(' '), notinterested_users.split(' ')]
                total = len(interested_users) + len(maybe_users) + len(invited_users) + len(notinterested_users)
                (total_interested, total_maybe, total_invited, total_no) = \
                    [float(len(interested_users))/total,float(len(maybe_users))/total,
                     float(len(invited_users))/total,float(len(notinterested_users))/total]
                attendees_data.append([int(event_id), total_interested, total_maybe, total_invited, total_no])
    final_data=DataFrame(attendees_data, columns=attendance_headers)
    return pd.merge(training_data,final_data)


def getRatioOfInterestedAttendees(k, event_attendees, user_friends):
   e = k[1]['event']
   u = k[1]['user']
   return float(len(set(event_attendees[e]['interested_users']).intersection(set(user_friends[u]))))/len(set(user_friends[u]))

def getRatioOfNotInterestedAttendees(k, event_attendees, user_friends):
   e = k[1]['event']
   u = k[1]['user']
   return float(len(set(event_attendees[e]['notinterested_users']).intersection(set(user_friends[u]))))/len(set(user_friends[u]))

def getRatioOfMaybeAttendees(k, event_attendees, user_friends):
   e = k[1]['event']
   u = k[1]['user']
   return float(len(set(event_attendees[e]['maybe_users']).intersection(set(user_friends[u]))))/len(set(user_friends[u]))

def getRatioOfInvitedAttendees(k, event_attendees, user_friends):
   e = k[1]['event']
   u = k[1]['user']
   return float(len(set(event_attendees[e]['invited_users']).intersection(set(user_friends[u]))))/len(set(user_friends[u]))

def addFriendAttendees(train, user_friends, event_attendees):
  interested = []
  notInterested = []
  maybe = []
  invited = []
  for k in train.iterrows():
      interestedUsers = getRatioOfInterestedAttendees(k, event_attendees, user_friends)
      invitedUsers = getRatioOfInvitedAttendees(k, event_attendees, user_friends)
      maybeUsers = getRatioOfMaybeAttendees(k, event_attendees, user_friends)
      notInterestedUsers = getRatioOfNotInterestedAttendees(k, event_attendees, user_friends)
      interested.append(interestedUsers)
      notInterested.append(notInterestedUsers)
      maybe.append(maybeUsers)
      invited.append(invitedUsers)
  train['interested_frnds_ratio'] = interested
  train['notinterested_frnds_ratio'] = notInterested
  train['maybe_frnds_ratio'] = maybe
  train['invited_frnds_ratio'] = invited
  return train

def sameCity(k):
   event_city = k['event_header_city'].lower()
   location = k['user_location'].lower()
   if location in 'na':
       return False
   return event_city in location

def sameCountry(k):
   event_city = k['event_header_city'].lower()
   location = k['user_location'].lower()
   if location in 'na':
       return False
   if event_city in location:
       return True
   event_country = k['event_header_country'].lower()
   location = k['user_location'].lower()
   return event_country in location

def fixNA(k):
   list = []
   for i in k:
       if i in na:
           list.append('NA')
       else:
           list.append(i)
   return list

def calcAge(k):
   if (k['user_birthyear'] is not 'NA'):
       year = int(k['user_birthyear'])
       return 2016 - year
   else:
       return 'NA'

def calcTime(k):
   start = parse(k['event_header_start_time'])
   end = parse(k['timestamp'])
   timeLeft = (start - end).total_seconds() / 3600.0
   return timeLeft

def generateModelData(training_data):
    training_data = training_data.apply(fixNA, axis = 1)
    training_data['time_left'] = training_data.apply(calcTime, axis = 1)
    training_data['user_age'] = training_data.apply(calcAge, axis = 1)
    user_friends = findFriends(training_data)
    training_data['admin_friend'] = training_data.apply(lambda r: int(r['admin']) in user_friends[r['user']],axis = 1)
    print 'finish adding friend_with_creator', len(training_data)
    event_attendees = eventAttendees(training_data)
    training_data = addFriendAttendees(training_data, user_friends, event_attendees)
    print 'finish adding friends', len(training_data)

    training_data['same_city'] = training_data.apply(sameCity, axis = 1)
    training_data['same_country'] = training_data.apply(sameCountry, axis = 1)

<<<<<<< HEAD
    training_data.to_csv("data/output.csv", na_rep = 'NA', header = True, index = False)

    inputs_in_use = ['user',
                     'event',
                     'invited',
                     'user_locale',
                     'same_city',
                     'same_country',
                     'user_gender',
                     'admin_friend',
                     # 'event_interests',
                     # 'event_potential_interests',
                     # 'event_invites',
                     # 'event_nointerests',
                     'event_interested',
                     'event_no',
                     'event_maybe',
                     'event_invited',
                     # 'event_interests_ratio',
                     # 'event_potential_interests_ratio',
                     # 'event_invites_ratio',
                     # 'event_nointerests_ratio',
                     'time_left',
                     'user_age',
                     'interested_frnds',
                     'maybe_frnds',
                     'invited_frnds',
                     'notinterested_frnds',
                     # 'topic',
                     # 'user_community',
                     # 'interested_frnds_ratio',
                     # 'maybe_frnds_ratio',
                     # 'invited_frnds_ratio',
                     # 'notinterested_frnds_ratio',
                     ]

    training_data = training_data[inputs_in_use]
=======
    training_data.to_csv("output.csv", na_rep = 'NA', header = True, index = False)

    cols_used = ['user',
                'event',
                'invited',
                'user_locale',
                'user_joinedAt'
                'same_city',
                'same_country',
                'user_gender',
                'admin_friend',
                'event_interested_ratio',
                'event_no_ratio',
                'event_maybe_ratio',
                'event_invited_ratio',
                'time_left',
                'user_age',
                'interested_frnds_ratio',
                'maybe_frnds_ratio',
                'invited_frnds_ratio',
                'notinterested_frnds_ratio',

                # 'topic',
                # 'user_community',

                ]

    training_data = training_data[cols_used]
>>>>>>> 63078ea947fd942723d48563c13b4801461d62a4
    return training_data


def writeToFile(training_data, file_path):
    training_data = training_data.sort_values(by = 'user')
    training_data.to_csv(file_path, na_rep = 'NA', header = True, index = False)


def main():

    if len(sys.argv) is not 1:
        print len(sys.argv)
        print 'Usage: data_preprocessor.py'
        sys.exit(-1)

    training_data = loadTrainingData('data/train_small.csv')

    print 'Finished reading original data', len(training_data)
    training_data = expandUsers(training_data)
    print 'Finished filling user information', len(training_data)
    training_data = expandEvents(training_data)
    print 'Finished filling events information', len(training_data)

    # training_data = findUserCommunities(training_data)
    # print 'Finished filling user communities', len(training_data)

    training_data = addAttendeesInfo(training_data)
    print 'Finished filling attendence information', len(training_data)

    # training_data = findEvenClusters(training_data)
    # print 'finished filling event clustering information', len(training_data)

    training_data = generateModelData(training_data)
    print 'Finished post-processing train data'

    writeToFile(training_data, "feature_train.csv")
    print 'Finished writing data'

if __name__ == '__main__':
    main()