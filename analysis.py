import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functions import *
import pandas

rawLines = []

with open('data.txt') as inputFile:
	rawLines = inputFile.readlines()

def cosScore(series1, series2):

	s1 = series1
	s2 = series2

	score = 0

	ls1 = len(series1)
	ls2 = len(series2)

	if ls1!=ls2:
		raise Exception("cosScore(): ls1!=ls2")
		return None
	else:
		score = np.dot(s1,s2)
		modS1 = np.sqrt(np.dot(s1,s1))
		modS2 = np.sqrt(np.dot(s2,s2))
		score = score / modS1
		score = score / modS2
		score *= 100
		return score


def singleAnalysis(data, field, shouldPlot=False):

	# MAKE = lambda x: int(float(x))
	MAKE = lambda x: float(x)

	targetField = np.array(map(MAKE, getField(data, field)))
	baseField = np.array(map(MAKE, getField(data, 'eyeDetection')))

	Z1 = targetField * baseField

	analysis = ((field), (np.mean(targetField)), (np.max(targetField)), (cosScore(targetField, baseField)) )
	# print field, 'mean:', np.mean(targetField)
	# print field, 'max:',np.max(targetField)
	# print field, 'cosScore:', cosScore(targetField, baseField), '%'

	if shouldPlot:

		plt.figure(1)
		plt.subplot(311)
		plt.plot(targetField)

		plt.subplot(312)
		plt.plot(Z1)

		plt.subplot(313)
		plt.plot(baseField)

		plt.show()

	return analysis


def fourierAnalysis(data, field, shouldPlot=False):

	MAKE = lambda x: float(x)
	targetField = np.array(map(MAKE, getField(data, field)))
	
	FFT = np.fft.fft(targetField)
	l = len(targetField)
	m = 1
	FFTFREQ = np.fft.fftfreq(l/m)
	
	print FFT
	print FFTFREQ

	if shouldPlot:

		plt.figure()
		plt.subplot(211)
		plt.plot(targetField)
		plt.subplot(212)
		plt.plot(FFTFREQ, FFT.real, FFTFREQ, FFT.imag)
		plt.show()


data = getData(rawLines)

analysis = []
# keys = []

for field in data['attributes']:
	if field!='eyeDetection':
		a = singleAnalysis(data, field, shouldPlot=False)
		analysis.append(a)

pandasReportColumns = ['field', 'mean', 'max', 'cos']

df = pd.DataFrame(analysis, columns = pandasReportColumns)
DF = df.sort_values('cos', ascending=False)
# df.style.apply(highlight_max, color='darkorange', axis=None)

print "Calculating cos similarity with field eyeDetection:\n"
print DF
print
print "Fourier Analysis:\n"
fourierAnalysis(data, 'FC6', shouldPlot=True)
print
print