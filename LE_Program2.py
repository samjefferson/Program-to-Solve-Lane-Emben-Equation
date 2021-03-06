import matplotlib.pyplot as plt
import math

#Below is the beginning of the multi-dimensional array/lists for the lane-emden numerical integration.

#dimensionless density list
dDArray = []
#dimensionless radius list
dRArray = []
#list to store the value of the differential of dimensionless density 
firstDifArray = []


#Below is the beginning of the multi-dimensional array/lists for the calculations of stellar properties for comparision with the Standard Solar Model.

#Mass list
massArray = []
#Radius list
radiusArray = []
#log10 Density list
logDensityArray = []
#log10 Pressure list
logPressureArray = []
#log10 Temperature list
logTemperatureArray = []


#Below is the lane-emden numerical integration.

#The integration must be repeated six times for n values 0,1,2,3,4,5.  This is done with the for loop below.
for n in range(0,6):
	#Here are some variable which are required for the integration
	#dimensionless density i 
	dDi = 1
	#the differential of Dimensionaless density
	dDD = 0
	#dimensionless radius i (a very small number is used instead of 0) 
	dRi = 0.00001
	#delta dimensionless radius (the change in)
	ciDR = 0.001
	#this variable is set to the intial dRi value and can be used later to take away the 0.00001 if needed
	dRiLocked = dRi
	
	#now another list is append into an the next available index of the lists defined above to add a dimension
	dDArray.append([])
	dRArray.append([])
	firstDifArray.append([])
	#the counter is used to stop the integration continuing indefinitely at n = 5 as the n = 5 curve tends towards zero, never actually reaching it
	counter = 0
	
	#The while loop below runs the intergration until each n value drops below 0, or in the case of n = 5, 20000 times. 
	while (dDi > -0.001)&(counter<20000):
		#this increases the counter 
		counter+=1
		#here the dimensionaless values are appended into the list for the corresponding value of n
		dDArray[n].append(dDi)
		dRArray[n].append(dRi)
		firstDifArray[n].append(dDD)
		#the calculation below uses the LE equation to alter the values at an increase in dR of 0.001 (ciDR) 
		lETemp = 2/dRi
		lETemp = lETemp * dDD
		lETemp = lETemp + dDi**n
		
		lETemp = lETemp * ciDR
		lETemp = dDD-lETemp
		
		
		dDD = lETemp
		
		lETemp = lETemp * ciDR
		lETemp = lETemp + dDi
		dDi = lETemp
		dRi = dRi + ciDR
	
		
	
	#Below is the linear interpolation for n values 0 to 4 (n=5 doesnt have cross the x-axis)
	
	if n!=5:
		#the y0 variable will be the minimum positive value of y produced by the program
		y0 = min(filter( lambda x:x>0,dDArray[n]))
		#the y1 variable will be the maximum negative value of y produced by the program
		y1 = max(filter( lambda x:x<0,dDArray[n]))
		#these two variables therefore represent the two closest known points to y= 0
		#the x variables below represent the x value which corresponds to the y values above with resprect to the graph
		#the dRiLocked variable is now used to substract the original value added to make the program run
		#the function below in affect takes the value of dRi stored in the array at "row n" with an index equal
		#..to the index of the value taken from the dDArray
		x0 = (dRArray[n][dDArray[n].index(y0)])- dRiLocked
		x1 = (dRArray[n][dDArray[n].index(y1)])- dRiLocked
		
		#below is a function to find the equation of a straight line between points (x0,y0) and (x1,y1), the results will be the gradient and y-intercept
		
		gradient = (y1-y0)/(x1-x0)
		
		intercept = y0 - (gradient*x0)
		
		#now the program subs in y=0 to find the point where dimensionless density is zero
		
		y = 0
		x = (y - intercept)/gradient 
		
		
		#finally the program prints the value of x when y=0 to 3 decimal place
		
		
		#PLOTTING GRAPH OF MASS VS RADIUS (for sun)
		
	
		#i have created new variables to rename the older variables needed to names which are more recognisable in this context
		dRSurface = x
		dDbyDRSurface = gradient
		
		#alpha must be calculated for solar radii so that radius and dimensionless radius can be interchanged
		alpha = 1/dRSurface
		
		#central density must now be calculated as it is a term in the equation linking mass and radius
		#using formala for the mean density of the Sun and the formula linking mean density and central density
		lITempOne = 1/dRSurface
		lITempOne = lITempOne * dDbyDRSurface
		lITempOne = lITempOne * -3
		lITempTwo = 3 * 1
		lITempTwo = lITempTwo / (4*math.pi*1**3)
		centDensity = lITempTwo/lITempOne
		i = math.log(centDensity)
		
		#we can now use the array from earlier and the already know relationship between (dDimensionlessDensity/dDimensionalessRadius)and dimensionless radius
		#again the arrays/lists are used to store values to later create a graph
		
		massArray.append([])
		radiusArray.append([])
		
		
		#the origin of the graph is at solar radius and solar mass zero so we begin the lists with these values, they are appended below
		#the loop will run every value of solar mass and solar radius for each value of dimensionless radius in the array 
		
		
		for m in range(0, int(math.floor(dRSurface*1000))):
			#saving radius to a list for producing graph later (this is dimensionless radius x alpha)
			radius = (dRArray[n][m]) * alpha
			radiusArray[n].append(radius)
			#equation M = 4pi*alpha^3*ksi*(dTheta/dKsi)
			mTemp = (dRArray[n][m])**2 * firstDifArray[n][m]
			mTemp = mTemp * centDensity
			mTemp = mTemp * (-4*math.pi*alpha**3)
			#mTemp now equals M and so can be saved to the mass list
			massArray[n].append(mTemp)
			
		#CALCULATING THE GRAPH FOR DENSITY VS RADIUS
		
		#radius from the previous array can be used
		#central density must be changed to kg/m^3 this is done below
		
		dTempOne = 1/dRSurface
		dTempOne = dTempOne * dDbyDRSurface
		dTempOne = dTempOne * -3
		dTempTwo = 3 * (1.99*10**30)
		dTempTwo = dTempTwo / (4*math.pi*695500000**3)
		centDensityTwo = dTempTwo/dTempOne
		
		logDensityArray.append([])
		
		for d in range(0, int(math.floor(dRSurface*1000))):
			#now the conversion from dimensionless density to density can be made, density = dimensionless density^n * central density
			density = ((dDArray[n][d])**n) * centDensityTwo
			logDensity = math.log10(density)
			logDensityArray[n].append(logDensity)
			
		#CALCULATING PRESSURE VS RADIUS
		
		logPressureArray.append([])
		
		#first the constant K must be calculated which is done below 
		#this calculation cannot be done for n = 0 as it involves an unavoidable division by zero
		k = None 
		if n!=0:
			kTemp = 4*math.pi*(6.673*10**-11)
			
			kTemp = kTemp * centDensityTwo**((n-1)/n)

			kTemp = kTemp*alpha**2

			k = (n+1)/kTemp
			
			
			for p in range(0, int(math.floor(dRSurface*1000))):
				#now the equation relating pressure and dimensionless density can be used
				pTemp = (n+1)/n
				pressure = k*(centDensityTwo**pTemp)*(dDArray[n][p]**(n+1))
				logPressure = math.log10(pressure)
				logPressureArray[n].append(logPressure)
		else:
			#empty string as placeholder for n = 0 
			logPressureArray[n].append("")
			
		
		#NOW TEMPERTURE VS RADIUS IS CALCULATED
		logTemperatureArray.append([])
		#equation simply uses variable we already know and constants
		#T = Mh*mu*K*centDens^(1/n)*dimensionlessdens*(1/k)
		#also requires constant K; n = 0 is once again omitted
		if n!=0:
			ttemp = (1.66*10**-27)*0.5954
			ttemp = ttemp * k
			ttemp = ttemp * (centDensity**(1/n))
			ttemp = ttemp / (1.38*10**-23)
			
			for t in range(0,int(math.floor(dRSurface*1000))):
				ttempLoop = ttemp * dDArray[n][t]
				ttempLoop = math.log10(ttempLoop)
				logTemperatureArray[n].append(ttempLoop)
				
		else:
			#empty string as placeholder for n = 0
			logTemperatureArray[n].append("")	
		

		
