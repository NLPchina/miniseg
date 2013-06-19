import marshal
import traceback
from math import log

feature_count = 11

model={
	'states':{'S':0.0,'B':0.0,'M':0.0,'E':0.0},
	'obs':
	{
		'S':[{} for x in range(feature_count)],
		'B':[{} for x in range(feature_count)],
		'M':[{} for x in range(feature_count)],
		'E':[{} for x in range(feature_count)],
		'sum_S':[0]*feature_count,
		'sum_B':[0]*feature_count,
		'sum_M':[0]*feature_count,
		'sum_E':[0]*feature_count
	}
}

def line_update(line):
	global model
	try:
		items = line.split("\t")
		features = items[:feature_count]
		state = items[feature_count].upper()
		model['states'][state]+=1.0
		for idx,chars in enumerate(features):
			if chars.strip()=="":
				continue
			table = model['obs'][state][idx]
			if not (chars in table):
				table[chars]=0.0
			table[chars]+=1.0
			model['obs']['sum_'+state][idx]+=1.0
	except:
		try:
			print line
			print traceback.format_exc()
		except:
			pass

def log_normalize():
	global model
	total = sum(model['states'].values())
	model['states'] = dict([(k,log(v/total)) for k,v in model['states'].iteritems()])
	for state in ('S','B','M','E'):
		for idx,table in enumerate(model['obs'][state]):
			ssum = model['obs']['sum_'+state][idx]
			model['obs'][state][idx] = dict([ (k,log(v/ssum)) for k,v in table.iteritems() if v>1])

def dump_model(file_name):
	global model
	outf = open(file_name,"wb")
	with outf:
		marshal.dump(model,outf)

if __name__ == "__main__":

	ct = 0 
	for line in open("feature.txt",'rb'):
		line = line.rstrip().decode('utf-8')
		line_update(line)
		ct+=1
		if ct%10000==0:
			print "line ", ct, "completed."
	print "loaded."
	log_normalize()
	print "normalized."
	dump_model("bayes_model.marshal")
	print "dumped"

