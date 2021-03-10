# --------------------LICENSE AGREEMENT----------------------------------------
# Copyright (c) 2020 Analog Devices, Inc.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#   - Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation 
#   and/or other materials provided with the distribution.  
#   - Modified versions of the software must be conspicuously marked as such.
#   - This software is licensed solely and exclusively for use with 
#   processors/products manufactured by or for Analog Devices, Inc.
#   - This software may not be combined or merged with other code in any manner 
#   that would cause the software to become subject to terms and conditions 
#   which differ from those listed here.
#   - Neither the name of Analog Devices, Inc. nor the names of its 
#   contributors may be used to endorse or promote products derived from this 
#   software without specific prior written permission.
#   - The use of this software may or may not infringe the patent rights of  
#   one or more patent holders.  This license does not release you from the 
#   requirement that you obtain separate licenses from these patent holders 
#   to use this software.
# 
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES, INC. AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
# NON-INFRINGEMENT, TITLE, MERCHANTABILITY AND FITNESS FOR A PARTICULAR  
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ANALOG DEVICES, INC. OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, PUNITIVE OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
# DAMAGES ARISING OUT OF CLAIMS OF INTELLECTUAL PROPERTY RIGHTS INFRINGEMENT; 
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR  
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# 2020-02-24-7CBSD SLA
# -----------------------------------------------------------------------------
#
# ------------------------BRIEF DESCRIPTION OF PROGRAM-------------------------
# Note: 
# The program captures data from the AD7768 EVAL board via the DataStorm DAQ 
# board. The sample rate is fixed to 1.8Msps and hence the sample rate can't
# be changed.
# -----------------------------------------------------------------------------

import sys

try: 
    import iio
except:
    print ("iio not found!")
    sys.exit(0)

import time
import numpy as np
import matplotlib.pyplot as plt

num_samples = 65536 ###Captures 65536 sample from the AD7768
N = num_samples
diff_bits = 24 ###AD7768 is a 24bit SAR ADC

# Setup Context and set the IP address
my_ip = 'ip:192.168.0.2' # default hardcoded ip

try:
    ctx = iio.Context(my_ip)
    print("Successfully connected to the Data Storm DAQ board")
except:
    print("Unable to connect to the Data Storm DAQ board.")
    print("Please check the IP address of the host Ethernet Adapter")
    sys.exit(0)    

rxadc = ctx.find_device("axi-ad7768-adc") # RX/ADC Core in HDL for DMA

v0 = rxadc.find_channel("voltage0") #There are 8 available channels 
v0.enabled = True ##Enable the channel in IIO to start receiving data

time.sleep(10)  ##A 10s delay is needed.

####Writes 0x63 to register address 0x00####
reg_value = 0xF7
#print("Reg_Value = " + reg_value)
#rxadc.reg_write(0x0B, reg_value)
###Reads back from the Register address 0x00###
reg_val = hex(rxadc.reg_read(0x0B))
reg_val = hex(rxadc.reg_read(0x0B))
print("Reg_Val = " + reg_val)

###Sets or Gets the sampling frequency for AD7768###
#rxadc.attrs["sampling_frequency"].value = "1800000" ###To write sampling frequency 
fs_str = rxadc.attrs["sampling_frequency"].value
fs = int(fs_str)
print("Sampling_Frequency = " , fs)
# sjk fs = 1852000 ##Measured Sample Rate of AD7768 from Osciloscope

###Implement a buffer to capture data from the DMA engine#######
rxbuf = iio.Buffer(rxadc, num_samples, False) # False = non-cyclic buffer

for j in range(5): #Flush buffers.
    rxbuf.refill()
    x = rxbuf.read()
    
# got our data, hence delete the buffer
del rxbuf

####Extract data from buffer########
data = np.frombuffer(x, np.int32)

data = data & 0x00ffffff

print(data[:1])

####Convert the extracted 2's complement data into positive/negative values#### 
for i in range(0, len(data)):
    if(data[i] > 2**(diff_bits - 1)):
        data[i] = data[i] - 2**diff_bits
    else:
        data[i] = data[i]

print(data[:1])

data_dc = round(np.average(data)) ##Gets the DC value present in the captured signal
adc_amplitude_adj = 2.0**(diff_bits-1) ##x**y is same as x^y in python
max_data = max(data)
min_data = min(data)
adc_amplitude_peak = max_data - min_data

mag_adj = (adc_amplitude_peak/(2*adc_amplitude_adj))
#print(mag_adj)

mag_adj_db = 20*np.log10(mag_adj)
data_no_dc = [0]*num_samples
######Removing DC content to avoid spectral leakage#########
for i in range(0, N):
    data_no_dc[i]= data[i] - data_dc
    
######### Apply 7-term Blackman-Harris Window 180dB to remove spectral leakage caused by non-coherent sampling#######
a0 = 0.27105140069342
a1 = 0.43329793923448
a2 = 0.21812299954311
a3 = 0.06592544638803
a4 = 0.01081174209837
a5 = 0.00077658482522
a6 = 0.00001388721735
t = np.linspace(0, 1, num_samples, False)
norm = 1

win = a0 - a1*np.cos(2*np.pi* t) + a2*np.cos(4*np.pi* t) - a3*np.cos(6*np.pi* t) + a4*np.cos(8*np.pi*t) - a5*np.cos(10*np.pi*t) + a6*np.cos(12*np.pi*t)
        
win = win*norm

######Compute the FFT of the window########
win_fft = np.fft.fft(win, N*10)/(N)  ####Same as MATLAB command to increase the FFT resolution to see lobes
win_fft_mag = 2*(np.abs(win_fft[0:int(N/2)+1]))
win_fft_mag_db = 20*np.log10(win_fft_mag[1:int(N/2)+1])
#######Find the maximum value and shift everything down#####
win_fft_mag_db_max = max(win_fft_mag_db)

for i in range(0, len(win_fft_mag_db)):
    win_fft_mag_db[i] = win_fft_mag_db[i] - win_fft_mag_db_max
    
######Apply the Window to the captured Data###################    
windowed_data = data_no_dc*win

#windowed_data = data_no_dc ###In case of coherent sampling no need to apply window
win_data_fft = np.fft.fft(windowed_data)/(N) # FFT normalized
win_data_fft_mag = 2*(np.abs(win_data_fft[0:int(N/2)+1]))
global freq_domain_magnitude_db
freq_domain_magnitude_db = 20*np.log10((win_data_fft_mag[1:int(N/2)+1])/adc_amplitude_adj)
freq_domain_mag_db_loss = mag_adj_db - max(freq_domain_magnitude_db) ###Amplitude loss due to windowing application

for i in range(0, len(freq_domain_magnitude_db)):
    freq_domain_magnitude_db[i] = freq_domain_magnitude_db[i] + freq_domain_mag_db_loss
            
freq_array = np.linspace(0, 0.5*fs, int(N/2), False)
len_freq_array = len(freq_array)
freq_array = freq_array[5:len_freq_array] ###Discard the DC component/bins from the FFT
freq_domain_magnitude_db = freq_domain_magnitude_db[5:len_freq_array]



###Begin Plotting########
plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(data_no_dc)
#plt.plot(data)
plt.title('ADC Data captured from AD7768')
plt.xlabel('Time Samples')
plt.ylabel('Amplitude')
plt.subplot(2,1,2)
plt.title("Frequency Domain Plot")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.plot(freq_array, freq_domain_magnitude_db)
plt.show()
del ctx
del rxadc