#read in SSM using character loops to place each column in a seperate array
sSMMass = []
sSMRadius = []
sSMTemp = []
sSMDens = []
sSMPressure = []
f = open("SSM.txt", "r")

readCounter = 0

fileLines = f.read().splitlines()

for q in range(0,len(fileLines)):
	readList = list(fileLines[q])
	one = []
	two = []
	three = []
	threeE = []
	four = []
	fourE = []
	five = []
	fiveE = []
	
	for pA in range(1, 10):
		one.append(readList[pA])
		
	
	sSMMass.append(float("".join(one)))
	
	for pB in range(12, 19):
		two.append(readList[pB])
	
	sSMRadius.append(float("".join(two)))
	
	for pC in range(21, 26):
		three.append(readList[pC])
		
	for pCE in range(28,30):
		threeE.append(readList[pCE])
	
	cExp = int("".join(threeE))
	if readList[27] == "-":
		cExp = -cExp
	
	
	#this joins the characters into strings, converts to float
	sSMTemp.append(math.log10(float("".join(three))*(10**cExp)))
	
	for pD in range(32, 37):
		four.append(readList[pD])
		
	for pDE in range(39,41):
		fourE.append(readList[pDE])
	
	dExp = int("".join(fourE))
	if readList[38] == "-":
		dExp = -dExp
	
	#this joins the characters into strings, converts to float multiplied by 1000 to conver g/cm^3 into kg/m^3
	sSMDens.append(math.log10(1000*(float("".join(four))*10**dExp))) 
	
	for pE in range(43, 48):
		five.append(readList[pE])
		
	for pEE in range(50,52):
		fiveE.append(readList[pEE])
	
	eExp = int("".join(fiveE))
	if readList[49] == "-":
		eExp = -eExp
		
	#this joins the characters into strings, converts to float
	sSMPressure.append(math.log10((float("".join(five)))*10**eExp))
	
	

		
	
	




