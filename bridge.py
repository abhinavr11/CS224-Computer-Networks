class Bridge :
    def __init__(self, name , id_ , flag ):
        self.name = name
        self.id = id_
        
        self.connections = set()
        self.root = self
        self.dist = 0
        
        self.rp = None
        self.dp = set() 
        self.np = set()
        self.next = None
        
        self.change = False
        self.forward = False
        self.final_config = []
        
        self.flag = flag
        self.trace = []
        
        
    def send(self,t):
        if self.root is self or self.forward :
            if self.flag:
                self.trace.append(f'{t} s {self.name} ({self.root.name} {self.dist} {self.name})')
            
            for lan in self.connections:
                
                lan.forward((self.root,self.dist,self),t)
        
        self.change = False
        self.forward = False
    
    def connect(self,lan):
        self.connections.add(lan)
        self.dp.add(lan) 
    
    def receive(self,msg,lan,t):
        root,dist,bridge = msg
        
        if self.flag:
            self.trace.append(f'{t+1} r {self.name} ({root.name} {dist} {bridge.name})')
            
        if self.dist > dist or (self.dist == dist and self.id > bridge.id):
            if lan in self.dp:
                self.dp.remove(lan)
                self.change = True
        
        dist +=1
        
        if root.id > self.root.id or (root.id == self.root.id and dist > self.dist):
            return
        if self.next:
            if root.id == self.root.id and dist == self.dist and bridge.id > self.next.id:
                return
            
        self.change = True
        self.forward = True
        self.root = root
        self.dist = dist
        self.rp = lan
        #self.dp.remove(lan)
        self.next = bridge

    
    def finalize(self):
        config = []
        rp = 0
        dp = 0
        np = 0
        
        for con in self.connections:
                if con is self.rp:
                    rp +=1
            
                elif con in self.dp :
                    dp +=1
            
                else: 
                    np +=1

        if dp == 0 :
            #self.np.add(self.rp)
            #print(len(self.dp))
            self.rp = None
            for con in self.connections:
                self.np.add(con)
                config.append(f'{con.name}-NP')

        
        else :

            #print(len(self.dp))
            for con in self.connections:
                if con is self.rp:
                    config.append(f'{con.name}-RP')
            
                elif con in self.dp :
                    config.append(f'{con.name}-DP')
            
                else:
                    self.np.add(con)
                    config.append(f'{con.name}-NP')
                
        self.final_config = config
        return config
    
class LAN:
    
    def __init__(self,name):
        self.name = name
        self.connections = set()
        
    
    def connect(self,bridge):
        self.connections.add(bridge)
        
    def forward(self,message,t):
        sender = message[2]
        
        for bridge in self.connections:
            
            if bridge is not sender:
                bridge.receive(message,self,t)
           
    
        