import marshal
import traceback
from math import log,exp
import sys

feature_count = 11

model={
	'obs':
	{
		'S':[{} for x in range(feature_count)],
		'B':[{} for x in range(feature_count)],
		'M':[{} for x in range(feature_count)],
		'E':[{} for x in range(feature_count)],
	},
	'total':{
		'S':[0.0]*feature_count,
		'B':[0.0]*feature_count,
		'M':[0.0]*feature_count,
		'E':[0.0]*feature_count,
	}
}

def line_update(line):
	global model
	try:
		items = line.split("\t")
		features = items[:feature_count]
		state = items[feature_count].upper()
		for idx,chars in enumerate(features):
			if chars.strip()=="":
				continue
			table = model['obs'][state][idx]
			if not (chars in table):
				table[chars]=0.0
			table[chars]+=1.0
	except:
		try:
			print line
			print traceback.format_exc()
		except:
			pass

def log_normalize():
	global model
	for state in ('S','B','M','E'):
		for idx,table in enumerate(model['obs'][state]):
			ssum = sum([v for v in table.itervalues() if v>1])
			model['total'][state][idx] = ssum
			model['obs'][state][idx] = dict([ (k,log(v/ssum)) for k,v in table.iteritems() if v>1])

def dump_model(file_name):
	global model
	outf = open(file_name,"wb")
	with outf:
		marshal.dump(model,outf)

def load_old_model(file_name):
	global model
	inf = open(file_name,"rb")
	with inf:
		model = marshal.load(inf)
	for state in ('S','B','M','E'):
		for idx,table in enumerate(model['obs'][state]):
			ssum = model['total'][state][idx]
			model['obs'][state][idx] = dict([ (k,exp(p)*ssum) for k,p in table.iteritems()])

if __name__ == "__main__":
	if len(sys.argv)<3:
		print "usage: python train_incremental.py [model file name] [feature file name]"
		sys.exit(0)

	old_model_file_name = sys.argv[1]
	feature_file_name = sys.argv[2]
	load_old_model(old_model_file_name)
	print "old model loaded."
	ct = 0 
	for line in open("feature.txt",'rb'):
		line = line.rstrip().decode('utf-8')
		line_update(line)
		ct+=1
		if ct%10000==0:
			print "line ", ct, "completed."
	
	log_normalize()
	print "normalized."
	new_model_name = old_model_file_name+".new"
	dump_model(new_model_name)
	print new_model_name,"dumped"


