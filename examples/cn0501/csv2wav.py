import os
import csv
import wave
import numpy as np
import pandas as pd
import soundfile as sf

sps = 16000
froot = os.getcwd()
print(froot)



fpath = 'C:\Users\jsantos5\OneDrive - Analog Devices, Inc\Desktop\Codes\CN0501\RevB\pyadi-iio-master\examples\cn0501\csv_files\APXX\V_1.0_F_1000.0\CH0\\'
fname = "DATA_FAST_MODE_WIDEBAND_256000.csv"

data = pd.read_csv(fpath+fname)
t = np.arange(0,len(data),1/sps)

sf.write('DATA_256000.wav',data,256000)