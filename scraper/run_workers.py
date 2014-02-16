import worker
import redis
import multiprocessing
from hotqueue import HotQueue
from config import redis_name, num_workers, timeout, wayback

def get_redis(name):
    q = HotQueue(name)
    r = redis.Redis('localhost')
    return q, r

def main():
    workers = []
    q, r = get_redis(redis_name)
    for i in xrange(num_workers):
        p = multiprocessing.Process(target=worker.scraper_worker, args=(i, q, r, timeout, wayback))
        p.start()
        workers.append(p)

    for w in workers:
        w.join()

if __name__ == '__main__':
    main()
