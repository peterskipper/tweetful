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

def popular(friend_list, size):
    followers = []
    for friend in friend_list["users"]:
        followers.append((friend["name"],friend["followers_count"]))
    sorted_followers = sorted(followers, key=operator.itemgetter(1),
        reverse=True)
    return sorted_followers[:size]

def main():
    """Main function"""
    auth = authorization.authorize()
    response = requests.get(FRIENDS_URL, auth=auth)
    pop_list = popular(response.json(),10)
    for item in pop_list:
        print "{} : {:,} followers".format(item[0], item[1])
    #response = requests.get(TIMELINE_URL, auth=auth)
    #print json.dumps(response.json(), indent=4)
    #total, locs = where_from(response.json())
    #sorted_locs = sorted(locs.iteritems(),
    #    key=operator.itemgetter(1),
    #    reverse=True)
    #print total

    #for loc, tweets in sorted_locs:
    #    print "{}: {:.1%}".format(loc, tweets/float(total))



if __name__ == '__main__':
    main()