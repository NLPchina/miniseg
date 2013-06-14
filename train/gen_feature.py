import glob

def line2items(line):
	items =[x.split('/') for x in  line.split("  ") if x!=""]
	return items

def item2feature(items,idx):
	feature = []
	for j in xrange(idx-2,idx+3):
		if j<0 or j>=len(items):
			feature.append(" ")
		else:
			feature.append(items[j][0])
	feature.append(feature[0]+feature[1])
	feature.append(feature[1]+feature[2])
	feature.append(feature[2]+feature[3])
	feature.append(feature[3]+feature[4])
	feature.append(feature[1]+feature[3])

	tag = items[idx][1]

	return feature,tag

if __name__ == "__main__":
	out_f = open("feature.txt","wb")

	for fname in glob.glob("train_txt/*.txt"):
		print "reading ", fname
		for line in open(fname,'rb'):
			line = line.rstrip()
			items = line2items(line)
			for idx in range(len(items)):
				feature, tag = item2feature(items,idx)
				#print feature
				out_f.write("\t".join(feature)+"\t"+tag+"\n")

	out_f.close()









