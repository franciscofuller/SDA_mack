
#======================================================================================
# SCIENTIFIC DATA ANALYSIS
#
# FRANCISCO A G FULLER
# 722.5599-4

# ASSIGNMENT 2
# 
# Complete de analysis of the movement of the elevator we have started in class, 
# during Session 04.

# Obtain: 

# 1. the speed of the elevador during its motion with acceleration;

# 2. the distance travelled by the elevator;

# 3. a figure with 3 panels (1 column, 3 rows) showing the acceleration, speed and 
#    position vs. time. Try to put your own style in the plot! Make it look nice!

# For 1 and 2, find the values from the data and not from reading the value from a plot!
#
#======================================================================================

# THE CODE:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


url = 'https://raw.githubusercontent.com/pjasimoes/PIPythonData/main/Elevador_predio45_PS.csv'

data_file = pd.read_csv(url)

print("")
print("HEADERS:")
print("----------------------------------")

k = data_file.keys()

for i in k:
  print(i)
print("")
print("")

print("X-axis  mean: "+np.array2string(data_file[k[1]].mean()))
print("Y-axis  mean: "+np.array2string(data_file[k[2]].mean()))
print("Z-axis  mean: "+np.array2string(data_file[k[3]].mean()))
print("a-value mean: "+np.array2string(data_file[k[4]].mean()))
print("")
print("")

g=9.81

SZ=data_file[k[3]].std()

len(data_file[k[3]])

#fig= plt.figure()

#plt.grid()

#plt.plot(data_file[k[0]],data_file[k[3]] - np.median(data_file[k[3]]))

#plt.axhline(y)
#plt.axvline(x)

from scipy.integrate import trapezoid
v = trapezoid(data_file[k[3]],data_file[k[0]])
v_med = trapezoid(data_file[k[3]]- np.median(data_file[k[3]]), data_file[k[0]])


print("v-value w/o the median: "+np.array2string(v))
print("v-value w/  the median: "+np.array2string(v_med))

from scipy.integrate import cumulative_trapezoid as ctrap

v_values = ctrap(data_file[k[3]]- np.median(data_file[k[3]]),data_file[k[0]])
v_values = np.insert(v_values,0,0)

print("")
print(f"There are {len(data_file[k[0]])} values in the data file and {len(v_values)} in v.")
print("")

plt.plot(data_file[k[0]],v_values)
plt.grid()

#aceleração, velocidade,  posição (valores e plots)

pos = np.arange(6)
t = np.arange(6.00)
t[0]=0
pos[0] = 0

i=1
while v_values[i]!=max(v_values):
    i=i+1
t[2] = data_file.get(k[0])[i]
pos[2] = i

while v_values[i]>0:
    i=i-1
t[1] = data_file.get(k[0])[i]
pos[1] = i


i=len(v_values)-1
pos[5] = i
t[5] = max(data_file.get(k[0]))

while v_values[i]<=1.74:
    i=i-1
    if i==0:
        break
pos[3] = i
t[3] = data_file.get(k[0])[i]

while v_values[i]>=0:
    i=i+1
    if i==0:
        break
pos[4] = i 
t[4] = data_file.get(k[0])[i]

print("TRANSITION POINTS:")
print("----------------------------------")

for i in range(6):
    print(f"pos{i+1} = {t[i]}  s")
print("")
print("")


print("ACCELERATION VAUES:")
print("----------------------------------")

ac = np.arange(6.00)
acc = np.arange(5.00)

for i in range(6):
    ac[i] = v_values[pos[i]]

for i in range(5):
    acc[i] = (ac[i]+ac[i+1])/2
    print(f"acc{i} = {acc[i]}  m/s²")
print("")
print("")


print("SPEED VALUES:")
print("----------------------------------")

V = np.arange(6.00)

for i in range(1,6):
    V[i] = ac[i]*(t[i]-t[i-1])
    print(f"V{i} = {V[i]}  m/s")
print("")
print("")


print("INSTRUMENT POSITION:")
print("----------------------------------")

S = np.arange(6.00)

print(f"S{0} = {S[0]} m")
for i in range(1,6):
    if (i>=2 and i<=3):
        S[i]= S[i-1] + v_values[pos[i-1]]*(t[i]-t[i-1])
    if (i<=1 or i>=4):
        S[i]= S[i-1] + v_values[pos[i-1]]*(t[i]-t[i-1])+ac[i]*(t[i]-t[i-1])/2
    print(f"S{i} = {S[i]} m")



fig,Az  = plt.subplots(3,1)

i=0
Az[i].plot(data_file[k[0]],data_file[k[3]] - np.median(data_file[k[3]]), label ='Raw')
Az[i].plot(t,ac, label ='Processed')
Az[i].set_ylabel('Accel. (m/s²)')
Az[i].set_title(' Accelleration')
    
i=1
Az[i].plot(t,V)
Az[i].set_ylabel('Speed (m/s)')
Az[i].set_title('Speed')

i=2
Az[i].plot(t,S)
Az[i].set_ylabel('Position (m)')
Az[i].set_title('Position')


for  i in Az:
  i.set_xlim(t[0]-0.1,max(t)+0.1)
  i.set_xlabel('Time (s)')
  if i==Az[0]:
      i.axvline(x=t[2], color='r', linestyle = 'dotted' )
      i.axvline(x=t[5], color='k', linestyle = 'dotted' )
  else:
      i.axvline(x=t[2], color='r', linestyle = 'dotted' , label ='Variable acceleration')
      i.axvline(x=t[5], color='k', linestyle = 'dotted' , label ='Constant or no acceleration')

  for j in range(6):
      if j==4:
          i.axvline(x=t[j], color='r', linestyle = 'dotted' )
      if j<=1 or j==3:
          i.axvline(x=t[j], color='k', linestyle = 'dotted' )
  i.legend()
  i.grid()

plt.tight_layout()



