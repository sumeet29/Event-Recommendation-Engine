import louvain
import igraph as ig
import pandas as pd
import itertools

G=ig.Graph()

df = pd.DataFrame
df = df.from_csv('data/user_friends_new.csv')

def limit_communities(partitions, n_communities):
    keyfn = lambda (user, community): community
    sorted_partitions = sorted(partitions.items(), key = keyfn)
    community_groups = [ (community, map(lambda (u,c): u,list(users)))
            for (community, users)
            in itertools.groupby(sorted_partitions, keyfn)]
    major_groups = sorted(community_groups,
                        key = lambda (c, users): len(users),
                        reverse = True)
    major_groups = major_groups[:(n_communities-1)]
    forced_partitions = dict(zip(partitions.keys(),
                    itertools.repeat('level0')))
    for (igroup, (_, users)) in enumerate(major_groups, 1):
        for user in users:
            forced_partitions[user] = 'level'+str(igroup)
    return forced_partitions

users = []
dict_users = {}
dict_reverse = {}
id = 0
for index, row in df.iterrows():
    dict_users[row[0]] = id
    dict_reverse[id] = [row[0]]
    users.append(id)
    G.add_vertex(id)
    id = id + 1
print len(dict_users)

for index, row in df.iterrows():
    print index
    rowList = str(row['friends']).split(' ')
    if rowList:
        for v in rowList:
            if v != 'nan' and int(v) in dict_users:
                G.add_edge(dict_users[row[0]], dict_users[int(v)])

# compute the best partition
partition = louvain.find_partition(G, method='Modularity')

p_dict = {}
index = 0
for i in partition.membership:
    p_dict[index] = i
    index =index + 1

forced_partitions = limit_communities(p_dict, 50)


user_partitions = pd.DataFrame({'user': users,
                    'user_community': map(lambda u: forced_partitions[u], users)})

user_partitions['user'] = user_partitions['user'].replace(dict_reverse)

user_partitions.to_csv("data/communities.csv", header = True, index = False)