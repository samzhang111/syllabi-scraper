from hotqueue import HotQueue as hq
import redis
import sys

sys.path.append('../scraper')
from config import redis_name

def clear(redis_name):
    if len(sys.argv) > 1:
        name = sys.argv[1]
    q = hq(name)
    q.clear()
