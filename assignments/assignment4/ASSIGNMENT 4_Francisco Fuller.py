
#======================================================================================
# SCIENTIFIC DATA ANALYSIS

# FRANCISCO A G FULLER
# 722.5599-4

# ASSIGNMENT 4

# Using the SSN data (see Course Materials), create a figure showing all the 
# solar cycles superposed, as shown in 

# https://posgraduacao.mackenzie.br/mod/resource/view.php?id=113502

# Then, from the data*, find:

# 1) the cycle with the highest count of sunsposts

# 2) the cycle with the lowest count of sunsposts

# 3) the cycle with the shortest duration

# 4) the cycle with the longest duration

# * this information CAN be found in the solar cycle files (also available), 
#   you can use that information to check your results
#
#======================================================================================


#======================================================================================
# FROM CLASSROOM


## https://www.sidc.be/SILSO/Tabela_Auxiliar/
## 13-month smoothed monthly total sunspot number [1/1749 - now]
# - [1-4] Year
# - [6-7] Month
# - [9-16] Decimal date
# - [19-23] Smoothed total sunspot number (SSN)
# - [25-29] Standard deviation
# - [32-35] Number of observations (SDT)
# - [37] Definitive/provisional indicator

# example:
    
    
    
# colspecs = [(0,3),(5,6),(8,15),(18,22),(24,28),(31,34)]
# data = pd.read_fwf(url,colspecs=colspecs)
# data.columns = ["year", "month", "date", "SSN", "sdt", "no_obs"]

#======================================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def readData(url, colspecs, keys, header):
    
    # reads a table from a file or URL and returns a DataFrame object
    
    data = pd.read_fwf(url,colspecs=colspecs, header=header) # this file have no headers
    data=data.convert_dtypes(infer_objects=True) # converting string to number
    data.columns = keys
    return data

#======================================================================================
# DATA READING AND CONDITIONING
#======================================================================================


# the URL or filenames
url_set = 'https://www.sidc.be/SILSO/DATA/SN_ms_tot_V2.0.txt'
url_cycles =  'https://www.sidc.be/SILSO/DATA/Cycles/TableCyclesMiMa.txt'

# the headers and column widths according to the datasets specifications
colspecs_set = [(0,4),(5,7),(8,16),(18,23),(24,29),(31,35)]
colspecs_cycles = [(0,2),(6,11),(11,13),(16,20),(22,26),(27,29),(31,36),(39,41),(42,45)]
keys_set = ["year", "month", "date", "SSN", "sdt", "no_obs"] 
keys_cycles = ['Cycle Nb', 'Minimum Year', 'Minimum Month', 'Minimum SN','Maximum Year', 'Maximum Month', 'Maximum SN', 'Duration in Year','Duration in Month']
header_set = None
header_cycles = 1

data_set = readData(url_set, colspecs_set, keys_set, header_set)
data_set.insert(0,"cycle", 0) # insert a column to assign the solar cycle value

data_cycles = readData(url_cycles, colspecs_cycles, keys_cycles, header_cycles)



# create auxiliar table with solar cycles start and end in format yyyy.mm
ciclo_solar = pd.DataFrame(data=None, index=None, columns=['cycle','begin_ym','end_ym'])
    
for i in range(len(data_cycles)):
    cycle = data_cycles['Cycle Nb'][i]
    begin_ym = data_cycles['Minimum Year'][i]+(data_cycles['Minimum Month'][i]*0.01)
    end_ym =   begin_ym+data_cycles['Duration in Year'][i]+((data_cycles['Duration in Month'][i]-1)*0.01)
    ciclo_solar = ciclo_solar.append({'cycle':cycle,'begin_ym':begin_ym,'end_ym':end_ym},ignore_index=True)

# scan 

for i in range(len(data_set)):
    event_date = data_set['year'][i]+(data_set['month'][i]*0.01)
    for j in range(len(ciclo_solar)):
        if (event_date>=ciclo_solar['begin_ym'][j] and event_date<=ciclo_solar['end_ym'][j]) or (event_date>=ciclo_solar['begin_ym'][j] and j>23):
            data_set['cycle'][i]=ciclo_solar['cycle'][j]

data_set.sort_values(["cycle", "year", "month"], ascending=True)

# #DadosCiclo =   data_set["cycle"]
# #DadosY =   data_set["year"]
# #DadosM =   data_set["month"]
# #DadosDm =  data_set["date"]
# DadosSSN = data_set["SSN"]
# #DadosSDT = data_set["sdt"]
# #DadosNO =  data_set["no_obs"]

# Ciclo =    data_cycles['Cycle Nb']
# MinY =     data_cycles['Minimum Year']
# MinM =     data_cycles['Minimum Month']
# MinSN =    data_cycles['Minimum SN']
# MaxY =     data_cycles['Maximum Year']
# MaxM =     data_cycles['Maximum Month']
# MaxSN =    data_cycles['Maximum SN']
# DuraçãoY = data_cycles['Duration in Year']
# DuraçãoM = data_cycles['Duration in Month']
  
#======================================================================================
# DATA PROCESSING
#======================================================================================


nn = 160 # list size
cycle_plot=pd.DataFrame(0.0, columns=range(len(ciclo_solar)+1), index=np.arange(nn))

for i in range(len(ciclo_solar)):
    temp=data_set.loc[data_set['cycle']==i+1, ['SSN']].values.tolist()
    ds = list()
    for j in range(len(temp)):
        ds.append(temp[j][0])
    ds+=[0.0]*(nn-len(ds))
    cycle_plot[i+1]=ds
cycle_plot=cycle_plot.drop(columns=0)


#======================================================================================
# PLOT THE GRAPHICS
#======================================================================================


import matplotlib.colors

n_lines = len(ciclo_solar)
x = np.linspace(0, 14, nn)
c = np.arange(1., n_lines + 1)

cmap = plt.get_cmap("rainbow", len(c))
norm = matplotlib.colors.BoundaryNorm(np.arange(len(c)+1)+0.5,len(c))
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

fig, ax = plt.subplots(dpi=150)
for i in range(len(ciclo_solar)):
    ax.plot(x, cycle_plot[i+1], c=cmap(i+1), linewidth=1)
fig.colorbar(sm, ticks=c)

plt.grid()
plt.xlabel('Cycle Years')
plt.ylabel('SSN/Month')
ax.set_title("Sun Spots per Solar Cycle")
plt.legend()

#======================================================================================
# SOME STATISTICS 
#======================================================================================

print('___________________________________________________________')
spots = pd.Series(cycle_plot.max())
time = pd.Series(ciclo_solar['end_ym']-ciclo_solar['begin_ym'])

# 1) o ciclo com a maior contagem de mensagens solares
for i in range(len(ciclo_solar)):
    if spots[i+1] == max(cycle_plot.max()):
        print(f'Maior máxima no Ciclo {i+1} = {max(cycle_plot.max())} SSN')
        print("")
        break

# 2) o ciclo com a menor contagem de mensagens solares
for i in range(len(ciclo_solar)):
    if spots[i+1] == min(cycle_plot.max()):
        print(f'Menor máxima no Ciclo {i+1} = {min(cycle_plot.max())} SSN')
        print("")
        break

# 3) o ciclo com menor duração
for i in range(len(ciclo_solar)):
    if time[i+1] == time.min():
        print(f'Menor duração no Ciclo {i+1} = {int(round(time.min()))} anos')
        print("")
        break

# 4) o ciclo com maior duração
for i in range(len(ciclo_solar)):
    if time[i+1] == time.max():
        print(f'Maior duração no Ciclo {i+1} = {int(round(time.max()))} anos')
        print("")
        break
