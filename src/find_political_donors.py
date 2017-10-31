##### Functions #####

### Function 1: The function to calculate the median value
def median(list):
    sorted_list = sorted(list)
    length = len(sorted_list)
    c = length // 2
    if length == 1:
        return sorted_list[0]
    elif length % 2 == 0:
        return sum(sorted_list[c - 1: c + 1]) / 2.0
    else:
        return sorted_list[c]

### Function 2: Calculate the zip code values
def medianvals_zipcode(ID):
	if ID not in zipcode_ID:
		zipcode_ID.append(ID)
		zipcode_count.append(1)
		zipcode_amount.append(int(split_data[14]))
		zipcode_all.append([int(split_data[14])])
		count = 1
		amount = split_data[14]
		median_value = split_data[14]
	else:
		index = zipcode_ID.index(ID)
		count = zipcode_count[index] + 1
		amount = int(zipcode_amount[index]) + int(split_data[14])
		zipcode_count[index] = count
		zipcode_amount[index] = amount
		zipcode_all[index].append(int(split_data[14]))
		median_value = median(zipcode_all[index])
	result_temp = "|".join([customer_ID, zipcode, str(round(int(median_value))), str(count), str(amount)])
	return result_temp

### Function 3: Calculate the date value
def medianvals_date(ID):
	if ID not in acc_list_date_ID:
		acc_list_date_ID.append(ID)
		result_temp = [customer_ID, date, [int(split_data[14])], 1, int(split_data[14])]
		result_date.append(result_temp)
	else:
		index = acc_list_date_ID.index(ID)
		result_date[index][2].append(int(split_data[14]))
		result_date[index][3] += 1
		result_date[index][4] += int(split_data[14])

### Function 4: Check whether the date format is valid
def valid_date(date_input):
	if date_input.isdigit() == False:
		return False
	if len(date_input) != 8:
		return False
	if int(date_input[0:2]) <= 0 or int(date_input[0:2]) >= 13:
		return False
	if int(date_input[2:4]) <= 0 or int(date_input[2:4]) >= 32:
		return False
	else:
		return True 

### Function 6: Check whether the zipcode format is valid
def valid_zipcode(zip_input): # check for zipcode
    if len(zip_input) > 4 and len(zip_input) < 10:
        return True
    else:
        return False

### Function 7: Rank the data for the re-order in the date file
def rank(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)

##### Main Process to calculate the data ######
if __name__ == '__main__': 
	zipcode_ID = []
	zipcode_count = []
	zipcode_amount = []
	zipcode_all = []
	acc_list_date = [[],[],[],[],[]]
	acc_list_date_ID = []
	acc_list_date_median = []
	result_zipcode = []
	result_date = []

	# Read the raw data into the python line by line, save the memory
	print("Calculating the value for the zipcode and date... ", end = "")
	with open('./input/itcont.txt') as f:
		for line in f:
			split_data = line.split('|')
			if split_data[15] != "" or split_data[0] == "" or split_data[14] == "":
				continue
			customer_ID = split_data[0]
			zipcode = split_data[10]
			date = split_data[13]
			transaction_amount = split_data[14]
			if valid_zipcode(zipcode):
				zipcode = zipcode[:5]
				if len(zipcode) == 5:
					ID = customer_ID + " " + zipcode
					result_zipcode.append(medianvals_zipcode(ID))
			if valid_date(date): 
				ID = customer_ID + " " + date
				medianvals_date(ID)
	print("Done!")
	
	# Clean, reorder the date results
	print("Cleaning the date results... ", end = "")
	for i in range(len(result_date)):
		result_date[i][2] = str(round(median(result_date[i][2])))
		result_date[i][3] = str(result_date[i][3])
		result_date[i][4] = str(result_date[i][4])
	sorted_ID = [i[0][1:] + i[1][4:8] + i[1][0:2] + i[1][2:4] for i in result_date] # Reorder the date in the approciate order
	ranked_ID = rank(sorted_ID)
	result_date = [result_date[i] for i in ranked_ID] # Change the order of the result
	result_date = list(map(lambda x: "|".join(x), result_date))
	print("Done!")

	# Write the data into the output folder
	print("Writing the zipcode results... ", end = "")
	with open("./output/medianvals_by_zip.txt", "w") as output_zip:
		for i in result_zipcode:
			output_zip.write(i + "\n")
		output_zip.close()
	print("Done!")
	print("Writing the date results... ", end = "")
	with open("./output/medianvals_by_date.txt", "w") as output_date:
		for i in result_date:
			output_date.write(i + "\n")
		output_date.close()
	print("Done!")
	print("Finish!")
