POS="+"
NEG='-'
cat = ["A/((B/C)\\(B/C))","A"]
pol = [NEG]*(len(cat)-1)+[POS]
labels = [chr(ord('a')+i) for i in range(len(cat)) ]
cur_label = labels[-1]

def expand(c,p,l):
	par=0
	for i in range(len(c)):
		ch = c[i]
		if (ch=='/' or ch=='\\') and par==0:
			break
		elif ch=='(':
			par+=1
		elif ch==')':
			par-=1
	sep = i
	if ch=='(':
		for i in range(len(c)-1,0,-1):
			ch = c[i]
			if ch=='/' or ch=='\\':
				sep=i
				break
	left = c[:sep] if c[0]!="(" else c[1:sep-1]
	right = c[sep+1:] if c[-1]!=")" else c[sep+2:-1]
	# print(c,left,right)
	global cur_label
	if ch=='\\' and p==POS:
		cur_label=chr(ord(cur_label) + 2) 
		print(l,"= lambda ",cur_label," ", chr(ord(cur_label) - 1) )
		return [right,left], [POS,NEG], [chr(ord(cur_label) - 1),cur_label]
	elif ch=='\\' and p == NEG:
		cur_label=chr(ord(cur_label) + 1) 
		return [left,right], [POS,NEG], [cur_label,l+cur_label]
	elif ch=='/' and p==POS:
		cur_label=chr(ord(cur_label) + 2) 
		print(l,"= lambda ",chr(ord(cur_label) - 1)," ", cur_label)
		return [right,left], [NEG,POS], [chr(ord(cur_label) - 1),cur_label]
	elif ch=='/' and p==NEG:
		cur_label=chr(ord(cur_label) + 1) 
		return [left,right], [NEG,POS], [l+cur_label,cur_label]

def step1_2(cat,pol,labels):
	print(cat[0])
	total_prime = sum([c.count("\\")+c.count("/")+1 for c in cat])
	while len(cat)!=total_prime:
		new_cat = []
		new_pol = []
		new_lables = []
		for c,p,l in zip(cat,pol,labels):
			if c.count("\\")+c.count("/")!=0:
				cc,pp,ll = expand(c,p,l)
				new_cat+=cc
				new_pol+=pp
				new_lables+=ll
			else:
				new_cat.append(c)
				new_pol.append(p)
				new_lables.append(l)
		cat = new_cat
		pol = new_pol
		labels = new_lables
		print(cat,pol,labels)
if __name__ == '__main__':
	step1_2(cat,pol,labels)
