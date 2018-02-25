import "vitarbi.py"

testcase=input()
while testcase :
	pseq=raw_input().split()
	seqs=viterbiPG(_Gstates,pseq)
	tgrapheme=[]
	printPG(seqs,len(pseq)-1,_totalP,tgrapheme)
	possible_path[:]=[]
	testcase=testcase-1