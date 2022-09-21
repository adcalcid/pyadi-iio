import os
import csv
import wave
import numpy as np
import pandas as pd
import soundfile as sf

froot = os.getcwd()
vp = 1.0
f = 1000.0
sps=128000
fpath = '\examples\cn0501\csv_files\APXX\V_'+str(vp)+'_F_'+str(f)+'\CH0\\'
fname = 'DATA_FAST_MODE_WIDEBAND_'+str(sps)+'.csv'

data = pd.read_csv(froot+fpath+fname)
#t = np.arange(0,len(data),1/sps)

print("Creating wav file")
sf.write('DATA_V_'+str(vp)+'_F_'+str(f)+'_'+str(sps)+'.wav',data,sps)
print("File created")
