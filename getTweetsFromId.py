import codecs
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
    l = 1
  else:
    l = 0
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
f = open(sys.argv[1],"r")
CONSUMER = (int(sys.argv[2]) if len(sys.argv) >= 3 else 0)
tokensIndex = loadTokensIndex(os.sep.join([CONF_DIR,".twittertokens"]))
tokens = tokensIndex[CONSUMER]

auth = tweepy.OAuthHandler(tokens['CLIENT_KEY'], tokens['CLIENT_SECRET'])
auth.set_access_token(tokens['ATOKEN_KEY'], tokens['ATOKEN_SECRET'])

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

twids = []
for line in f:
  twid = line.strip()
  twids.append(twid)
  if len(twids) >= 100:
    l = 0
    while l == 0:
      try:
        new_tweets = api.statuses_lookup(twids)
        l = len(new_tweets)
      except tweepy.TweepError as e:
        l = handle(e)
    for tweet in new_tweets:
      print json.dumps(tweet)
    twids = []

f.close()
