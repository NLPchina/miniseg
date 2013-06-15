import glob
import pprint
from math import log

prob_start ={
	'S':0.0,
	'B':0.0
}

prob_trans={
	'S':{},
	'B':{},
	'M':{},
	'E':{}	
}

def line2items(line):
	items =[x.split('/') for x in  line.split("  ") if x!=""]
	items = [x[1] for x in items if x[1] in ('B','M','E','S')]
	return items

def update_freq(items):
	global prob_trans,prob_start
	prev_state = None
	for item in items:
		if prev_state == None:
			prob_start[item]+=1.0
			prev_state = item
		else:
			if not (item in prob_trans[prev_state]):
				prob_trans[prev_state][item] = 0.0
			prob_trans[prev_state][item]+=1.0
			prev_state = item

def log_norm_freq():
	global prob_trans,prob_start
	total = sum(prob_start.values())
	prob_start = dict( [ (k, log(v/total)) for k,v in prob_start.iteritems() ] )
	for k,v in prob_trans.iteritems():
		sub_sum = sum(v.values())
		prob_trans[k] = dict([ (kk,log(vv/sub_sum)) for kk,vv in v.iteritems()])

def dump():
	global prob_trans,prob_start
	pprint.pprint(prob_start,open("prob_start.py",'wb'))
	pprint.pprint(prob_trans,open("prob_trans.py",'wb'))

if __name__ == "__main__":

	for fname in glob.glob("train_txt/*.txt"):
		print "reading ", fname
		for line in open(fname,'rb'):
			line = line.rstrip().replace("\t"," ").upper()
			items = line2items(line)
			update_freq(items)
	log_norm_freq()
	dump()



