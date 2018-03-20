GD= array([[1,0,1],[1,1,1]])
bi = array([0,1,0,1,0,1,1,1,0,1])
nm = len(GD[0])-1
x = repeat(arange(2**nm),2)
state =array([])
bit = 0
AM = array([])
for i in x:
    state = append(state,append([bit],array(list(bin(i)[2:].zfill(nm)),int)))
    bit = (bit+1)%2
    AM = append(AM, append(state[-nm:],state[-nm-1:-1]))
state = state.reshape(2**(nm+1),nm+1)
AM = AM.reshape(2**(nm+1),2*nm)
graph = dot(state,GD.T)%2
print(AM)
value = array(zeros(2**nm))
value[0]=1000
z = array([])
l=0
for j in bi.reshape(int(len(bi)/len(GD)),len(GD)):
    ixn = where(j==0)
    j[ixn]=-1
    ixn = where(AM==0)
    AM[ixn] = -1
    for k in arange(2**nm):
    #   value = append(value, value[k] + max(dot(j,AM[k][0:2]), dot(j,AM[k+2][0:2])))
        z= append(z,max(dot(j,AM[k][0:2]), dot(j,AM[k+2][0:2])))
        print(z)
    value = append(value, value[0:2**nm] + z)
    z = array([])
    print(value)
value.reshape(2**nm,int(len(bi)/len(GD))+1)