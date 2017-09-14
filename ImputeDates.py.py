## REWRITE THIS CODE NEATLY USING FUNCTIONS TO HANDLES SOME TASKS######################
#																					  #
#																					  #
#######################################################################################
# 1. 	Write a function to read the data file into a pandas dataframe
# 2. 	Write another function that will take in the first and last date in the DATE and generate date range and store the date range in a list
# 3. 	Write another function that will compare the date entries in the original data file with the date range list  and keep the difference as the missing dates in a list.
# 4. 	Then generate a new dataframe from the missing_dates list and concatenate it with the original dataframe s 	


import pandas as pd
import numpy as np
import sys
######IDEA
# Get the dates not in the df['DATE'] then convert that list into dataframe and concantebnate with df and the sort
#
#
#

def makeDateRange(start, end):

	start_date = str(start)
	start_year = start_date[:4]
	start_month = start_date[4:6]
	start_day = start_date[6:]
	end_date = str(end)
	end_year = end_date[:4]
	end_month = end_date[4:6]
	end_day = end_date[6:]

	start_d = "/".join([start_year, start_month, start_day])
	end_d = "/".join([end_year, end_month, end_day])


	date_series = pd.date_range(start=start_d,  end=end_d)

	date_series = date_series.normalize()

	return date_series

def makeDateRangeList(date_series):

	date_s = []
	for i in date_series:		
		i = str(i).replace(r'-', '').replace(r' 00:00:00', '')
		i = int(i)		
		date_s.append(i) 
	return date_s	


def findMissingDates(date_s, dates_in_file):


	# convert date_s to a set
	date_s_set = set(date_s)
	# convert  df['DATE'] to a set

	df_date_set = set(dates_in_file)


	df_date_set = set(df['DATE'])

	missing_dates = date_s_set.difference(df_date_set)
	#print max(missing_dates)
	#print max(df_date_set)
	#print max(date_s_set)
	missing_dates = list(missing_dates)

	return missing_dates

def makeMisssingDatesDataFrame(missing_dates, stationValue, stationName):

	station = [stationValue for i in range(len(missing_dates))]
	station_name = [stationName for i in range(len(missing_dates))]

	prcp = list(np.zeros(len(missing_dates)))
	snwd = list(np.zeros(len(missing_dates)))
	tmax = list(np.zeros(len(missing_dates)))
	tmin = list(np.zeros(len(missing_dates)))

	df2 = pd.DataFrame({'STATION': station, 'STATION_NAME': station_name, 'DATE': missing_dates, 'PRCP': prcp, 'SNWD': snwd, 'TMAX': tmax, 'TMIN': tmin})
	# reorder the column of the new df to look like the original data
	df2 = df2[['STATION', 'STATION_NAME', 'DATE', 'PRCP', 'SNWD', 'TMAX', 'TMIN']]

	return df2

if __name__ == '__main__':

	path = sys.argv[1]

	

	df = pd.read_csv(path)
	start_date = df.ix[0, 'DATE'] # gets the first date from the file
	end_date =  df.ix[df.index[-1], 'DATE'] # gets the last date from the file
	dates = df['DATE']	
	station_value = df.ix[0,'STATION']
	station_name_value = df.ix[0, 'STATION_NAME']

	

	#startDate, endDate, datesInfile = readFile(path)

	dateSeries = makeDateRange(start_date, end_date)

	dateList = makeDateRangeList(dateSeries)

	missingDates = findMissingDates(dateList, dates )
	df2 = makeMisssingDatesDataFrame(missingDates, station_value, station_name_value )


	new_df = pd.concat([df, df2])

	new_df = new_df.sort_values('DATE')

	new_df = new_df.replace(-9999, " ")
	new_df['PRCP'] = new_df['PRCP'].replace(0, " ")
	
	#print new_df
	new_df.to_csv("1004462-new.csv", encoding='ascii')		

	print "Done !"	

