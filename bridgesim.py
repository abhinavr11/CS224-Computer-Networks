from bridge import Bridge , LAN
def learn(bridges,lans,flag):
    cond = True
    t=1
    
    while cond:
        
        for i in bridges:
            bridges[i].send(t)
        t+=1
        cond=False
        
        for j in bridges:
            if bridges[j].change:
                cond = True
                break
    if flag:
        trace = []
        
        for k in bridges:
            trace.extend(bridges[k].trace)
            bridges[k].trace.clear()
        print('\n'.join(sorted(trace)))
        
    for l in range(len(bridges)):
        print(f'{bridges[l].name}: ' + ' '.join(sorted(bridges[l].finalize())))

bridges = {}
lans = {}   

f = int(input()) 
B = int(input())

    
for i in range(B):
    x = input()
    
    bridge = x.split()[0][:-1]
    ports =  x.split()[1:]
    
    bridges[i] = Bridge(bridge,i,f)
        
    for pt in ports :
        #print(p)
        if pt not in lans:
            lans[pt] = LAN(pt)
                
        bridges[i].connect(lans[pt])
        lans[pt].connect(bridges[i])
            
   
        
learn(bridges, lans , f)
 
            
            
            
            
            
            
            
            
            
            
        