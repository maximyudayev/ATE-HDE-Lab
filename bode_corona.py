import pyvisa as visa
import time
import numpy as np
import matplotlib.pyplot as plt

# Setup resource
rm = visa.ResourceManager()
# Fill in your IP address
scope = rm.open_resource('TCPIP0::10.35.152.3::INSTR')

phPoints = []
ampPointsdB = []

freqPoints = [5,10,20,50,100,200,500,1000,2000,5000,10000,20000,50000]
genWfNumOnScr = 3

#To query something use : scope.query('SCPI cmd?').
#To set   something use : scope.write('SCPI cmd').
#Test: scope.write('GEN:FREQ 100')

#################
### When *RST ###
#################
# 'GEN:FUNC SIN'    # sine
# 'GEN:VOLT 0.5'    # 0.5 Vpp
# 'GEN:OFFS 0'      # offset 0V
# 'GEN:FREQ 1K'     # 1kHz
# 'GEN:OUT:OFF'     # generator output disabled
# 'TIM:SCAL 10U'    # 10us
# 'ACQ:AVER:COUN 2' # averages over 2 waveforms


############START CODE HERE################
# Identity check
print(scope.query('*IDN?'))

# Reset scope
scope.write('*RST')                                                     #Resets scope

# Enable generator and connect it to oscilloscope
print(scope.write('GEN:OUTP ON'))                                       #Enables generator output
print(scope.write('CHAN1:STAT ON'))                                     #Activates channel 1
print(scope.write('CHAN2:STAT ON'))                                     #Activates channel 2
horDivNum = int(scope.query('TIM:DIV?'))                                #Gets number of horizontal divisons

# ############################################
# ### Output sine wave 3V 1V offset @ 3kHz ###
# ############################################
# print(scope.write('TRIG:OUT:MODE GEN'))                                 #Triggers on generator output
# print(scope.write('GEN:FUNC SIN'))                                      #Selects since generator function
# print(scope.write('GEN:VOLT 3'))                                        #Sets amplitude to 3Vpp
# print(scope.write('GEN:VOLT:OFFS 1'))                                   #Sets 2V DC offset
# print(scope.write('GEN:FREQ 3K'))                                       #Sets 3kHz frequency
# print(scope.write('ACQ:AVER:COUN 10'))                                  #Average over 10 consecutive waveforms
# print(scope.write('CHAN1:ARIT AVER'))                                   #Average over channel 1
# print('Result of averaging: ', scope.query('ACQ:AVER:COMP?'))           #Print result of averaging

# # Finished?
# print('Operation completion status (1==yes): ', scope.query('*OPC?'))   #Operation complete
# print(scope.query(':SYST:ERR:ALL?'))


# #########################################################
# ### Output pulse between 0 & 3V duty cycle 30% @ 5kHz ###
# #########################################################
# print(scope.write('TRIG:OUT:MODE GEN'))                                 #Triggers on generator output
# print(scope.write('GEN:FUNC PULS'))                                     #Selects pulse generator function
# print(scope.write('GEN:VOLT 3'))                                        #Sets amplitude to 3Vpp
# print(scope.write('GEN:VOLT:OFFS 1.5'))                                 #Sets 1.5V DC offset
# print(scope.write('GEN:FUNC:PULS:DCYC 30'))                             #Sets 30% duty cycle
# print(scope.write('GEN:FREQ 5K'))                                       #Sets 5kHz frequency
# print(scope.write('ACQ:AVER:COUN 10'))                                  #Average over 10 consecutive waveforms
# print(scope.write('CHAN1:ARIT AVER'))                                   #Average over channel 1
# print('Result of averaging: ', scope.query('ACQ:AVER:COMP?'))           #Prints result of averaging

# # Finished?
# print('Operation completion status (1==yes): ', scope.query('*OPC?'))   #Operation completed
# print(scope.query(':SYST:ERR:ALL?'))


#################
### Bode Plot ###
#################
# Generator settings
print(scope.write('TRIG:OUT:MODE GEN'))                                 #Triggers on generator output
print(scope.write('GEN:FUNC SIN'))                                      #Selects sine generator function
print(scope.write('GEN:VOLT 6'))                                        #Sets amplitude to 6Vpp

# Probe settings
print(scope.query('PROB1:SET:TYPE?'))                                   #Queries probe type
print(scope.write('PROB1:SET:ATT:UNIT V'))                              #Configures voltage probe 1
print(scope.query('PROB1:SET:ATT:AUTO?'))                               #Scope's probe auto recognition
print(scope.write('PROB1:SET:ATT:MAN 1'))                               #Set manually to 1:1 gain
print(scope.query('PROB2:SET:TYPE?'))                                   #Queries probe type
print(scope.write('PROB2:SET:ATT:UNIT V'))                              #Configures voltage probe 2
print(scope.query('PROB2:SET:ATT:AUTO?'))                               #Scope's probe auto recognition
print(scope.write('PROB2:SET:ATT:MAN 1'))                               #Set manually to 1:1 gain

