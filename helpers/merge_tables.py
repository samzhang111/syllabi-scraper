import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'toor', 'syllabi')
cur = con.cursor()

for i in xrange(2, 50):
    cur.execute('INSERT INTO worker_0 SELECT * FROM worker_%d'%i)
    con.commit()
    print "Merging tables 0 and", i
