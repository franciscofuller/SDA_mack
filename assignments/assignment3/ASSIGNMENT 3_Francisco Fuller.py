
#======================================================================================
# SCIENTIFIC DATA ANALYSIS

# FRANCISCO A G FULLER
# 722.5599-4

# ASSIGNMENT 3

# Obtain the Doppler velocity of the plasma in a solar flare using EVE data. 

# Step by step:

# 1. determinte the time interval for a quiet period (not flaring) in the time 
#    series of the CIII line irradiance

# 2. obtain the wavelength interval for the CIII line. Tip: use 97.7-0.2 
#    and 97.7+0.2

# 3. determine the average spectrum of the C III 97.7nm line for the quiet Sun 
#    (the interval you found above) Tip: use .mean() and .std() in irr

# 4. Fit a Gaussian function to the CIII line to get the amplitude, center 
#    and width of the line. Tip: use a "Gaussian plus a constant" function

# 5. Repeat, but now for the time interval for the flare

# 6. Compare the line center obtained for the quiet Sun and flare (delta lambda)

# 7. Find the Doppler expression for light, that relates the wavelength shoft 
#    into velocity

# 8. Document your work with figures and text to explain your process
#
#======================================================================================


#======================================================================================
# FROM CLASSROOM

## some solar data now!

## file format: FITS 'Flexible Image Transport System'
## https://fits.gsfc.nasa.gov/

## url for data file

url = 'https://lasp.colorado.edu/eve/data_access/eve_data/products/level2'

year = '2011'
doy = '046'
FITSfile = 'EVS_L2_2011046_00_007_02.fit.gz'
sep = '/'

url_file = sep.join((url,year,doy,FITSfile))

print("Source File: " + url_file)
print("")

## read EVE spectra

def read_eve(FITSfile):
  from astropy.io import fits
  ## open FITS file
  hdu = fits.open(FITSfile)
  
  ## date
  dat = hdu[3].data['YYYYDOY']
  
  ## SOD = seconds of day (tempo)
  sod = hdu[3].data['SOD']
  
  ## array wavelength (comprimento de onda)
  wav = hdu[1].data['WAVELENGTH']
  
  ## array spectra (irradiance W/m2/nm)
  irr = hdu[3].data['IRRADIANCE'] # time,irr (360,5200)
  
  hdu.close()
  return wav,sod,irr

import numpy as np
import matplotlib.pyplot as plt

wav,sod,irr = read_eve(url_file)


# plt.title("FULL SPECTRUM ")
# plt.semilogy(wav,irr[0,:])
# plt.figure()


# plt.title("SPECTRUM 97.7+-0.5 nm")
# plt.semilogy(wav,irr[0,:],marker='o')
# plt.xlim(97.7-0.5,97.7+0.5)
# plt.figure()

# a = np.array([10.1,20.3,50.3,80.1,90,100.,203])
# value = 50
# b = np.abs(a - value)
# print(b)
# print(b.argmin())

def find_nearest(array,value):
  return np.abs(array-value).argmin()

# w = 97.7
# index = find_nearest(wav,w)
# print(index,wav[index])

# print(find_nearest(a,value))


# plt.title("IRRADIATION x TIME (s)")
# plt.plot(sod,irr[:,index])
# plt.figure()


# indmax = irr[:,index].argmax()


# w1 = 2*np.pi
# print(w1)
# index = find_nearest(wav,w1)
# print(index,wav[index])
# plt.plot(sod,irr[:,index])
# plt.figure()


# plt.semilogy(wav,irr[0,:])
# plt.semilogy(wav,irr[indmax,:])
# plt.xlim(5.7,7)
# plt.axvline(w1,linestyle='dashed')
# plt.ylim(1e-5,5e-4)
# for i in range(0,len(sod),10):
#   plt.semilogy(wav,irr[i,:])
# plt.figure()


# plt.semilogy(wav,irr[0,:])
# plt.semilogy(wav,irr[indmax,:])
# plt.xlim(97.5,98)
# plt.axvline(w1,linestyle='dashed')
# plt.ylim(1e-6,5e-3)
# for i in range(0,len(sod),10):
#   plt.semilogy(wav,irr[i,:])
# plt.figure()


# plt.semilogy(wav,irr[0,:])
# plt.semilogy(wav,irr[indmax,:])
# plt.xlim(97.5,98)
# plt.axvline(w1,linestyle='dashed')
# plt.ylim(1e-6,5e-3)
# for i in range(0,len(sod),10):
#   plt.semilogy(wav,irr[i,:] - irr[0,:])
# plt.figure()


