import marshal
from math import log

model={
	'states':{'S':0.0,'B':0.0,'M':0.0,'E':0.0},
	'obs':
	{
		'S':[{} for x in range(10)],
		'B':[{} for x in range(10)],
		'M':[{} for x in range(10)],
		'E':[{} for x in range(10)],
		'sum_S':[0]*10,
		'sum_B':[0]*10,
		'sum_M':[0]*10,
		'sum_E':[0]*10
	}
}

def line_update(line):
	global model
	items = line.split("\t")
	features = items[:10]
	state = items[10].upper()
	model['states'][state]+=1.0
	for idx,chars in enumerate(features):
		table = model['obs'][state][idx]
		if not (chars in table):
			table[chars]=0.0
		table[chars]+=1.0
		model['obs']['sum_'+state][idx]+=1.0

def log_normalize():
	global model
	total = sum(model['states'].values())
	model['states'] = dict([(k,log(v/total)) for k,v in model['states'].iteritems()])
	for state in ('S','B','M','E'):
		for idx,table in enumerate(model['obs'][state]):
			ssum = model['obs']['sum_'+state][idx]
			model['obs'][state][idx] = dict([ (k,log(v/ssum)) for k,v in table.iteritems() ])

def dump_model(file_name):
	global model
	outf = open(file_name,"wb")
	with outf:
		marshal.dump(model,outf)

if __name__ == "__main__":

	for line in open("train_data.txt",'rb'):
		line = line.rstrip().decode('utf-8')
		line_update(line)

	print "loaded."
	log_normalize()
	print "normalized."
	dump_model("bayes_model.marshal")
	print "dumped"

