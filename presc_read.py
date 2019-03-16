
#importing the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import json



def parse_func(text):
	"""
	:param text:
	:return:
	"""
	drug_dictionary = {}
	drug_details = []
	# splitting doctor's , patient's info and prescription.
	text_split = re.split('Rx',text)
	non_prescription = text_split[0]
	prescription = text_split[1]
	# first string has Doctor and patient's info
	print(" First string is", non_prescription)
	# second string has Doctor's prescription

	print(" Second string is",prescription)

	# splitting doctor's and patient's information present in text_split[0]
	doc_patient_split = re.split("(?:Mr\.|Mrs\.)+ [a-zA-Z]+", text_split[0])
	patient_name = re.findall("(?:Mr\.|Mrs\.)+ [a-zA-Z]+", text_split[0])
	doctor_details = doc_patient_split[0]
	# printing the patient's and doctor's separate

	print("doctor's info",doctor_details)

	print ("patient's info",patient_name)

	# Splitting the medicines, dosage and number of days
	drug_lines = re.split("\n",prescription)
	#srtip off the leading and trailing white spaces

	for line in drug_lines:
		if line != '':
			drug_info = line.strip()
			print(drug_info)
			drug = re.search(r'^([a-zA-Z]+\s*[a-zA-Z]*\s*[a-zA-Z]*)',drug_info)
			drug_dictionary['drug_name'] = drug.group()

			dosage = re.search('[0-9]+(\.[0-9]*)?(\s*)?(MG|ML|mg|ml)', drug_info)
			drug_dictionary['dosage'] = dosage.group()

			times = re.search('\d-\d-\d',drug_info)
			drug_dictionary['times']=times.group()
			times_temp = times.group()

			for i in range(3):
				a = re.search('^\d',times_temp).group()
				#print(a)
				b = re.search('\d$',times_temp).group()
				#print(b)
				c = re.search('-\d-',times_temp).group()
				d = re.search('\d',c).group()
				#print(d)
			print(times_temp)

			total_times = int(a)+int(b)+int(d)
			drug_dictionary['total_times'] = total_times

			count_of_days = re.search('\d+ (Days|days)',drug_info).group()
			drug_dictionary['count_of_days']=count_of_days


			num_in_count_of_days =re.search('\d+',count_of_days).group()
			drug_dictionary['num_in_count_of_days'] = num_in_count_of_days

			count_of_tablets = total_times * int(num_in_count_of_days)
			drug_dictionary['count'] = count_of_tablets


			#print(drug_dictionary)
			#print('appending it to list')
			drug_details.append(drug_dictionary.copy())
			#print('appended it to list')
			#print('list is', drug_details)
			#drug_info = re.split('^([a-zA-Z]+)',drug_info)
	#print(drug_dictionary)
	print(drug_details)
	json_value = json.dumps(drug_details)



# constructing the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
						 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)


# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
#print("The text is ", text)

parse_func(text)

# show the output images

#cv2.imshow("Image", image)
#cv2.imshow("Output", gray)
#cv2.waitKey(0)




