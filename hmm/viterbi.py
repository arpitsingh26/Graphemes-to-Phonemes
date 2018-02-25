import sys
_totseq=0

_totalphoneme=0
_totalgrapheme=26

_symbolmap=dict()
_phonememap=[]

_graphemestates=[]
_phonemestates=[]

possiblepath=[]

class _node:
	def __init__(self):
		self._start=0
		self._end=0
		self._totaloccurrence=0
		self._transition=[]
		self._emission=[]

def _init(lstate,nums,nume):
	for i in range(0,nums):
		node=_node()
		node._emission=[0 for j in range(0,nume)]
		node._transition=[0 for j in range(0,nums)]
		lstate.append(node)
	return
	
_gtopFile=open("training.txt",'r')
_sFile=open("symbol.txt",'r')

for line in _sFile:
	l=line.split()
	_symbolmap[l[0]]=_totalphoneme
	_phonememap.append(l[0])
	_totalphoneme=_totalphoneme+1

_init(_graphemestates,_totalgrapheme,_totalphoneme)

_init(_phonemestates,_totalphoneme,_totalgrapheme)

def _transitiongrapheme(seqstr):
	k=len(seqstr)
	a=ord(seqstr[0])-65
	
	_graphemestates[a]._start=_graphemestates[a]._start+1
	_graphemestates[a]._totaloccurrence=_graphemestates[a]._totaloccurrence+1

	for i in range(1,k):
		a=ord(seqstr[i-1])-65
		b=ord(seqstr[i])-65
		_graphemestates[a]._transition[b]=_graphemestates[a]._transition[b]+1
		_graphemestates[b]._totaloccurrence=_graphemestates[b]._totaloccurrence+1

	a=ord(seqstr[k-1])-65
	_graphemestates[a]._end=_graphemestates[a]._end+1	
	return
	
def _transitionphoneme(seqstr):
	k=len(seqstr)
	a=_symbolmap[seqstr[0]]

	_phonemestates[a]._start=_phonemestates[a]._start+1
	_phonemestates[a]._totaloccurrence=_phonemestates[a]._totaloccurrence+1

	for i in range(1,k):
		a=_symbolmap[seqstr[i-1]]
		b=_symbolmap[seqstr[i]]
		_phonemestates[a]._transition[b]=_phonemestates[a]._transition[b]+1
		_phonemestates[b]._totaloccurrence=_phonemestates[b]._totaloccurrence+1

	a=_symbolmap[seqstr[k-1]]	
	_phonemestates[a]._end=_phonemestates[a]._end+1		
	return
	
def _emissiongp(gpseq):
	k=len(gpseq[0])
	for i in range(0,k):
		a=ord(gpseq[0][i])-65
		b=_symbolmap[gpseq[1+i]]
		_graphemestates[a]._emission[b]=_graphemestates[a]._emission[b]+1
		_phonemestates[b]._emission[a]=_phonemestates[b]._emission[a]+1
	return
	
for line in _gtopFile:
	lstr=line.split()
	_totseq=_totseq+1
	_transitiongrapheme(lstr[0])
	
	rstr=[]
	k=len(lstr)
	for i in range(1,k):
		rstr.append(lstr[i])
	_transitionphoneme(rstr)
	_emissiongp(lstr)

def viterbigp(pstates,gseq):
	tpState=[]
	no_obs=len(gseq)-1
	
	global possiblepath
	possiblepath=[[[] for j in range(0,_totalphoneme)] for i in range(0,no_obs+1)]

	for i in range(0,_totalphoneme):
		possiblepath[0][i].append(-1)
		tpState.append(pstates[i]._start*1.0/_totseq)

	for i in range(0,no_obs):		
		a=ord(gseq[i])-65
		levelMax=[]						
		for j in range(0,_totalphoneme):
			tpmax=[]					    
			probmax=-1			
			for k in range(0,_totalphoneme):			
				if pstates[k]._totaloccurrence:			
					tprob=1.0*pstates[k]._transition[j]*pstates[k]._emission[a]/(pow(pstates[k]._totaloccurrence,2))
					tprob=tpState[k]*tprob
					if tprob==probmax:				
						tpmax.append(k)
					elif tprob>probmax:
						probmax=tprob
						tpmax[:]=[]
						tpmax.append(k)
			levelMax.append(probmax)
			possiblepath[i+1][j]=tpmax
		for j in range(0,_totalphoneme):
			tpState[j]=levelMax[j]
	
	a=ord(gseq[no_obs])-65
	tpmax=[]
	probmax=-1
	levelMax=[]
	for k in range(0,_totalphoneme):
		if pstates[k]._totaloccurrence:		
			tprob=1.0*pstates[k]._end*pstates[k]._emission[a]/(pstates[k]._totaloccurrence*_totseq)
			tprob=tpState[k]*tprob
			if probmax==tprob:
				tpmax.append(k)
			elif probmax<tprob:
				tpmax[:]=[]
				tpmax.append(k)
				probmax=tprob
		levelMax.append(probmax)
	return tpmax

