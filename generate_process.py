from nodes import *
primes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
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
	result = []
	# print(folding,unf)
	# print("leaf",unf)
	for i,n in enumerate(unf):
		other = unf.index(n.link)
		if other>i:
			result.append((i+1,other+1))
	return result
def check_planar(folding):
	# print(folding,lc_root)
	links = get_link(folding)
	# print(links)
	for l in links[:-1]:
		for ll in links[1:]:
			if ll[0]<l[1] and ll[1]>l[1]:
				return False
	return True


def gen(l,folding,primes):
	# print(lc_root,folding,get_link(folding))
	global lc_root
	if l==6:
		global all
		if check_planar(folding):
			print(folding,lc_root)
			# print(lc_root,folding,get_link(folding))
			all.add(folding.__str__())
		else:
			return
		#valid lambda node in lcgraph
		possible_pairs = lc_root.get_possible_pairs()

		# for p in possible_pairs:
		# 	print(p[0].label,p[1].label)
		#check still plannar
		for (plus_d,minus_d) in possible_pairs:
			
			plus_dau,minus_dau = plus_d.node,minus_d.node
			# print()
			# print("pick:",plus_d.label,minus_d.label)
			#plus,minus
			back_folding = folding[:]
			back_lc_root = lc_root
			folding.remove(minus_dau)
			prev_parent = plus_dau.parent
			# print(folding,plus_dau,minus_dau,prev_parent)
			new_node = Node(pol=POS,label=get_cur_lable(),left=plus_dau,right=minus_dau,op='\\')
			new_lcnode=LcNode(new_node,islambda=True)
			new_lcnode.add_child(plus_d)
			new_lcnode.add_child(minus_d)
			plus_d.islambdaplus=True

			if plus_d==lc_root:
				lc_root=new_lcnode
				folding.pop(-1)
				folding.append(new_node)
			else:
				plus_d.parent[0].add_child(new_lcnode)
				plus_d.parent[0].del_child(plus_d)
				# print("add to",prev_parent)
				if prev_parent.left==plus_dau:
					prev_parent.left = new_node
				else:
					prev_parent.right = new_node
				prev_parent.child.remove(plus_dau)
				prev_parent.child.append(new_node)
				new_node.parent=prev_parent
				prev_parent.updatechild_label(plus_dau.label,new_node.label)

			gen(l,folding,primes)
			#backtrack
			decrement_label()
			folding=back_folding
			plus_d.islambdaplus = False
			plus_d.parent.remove(new_lcnode)
			minus_d.parent.remove(new_lcnode)
			if new_lcnode==lc_root:
				lc_root=back_lc_root
				plus_dau.parent=None
			else:
				new_lcnode.parent[0].add_child(plus_d)
				new_lcnode.parent[0].del_child(new_lcnode)
				if prev_parent.left==new_node:
					prev_parent.left=plus_dau
				else:
					prev_parent.right=plus_dau
				plus_dau.parent=prev_parent
				minus_dau.parent=None
				prev_parent.child.remove(new_node)
				prev_parent.child.append(plus_dau)
				new_node.parent=None
				prev_parent.updatechild_label(new_node.label,plus_dau.label)

			#m+p
			back_folding = folding[:]
			back_lc_root = lc_root
			folding.remove(minus_dau)
			prev_parent = plus_dau.parent
			# print(folding,plus_dau,minus_dau,prev_parent)
			new_node = Node(pol=POS,label=get_cur_lable(),left=minus_dau,right=plus_dau,op='/')
			new_lcnode=LcNode(new_node,islambda=True)
			new_lcnode.add_child(plus_d)
			new_lcnode.add_child(minus_d)
			plus_d.islambdaplus=True

			if plus_d==lc_root:
				lc_root=new_lcnode
				folding.pop(-1)
				folding.append(new_node)
			else:
				plus_d.parent[0].add_child(new_lcnode)
				plus_d.parent[0].del_child(plus_d)
				# print("add to",prev_parent)
				if prev_parent.left==plus_dau:
					prev_parent.left = new_node
				else:
					prev_parent.right = new_node
				prev_parent.child.remove(plus_dau)
				prev_parent.child.append(new_node)
				new_node.parent=prev_parent
				prev_parent.updatechild_label(plus_dau.label,new_node.label)

			gen(l,folding,primes)
			#backtrack
			decrement_label()
			folding=back_folding
			plus_d.islambdaplus = False
			plus_d.parent.remove(new_lcnode)
			minus_d.parent.remove(new_lcnode)
			if new_lcnode==lc_root:
				lc_root=back_lc_root
				plus_dau.parent=None
			else:
				new_lcnode.parent[0].add_child(plus_d)
				new_lcnode.parent[0].del_child(new_lcnode)
				if prev_parent.left==new_node:
					prev_parent.left=plus_dau
				else:
					prev_parent.right=plus_dau
				plus_dau.parent=prev_parent
				minus_dau.parent=None
				prev_parent.child.remove(new_node)
				prev_parent.child.append(plus_dau)
				new_node.parent=None
				prev_parent.updatechild_label(new_node.label,plus_dau.label)

		
		return

	#all none-lambda node
	for new_prime in[primes[l+1]]:#:
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
				p.lcnode.node=new_folding_n
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
				p.lcnode.node=p


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
				p.lcnode.node=new_folding_n
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
				p.lcnode.node=p


gen(0,folding,primes)
print(len(all))


