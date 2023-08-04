from func_timeout import func_set_timeout
import torch
from torch.nn import init
import torch.nn as nn
from copy import deepcopy
import math

model_num=181

@func_set_timeout(60)
def getinput60():
    tmps=input()
    return tmps

def Net2Init(tmpnet):
    for key in tmpnet.state_dict():
        if('weight' in key):
            init.zeros_(tmpnet.state_dict()[key])
        else:
            tmpnet.state_dict()[key][...] = 0
    return tmpnet

def max_label(t):
    labellist = t.tolist()[0]
    maxnum = -10000
    loc = 0
    for j in range(len(labellist)):
        if (maxnum < labellist[j]):
            loc = j
            maxnum = labellist[j]
    return loc

class EasyNet(nn.Module):
    def __init__(self):
        super(EasyNet, self).__init__()
        self.norm=nn.Softmax()
        self.filter=nn.Linear(1,2)
        self.bypass = nn.Linear(2,model_num,bias=False)

    def forward(self, x):
        x=self.filter(x)
        x=self.bypass(x)
        x=self.norm(x)
        return x

namelist=['filter.weight', 'filter.bias', 'bypass.weight']
weightlist=[]
net=EasyNet()
mydict=net.state_dict()
net=Net2Init(net)
for i in range(len(namelist)):
    weightlist.append(mydict[namelist[i]].tolist())

def Increazing_check(tmpnet,changelist):
    for i in range(0,model_num-1):
        tmpinput = torch.tensor([i * 1.0]).reshape([1, 1])
        tmpwl = deepcopy(weightlist)
        tmpdict = deepcopy(mydict)
        tmpcl=changelist[i]
        for j in range(len(tmpcl)):
            if(len(tmpcl[j])==3):
                a,b,c=tmpcl[j]
                tmpwl[a][b]=c
            if(len(tmpcl[j])==4):
                a,b,c,d=tmpcl[j]
                tmpwl[a][b][c]=d
        for j in range(len(namelist)):
            tmpdict[namelist[j]] = torch.tensor(tmpwl[j])
        tmpnet.load_state_dict(tmpdict)
        if(max_label(tmpnet(tmpinput))!=i+1):
            return False
    return True

def Main():
    print('Please give me the weights!')
    imgstr=getinput60()
    weightstr=imgstr.split('|')
    if(len(weightstr)!=model_num-1):
        print('Wrong model number!')
    else:
        format_ok=True
        changelist=[]
        for i in range(len(weightstr)):
            tmpstr=weightstr[i]
            tmplist=[]
            tmpchange=tmpstr.split('#')
            for j in range(len(tmpchange)):
                tmpweight=tmpchange[j]
                tmpnum=tmpweight.split(',')
                if(len(tmpnum)==4):
                    a,b,c,d=int(tmpnum[0]),int(tmpnum[1]),int(tmpnum[2]),float(tmpnum[3])
                    if(a<0 or a>2 or b<0 or b>model_num or c<0 or c>2 or math.isnan(d)):
                        format_ok=False
                        break
                    tmplist.append((a,b,c,d))
                elif(len(tmpnum)==3):
                    a,b,c=int(tmpnum[0]),int(tmpnum[1]),float(tmpnum[2])
                    if (a < 0 or a > 2 or b<0 or b>2 or math.isnan(c)):
                        format_ok = False
                        break
                    tmplist.append((a,b,c))
                else:
                    format_ok=False
                    break
            changelist.append(tmplist)
        if(format_ok):
            if(Increazing_check(net,changelist)):
                print('flag{test}')
            else:
                print('Increazing failure!')
        else:
            print('Format error!')

if __name__ == '__main__':
    Main()
