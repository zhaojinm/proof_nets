from nodes import *
primes = ['A','B','C','D','E','F','G']
cur_label = 0
def get_cur_lable():
	global cur_label
	ch = chr(ord('a')+cur_label)
	cur_label+=1
	return ch
def decrement_label():
	global cur_label
	cur_label-=1

POS="+"
NEG='-'
n2 = Node('A',POS,get_cur_lable())
n1 = Node('A',NEG,get_cur_lable())
n1.add_link(n2)
lc_root = LcNode(n2)
lc_leaf = LcNode(n1)
lc_root.add_child(lc_leaf)
unfolding = [n1,n2]
folding = [n1,n2]
polarities = [NEG,POS] 

all = set()

def get_link(folding):
	unf = []
	for n in folding:
		unf+=n.leaf()
	result = ""
	# print(folding,unf)
	for i,n in enumerate(unf):
		other = unf.index(n.link)
		if other>i:
			result=result+str(i+1)+str(unf.index(n.link)+1)+" "
	return result

def gen(l,folding,primes):
	# print(lc_root,folding,get_link(folding))
	if l==2:
		global all
		all.add(folding.__str__())
		print(lc_root,folding,get_link(folding))
		#valid lambda node in lcgraph
		possible_pairs = lc_root.get_possible_pairs()
		#check still plannar

		#add lambda node
		return
	#all none-lambda node
	for new_prime in [primes[l+1]]:#:
		new_folding = []
		for i,p in enumerate(folding):
			if p.pol==NEG:
				
				#add to left
				new_folding = folding[:i]
				new_n1 = Node(new_prime,POS,get_cur_lable())
				new_n2 = Node(new_prime,NEG,get_cur_lable())
				new_n1.add_link(new_n2)
				lcnode1 = LcNode(new_n1)
				lcnode2 = LcNode(new_n2)
				lcnode1.add_child(lcnode2)
				# print(lc_root)
				# print(p)
				p.lcnode.parent[0].add_child(lcnode1)
				new_folding_n = Node(pol=NEG,label=p.label,op='\\',left=new_n1,right=p)
				new_folding_n.lcnode=p.lcnode
				ori,des = p.label,p.label+new_n1.label
				new_folding_n.updatechild_label(ori,des)
				new_folding+=[new_n2,new_folding_n]
				new_folding+=folding[i+1:]
				gen(l+1,new_folding,primes)
				#backtrack
				decrement_label()
				decrement_label()
				p.lcnode.parent[0].del_child(lcnode1)
				new_folding_n.updatechild_label(des,ori)
				p.parent=None
				#add to right
				new_folding = folding[:i]
				new_n1 = Node(new_prime,POS,get_cur_lable())
				new_n2 = Node(new_prime,NEG,get_cur_lable())
				new_n1.add_link(new_n2)
				lcnode1 = LcNode(new_n1)
				lcnode2 = LcNode(new_n2)
				lcnode1.add_child(lcnode2)
				p.lcnode.parent[0].add_child(lcnode1)
				new_folding_n = Node(pol=NEG,label=p.label,op='/',left=p,right=new_n1)
				new_folding_n.lcnode=p.lcnode
				ori,des = p.label,p.label+new_n1.label
				new_folding_n.updatechild_label(ori,des)
				new_folding+=[new_folding_n,new_n2]
				new_folding+=folding[i+1:]
				gen(l+1,new_folding,primes)
				#backtrack
				decrement_label()
				decrement_label()
				p.lcnode.parent[0].del_child(lcnode1)
				new_folding_n.updatechild_label(des,ori)
				p.parent=None


gen(0,folding,primes)
print(len(all))


