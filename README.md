# Twitter Collection Scripts

## Description

This is a set of Python scripts that performs some usual data collection tasks from Twitter. This includes continuous crawling of tweets of a list of users or getting all the tweets from a user's timeline.

## Installation

**Packages**

In order for the scripts to run, you need to install [Tweepy](http://docs.tweepy.org/en/v3.5.0/).

**Add the Twitter API Keys (required)**

In order for your scripts to run, you need to authenticate with the Twitter API. This can be done by using the 4 keys Twitter provides you when you register an application. For more information go to https://dev.twitter.com/ To use some scripts (e.g. follow.py) you need to add the read&write access for your application.

You may have multiple consumers, associated with different accounts/applications. You should store these keys in your home directory in a file named .twittertokens The file should contain the 4 keys associated with an application on each line in the following format:
ConsumerKey,ConsumerSecret,AccessToken,AccessSecret

Whenever consumerid is mentioned, it is a integer value k that indicates the credentials on the line k-1 of the file. If not specified, the default consumerid is always 0.

## Scripts

#### getTweets.py

Gets the historical tweets of a list of users. If given a folder where tweet files of users exists, resumes from the last seen tweet. Suitable for running as a cron job in order to update the tweets at a regular time interval.

        python getTweets.py userfile consumerid targetfolder

userfile - file with the list of user ids, one/line (default 'user-file')

consumerid - number of consumer (see installation section)

targetfolder - the target folder name (default 'timelines', creates the folder if it doesn't exist)

#### getTweetsFromId.py

Gets the tweets based on a list of tweet ids.

        python getTweets.py tweetids consumerid 

tweetids - file with the list of tweet ids, one/line

consumerid - number of consumer (see installation section)

Outputs to stdout

#### getReplyId.py

Gets the ids of the tweets that were replied to. 

	cat tweetfile | python getReplyId.py > tweetids

#### pp.py 

Pretty print file with json (sorts keys alphabetically)
	
	cat tt-uk | python pp.py | less
		
## Bugs

The scripts were all ran continuously and all the bugs seem to have been eliminated, so the scripts are safe to be run without needing to worry about crashing. However, if you encounter any bugs, please tell me. All the scripts were tested under Unix.

## To add

Generalize some functions

Make package

## Licence