# plt.plot(wav,irr[indmax,:],color='k',linewidth=3)
# plt.xlim(97.5,98)
# plt.axvline(w1,linestyle='dashed')
# plt.ylim(1e-6,5e-3)
# for i in range(0,len(sod),10):
#   plt.plot(wav,irr[i,:] - irr[0,:])
# plt.figure()

# print("------------------------------")
# print("")
# print("")
# print("")

#======================================================================================

# THE CODE:

#------------------------------------------------------------------------------
# 1. determinte the time interval for a quiet period (not flaring) in the time 
#    series of the C-III line irradiance

t0 =find_nearest(sod,500)
t1 =find_nearest(sod,1500)


#------------------------------------------------------------------------------
# 2. obtain the wavelength interval for the C-III line. Tip: use 97.7-0.2 
#    and 97.7+0.2

wav0= find_nearest( wav, 97.7-0.2)
wav1= find_nearest( wav, 97.7+0.2)


#------------------------------------------------------------------------------
# 3. determine the average spectrum of the C-III 97.7nm line for the quiet Sun 
#    (the interval you found above) Tip: use .mean() and .std() in irr

AveSpectrum = irr[t0:t1, wav0:wav1].std()

print(f'Quiet SUN average spectrum of the C-III (97,7nm) line = {AveSpectrum}')
print("")


# 3 graphs in a single page

fig,graph  = plt.subplots(3,1)


#------------------------------------------------------------------------------
# 4. Fit a Gaussian function to the C-III line to get the amplitude, center 
#    and width of the line. Tip: use a "Gaussian plus a constant" function

WC3= wav[wav0:wav1]
Qs =irr[t0:t1, wav0:wav1].mean(axis=0)

i=0

graph[i].set_title("QUIET SUN")
graph[i].axhline(y=Qs.mean(), color="b", linestyle="dotted", label=" ")
graph[i].axvline(x=WC3[find_nearest(Qs,Qs.mean())], color="b", linestyle="dotted", label="wavelength (nm)")
graph[i].plot(WC3,Qs,marker='o', color="b")
#plt.figure()


#------------------------------------------------------------------------------
# 5. Repeat, but now for the time interval for the flare

t2 =find_nearest(sod,2076)
t3 =find_nearest(sod,2378)
QF =irr[t2:t3, wav0:wav1].mean(axis=0)

print(f'Sun + Flare average spectrum of the C III (97,7 nm) line = {irr[t2:t3, wav0:wav1].std()}')
print("")

i=1

graph[i].set_title("SUN + FLARE")
graph[i].axhline(y=QF.mean(), color="b", linestyle="dotted")
graph[i].axvline(x=WC3[find_nearest(QF,QF.mean())], color="b", linestyle="dotted", label="wavelength (nm)")
graph[i].plot(WC3,QF,marker='o', color="k")
#plt.figure()


#------------------------------------------------------------------------------
# 6. Compare the centerline obtained for the quiet Sun and flare (delta lambda)

SF=QF - Qs

i=2

graph[i].set_title("DELTA LAMBDA CENTER LINES (C.L.)")
graph[i].plot(WC3,SF,color="b",marker='.', label="Flare")
graph[i].plot(WC3[find_nearest(Qs,Qs.mean())],Qs.mean(), 'o',color= "r", label= "C.L. Quiet Sun")
graph[i].plot(WC3[find_nearest(QF,QF.mean())],QF.mean(), '*',color= "g", label= "C.L. Sun + Flare")
graph[i].plot(WC3[find_nearest(SF,SF.mean())],SF.mean(), 'x',color= "darkred", label= "C.L. Flare")

#------------------------------------------------------------------------------
# 7. Find the Doppler expression for light that relates the wavelength shoft 
#    into velocity

c=299792456.2 #m/s
v=c*(SF.mean()/Qs.mean())
V = (v/(3600/1000))/(149597870700)
#1 ua = 149597870700 m em (8 min luz)
print(f'Velocidade do efeito Doppler= {V} ua')

graph[i].set_title("DOPPLER EFFECT AJUSTMENT")
graph[i].plot(WC3[find_nearest(SF,V)],V, 'X',color= "k", label= "C.L. Flare with Doppler Effect adjustment")
graph[i].axvline(x=WC3[find_nearest(SF,V)], color="green", label="Doppler Effect Adjustment", linestyle="dotted")


for  i in graph:

  i.legend(loc='upper left', borderaxespad=0, fontsize='xx-small')
  i.grid()

plt.tight_layout()