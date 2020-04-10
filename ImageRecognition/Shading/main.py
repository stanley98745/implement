from shadingdetect import CornerImage, AverageGray, CenterGrayValue
from shadingdetect import QualifiedCondition as QC
import numpy as np
import cv2


if __name__ == '__main__':
	# parameters
	input_file = '19271_en_1.jpg'
	partition_n = 2
	ROI = (1/10, 1/10)
	qualifiedCondition = {'centerUp': 220, 'centerLow': 100,
	                      'passUp': 120, 'passLow': 70,
	                      'diff': 20}

	image = cv2.imread(input_file)

	UL_image, UR_image, LL_image, LR_image = CornerImage(image, ROI)

	# Convert RGB images at corner to gray scale.
	# Calculate average gray value.
	UL_gray = AverageGray(UL_image)
	UR_gray = AverageGray(UR_image)
	LL_gray = AverageGray(LL_image)
	LR_gray = AverageGray(LR_image)

	# Find Max Y value in Center image
	centerMaxGray = CenterGrayValue(image, partition_n, ROI)

	# Qualified Condition
	# 1. centerUp <= Center average gray value <= centerLow
	# 2. PassUp <= Gray value at corners (percentage) <= PassLow
	# 3. The difference between maximum and minimum gray values at corner
	#    should be less than or equal to 20.
	qc = QC(qualifiedCondition, centerMaxGray=centerMaxGray,
	        UL_gray=UL_gray, UR_gray=UR_gray, LL_gray=LL_gray, LR_gray=LR_gray)

	for key, value in qc.items():
		if value[0] is False:
			print(f'Failed!! {key} testing! It value is {value[1]}')

	for key, value in qc.items():
		if value[0] is True:
			print(f'{key} testing is passed! It value is {value[1]}')

	# Show the picture
	# cv2.namedWindow('MyImage', cv2.WINDOW_NORMAL)

	# cv2.imshow('MyImage', image)
	# cv2.imshow('UpperLeft', UL_image)
	# cv2.imshow('UpperRight', UR_image)
	# cv2.imshow('LowerLeft', LL_image)
	# cv2.imshow('LowerRight', LR_image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
