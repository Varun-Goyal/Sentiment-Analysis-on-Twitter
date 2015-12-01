import sys
import json

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1], 'r')
    tweet_file = open(sys.argv[2], 'r')
    
    # construct an initial dict
    dict = construct_dict(sent_file)
    # construc a new dict to store the new terms
    # the items are lists of integers, each of the integer suggesting the score of the sentence with the word in it
    newdict = construct_new_dict(tweet_file, dict)
    for newterm in newdict:
    	print newterm.encode("utf-8")+" ", (sum(newdict[newterm])/len(newdict[newterm]))

def construct_dict(sent_file):
	scores = {} # initialize an empty dictionary
	for line in sent_file:
	  term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
	  scores[term] = int(score)  # Convert the score to an integer.
	return scores

def construct_new_dict(tweet_file, dict):
	newdict = {}
	for line in tweet_file:
		data = json.loads(line)
		if "tweet" in line:
			tweet = data['text']
			tweet_score = get_score(dict, tweet)
			for word in tweet.split(" "):
				if word not in dict:
					# handle new term
					if word not in newdict:
						newdict[word] = [tweet_score]
					else:
						newdict[word].append(tweet_score)
	return newdict

## given the dict and a single tweet, return the score of this tweet
def get_score(dict, tweet):
	score = 0
	for word in tweet.split(" "):
		if word in dict:
			current_score = dict[word]
		else:
			current_score = 0
		score += current_score
	return score

if __name__ == '__main__':
    main()