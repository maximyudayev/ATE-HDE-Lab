import visa
#for waiting 1s if desired
import time
# for random in the example
import numpy as np

import matplotlib.pyplot as plt
import math

# Setup resource
rm = visa.ResourceManager()
# Fill in your IP address
scope = rm.open_resource('TCPIP0::10.35.152.x::INSTR')

phasePoints = []
amplPoints_dB = []

freqPoints = [10,20,50,100,200,500,1000,2000,5000,10000,20000,50000]

# Identity check

# Reset scope

# Finished?

# Check for errors

# Setup generator


# Finished?

# Check for errors


# Scope settings


# Trigger Settings


# Finished?

# Check for errors


# Create measurements


# Finished?

# Check for errors


for freq in freqPoints:
    # Setup generator frequency
    # Setup scope timebase find a nice formula where you have around 3 to 4 periods on a screen
    # Wait for a second

    # Read the measurement value for your amplitudes
    newPointIn = np.random.random(1) # Read your amplitude measurement instead of this random number
    newPointOut = np.random.random(1)

    # calculate Amplification in dB instead of 1 and append it
    amplPoints_dB.append(1)

    # Read your phase measurement
    newPhase = np.random.random(1) * 90 # Read your phase measurement instead of this random number
    phasePoints.append(newPhase)

    # Add synchronization and error checking


# plot the data
fig, dat = plt.subplots(2,1)

dat[0].semilogx(freqPoints, amplPoints_dB,'ro-')
dat[0].set(xlabel='freq (Hz)', ylabel='A(dB)', title='A(f)')

dat[1].semilogx(freqPoints, phasePoints,'ro-')
dat[1].set(xlabel='freq (Hz)', ylabel='phase(°)', title='Phase(f)')

fig.tight_layout()

# display the plot
plt.show()

scope.close()