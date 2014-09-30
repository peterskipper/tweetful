import authorization
import json
import requests
from collections import defaultdict
import operator

from urls import *

def where_from(timeline):
    total = 0
    locs = defaultdict(int)
    for tweet in timeline:
        try:
            key = tweet["user"]["location"]
        except KeyError:
            continue
        locs[key] += 1
        total += 1
    try:
        val = locs.pop('')
        locs["No Location Given"] = val
    except KeyError:
        pass

    return total, locs


def main():
    """Main function"""
    auth = authorization.authorize()
    response = requests.get(TIMELINE_URL, auth=auth)
    #print json.dumps(response.json(), indent=4)
    total, locs = where_from(response.json())
    sorted_locs = sorted(locs.iteritems(),
        key=operator.itemgetter(1),
        reverse=True)
    print total

    for loc, tweets in sorted_locs:
        print "{}: {:.1%}".format(loc, tweets/float(total))



if __name__ == '__main__':
    main()