import json
import sys
for line in sys.stdin:
  try:
    tweet=json.loads(line)
    print json.dumps(tweet,indent=4,sort_keys=True)
  except:
    pass
