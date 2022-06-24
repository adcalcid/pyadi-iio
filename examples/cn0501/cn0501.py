# Copyright (C) 2022 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTIT11111111111111111111111111111111111111111111111111111111111111111111UTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
print("Program start")

from math import ceil
from time import sleep as sec_delay
import matplotlib.pyplot as plt
import numpy as np
import os
import cn0501_aux_functions
print("Python Packages Import done")

from adi.ad7768 import ad7768
#import libm2k
#from py_utils.sin_params import *
from sin_params import *
from save_for_pscope import save_for_pscope
print("ADI Packages Import done")

def save_pscope():
    global srate
    data = []
    cwd = os.getcwd() #pyadi-iio branch
    adc_properties = (str(powers) + "_" + str(filters) + "_" + str(srate[rates]['SPS']))

    #fpath = cwd + "\examples\cn0501\csv_files\CH" + str(ch) + "\\"
    fpath = cwd + "\examples\cn0501\\adc_files\\"
    fpath_sub = "\M2K\V_" + str(vpeaks) + "_F_" + str(freqs) +"\CH"+ str(adc_ch) + "\\"

    if(os.path.exists(fpath+fpath_sub)):
        pass
    else:
        print("Creating ADC FILES Folder")
        os.makedirs(fpath+fpath_sub)
    fname_dat = "DATA_" + adc_properties + ".adc"

    vtocode = lambda v: int((v/5)*(2**24))
    data = []
    try:
        print("Converting V to ADC Code")
        for x in srate[rates]['DATA'][adc_ch]:
            data.append(str(vtocode(x)).split('.')[0])
        print("Saving ADC file")
        save_for_pscope(fpath+fpath_sub+fname_dat, 24, True, len(data), "DC0000", "LTC1111", data, data, )   
    except Exception as e_pscope:
        print("Error Pscope Log")
        print(e_pscope)

    pass


def write_csv():
    global srate
    cwd = os.getcwd() #pyadi-iio branch
    adc_properties = (str(powers) + "_" + str(filters) + "_" + str(srate[rates]['SPS']))

    #fpath = cwd + "\examples\cn0501\csv_files\CH" + str(ch) + "\\"
    fpath = cwd + "\examples\cn0501\csv_files\\"
    fpath_sub = "\M2K\V_" + str(vpeaks) + "_F_" + str(freqs) +"\CH"+ str(adc_ch) + "\\"
    #fpath_sub = "\M2K_EDITED\V_" + str(vpeaks) + "_F_" + str(freqs) +"\CH"+ str(adc_ch) + "\\"

    if(os.path.exists(fpath+fpath_sub)):
        pass
    else:
        print("Creating CSV FILES Folder")
        os.makedirs(fpath+fpath_sub)

    fname_dat = "DATA_" + adc_properties + ".csv"
    fname_param = "SINE_" + adc_properties + ".csv"
    try:
        print("Saving CSV Data File")
        with open(fpath+fpath_sub+fname_dat, 'w+') as f:
            #print("Storing data to csv")
            if (rec_all is True): #record all channels
                f.write("CH0,CH1,CH2,CH3,CH4,CH5,CH6,CH7" + '\n')
                for i in range(0, len(srate[rates]['DATA'][0]-1)):
                    f.write(str(srate[rates]['DATA'][0][i]) + "," + str(srate[rates]['DATA'][1][i]) + "," +
                            str(srate[rates]['DATA'][2][i]) + "," + str(srate[rates]['DATA'][3][i]) + "," +
                            str(srate[rates]['DATA'][4][i]) + "," + str(srate[rates]['DATA'][5][i]) + "," +
                            str(srate[rates]['DATA'][6][i]) + "," + str(srate[rates]['DATA'][7][i]) + "," + '\n')
            else: #record adc_ch only
                f.write("CH"+ str(adc_ch) + '\n')
                for i in range(0, len(srate[rates]['DATA'][adc_ch]-1)):
                    f.write(str(srate[rates]['DATA'][adc_ch][i]) + '\n')
        f.close()
        #print("---Data Log Done---\n\n")
    except Exception as e_data_log:
        print("\n Error Data Log:")
        print(e_data_log)

    print("Saving CSV Sin Params File")
    if (param_get == True):
        try:
            with open(fpath+fpath_sub+fname_param, 'w+') as f:
                f.write("SNR,THD,SINAD,ENOB,SFDR,FLOOR" + '\n')
                #print("Storing sine param to csv")
                for i in range (0, len(srate[rates]['SNR'])):                
                    f.write(str(srate[rates]['SNR'][i]) + "," + str(srate[rates]['THD'][i]) + "," +
                            str(srate[rates]['SINAD'][i]) + "," + str(srate[rates]['ENOB'][i]) + "," +
                            str(srate[rates]['SFDR'][i]) + "," + str(srate[rates]['FLOOR'][i]) + "," + '\n')
            f.close()
            #print("---Sine Parameter Log Done---\n\n")
            
        except Exception as e_sine_log:
            print("\n Error Sine Param Log:")
            print(e_sine_log)