#Below is the plotting of the lane-emden graph		
fig, aa = plt.subplots()
aa.plot(dRArray[0], dDArray[0], color = "purple", label = "n=0")
aa.plot(dRArray[1], dDArray[1], color = "orange", label = "n=1")
aa.plot(dRArray[2], dDArray[2], color = "green", label = "n=2")
aa.plot(dRArray[3], dDArray[3], color = "red", label = "n=3")
aa.plot(dRArray[4], dDArray[4], color = "blue", label = "n=4")
aa.plot(dRArray[5], dDArray[5], color = "black", label = "n=5")
aa.set_xlim(0,20)
aa.set_ylim(0,1.2)
aa.set_xlabel("Dimensionless Radius")
aa.set_ylabel("Dimensionless Density")
aa.legend(loc=0)
aa.set_title("Solutions for the Lane-Emden equation")
plt.show()

#plotting the mass graph
fig, ab = plt.subplots()
ab.plot(radiusArray[0], massArray[0], color = "purple", label = "n=0")
ab.plot(radiusArray[1], massArray[1], color = "orange", label = "n=1")
ab.plot(radiusArray[2], massArray[2], color = "green", label = "n=2")
ab.plot(radiusArray[3], massArray[3], color = "red", label = "n=3")
ab.plot(radiusArray[4], massArray[4], color = "blue", label = "n=4")
ab.plot(sSMRadius, sSMMass, color = "black", label = "SSM")

ab.set_xlim(0,1)
ab.set_ylim(0,1)
ab.set_xlabel("Radius in solar radii")
ab.set_ylabel("Mass in solar masses")
ab.legend(loc=0)
ab.set_title("Mass vs radius for the sun, compared with the SSM")
plt.show()
			
#plotting the density vs radius graph

fig, ac = plt.subplots()
ac.plot(radiusArray[0], logDensityArray[0], color = "purple", label = "n=0")
ac.plot(radiusArray[1], logDensityArray[1], color = "orange", label = "n=1")
ac.plot(radiusArray[2], logDensityArray[2], color = "green", label = "n=2")
ac.plot(radiusArray[3], logDensityArray[3], color = "red", label = "n=3")
ac.plot(radiusArray[4], logDensityArray[4], color = "blue", label = "n=4")
ac.plot(sSMRadius, sSMDens, color = "black", label = "SSM")

ac.set_xlim(0,1)
ac.set_ylim(0,6)
ac.set_xlabel("Radius in solar radii")
ac.set_ylabel("log Density in kgm^-3")
ac.legend(loc=0)
ac.set_title("log Density vs radius for the sun, compared with the SSM")
plt.show()

#plotting the pressure vs radius graph

fig, ad = plt.subplots()

ad.plot(radiusArray[1], logPressureArray[1], color = "orange", label = "n=1")
ad.plot(radiusArray[2], logPressureArray[2], color = "green", label = "n=2")
ad.plot(radiusArray[3], logPressureArray[3], color = "red", label = "n=3")
ad.plot(radiusArray[4], logPressureArray[4], color = "blue", label = "n=4")
ad.plot(sSMRadius, sSMPressure, color = "black", label = "SSM")

ad.set_xlim(0,1)
ad.set_ylim(0,20)
ad.set_xlabel("Radius in solar radii")
ad.set_ylabel("log Pressure in N/m^2")
ad.legend(loc=0)
ad.set_title("log Pressure vs radius for the sun, compared with the SSM")
plt.show()


		
#plotting the temperature vs radius graph


fig, aT = plt.subplots()

aT.plot(radiusArray[1], logTemperatureArray[1], color = "orange", label = "n=1")
aT.plot(radiusArray[2], logTemperatureArray[2], color = "green", label = "n=2")
aT.plot(radiusArray[3], logTemperatureArray[3], color = "red", label = "n=3")
aT.plot(radiusArray[4], logTemperatureArray[4], color = "blue", label = "n=4")
aT.plot(sSMRadius, sSMTemp, color = "black", label = "SSM")

aT.set_xlim(0,1)
aT.set_ylim(3,9)
aT.set_xlabel("Radius in solar radii")
aT.set_ylabel("log Temperature in K")
aT.legend(loc=0)
aT.set_title("log Temperature vs radius for the sun, compared with the SSM")
plt.show()
	
	
	

