#encoding=utf-8
import re
import os
import marshal
import logging
import sys

logger = logging.getLogger("miniseg")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

MIN_FLOAT=-35.0

MINUS_INF=float("-inf")

def load_model(f_name):
	_curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) )  )
	prob_p_path = os.path.join(_curpath,f_name)
	in_f = open(prob_p_path,'rb')
	with in_f:
		if f_name.endswith(".py"):
			return eval(in_f.read())
		elif f_name.endswith(".marshal"):
			result = marshal.load(in_f)
			return result

logger.info("start loading model...")
prob_start = load_model("prob_start.py")
prob_trans = load_model("prob_trans.py")
bayes_model = load_model("bayes_model.marshal")
logger.info("loaded.")

def get_emit_prob(obs,idx,state):
	global bayes_model
	feature = []					
	feature = [obs[j] if (j>=0 and j<len(obs)) else " " for j in xrange(idx-2,idx+3) ]

	feature.append(feature[0]+feature[1])
	feature.append(feature[1]+feature[2])
	feature.append(feature[2]+feature[3])
	feature.append(feature[3]+feature[4])
	feature.append(feature[1]+feature[3])
	feature.append(feature[0]+feature[2]+feature[4])

	
	factor = sum( [bayes_model['obs'][state][j].get(chars,MIN_FLOAT) for j,chars in enumerate(feature)])
	return factor

PREVE_STATES = {
	'B':('E','S'),
	'M':('M','B'),
	'S':('S','E'),
	'E':('B','M')
}

def viterbi(obs, states, start_p, trans_p):
	V = [{}] #tabular
	path = {}
	for y in states: #init
		V[0][y] = start_p.get(y,MINUS_INF) + get_emit_prob(obs,0,y)
		path[y] = [y]
	for t in range(1,len(obs)):
		V.append({})
		newpath = {}
		for y in states:
			emit_p = get_emit_prob(obs,t,y)
			(prob,state ) = max([(V[t-1][y0] + trans_p[y0].get(y,MINUS_INF) + emit_p ,y0) for y0 in PREVE_STATES[y]])
			V[t][y] =prob
			newpath[y] = path[state] + [y]
		path = newpath
	
	(prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
	
	return (prob, path[state])


def __cut(sentence):
	prob, pos_list =  viterbi(sentence,('B','M','E','S'), prob_start, prob_trans)
	#print prob, pos_list
	begin, next = 0,0
	for i,char in enumerate(sentence):
		pos = pos_list[i]
		if pos=='B':
			begin = i
		elif pos=='E':
			yield sentence[begin:i+1]
			next = i+1
		elif pos=='S':
			yield char
			next = i+1
	if next<len(sentence):
		yield sentence[next:]

def cut(sentence):
	if not ( type(sentence) is unicode):
		try:
			sentence = sentence.decode('utf-8')
		except:
			sentence = sentence.decode('gbk','ignore')
	re_han, re_skip = re.compile(ur"([\u4E00-\u9FA5，。【】？、：（）！·“”……《》]+)"), re.compile(ur"([a-zA-Z0-9+#]+)")
	re_not_han = re.compile(ur"([^\u4E00-\u9FA5，。【】？、：（）！·“”……《》]+)")
	blocks = re_not_han.split(sentence)

	for blk in blocks:
		#print blk
		if re_han.match(blk):
			for word in __cut(blk):
				yield word
		else:
			tmp = re_skip.split(blk)
			for x in tmp:
				if x!="":
					yield x