class EndProg( Exception ): pass

class ChErr( Exception ): pass

# This should eventually move into adi folder, and add an import to __init__
class cn0501(ad7768):
    def __init__(self, uri=""):
        ad7768.__init__(self, uri=uri)

    def single_capture(self):
        self.power_mode = "FAST_MODE" #FAST_MODE MEDIAN_MODE LOW_POWER_MODE
        self.filter = "WIDEBAND" #WIDEBAND SINC5
        self.sample_rate = 16000
        self.rx_buffer_size = self.sample_rate*2

        print("Sample Rate: ",self.sample_rate)
        print("Buffer Size: ",self.rx_buffer_size)
        print("Enabled Channels: ",self.rx_enabled_channels)
        x = self.rx()
        return x

    def run_sample_rate_tests(self):
        global srate, counter
        
        #Clear Previous Values
        for i in range(0,len(srate)):
            srate[i]['DATA'] = []
            srate[i]['SNR'] = []
            srate[i]['THD'] = []
            srate[i]['SINAD'] = []
            srate[i]['ENOB'] = []
            srate[i]['SFDR'] = []
            srate[i]['FLOOR'] = []

        if(True):
            #Progress Display
            counter +=1
            print ("Progress: ",ceil(counter/total_loops*100),'%')

            #print("Enabled Channels: ",self.rx_enabled_channels)
            self.power_mode = powers
            #print("Power Mode: ",self.power_mode)
            self.filter = filters 
            #print("Filter Type: ",self.filter)
            self.sample_rate = srate[rates]['SPS'] 
            #print("Sample Rate: ",self.sample_rate)
            self.rx_buffer_size = int(self.sample_rate*2) #max 512000
            if self.rx_buffer_size > 512000: self.rx_buffer_size = 512000
            #print("Buffer Size: ",self.rx_buffer_size)

            sec_rec = ceil(self.sample_rate/self.rx_buffer_size*nsecs/2) #use for n sec worth

            #print("\nSwitching Sample Rate")
            sec_delay(1)

            #print("\nSTART CAPTURE")
            for nloop in range(0,loops):
                sec_delay(1)
                #print("." + str(nloop))

                vdata = np.empty(shape=(8,0)) # Change 8 to number of enabled channels
                for _ in range(int(sec_rec)):
                    vdata = np.concatenate((vdata, self.rx()), axis=1)
                
                #Capture data of last loop
                if (nloop == loops-1):
                    srate[rates]['DATA'] = vdata

                #Compute Sine parameters
                if(param_get == True):
                    #print("Calculating Sine Parameters")
                    harmonics, snr, thd, sinad, enob, sfdr, floor = sin_params(vdata[adc_ch])
                    #srate[sps]['HARMONICS'] = np.concatenate((srate[sps]['HARMONICS'],[harmonics]),axis=0)
                    srate[rates]['SNR'] = np.concatenate((srate[rates]['SNR'],[snr]),axis=0)
                    srate[rates]['THD'] = np.concatenate((srate[rates]['THD'],[thd]),axis=0)
                    srate[rates]['SINAD'] = np.concatenate((srate[rates]['SINAD'],[sinad]),axis=0)
                    srate[rates]['ENOB'] = np.concatenate((srate[rates]['ENOB'],[enob]),axis=0)
                    srate[rates]['SFDR'] = np.concatenate((srate[rates]['SFDR'],[sfdr]),axis=0)
                    srate[rates]['FLOOR'] = np.concatenate((srate[rates]['FLOOR'],[floor]),axis=0)

                #Plot Data figures
                if (nloop == 0 and plot_show == True):
                    plt.figure(rates)
                    if(adc_ch ==0 ):
                        plt.plot(vdata[0],color='red') #X GP
                    if(adc_ch == 1):
                        plt.plot(vdata[1],color='blue') #Y GP
                    if(adc_ch ==2):
                        plt.plot(vdata[2],color='green') #Z GP
            
            #print("---Data Capture Done---\n\n")
        
        #Plot Average of Sine Params
        if(plot_show==True):
            snr_arr = []
            thd_arr =[]
            sinad_arr = []
            enob_arr = []
            sfdr_arr = []
            floor_arr = []
            sr = np.zeros(len(srate))
            for i in range(0,len(srate)):
                sr[i] = int(srate[i]['SPS'])
            for i in range(0,len(sr)):
                snr_arr = np.concatenate((snr_arr,[np.average(srate[i]['SNR'])]),axis=0)
                thd_arr = np.concatenate((thd_arr,[np.average(srate[i]['THD'])]),axis=0)
                sinad_arr = np.concatenate((sinad_arr,[np.average(srate[i]['SINAD'])]),axis=0)
                enob_arr = np.concatenate((enob_arr,[np.average(srate[i]['ENOB'])]),axis=0)
                sfdr_arr = np.concatenate((sfdr_arr,[np.average(srate[i]['SFDR'])]),axis=0)
                floor_arr = np.concatenate((floor_arr,[np.average(srate[i]['FLOOR'])]),axis=0)
            
            if (plot_show == True):
                plt.figure(101)
                plt.title("SNR")
                plt.plot(sr,snr_arr,marker="s")
                plt.figure(102)
                plt.title("THD")
                plt.plot(sr,thd_arr,marker="s")
                plt.figure(103)
                plt.title("SINAD")
                plt.plot(sr,sinad_arr,marker="s")
                plt.figure(104)
                plt.title("ENOB")
                plt.plot(sr,enob_arr,marker="s")
                plt.figure(105)
                plt.title("SFDR")
                plt.plot(sr,sfdr_arr,marker="s")
                plt.figure(106)
                plt.title("FLOOR")
                plt.plot(sr,floor_arr,marker="s")           

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#TEST PARAMETER VALUES
param_get = True
plot_show = False
rec_all = False
loops = 1 #loops per channel 
nsecs = 1 #even number

