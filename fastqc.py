#!/usr/bin/env python
#file name:fast_1.py
# Output:
# fig1: per base sequence quality of fastq files
# fig2: per sequence quality scores
# fig3: per base sequence content
# fig4: per sequence GC content

import numpy as np 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

fastq_file="./sample/sample1.fq" #input file
FILE=open(fastq_file,"r")
lnum = 0

for line in FILE:
    lnum += 1
    line=line.strip('\n')

    # Compute line number
    if lnum == 2:
        # initialize
        seq_length = len(line)
        bq_ls = np.zeros((seq_length,92)) # for per base sequence quality
        bq_ls2 = np.zeros((92)) # for per sequence quality scores
        lista = np.zeros((seq_length)) # initialize for per base sequence content
        listt = np.zeros((seq_length))
        listg = np.zeros((seq_length))
        listc = np.zeros((seq_length))
        listn = np.zeros((seq_length))
        gc_ls = np.zeros((150)) # initialize for per sequence GC content
        print('\033[1;31;40m'+'Sequence length: '+'\033[0m'+ str(len(line)))

    if lnum % 4 == 0:
        #print(line)
        ##### per base sequence quality
        count = 0
        bq_sum = 0
        for char in line:
            bq = ord(char) - 33 -2
            bq_ls[count][bq]+=1
            count +=1
        ##### per sequence quality scores
            bq_sum+=bq
        mean_bq = bq_sum//seq_length
        bq_ls2[mean_bq]+=1
        ##### 
    if lnum % 4 == 2:
        line.upper()
        count = 0
        gc = 0
        if len(line) != seq_length:
            print(str(lnum)+': '+line)
        ##### per base sequence content
        for char in line:
            if char == 'A':
                lista[count]+=1
            elif char == 'T':
                listt[count]+=1
            elif char == 'G':
                listg[count]+=1
            elif char == 'C':
                listc[count]+=1
            elif char == 'N':
                listn[count]+=1
            count+=1
            ##### per sequence GC content
            if char == 'G' or char == 'C':
                gc+=1
        #print(gc)
        gc_ls[gc]+=1
#print(gc)
#print(gc_ls)

            
list_sum = lista + listt + listg + listc
print('\033[1;31;40m'+'Total sequence: '+'\033[0m'+str(lnum/4))
ls = []
box_ls =[]
for i in bq_ls:
    score_sum = 0
    sub = 2
    for j in i: # len(i) == 92
        score_sum += j*sub
        sub +=1
    ls.append(score_sum*4/lnum)
    count = 0
    tem_ls = []
    ## get the median value, first quartile, third quartile, maximum, minimum, 10%, 90% value.
    for k in range(92):
        count += i[k]
        #if count <=0 and count+(i[k+1])>0:
        #    tem_ls.append(k+3)
        #if k <91 and count == count+(i[k+1]) and k>30:
        if count <= 0.1*lnum/4 and count+(i[k+1]) >= 0.1*lnum/4:
            tem_ls.append(k+3)
        if count <= 0.25*lnum/4 and count+(i[k+1]) >= 0.25*lnum/4:
            tem_ls.append(k+3)
            tem_ls.append(k+3)
        if count <= 0.5*lnum/4 and count+(i[k+1]) >= 0.5*lnum/4:
            tem_ls.append(k+3)
        if count <= 0.75*lnum/4 and count+(i[k+1]) >= 0.75*lnum/4:
            tem_ls.append(k+3)
            tem_ls.append(k+3)
        if count <= 0.9*lnum/4 and count+(i[k+1]) >= 0.9*lnum/4:
            tem_ls.append(k+3)
    box_ls.append(tem_ls)
#print(box_ls)
############################################################### Figures
############################################################### box plot: Per base sequence quality
labels=[]
for i in range(150):
    if (i+1) % 5 ==0:
        labels.append(i+1)
    else:
        labels.append('')
#print(labels)
fig, ax1 = plt.subplots(figsize=(10, 6))
fig.canvas.set_window_title('Quality Scores Across All Bases')
plt.subplots_adjust (left=0.075, right=0.95, top=0.9, bottom=0.25)

bp = plt.boxplot(box_ls, notch=0, sym='+', vert=1, whis=0.25 )
plt.setp(bp['boxes'], color='black')
plt.setp(bp['whiskers'], color='black')
plt.setp(bp['fliers'], color='red', marker='+')