# Time/div, V/div
print(scope.write('CHAN1:SCAL 1'))                                      #1V/div vertical scale for channel 1
print(scope.write('CHAN2:SCAL 1'))                                      #1V/div vertical scale for channel 2
chan2Scale = 1

print(scope.write('CHAN1:POS 0'))                                       #Superimposes both signals on top
print(scope.write('CHAN2:POS 0'))

# Trigger
print(scope.write('TRIG:A:MODE AUTO'))                                  #Sets auto trigger mode
print(scope.write('TRIG:A:SOUR CH1'))                                   #Trigger on channel 1
print(scope.write('TRIG:A:TYPE EDGE'))                                  #Trigger on edge
print(scope.write('TRIG:A:EDGE:SLOP POS'))                              #Trigger on rising edge

# Measurements
print(scope.write('ACQ:AVER:COUN 10'))                                  #Average over 10 consecutive waveforms
print(scope.write('CHAN1:ARIT AVER'))                                   #Average over channel 1
print(scope.write('CHAN2:ARIT AVER'))                                   #Average over channel 2

print(scope.write('MEAS1:SOUR CH1'))                                    #Measure amplitude of CH1
print(scope.write('MEAS1:MAIN PEAK'))                                   #Setup of Channel 1 amplitude measurement
print(scope.write('MEAS1 ON'))                                          #Enable measurement source 1

print(scope.write('MEAS2:SOUR CH2'))                                    #Measure amplitude of CH2
print(scope.write('MEAS2:MAIN PEAK'))                                   #Setup of Channel 2 amplitude measurement
print(scope.write('MEAS2 ON'))                                          #Enable measurement source 2

print(scope.write('MEAS3:SOUR CH2,CH1'))                                #Measure phase of CH2 with respect to CH1
print(scope.write('MEAS3:MAIN PHAS'))                                   #Setup of phase difference measurement
print(scope.write('MEAS3 ON'))                                          #Enable measurement source 3

# print(scope.write('REFL4:REL:MODE TEN'))                                #0.1-0.9 rise time reference level setup
# print(scope.write('MEAS4:SOUR CH2'))                                    #Measure rise time on channel 2
# print(scope.write('MEAS4:MAIN RTI'))                                    #Setup of Channel 2 rise time measurement
# print(scope.write('MEAS4 ON'))                                          #Enable measurement source 4

# Finished?
print('Operation completion status (1==yes): ', scope.query('*OPC?'))   #Operation completed
print(scope.query(':SYST:ERR:ALL?'))

for freq in freqPoints:
    # Setup generator frequency    
    print(scope.write(f'GEN:FREQ {freq}'))                              #Sets next frequency for sweep

    # Setup scope timebase, fit 3 to 4 wavelengths on a screen
    print(scope.write(f'TIM:SCAL {genWfNumOnScr/(freq*horDivNum)}'))    #Sets horizontal scale proportional to sweep frequency    

    # Synchronization
    print('Operation completion status (1==yes): ', scope.query('*OPC?'))
    print(scope.query(':SYST:ERR:ALL?'))

    time.sleep(1)

    # Read the measurement value for your amplitudes
    ampIn = scope.query('MEAS1:RES?')                                   #Read input signal amplitude
    ampOut = scope.query('MEAS2:RES?')                                  #Read output signal amplitude

    while float(ampOut) < (2*chan2Scale):
        chan2Scale /= 2
        print(scope.write(f'CHAN2:SCAL {chan2Scale}'))
        
        # Synchronization
        print('Operation completion status (1==yes): ', scope.query('*OPC?'))
        print(scope.query(':SYST:ERR:ALL?'))

        ampOut = scope.query('MEAS2:RES?')

    # Calculate gain in dB instead of 1 and append it
    ampPointsdB.append(20*np.log10(float(ampOut)/float(ampIn)))         #Convert ratio of amplitude to dB

    # Read your phase measurement
    phDiff = scope.query('MEAS3:RES?')                                  #Read phase difference
    phPoints.append(float(phDiff))

    # Synchronization
    print('Operation completion status (1==yes): ', scope.query('*OPC?'))
    print(scope.query(':SYST:ERR:ALL?'))


# Plot results
fig, dat = plt.subplots(2,1)

dat[0].semilogx(freqPoints, ampPointsdB,'ro-')
dat[0].set(xlabel='freq (Hz)', ylabel='A(dB)', title='A(f)')

dat[1].semilogx(freqPoints, phPoints,'ro-')
dat[1].set(xlabel='freq (Hz)', ylabel='phase(°)', title='Phase(f)')

fig.tight_layout()

plt.show()


###################
### Immortality ###
###################
# Reset scope
scope.write('*RST')                                                     #Resets scope

# Enable generator and connect it to oscilloscope
print(scope.write('GEN:OUTP ON'))                                       #Enables generator output
print(scope.write('CHAN1:STAT ON'))                                     #Activates channel 1
print(scope.write('CHAN2:STAT ON'))                                     #Activates channel 2

