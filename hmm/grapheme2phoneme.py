import vitarbi

testcase=input()
print testcase
while testcase>0 :
	gseq=raw_input().split()
	seqs=viterbiGP(_Pstates,gseq)
	tphoneme=[]
	printGP(seqs,len(gseq)-1,_totalG,tphoneme)
	possible_path[:]=[]
	testcase=testcase-1	