import sys
import json
import re

def analyze(scores,tweet):

		nonalpha = re.compile(r'[^a-z]+')
		tokens = nonalpha.split(tweet.lower())
		ssum = 0
		for word in tokens:
			try:
			 ssum = ssum + scores[word]
			except:
			 pass
		#print ssum	 
		return ssum


def tweetparse(tweet_file,sent_file):
	f = sent_file
	scores = {} # initialize an empty dictionary
	for line in f:
	  term, score  = line.split("\t")  
	  # The file is tab-	delimited. "\t" means "tab character"
	  scores[term] = int(score)  # Convert the score to an integer.
	state_dict = {}
	count = 0
	for line in tweet_file:
		count+=1		
		temp = json.loads(line)
		try:	
			if(temp['place']['country_code'] == 'US'):
				state = temp['place']["full_name"][-2:].encode("ascii","ignore")
				if state in state_dict.keys():
					points, num = state_dict[state]
					state_dict[state]= (points + analyze(scores, temp
					["text"].encode('utf-8')), num +1)				
				else:
					state_dict[state]= (analyze(scores,temp["text"].encode
					('utf-8')),1)

		except:
			pass
	
	return state_dict
				

def lines(fp):
    print str(len(fp.readlines()))

def main():
    	sent_file = open(sys.argv[1])
    	tweet_file = open(sys.argv[2])
	dic = tweetparse(tweet_file,sent_file)	
	lst = []	
	for state in dic.keys():
		lst.append((state, float(dic[state][0])/dic[state][1]))
	lst=sorted(lst, key = lambda x: -x[1])
	if lst[0][0]!='US':
		print lst[0][0]
	else: 
		print lst[1][0]

if __name__ == '__main__':
    main()