import numpy
import csv
import math
from matplotlib import pyplot
import os

class spenvisAnalysis:
    def __init__ (self, path , minParticle ,maxParticle , particleType , cutLength , surfaceDensity, R,h,zMinus,zPlus, deltaR, xBlood,yBlood,zBlood,xA150,yA150,zA150):
        self.path = path
        self.minParticle = minParticle
        self.maxParticle = maxParticle
        self.particleType = particleType
        self.cutLength = cutLength
        self.surfaceDensity = surfaceDensity
        self.R = R
        self.h = h
        self.zMinus = zMinus
        self.zPlus = zPlus
        self.deltaR = deltaR
        self.xBlood = xBlood
        self.xBlood = yBlood
        self.xBlood = zBlood
        self.xA150 = xA150
        self.yA150 = yA150
        self.zA150 = zA150
        self.area = [getAreaCylinder(R,h,zMinus,zPlus, deltaR),getAreaBox(xBlood,yBlood,zBlood),getAreaBox(xA150,yA150,zA150)]
        
    def spenvisTo2DArray(self):
        with open(self.path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
        line_count = 0
        total_line_count = 0
        output_csv = []
        for row in csv_reader:
            counter = 0
        
            for element in row:
            
                row[counter] = row[counter].replace("\"","")
                row[counter] = row[counter].replace("\'","")
                row[counter] = row[counter].replace(" ","")
                
                if (row[counter]== "GRAS_DATA_TITLE"):
                    line_count += 1
                
                if (counter == len(row)-1):
                    #print(row)
                    output_csv.append(row)
                counter = counter + 1
            total_line_count = total_line_count +1
        return output_csv

    
def spenvisTo2DArray(path):
    with open(path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        total_line_count = 0
        output_csv = []
        for row in csv_reader:
            counter = 0
        
            for element in row:
            
                row[counter] = row[counter].replace("\"","")
                row[counter] = row[counter].replace("\'","")
                row[counter] = row[counter].replace(" ","")
                
                if (row[counter]== "GRAS_DATA_TITLE"):
                    line_count += 1
                
                if (counter == len(row)-1):
                    #print(row)
                    output_csv.append(row)
                counter = counter + 1
            
           
                
            
            total_line_count = total_line_count +1
        return output_csv



def getModule(path,n):
    array = spenvisTo2DArray(path)
    if(n == 1):#First histogram
        return array[4][2]
    if(n == 2):#Second histogram
        return array[136][2]
    if(n == 3):
        return array[280][2]
    if(n == 4):
        return array[423][2]
    if(n == 5):
        return array[556][2]
    if(n == 6):
        return array[688][2]
def getTitle(path,n):
    array = spenvisTo2DArray(path)
    if(n == 1):#First histogram
        return array[2][2]
    if(n == 2):#Second histogram
        return array[145][2]
    if(n == 3):
        return array[278][2]
    if(n == 4):
        return array[421][2]
    if(n == 5):
        return array[554][2]
    if(n == 6):
        return array[697][2]

def getOverflow(array,n,s):
    if(s=="ENTRIES")or(s=="Entries")or(s=="entries"):
        if(n == 1):#First histogram
            return array[10][2]
        if(n == 2):#Second histogram
            return array[153][2]
        if(n == 3):
            return array[286][2]
        if(n == 4):
            return array[429][2]
        if(n == 5):
            return array[562][2]
        if(n == 6):
            return array[705][2]
    if(s=="ERROR")or(s=="Error")or(s=="error"):
        if(n == 1):#First histogram
            return array[11][2]
        if(n == 2):#Second histogram
            return array[154][2]
        if(n == 3):
            return array[287][2]
        if(n == 4):
            return array[430][2]
        if(n == 5):
            return array[563][2]
        if(n == 6):
            return array[706][2]
    if(s=="MEAN")or(s=="Mean")or(s=="mean"):
        if(n == 1):#First histogram
            return array[12][2]
        if(n == 2):#Second histogram
            return array[155][2]
        if(n == 3):
            return array[288][2]
        if(n == 4):
            return array[431][2]
        if(n == 5):
            return array[564][2]
        if(n == 6):
            return array[707][2]

    if(s=="VALUE")or(s=="Value")or(s=="value"):
        if(n == 1):#First histogram
            return array[13][2]
        if(n == 2):#Second histogram
            return array[156][2]
        if(n == 3):
            return array[289][2]
        if(n == 4):
            return array[432][2]
        if(n == 5):
            return array[565][2]
        if(n == 6):
            return array[708][2]
def getHistogram(array,n,s):
    arr = []
    ###########################
    #Fill this in with other n#
    ###########################
    if(s=="ENTRIES")or(s=="Entries")or(s=="entries"):
        if(n == 1):#First histogram
            for i in range (32,131):
                arr.append(array[i][5])
            return arr
        if(n == 2):#Second histogram
            for i in range (175,274):
                arr.append(array[i][5])
            return arr
        if(n == 3):
            for i in range (308,407):
                arr.append(array[i][5])
            return arr
        if(n == 4):
            for i in range (451,550):
                arr.append(array[i][5])
            return arr
        if(n == 5):
            for i in range (584,683):
                arr.append(array[i][5])
            return arr
        if(n == 6):
            for i in range (727,826):
                arr.append(array[i][5])
            return arr
    if(s=="ERROR")or(s=="Error")or(s=="error"):
        if(n == 1):#First histogram
            for i in range (32,131):
                arr.append(array[i][4])
            return arr
        if(n == 2):#Second histogram
            for i in range (175,274):
                arr.append(array[i][4])
            return arr
        if(n == 3):
            for i in range (308,407):
                arr.append(array[i][4])
            return arr
        if(n == 4):
            for i in range (451,550):
                arr.append(array[i][4])
            return arr
        if(n == 5):
            for i in range (584,683):
                arr.append(array[i][4])
            return arr
        if(n == 6):
            for i in range (727,826):
                arr.append(array[i][4])
            return arr
    if(s=="MEAN")or(s=="Mean")or(s=="mean"):
        if(n == 1):#First histogram
            for i in range (32,131):
                arr.append(array[i][2])
            return arr
        if(n == 2):#Second histogram
            for i in range (175,274):
                arr.append(array[i][2])
            return arr
        if(n == 3):
            for i in range (308,407):
                arr.append(array[i][2])
            return arr
        if(n == 4):
            for i in range (451,550):
                arr.append(array[i][2])
            return arr
        if(n == 5):
            for i in range (584,683):
                arr.append(array[i][2])
            return arr
        if(n == 6):
            for i in range (727,826):
                arr.append(array[i][2])
            return arr

    if(s=="VALUE")or(s=="Value")or(s=="value"):
        if(n == 1):#First histogram
            for i in range (32,131):
                arr.append(array[i][3])
            return arr
        if(n == 2):#Second histogram
            for i in range (175,274):
                arr.append(array[i][3])
            return arr
        if(n == 3):
            for i in range (308,407):
                arr.append(array[i][3])
            return arr
        if(n == 4):
            for i in range (451,550):
                arr.append(array[i][3])
            return arr
        if(n == 5):
            for i in range (584,683):
                arr.append(array[i][3])
            return arr
        if(n == 6):
            for i in range (727,826):
                arr.append(array[i][3])
            return arr
def analyseFile(path,k):
    arr = []
    
    arr.append(getHistogram(spenvisTo2DArray(path),k,"mean"))#array[0]
    arr.append(getHistogram(spenvisTo2DArray(path),k,"value"))#array[1]
    arr.append(getHistogram(spenvisTo2DArray(path),k,"error"))#array[2]
    arr.append(getHistogram(spenvisTo2DArray(path),k,"entries"))#array[3]
    arr.append(getOverflow(spenvisTo2DArray(path),k,"mean"))#array[4]
    arr.append(getOverflow(spenvisTo2DArray(path),k,"value"))#array[5]
    arr.append(getOverflow(spenvisTo2DArray(path),k,"error"))#array[6]
    arr.append(getOverflow(spenvisTo2DArray(path),k,"entries"))#array[7]
    return arr
def dosePerCM2Array(path, k):
    #k = 1 is aluminium
    #k = 2 is blood
    #k = 3 is A150
    array = analyseFile(path,k)
    arr = []
    for i in range(0,len(array[0])):
        arr.append(float(array[0][i])*float(array[1][i]))
    return arr
def totalDosePerCM2(path, k):
    #k = 1 is aluminium
    #k = 2 is blood
    #k = 3 is A150
    array = analyseFile(path,k)
    arr = []
    total = 0
    for i in range(0,len(array[0])):
        total = total + (float(array[0][i])*float(array[1][i]))
    #total = total + (float(array[4][0])*float(array[5][0]))
    return total
def doseErrorPerCM2(path, k):
    #k = 1 is aluminium
    #k = 2 is blood
    #k = 3 is A150
    array = analyseFile(path,k)
    arr = []
    total = 0
    for i in range(0,len(array[0])):
        total = total + (float(array[0][i])*float(array[2][i]))
    #total = total + (float(array[4][0])*float(array[6][0]))
    return total

def fullAnalysis(path,area):
    
    for i in range (1,4):
        print()
        print("Volume : " +getModule(path,2*i))
        print()
        print("Dose per cm2 : " + str(totalDosePerCM2(path,(1+ 2*(i-1)))/area[i-1]) +u" \u00B1 " + str(doseErrorPerCM2(path,(1+ 2*(i-1)))/area[i-1]) + " mSv/cm2")
        print("Total Dose : " + str(totalDosePerCM2(path,(1+ 2*(i-1))))+u" \u00B1 "+str(doseErrorPerCM2(path,(1+ 2*(i-1))))+" mSv")
        print()
def mToCM(x):
    return 100*x
def mmToCM(x):
    return (x/10)
def getAreaCylinder(R,h,zMinus,zPlus, deltaR):#in cm2
    return (2*math.pi*pow((mToCM(R)),2)+2*math.pi*mToCM(R)*(mToCM(h)))
def getAreaBox(x,y,z):#in cm2
    return (2*mToCM(x)*mToCM(y)+2*mToCM(x)*mToCM(z)+2*mToCM(y)*mToCM(z))

def convert_to_scientific_notation(array):
 
    scientific_notation_array = [format(num, '.0e') for num in array]
    return scientific_notation_array
def particleToArray(path,area,minParticle,maxParticle,particleType,cutLength,surfaceDensity):
    #Follows the convention particleType_numberOfParticles_cutLengthInMicrometers_SurfaceDensityIng/cm2
    #Ex: H1_1000000_1000_30 -> Proton GCR, 1000000 particles, 1000 um cut-length, 30g/cm2 Surface Density
    #Ex: TP_1000_1_20 -> Trapped Proton, 1000 particles, 1 um cut-length, 20g/cm2 Surface Density
    particles =[]
    Aluminium = []
    AluminiumError=[]
    Blood = []
    BloodError = []
    A150 = []
    A150Error = []
    
    for i in range (int(math.log10(minParticle)),(int(math.log10(maxParticle))+1)):
        particles.append(pow(10,i))
    particles_sci = convert_to_scientific_notation(particles)
    for i in range (1,4):
        for k in range(0,len(particles)):
            path = os.path.dirname(path)+'/'+str(particleType)+'_'+str(particles[k])+'_'+str(cutLength)+'_'+str(surfaceDensity)+'.csv'
            if(i==1):
                Aluminium.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
                AluminiumError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
            if(i==2):
                Blood.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
                BloodError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
            if(i==3):
                A150.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
                A150Error.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
    x = [particles,particles_sci,Aluminium,AluminiumError,Blood,BloodError,A150,A150Error]
    return x
def particleDoseGraph(path,area,minParticle,maxParticle,particleType,cutLength,surfaceDensity):
    data = particleToArray(path,area,minParticle,maxParticle,particleType,cutLength,surfaceDensity)
    
    pyplot.xlabel('Number of particles')
    pyplot.ylabel('Dose(mSv)')
    pyplot.title('Dose received by Aluminium as a function of the Number of '+str(particleType)+', with an ISS module surface density of : '+str(surfaceDensity)+' g/cm2 and a Cut-Length of : '+str(cutLength)+'\u03BCm')
    pyplot.plot(data[0],data[2],'g',label="Aluminium")
    pyplot.plot(data[0],data[2],"ko")
    pyplot.legend(loc="upper left")
    pyplot.xscale('log')
    pyplot.errorbar(data[0],data[2],data[3],fmt="none",ecolor="k",linewidth=1, capsize=2)
    pyplot.xticks(data[0], data[1])
    pyplot.grid(True)
    pyplot.show()
    
    pyplot.xlabel('Number of particles')
    pyplot.ylabel('Error on Dose(mSv)')
    pyplot.title('Dose Error as a function of the Number of '+str(particleType)+', with an ISS module surface density of : '+str(surfaceDensity)+' g/cm2 and a Cut-Length of : '+str(cutLength)+'\u03BCm')
    pyplot.plot(data[0],data[3],'g',label="Aluminium")
    pyplot.plot(data[0],data[3],"ko")
    pyplot.legend(loc="upper left")
    pyplot.xscale('log')
    pyplot.xticks(data[0], data[1])
    pyplot.grid(True)
    
    pyplot.show()

    
    pyplot.xlabel('Number of particles')
    pyplot.ylabel('Dose(mSv)')
    pyplot.title('Dose received by Blood and A150 Phantoms as a function of the Number of '+str(particleType)+', with an ISS module surface density of : '+str(surfaceDensity)+' g/cm2 and a Cut-Length of : '+str(cutLength)+'\u03BCm')
    pyplot.plot(data[0],data[4],'r',label="Blood Phantom")
    pyplot.plot(data[0],data[4],'ko')
    pyplot.plot(data[0],data[6],'b',label="A150 Phantom")
    pyplot.plot(data[0],data[6],'ko')
    pyplot.legend(loc="upper left")
    pyplot.xscale('log')
    pyplot.errorbar(data[0],data[4],data[5],fmt="none",ecolor="k",linewidth=1, capsize=2)
    pyplot.errorbar(data[0],data[6],data[7],fmt="none",ecolor="k",linewidth=1, capsize=2)
    pyplot.xticks(data[0], data[1])
    pyplot.grid(True)
    pyplot.show()
    
    
    pyplot.xlabel('Number of particles')
    pyplot.ylabel('Error on Dose(mSv)')
    pyplot.title('Dose Error as a function of the Number of '+str(particleType)+', with an ISS module surface density of : '+str(surfaceDensity)+' g/cm2 and a Cut-Length of : '+str(cutLength)+'\u03BCm')
    pyplot.plot(data[0],data[5],'r',label="Blood Phantom")
    pyplot.plot(data[0],data[5],'ko')
    pyplot.plot(data[0],data[7],'b',label="A150 Phantom")
    pyplot.plot(data[0],data[7],'ko')
    pyplot.legend(loc="upper left")
    pyplot.xscale('log')
    pyplot.xticks(data[0], data[1])
    pyplot.grid(True)

    pyplot.show()

def gdmlToArea(path):
    with open(path, mode='r') as file:
        s = file.readlines()
    line_count = 0
    area = []
    total_line_count = 0
    output_csv = []
    for line in s :
        if("World" not in line):
            
            if("box name" in line):
                
                """
                print("x : "+str(float(next_n_characters_after_substring(line, "x=\"", 9).replace('E','e')))+" mm")
                print("y : "+str(float(next_n_characters_after_substring(line, "y=\"", 9).replace('E','e')))+" mm")
                print("z : "+str(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))+" mm")
                """
                if("_out" in line):
                    x_max = mmToCM(float(next_n_characters_after_substring(line, "x=\"", 9).replace('E','e')))
                    y_max = mmToCM(float(next_n_characters_after_substring(line, "y=\"", 9).replace('E','e')))
                    z_max = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    print(2*(x_max)*(y_max)+2*(y_max)*(z_max)+2*(x_max)*(z_max))
                if("_in" in line):
                    x_min = mmToCM(float(next_n_characters_after_substring(line, "x=\"", 9).replace('E','e')))
                    y_min = mmToCM(float(next_n_characters_after_substring(line, "y=\"", 9).replace('E','e')))
                    z_min = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    area.append(2*(x_max)*(y_max)+2*(y_max)*(z_max)+2*(x_max)*(z_max))
                elif(("_out" not in line) and ("_in" not in line)):
                    x = mmToCM(float(next_n_characters_after_substring(line, "x=\"", 9).replace('E','e')))
                    y = mmToCM(float(next_n_characters_after_substring(line, "y=\"", 9).replace('E','e')))
                    z = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    area.append(2*x*y+2*x*z+2*y*z)
            if("tube name" in line):
                
                if("_out" in line):#Large cylinder
                    """
                    print("Large cylinder : z : "+str(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))+" mm")
                    print("Large cylinder : r : "+str(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E','e')))+" mm")
                    """
                    z_max = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    r_max = mmToCM(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E','e')))
                     
                if("_in" in line):#small cylinder, subtracting both gives a hollow cylinder
                    """
                    print("Small cylinder : z : "+str(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))+" mm")
                    print("Small cylinder : r : "+str(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E','e')))+" mm")
                    """
                    z_min = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    r_min = mmToCM(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E','e')))
                    area.append(2*math.pi*r_max*(z_max+r_max))
                elif(("_out" not in line) and ("_in" not in line)):
                    z = mmToCM(float(next_n_characters_after_substring(line, "z=\"", 9).replace('E','e')))
                    r = mmToCM(float(next_n_characters_after_substring(line, "rmax=\"", 9).replace('E','e')))
                    area.append(2*math.pi*r_max*(z+r_max))
           
    return area
"""
def gdmlToVolume(path):
def gdmlToVolumeTuple(path):
"""
def next_n_characters_after_substring(string, substring, n):
    index = string.find(substring)
    if index != -1:
        next_characters = string[index + len(substring):index + len(substring) + n]
        return next_characters
    else:
        return "Substring not found"

# Example usage:


#30g/cm2
R = 1.475#m
h = 1.5#m
deltaR = 111 #mm
zMinus = 111 #mm
zPlus = 111 #mm
surfaceDensity = 30 #g/cm2
#print(str(getAreaCylinder(R,h,zMinus,zPlus, deltaR))+" cm2")
xBlood = 0.38 #m
yBlood = 0.23 #m
zBlood = 0.6 #m
#print(str(getAreaBox(xBlood,yBlood,zBlood))+" cm2")
xA150 = 0.38 #m
yA150 = 0.23 #m
zA150= 0.6 #m
area = [getAreaCylinder(R,h,zMinus,zPlus, deltaR),getAreaBox(xBlood,yBlood,zBlood),getAreaBox(xA150,yA150,zA150)]

#path = 'C:/Users/jussu/Downloads/TP_1000_0.001_30.csv'
#particleDoseGraph(path,area,1,1000000,'TP','0.001','30')


#path = 'C:/Users/jussu/Downloads/Si28_100_0.001_30.csv'
#fullAnalysis(path,area)
"""
path = 'C:/Users/jussu/Downloads/TrappedElectronDose20cm.csv'
print("##############################################")
fullAnalysis(path,area)
path = 'C:/Users/jussu/Downloads/H1Dose20cm.csv'
print("##############################################")
fullAnalysis(path,area)
path = 'C:/Users/jussu/Downloads/H2Dose20cm.csv'
print("##############################################")
fullAnalysis(path,area)
path = 'C:/Users/jussu/Downloads/He3Dose20cm.csv'
print("##############################################")
fullAnalysis(path,area)
path = 'C:/Users/jussu/Downloads/He4Dose20cm.csv'
print("##############################################")
fullAnalysis(path,area)

"""

"""
x = [0.0001,0.00025, 0.0005,0.001,0.0025,0.005,0.01,0.025,0.05,0.1,0.25,0.5,1,2.5,5,10,25,50,100,250,500,1000,2500,5000,10000,25000,50000,100000,250000,500000,1000000,2500000,5000000,10000000]#in um
x_reduced=[0.0001,0.001,0.01,0.1,1,10,100,1000,10000,100000,1000000,10000000]
x_sci = convert_to_scientific_notation(x_reduced)
particles=[1,10,100,1000,10000,100000,1000000,10000000]
particles_sci = convert_to_scientific_notation(particles)
Aluminium = []
AluminiumError=[]
Blood = []
BloodError = []
A150 = []
A150Error = []
for i in range (1,4):
    for k in range(0,len(x)):
        path = 'C:/Users/jussu/Downloads/TrappedProtonCL'+str(x[k])+'um.csv'
        if(i==1):
            Aluminium.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            AluminiumError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==2):
            Blood.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            BloodError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==3):
            A150.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            A150Error.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])


pyplot.xlabel('Cut-Length(\u03BCm)')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Aluminium as a function of Cut-Length')
pyplot.plot(x,Aluminium,'g',label="Aluminium")
pyplot.plot(x,Aluminium,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
pyplot.errorbar(x,Aluminium,AluminiumError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.xticks(x_reduced, x_sci)
pyplot.grid(True)
pyplot.show()
pyplot.xlabel('Cut-Length(\u03BCm)')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of Cut-Length')
pyplot.plot(x,AluminiumError,'g',label="Aluminium")
pyplot.plot(x,AluminiumError,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
pyplot.xticks(x_reduced, x_sci)
pyplot.grid(True)
pyplot.show()


pyplot.xlabel('Cut-Length(\u03BCm)')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Blood and A150 Phantoms as a function of Cut-Length')
pyplot.plot(x,Blood,'r',label="Blood Phantom")
pyplot.plot(x,Blood,'ko')
pyplot.plot(x,A150,'b',label="A150 Phantom")
pyplot.plot(x,A150,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')

pyplot.errorbar(x,Blood,BloodError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.errorbar(x,A150,A150Error,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.xticks(x_reduced, x_sci)
pyplot.grid(True)
pyplot.show()

pyplot.xlabel('Cut-Length(\u03BCm)')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of Cut-Length')
pyplot.plot(x,BloodError,'r',label="Blood Phantom")
pyplot.plot(x,BloodError,'ko')
pyplot.plot(x,A150Error,'b',label="A150 Phantom")
pyplot.plot(x,A150Error,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')
pyplot.xticks(x_reduced, x_sci)
pyplot.grid(True)

pyplot.show()

Aluminium = []
AluminiumError=[]
Blood = []
BloodError = []
A150 = []
A150Error = []
for i in range (1,4):
    for k in range(0,len(particles)):
        path = 'C:/Users/jussu/Downloads/TP'+str(particles[k])+'Particles.csv'
        if(i==1):
            Aluminium.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            AluminiumError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==2):
            Blood.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            BloodError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==3):
            A150.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            A150Error.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
pyplot.subplot(2,1,1)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Aluminium as a function of the Number of Simulated Particles')
pyplot.plot(particles,Aluminium,'g',label="Aluminium")
pyplot.plot(particles,Aluminium,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.errorbar(particles,Aluminium,AluminiumError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.grid(True)
pyplot.subplot(2,1,2)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of the Number of Simulated Particles')
pyplot.plot(particles,AluminiumError,'g',label="Aluminium")
pyplot.plot(particles,AluminiumError,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.grid(True)
pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.35)
pyplot.show()

pyplot.subplot(2,1,1)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Blood and A150 Phantoms as a function of the Number of Simulated Particles')
pyplot.plot(particles,Blood,'r',label="Blood Phantom")
pyplot.plot(particles,Blood,'ko')
pyplot.plot(particles,A150,'b',label="A150 Phantom")
pyplot.plot(particles,A150,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.errorbar(particles,Blood,BloodError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.errorbar(particles,A150,A150Error,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.grid(True)
pyplot.subplot(2,1,2)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of the Number of Simulated Particles')
pyplot.plot(particles,BloodError,'r',label="Blood Phantom")
pyplot.plot(particles,BloodError,'ko')
pyplot.plot(particles,A150Error,'b',label="A150 Phantom")
pyplot.plot(particles,A150Error,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.grid(True)
pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.35)
pyplot.show()
"""

'''
particles=[1,10,100,1000,10000,100000,1000000]
particles_sci = convert_to_scientific_notation(particles)
Aluminium = []
AluminiumError=[]
Blood = []
BloodError = []
A150 = []
A150Error = []
for i in range (1,4):
    for k in range(0,len(particles)):
        path = 'C:/Users/jussu/Downloads/H1_'+str(particles[k])+'P.csv'
        if(i==1):
            Aluminium.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            AluminiumError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==2):
            Blood.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            BloodError.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
        if(i==3):
            A150.append(totalDosePerCM2(path,(1+ 2*(i-1)))*area[i-1])
            A150Error.append(doseErrorPerCM2(path,(1+ 2*(i-1)))*area[i-1])
pyplot.subplot(2,1,1)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Aluminium as a function of the Number of Simulated Particles')
pyplot.plot(particles,Aluminium,'g',label="Aluminium")
pyplot.plot(particles,Aluminium,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.errorbar(particles,Aluminium,AluminiumError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.grid(True)
pyplot.subplot(2,1,2)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of the Number of Simulated Particles')
pyplot.plot(particles,AluminiumError,'g',label="Aluminium")
pyplot.plot(particles,AluminiumError,"ko")
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.grid(True)
pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.35)
pyplot.show()

pyplot.subplot(2,1,1)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Dose(mSv)')
pyplot.title('Dose received by Blood and A150 Phantoms as a function of the Number of Simulated Particles')
pyplot.plot(particles,Blood,'r',label="Blood Phantom")
pyplot.plot(particles,Blood,'ko')
pyplot.plot(particles,A150,'b',label="A150 Phantom")
pyplot.plot(particles,A150,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.errorbar(particles,Blood,BloodError,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.errorbar(particles,A150,A150Error,fmt="none",ecolor="k",linewidth=1, capsize=2)
pyplot.grid(True)
pyplot.subplot(2,1,2)
pyplot.xlabel('Number of Particles')
pyplot.ylabel('Error on Dose(mSv)')
pyplot.title('Dose Error as a function of the Number of Simulated Particles')
pyplot.plot(particles,BloodError,'r',label="Blood Phantom")
pyplot.plot(particles,BloodError,'ko')
pyplot.plot(particles,A150Error,'b',label="A150 Phantom")
pyplot.plot(particles,A150Error,'ko')
pyplot.legend(loc="upper left")
pyplot.xscale('log')
#pyplot.yscale('log')
pyplot.xticks(particles, particles_sci)
pyplot.grid(True)
pyplot.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,
                    wspace=0.35)
pyplot.show()
'''
