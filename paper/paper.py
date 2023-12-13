# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:05:25 2023

@author: 1155992
"""

#pip install adi-reader

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import adi
from astropy.io import fits




fits_filename = 'D:/__TRABALHOS EM ANDAMENTO/__MACK/_DOUTORADO/Disciplinas/Scientific Data Analysis/Paper/ATI-20130817.fits'


hdu_list = fits.open(fits_filename)
hdu_header = hdu_list[0].header
temp=hdu_list[0].data
hdu_cols_names=[]

for i in range(len(hdu_header)):
    if i>7:
        hdu_cols_names.append(hdu_header[i])
hdu_cols_names.append('x1') 
hdu_cols_names.append('x2')

vlf_data=pd.DataFrame(temp, index=None, columns=hdu_cols_names)

hdu_cols_phase = ['Time-UT (s)','NAA Phase (deg.)','NAU Phase (deg.)','NAA-L1 Phase (deg.)','NPM-L2 Phase (deg.)']
hdu_cols_ampl = ['Time-UT (s)','NAA Amp (dB)','NAU Amp (dB)','NAA-L1 Amp (dB)','NPM-L2 Amp (dB)']

temp1=hdu_list[0].data
temp2=hdu_list[0].data

from datetime import datetime
 
timestamp_string = "2013-08-17"
format_string = "%Y-%m-%d"
datetime_object = datetime.strptime(timestamp_string, format_string)



temp1=np.delete(temp1,[ 1, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15],axis=1)
vlf_phase = pd.DataFrame(data=temp1, index=None, columns = hdu_cols_phase)

temp2=np.delete(temp2,[ 1, 2, 4, 6, 7, 8, 10, 11, 12, 14, 15], axis=1)
vlf_ampl = pd.DataFrame(data=temp2, index=None, columns = hdu_cols_ampl)


import matplotlib.colors as mplc

n_lines = 4
x = np.linspace(0.5, 23.99, 86400)
c = np.arange(1., n_lines + 1)

# cmap = plt.get_cmap("rainbow", len(c))
# norm = mplc.BoundaryNorm(np.arange(len(c)+1)+0.5,len(c))
# sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
# sm.set_array([])

colormap=['r','b','g','c']
station=['NAA','NAU','NAA-L1','NPM']
fig, (ax1, ax2) = plt.subplots(2, dpi=150, sharex=True, figsize=(10,6), layout='constrained')
for i in range(n_lines):
        ax1.plot(x, vlf_phase[hdu_cols_phase[i+1]], c=colormap[i], linewidth=0.5, label=station[i])
        ax2.plot(x, vlf_ampl[hdu_cols_ampl[i+1]], c=colormap[i], linewidth=0.1)
ax1.xaxis.grid(True)
ax1.set_ylabel('degrees')
ax1.set_title("VLF Phase",loc='left')
ax1.tick_params( labelsize='small')

ax2.tick_params(labelsize='medium', width=2)
ax2.set_xlabel('hour UTC')
ax2.set_ylabel('db')
ax2.set_title("VLF Amplitude", loc='left')
ax2.tick_params( labelsize='small')

legend = ax1.legend(loc='upper left', shadow=True, fontsize='small')

plt.grid()
plt.legend()
plt.show()

