from hotqueue import HotQueue
import redis
import sys
sys.path.append('../scraper')

from config import redis_name, path, num_workers

"""
Create a Redis queue for urls to scrape
Populate it with lines from the tsv file at path
Put sentinals at end

"""
def make(name, path, sentinals):
    q = HotQueue(name)
    with open(path) as f:
        for line in f.readlines():
            q.put(line.strip().split('\t'))

    for n in xrange(sentinals):
        q.put(None)

def makestats():
    r = redis.Redis('localhost')
    r.set('success', 0)
    r.set('timeouts', 0)
    r.set('errors', 0)
    r.set('dberrors', 0)

if __name__ == '__main__':
    make(redis_name, path, num_workers)
    makestats()
