import json
import sys
for line in sys.stdin:
  try:
    tweet=json.loads(line)
    if tweet["in_reply_to_status_id_str"]:
      print tweet["in_reply_to_status_id_str"]
  except:
    pass