# Add a horizontal grid to the plot, but make it very light in color
# so we can use it for reading data values but not be distracting
ax1.yaxis.grid(True, linestyle='-', which ='major', color='lightgrey', alpha=0.5)
ax1.xaxis.grid(True, linestyle='-', which = 'major', color='grey', alpha=0.2)

# Hide these grid behind plot objects
ax1.set_axisbelow('True')
ax1. set_title('Quality scores across all bases')
ax1.set_xlabel('Position in read (bp)')
ax1.set_ylabel('Phred Score')

# Now fill the boxes with desired colors
boxColors = ['darkkhaki']

# Set the axes ranges and axes labels
ax1.set_xlim(1, seq_length)
ax1.set_ylim(0, 50)
xtickNames = plt.setp(ax1, xticklabels=labels)#range(1,seq_length+1))
#ytickNames = plt.setp(ax1, yticklabels=range(1,50))
#plt.setp(ytickNames, fontsize = 8)
plt.setp(xtickNames, rotation=15, fontsize=8)

# The following is the mean base quality curve line
#print('ls length: '+str(len(ls)))
x = np.linspace(1,seq_length, seq_length)
y = ls
#plt.title('Quality Scores Across All Bases', size = 14)
#plt.xlabel('Position in read (bp)', size = 14)
#plt.ylabel('Base Quality', size = 14)
plt.plot(x, y, color = 'b', linestyle = '-', label = 'Mean Quality')
#plt.axis([1, seq_length, 0, 50])

plt.legend(loc = 'upper right')
plt.savefig('1_QualityScoresAcrossAllBases.jpg', format='jpg')

################################################################################ Plot for Per sequence quality scores
x2 = np.linspace(1,50, 50)
y2 = (bq_ls2+2)[:50]
fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.yaxis.grid(True, linestyle='-', which ='major', color='lightgrey', alpha=0.5)
ax2.set_axisbelow('True')
ax2. set_title('Quality scores distribution over all sequences')
ax2.set_xlabel('Mean Sequence Quality (Phred Score)')
ax2.set_ylabel('Read Number')
plt.plot(x2, y2, linestyle = '-', label = 'Average Quality per read')
plt.legend(loc = 'upper left')
plt.savefig('./output/2_QualityScoreDistributionOverAllSequences.jpg', format='jpg')
################################################################################# Plot for per base sequence content
x3 = np.linspace(1, seq_length, seq_length)
list_sum = lista + listt + listg + listc
fig3, ax3 = plt.subplots(figsize=(10,6))
#ax3.yaxis.grid(True, linestyle='-', which ='major', color='lightgrey', alpha=0.5)
ax3.grid(True, linestyle='-', which ='both', color='lightgrey')
ax3.grid(which='minor', alpha=0.2)
ax3.grid(which='major',alpha=0.5)
ax3.set_axisbelow('True')
ax3. set_title('Sequence content across all bases')
ax3.set_xlabel('Position in read (bp)')
ax3.set_xlim(1,seq_length)
ax3.set_ylim(0,100)
#ax3.set_ylabel('Read Number')
plt.plot(x3, 100*lista/list_sum, linestyle = '-', label = '%A')
plt.plot(x3, 100*listt/list_sum, linestyle = '-', label = '%T')
plt.plot(x3, 100*listg/list_sum, linestyle = '-', label = '%G')
plt.plot(x3, 100*listc/list_sum, linestyle = '-', label = '%C')
plt.plot(x3, 100*listn/list_sum, linestyle = '-', label = '%N')
plt.legend(loc = 'upper right')
plt.savefig('./output/3_SequenceContentAcrossAllBases.jpg',format='jpg')
################################################################################ Plot for per sequence GC content
x4 = [] #np.linspace(1,100, 100)
y4 = []
e = 0
read_sum=0
for i in range(seq_length):
    x4.append(100.0*e/seq_length)
    y4.append(gc_ls[e])
    read_sum+=gc_ls[e]
    e+=1
fig4, ax4 = plt.subplots(figsize=(10,6))
ax4.yaxis.grid(True, linestyle='-', which ='major', color='lightgrey', alpha=0.5)
ax4.set_axisbelow('True')
ax4. set_title('GC distribution over all sequences')
ax4.set_xlabel('Mean GC content (%)')
ax4.set_ylabel('Read Number')
ax4.set_xlim(0,100)
plt.plot(x4, y4, linestyle = '-', label = 'GC count per read')
plt.legend(loc = 'upper right')
plt.savefig('./output/4_GCdistributionOverAllSequences.jpg',format='jpg')

