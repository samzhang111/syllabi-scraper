import redis

r = redis.Redis('localhost')

successes = r.get('success')
errors = r.get('errors')
timeouts = r.get('timeouts')
dberrors = r.get('dberrors')

print "Successes:", successes
print "404s:", errors
print "Timeouts:", timeouts
print "DB Errors:", dberrors

print "Total: ", int(successes) + int(errors) + int(timeouts) + int(dberrors)