def viterbiPG(gstates,pseq):
	tpState=[]
	no_obs=len(pseq)-1
	
	global possiblepath
	possiblepath=[[[] for j in range(0,_totalgrapheme)] for i in range(0,no_obs+1)]

	for i in range(0,_totalgrapheme):
		possiblepath[0][i].append(-1)
		tpState.append(gstates[i]._start*1.0/_totseq)
	
	for i in range(0,no_obs):
		a=_symbolmap[pseq[i]]
		levelMax=[]						
		for j in range(0,_totalgrapheme):
			tpmax=[]					
			probmax=-1
			for k in range(0,_totalgrapheme):			
				if gstates[k]._totaloccurrence:				
					tprob=1.0*gstates[k]._transition[j]*gstates[k]._emission[a]/(pow(gstates[k]._totaloccurrence,2))
					tprob=tpState[k]*tprob
					if tprob==probmax:		
						tpmax.append(k)
					elif tprob>probmax:
						probmax=tprob
						tpmax[:]=[]
						tpmax.append(k)
			levelMax.append(probmax)
			possiblepath[i+1][j]=tpmax
		for j in range(0,_totalgrapheme):
			tpState[j]=levelMax[j]
	
	a=_symbolmap[pseq[no_obs]]	
	tpmax=[]
	probmax=-1
	levelMax=[]	
	for k in range(0,_totalgrapheme):
		if gstates[k]._totaloccurrence:			
			tprob=1.0*gstates[k]._end*gstates[k]._emission[a]/(gstates[k]._totaloccurrence*_totseq)
			tprob=tpState[k]*tprob
			if probmax==tprob:
				tpmax.append(k)
			elif probmax<tprob:
				tpmax[:]=[]
				tpmax.append(k)
				probmax=tprob
		levelMax.append(probmax)
	return tpmax

def printdebug(obs,sta):
	for i in range(0,sta):
		sys.stdout.write("%d >> "%i)
		for j in range(0,obs):
			k=len(possiblepath[j][i])
			for l in range(0,k):
				sys.stdout.write("%d "%possiblepath[j][i][l])
			sys.stdout.write(" | ")
		print
			
def printGP(lmax,obs,sta,tphoneme):
	if obs<0:
		k=len(tphoneme)-1
		while k>-1:
			sys.stdout.write("%s "%tphoneme[k])
			k=k-1
		print	
		return 
	k=len(lmax)
	for i in range(0,k):
		tphoneme.append(_phonememap[lmax[i]])
		printGP(possiblepath[obs][lmax[i]],obs-1,sta,tphoneme)
	return 
				
def printPG(lmax,obs,sta,tgrapheme):
	if obs<0:
		k=len(tgrapheme)-1
		while k>-1:
			sys.stdout.write("%c"%tgrapheme[k])
			k=k-1
		print
		return 
	k=len(lmax)
	for i in range(0,k):
		tgrapheme.append(chr(lmax[i]+65))
		printPG(possiblepath[obs][lmax[i]],obs-1,sta,tgrapheme)
	return
			
gp=input()
if gp:
	tcase=input()
	while tcase>0 :
		gseq=raw_input()
		seqs=viterbigp(_phonemestates,gseq)
		tphoneme=[]
		printGP(seqs,len(gseq)-1,_totalgrapheme,tphoneme)
		possiblepath[:]=[]
		tcase=tcase-1	
else:
	tcase=input()
	while tcase :
		pseq=raw_input().split()
		seqs=viterbiPG(_graphemestates,pseq)
		tgrapheme=[]
		printPG(seqs,len(pseq)-1,_totalphoneme,tgrapheme)
		possiblepath[:]=[]
		tcase=tcase-1
