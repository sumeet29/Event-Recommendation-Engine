import random
import pandas

f = "data/events.csv"
outf = "data/events_small.csv"
len_train = sum(1 for line in open(f)) - 1
print len_train
lines = 50
skip = sorted(random.sample(range(1, len_train+1),len_train-lines))
df = pandas.read_csv(f,skiprows = skip)
df.to_csv(outf)