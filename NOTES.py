def NOTES()
#####################################################  
# DATE AND TIME
from datetime import datetime
now=datetime.now().strftime("%d_%m_%Y,%H_%M_%S")
#>>01_10_2019,13_23_44

#####################################################
# READ CSV AND ADD TO LIST
import csv
with open("C:/test/output (1).csv","rU",encoding="utf-16") as f:       
    read=csv.reader(f, delimiter='\t',)
    for row in read:
        List.append(Class(row[1],row[2]))
        
#####################################################        
# WRITE TO NOTEPAD
file= open(name,"w+",encoding='utf8')
file.write("..........\n")
file.close()

#####################################################
#OUTLOOK MAILS
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6).Folders.Item("subfolder_name")
messages = inbox.Items
message = messages.GetLast()
for message in messages:
    print(message.ReceivedTime)
    print(message.Subject)
    
    if message.SenderEmailType == "EX":
        print(message.Sender.GetExchangeUser().PrimarySmtpAddress)
    elif message.SenderEmailType == "SMTP":
        print(message.SenderEmailAddress)
    
#####################################################        
# FIND LATEST FILE NAME
import glob
import os

list_of_files = glob.glob('C:/Users/kpapaioa/Downloads/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
             
#####################################################        
# ELAPSED TIME
import time 
start_time = time.time()
elapsed_time = time.time() - start_time

#####################################################        
# PANDAS - data
import pandas as pd
df=pd.read_csv('path/file.csv',index_col = 0) # (path, sets the first column as index)
df=pd.read_excel('path/file.xls')
df.head()#examines the rows of the data frame default:5

df={'Album':['song1','song2','song3','song4'],
       'Released':[1999,1999,1998,1997],
       'Length':[2.43,2.43,2.43,2.43]}

df=pd.DataFrame(df).set_index('Album')#creates a dataframe for songs(table), 'Album' as index//  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
df['band'] = ["b1","b2","b3","b4"] # adds new column
df['Calc'] = df['Released']*df['Length'] # does calculations
x=df[['Length','Released']]# creates a dataframe with the specified columns
x=df.loc[0,'Album']# ==(x=df.ix[0,0]) >> 'song1'
x=df.loc[0:1,'Album':'Released']# selects two rows and two columns
df.loc["song1",'Released'] # key = song1, column = released

x=df['Released'].unique()# makes "a list" with all the unique elements in column
x=df['Released']>='1999' # males a boolean list
x=df[df['Released']>='1999']# applies a filter

df.to_csv('new.csv')



#####################################################        
# NUMPY - math
import numpy as np
a=np.array([0,1,2,300,400])# creates a numpy array (index data like a list)
type(a) #>> numpy.ndarray # show the type of the array
a.dtype #>> dtype('int32') #show data type (32 bit integer)
a.size #>> 5 # shows number of elements
a.ndim #>> 1 # shows the dimensions of the array
a.shape #>> (5,) # shows the size of the array on each dimension
a[3:5]=3,4 # changes the changes the last 2 elements

        # vectors - matrixes - scalars
z=a+a # adds two numphy arrays (z=a-a, z=a+1)
z=2*a # Hadamard product of two arrays (z=a*a)
z=np.dot(a,a) # Dot product/scalar product
z=a.mean() # mean value of array
z=a.max() # max value of array (z=a.min())
z=np.pi # π function (3,14)
z=np.sin(a) # applies sin dunction to every element of array
np.linspace(-2,-2,num=5) # creates a sequence(starting point, end point, number of samples)
z=np.column_stack((a,a))


        # Jupyter Notebook - can run in spyder
import matplotlib.pyplot as plt #plot module
x=np.linspace(0,2*np.pi,100) # 100 samples from 0 to 2pi
y=np.sin(x)

        # 2D Arrays - same as 1d except:
A=np.array([[1,2],[3,4]]) # 2d array like a list
A[0,1] # >> 2 # shows value in position. A[0,:] / A[:2,0]...
A=np.dot(A,A) # np.matmul(A,A) # >> Array multiplication


np.mean(A[:,0]) # >> mean value for column 0
np.median(A[:,0]) # >> finds the values that is closer to the middle
np.corrcoef(A[0,:]) #>> correlation coefficient, deikths Pearson
np.std(A[:,0])


#####################################################        
# MATPLOTLIB - data visualization, simple lists can be plotted
import matplotlib.pyplot as plt #plot module
x=np.linspace(0,2*np.pi,100) # 100 samples from 0 to 2pi
y=np.sin(x)

plt.plot(x,y) # PLOT
plt.scatter(x,y) # SCATTERPLOT
plt.hist(x,100000) # HISTOGRAM
plt.show()
        #cosmetics
plt.xlabel('This is x') # puts a label on the plot's x axis / plt.ylabel('y') # labels y axis
plt.title('Title')
plt.yticks([-1,0,1],["-","0","+"]) # [ Defines the axis values and ticks],[we can change label for the ticks]
plt.fill_between(x,y,0,color='red') # Creates a filled/colored plot. The color is filled until 0











#####################################################        
# 
#####################################################        
# 
#####################################################        
# 
#####################################################        
# 