# Generator settings
print(scope.write('TRIG:OUT:MODE GEN'))                                 #Triggers on generator output
print(scope.write('GEN:FUNC SIN'))                                      #Selects sine generator function
print(scope.write('GEN:VOLT 6'))                                        #Sets amplitude to 6Vpp

# Probe settings
print(scope.query('PROB1:SET:TYPE?'))                                   #Queries probe type
print(scope.write('PROB1:SET:ATT:UNIT V'))                              #Configures voltage probe 1
print(scope.query('PROB1:SET:ATT:AUTO?'))                               #Scope's probe auto recognition
print(scope.write('PROB1:SET:ATT:MAN 1'))                               #Set manually to 1:1 gain
print(scope.query('PROB2:SET:TYPE?'))                                   #Queries probe type
print(scope.write('PROB2:SET:ATT:UNIT V'))                              #Configures voltage probe 2
print(scope.query('PROB2:SET:ATT:AUTO?'))                               #Scope's probe auto recognition
print(scope.write('PROB2:SET:ATT:MAN 1'))                               #Set manually to 1:1 gain

freq = 410
# Setup generator frequency    
print(scope.write(f'GEN:FREQ {freq}'))                              #Sets next frequency for sweep

# Label signals with immortal names
print(scope.write(f'CHAN1:LAB "GORIK IS"'))
print(scope.write(f'CHAN2:LAB "AWESOME"'))
print(scope.write('CHAN1:LAB:STAT ON'))
print(scope.write('CHAN2:LAB:STAT ON'))

print(scope.write('CHAN1:SCAL 2.5'))                                    #2.5V/div vertical scale for channel 1
print(scope.write('CHAN2:SCAL 2.5'))                                    #2.5V/div vertical scale for channel 2
chan2Scale = 2.5

# Trigger
print(scope.write('TRIG:A:MODE AUTO'))                                  #Sets auto trigger mode
print(scope.write('TRIG:A:SOUR CH1'))                                   #Trigger on channel 1
print(scope.write('TRIG:A:TYPE EDGE'))                                  #Trigger on edge
print(scope.write('TRIG:A:EDGE:SLOP POS'))                              #Trigger on rising edge

# Measurements
print(scope.write('ACQ:AVER:COUN 10'))                                  #Average over 10 consecutive waveforms
print(scope.write('CHAN1:ARIT AVER'))                                   #Average over channel 1
print(scope.write('CHAN2:ARIT AVER'))                                   #Average over channel 2

print(scope.write('MEAS1:SOUR CH1'))                                    #Measure amplitude of CH1
print(scope.write('MEAS1:MAIN PEAK'))                                   #Setup of Channel 1 amplitude measurement
print(scope.write('MEAS1 ON'))                                          #Enable measurement source 1

print(scope.write('MEAS2:SOUR CH2'))                                    #Measure amplitude of CH2
print(scope.write('MEAS2:MAIN PEAK'))                                   #Setup of Channel 2 amplitude measurement
print(scope.write('MEAS2 ON'))                                          #Enable measurement source 2

print(scope.write('MEAS3:SOUR CH2,CH1'))                                #Measure phase of CH2 with respect to CH1
print(scope.write('MEAS3:MAIN PHAS'))                                   #Setup of phase difference measurement
print(scope.write('MEAS3 ON'))                                          #Enable measurement source 3

# Setup scope timebase, fit 3 to 4 wavelengths on a screen
print(scope.write(f'TIM:SCAL {genWfNumOnScr/(freq*horDivNum)}'))    #Sets horizontal scale proportional to sweep frequency    

# Synchronization
print('Operation completion status (1==yes): ', scope.query('*OPC?'))
print(scope.query(':SYST:ERR:ALL?'))

time.sleep(1)

# Read the measurement value for your amplitudes
ampIn = scope.query('MEAS1:RES?')                                   #Read input signal amplitude
ampOut = scope.query('MEAS2:RES?')                                  #Read output signal amplitude

while float(ampOut) < (2*chan2Scale):
    chan2Scale /= 2
    print(scope.write(f'CHAN2:SCAL {chan2Scale}'))
    
    # Synchronization
    print('Operation completion status (1==yes): ', scope.query('*OPC?'))
    print(scope.query(':SYST:ERR:ALL?'))

    ampOut = scope.query('MEAS2:RES?')

# Calculate gain in dB instead of 1 and append it
ampPointsdB.append(20*np.log10(float(ampOut)/float(ampIn)))         #Convert ratio of amplitude to dB

# Read your phase measurement
phDiff = scope.query('MEAS3:RES?')                                  #Read phase difference
phPoints.append(float(phDiff))

# Synchronization
print('Operation completion status (1==yes): ', scope.query('*OPC?'))
print(scope.query(':SYST:ERR:ALL?'))


# Added
print(rm.list_resources())

#End
scope.close()