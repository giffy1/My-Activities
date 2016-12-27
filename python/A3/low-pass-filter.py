# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 10:37:01 2016

Low-pass filter implementation.

Thank you Warren Weckesser for your implementation at
http://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units

"""

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    """
    Low-pass Butterworth filter. Frequencies above cutoff will be removed. fs 
    indicates the sampling rate.
    """
    nyq = 0.5 * fs # nyquist frequency
    normal_cutoff = cutoff / nyq # normalize the cut-off by the nyquist freq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    Applies a low-pass Butterworth filter to the given data. Frequencies 
    above cutoff will be removed. fs indicates the sampling rate. This method 
    calls butter_lowpass() to generate a low-pass filter and applies it 
    using lfilter().
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

"""
Example usage : Here is an example of a 6th-order low-pass filter applied 
to a 5-second signal sampled at 30Hz of three dominant frequencies: 
1.2 Hz, 9Hz and 12 Hz. By applying a low-pass filter with cut-off 3.667 Hz, 
we are able to recover the 1.2 Hz signal. We plot the frequency response of 
the filter, as well as the original and filtered signals superimposed.

Note in practical applications, your signal will not be the sum of three 
sinusoids but may require many sinusoidal bases to be accurately represented. 
This is related to the Fast Fourier Transform, which we covered in A2. The 
low-pass filter is able to filter arbitrary signals and has many uses in 
real-world applications.

"""

# Filter requirements.
order = 6
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response. You'll notice that frequencies close to the 
# cut-off will have a response around 0.5. After the cut-off, the response 
# quickly qpproaches 0; before, it approaches 1.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Demonstrate the use of the filter.
# First make some data to be filtered.
T = 5.0         # seconds
n = int(T * fs) # total number of samples
t = np.linspace(0, T, n, endpoint=False)
# "Noisy" data.  We want to recover the 1.2 Hz signal from this.
data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()