#ADC TEST MODES
#power_modes = ['LOW_POWER_MODE', 'MEDIAN_MODE', 'FAST_MODE']
power_modes = ['FAST_MODE']
filter_types= ['WIDEBAND']

#M2K TEST OUTPUTS
m2k_f = [1000] #Frequency Values
#m2k_f = [10,1000]
m2k_vp = [1.0] #Vpeak Values  max vp=2.5

srate = {0: {'SPS': 8000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [],'CODE':[]},
                1: {'SPS': 16000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [], 'CODE':[]},
                2: {'SPS': 32000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [],'CODE':[]},
                3: {'SPS': 64000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [],'CODE':[]},
                4: {'SPS': 128000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [],'CODE':[]},
                5: {'SPS': 256000, 'DATA': [], 'HARMONICS': [],'SNR': [],'THD': [],'SINAD': [],'ENOB': [],'SFDR': [],'FLOOR': [],'CODE':[]}}

total_loops = loops * len(m2k_f) * len(m2k_vp) * len(power_modes) * len(filter_types) * len(srate)

try:
    # Instantiate hardware
    #mym2k = cn0501_aux_functions.wav_init()
    #mycn0501 = cn0501(uri="ip:analog.local")
    #mycn0501 = cn0501(uri="ip:169.254.92.202")

    # Pick M2K output
    #cn0501_aux_functions.wavdiff_out(mym2k)
    #cn0501_aux_functions.seismic_out(mym2k)

    while(True):
        counter = 0
        print("\n\nEnter GP CHANNEL, x:0 y:1 z:2 exit:-1")
        val = input()
        if (int(val) == -1):
            print("Ending Program...")
            raise EndProg
        elif (int(val)>=0 and int(val)<=2):
            print("Starting Data Caputre and Storage. ",total_loops," total loops")
            adc_ch = int(val)
            for vpeaks in m2k_vp:
                for freqs in m2k_f:
                    mym2k = cn0501_aux_functions.wav_init()
                    cn0501_aux_functions.sine_1k_out(mym2k, vp=vpeaks, f=freqs)  
                    sec_delay(2)

                    for powers in power_modes:
                        for filters in filter_types:
                            for rates in range(5,-1,-1):
                                if (powers == 'MEDIAN_MODE'):  rates = 4 #128kps max on MEDIAN mode 
                                elif (powers == 'LOW_POWER_MODE'): rates = 2 #32ksps max on LOW POWER mode

                                #print("M2K Output: Vp=",vpeaks," Freq=",freqs)
                                mycn0501 = cn0501(uri="ip:169.254.92.202")
                                mycn0501.run_sample_rate_tests()
                                write_csv()
                                save_pscope()

                                del mycn0501

                    cn0501_aux_functions.wav_close(mym2k)
        else:
                raise ChErr

        if (plot_show == True):
            plt.show()
        
except EndProg:
    print("Close M2K handler")
    cn0501_aux_functions.wav_close(mym2k)
    pass
except ChErr:
    print("\nEnter valid value")
except Exception as e:
    print("\n Error:")
    print(e)