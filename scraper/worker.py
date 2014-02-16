import requests
import redis
import multiprocessing
from hotqueue import HotQueue
import MySQLdb as mdb
import db_settings
import sys
import lxml
from lxml.html.clean import clean_html
#import pdb

def strip_wayback(src):
    h = lxml.html.fromstring(src)
    h.remove(h.find('div[@id="wm-ipp"]'))
    return lxml.html.tostring(h)

def setup_db():
    try:
        con = mdb.connect(db_settings.host,\
                    db_settings.user,\
                    db_settings.pw,\
                    db_settings.db)

        cur = con.cursor()
    except mdb.Error, e:
        print "---> Database Connection Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    return con, cur

def scraper_worker(worker_id, q, r, timeout=2, wayback=False):
    wayback_base = "http://web.archive.org/web/"
    iteration = 0
    con, cur = setup_db()
    
    for item in q.consume():
        if not item:
            print "%d: RECEIVED SENTINEL" % worker_id
            #received sentinel
            break
        syllabi_id, link = item
        #pdb.set_trace()
        if wayback:
            link = wayback_base + link
        try:
            req = requests.get(link, timeout = timeout)
            if req.status_code != requests.codes.ok:
                r.incr("errors")
            else:
                src = clean_html(req.text)
                if wayback:
                    src = strip_wayback(src)
                try:
                    #pdb.set_trace()
                    cur.execute("INSERT INTO " + db_settings.table_name + " (syllabiID, chnm_cache) VALUES (%s,%s)", 
                                (syllabi_id, src))
                    con.commit()
                    r.incr("success")
                except mdb.Error, e:
                    print "---> DB insert error on worker %d on iteration %d -> %s\n\tReconnecting cursor..." % (worker_id, iteration, e)
                    r.incr("dberrors")
                    con, cur = setup_db()
        except:
            r.incr("timeouts")

if __name__ == "__main__":
    from config import redis_name, wayback
    scraper_worker(0, HotQueue(redis_name), redis.Redis('localhost'), wayback=wayback)
