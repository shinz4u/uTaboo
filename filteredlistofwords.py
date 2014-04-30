import operator
def getRankedList(filteredListofWords):
        rank={}
        for i in filteredListofWords:
            rank[i]=0
        for i in filteredListofWords:
            rank[i]=rank[i]+1
        
        ranked = sorted(rank.iteritems(), key=operator.itemgetter(1),reverse=True)
        keys=[x for (x,y) in ranked]
        print keys[0:3]

        #blah=[]
        #for x in keys:
        #	blah=x[0]
        #print blah

        
                
                
filteredListofWords=['hello','shinoy','smrithi','smrithi','vishnu' , 'shinoy','radhika', 'shinoy','vishnu','vishnu']   
getRankedList(filteredListofWords)
