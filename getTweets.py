import json
import time
import tweepy
import datetime
import sys
import os

def loadTokensIndex(loc):
  f = file(loc,"r")
  index = []
  for line in f.readlines():
    if line.startswith("#"): continue
    parts = [x.strip() for x in line.split(",")]
    (consumer_key,consumer_secret,auth_key,auth_secret) = parts
    tokens = dict()
    tokens["CLIENT_KEY"] = consumer_key
    tokens["CLIENT_SECRET"] = consumer_secret
    tokens["ATOKEN_KEY"] = auth_key
    tokens["ATOKEN_SECRET"] = auth_secret
    index = index + [tokens]
  return index

def wait(t, verbose = True):
  """Wait function, offers a nice countdown"""
  if not verbose:
    print "Waiting " + str(t) + " seconds"
  for i in xrange(t):
    if verbose:
      print "\rDone waiting in: %s" % datetime.timedelta(seconds=(t-i)),
      sys.stdout.flush()
    time.sleep(1)
  if verbose:
    print "\rDone waiting!           "

def handle(e):
  if str(e)=="Not authorized.":
    l = 0
  else:
    l = 1
    try:
      code = e.message[0]['code']
      if code == 88:
        r = api.rate_limit_status()
        now = int(time.time())
        reset = int(r["resources"]["statuses"]["/statuses/user_timeline"]["reset"])
        wait(reset - now + 1, False)
      elif code == 34:
        print e
        l = 0
      elif code == 130:
        print e
        wait(60, False)
      elif code == 131:
        print e
        wait(60, False)
      else:
        print e
    except:
      print e
  return l


CONF_DIR = os.getenv('HOME') # where to find the configuration
USER_FILE = (sys.argv[1] if len(sys.argv) >= 2 else "user-file")
CONSUMER = (int(sys.argv[2]) if len(sys.argv) >= 3 else 0)
FOLDER = (sys.argv[3] if len(sys.argv) >= 4 else "timelines")
if not os.path.exists(FOLDER): os.makedirs(FOLDER)
tokensIndex = loadTokensIndex(os.sep.join([CONF_DIR,".twittertokens"]))
tokens = tokensIndex[CONSUMER]

auth = tweepy.OAuthHandler(tokens['CLIENT_KEY'], tokens['CLIENT_SECRET'])
auth.set_access_token(tokens['ATOKEN_KEY'], tokens['ATOKEN_SECRET'])

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

fin = open(sys.argv[1],'r')
for line in fin:
  tweets = []
  uid = line.strip().lower().split()[0]
  print datetime.datetime.now()
  print "Getting tweets for user", uid
  old = 1
  maxid = sys.maxint - 1
  FNAME = FOLDER + "/" + uid
  if (os.path.exists(FNAME)) or (os.path.exists(FNAME+".gz")) or (os.path.exists(FNAME+".lzo")): 
    f=open(FNAME)
    lline=''
    for line in f:
      lline = line
    f.close()
    try:
      old = int(json.loads(lline)['id']) + 1
    except:
      pass

  l = 1 
  while l > 0:
    try: 
      new_tweets = api.user_timeline(id=uid, count=200, since_id=old, max_id=maxid)
      tweets.extend(new_tweets)
      l = len(new_tweets)
      if l > 0:
        maxid = tweets[-1]['id'] - 1 
    except tweepy.TweepError as e:
      l = handle(e)
  print len(tweets),"tweets downloaded"
  if len(tweets) > 0:
    fout = open(FOLDER + '/' + uid, 'a+')
    for tweet in reversed(tweets):
      print >> fout, json.dumps(tweet)  
    fout.close()
   
fin.close()
