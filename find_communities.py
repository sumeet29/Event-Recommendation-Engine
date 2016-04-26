import community
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

edgeDict = {}
G=nx.Graph()

df = pd.DataFrame
df = df.from_csv('../data/user_friends.csv')

for index, row in df.iterrows():
    G.add_node(row[0])
    # rowList = row['friends'].split(' ')
    # if int(row[0]) in edgeDict:
    #     edgeDict[int(row[0])].append(rowList)
    # else:
    #     edgeDict[int(row[0])] = rowList


for index, row in df.iterrows():
    rowList = str(row['friends']).split(' ')
    if not rowList:
        for v in rowList:
            G.add_edge(row[0], v)

# first compute the best partition
partition = community.best_partition(G)
counter = 0
for key in partition.keys():
    print ("Community" + str(counter))
    counter = counter + 1
    print key

#drawing
# size = float(len(set(partition.values())))
# pos = nx.spring_layout(G)
# count = 0.
# for com in set(partition.values()) :
#     count = count + 1.
#     list_nodes = [nodes for nodes in partition.keys()
#                                 if partition[nodes] == com]
#     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
#                                 node_color = str(count / size))
# nx.draw_networkx_edges(G,pos, alpha=0.5)
# plt.show()