import numpy as np


def QualifiedCondition(condition, **kwargs):
	qualify = {'CenterPassLevel': [False, kwargs['centerMaxGray']],
	           'ULPassLevel': [False, round(100 * kwargs['UL_gray'] / kwargs['centerMaxGray'], 3)],
	           'URPassLevel': [False, round(100 * kwargs['UR_gray'] / kwargs['centerMaxGray'], 3)],
	           'LLPassLevel': [False, round(100 * kwargs['LL_gray'] / kwargs['centerMaxGray'], 3)],
	           'LRPassLevel': [False, round(100 * kwargs['LR_gray'] / kwargs['centerMaxGray'], 3)],
	           'Diff': [False,
	                    max(kwargs['UL_gray'], kwargs['UR_gray'], kwargs['LL_gray'], kwargs['LR_gray']) -
	                    min(kwargs['UL_gray'], kwargs['UR_gray'], kwargs['LL_gray'], kwargs['LR_gray'])]
	           }
	# Center
	if condition['centerLow'] <= qualify['CenterPassLevel'][1] <= condition['centerUp']:
		qualify['CenterPassLevel'][0] = True

	# Corner
	if condition['passLow'] <= qualify['ULPassLevel'][1] <= condition['passUp']:
		qualify['ULPassLevel'][0] = True
	if condition['passLow'] <= qualify['URPassLevel'][1] <= condition['passUp']:
		qualify['URPassLevel'][0] = True
	if condition['passLow'] <= qualify['LLPassLevel'][1] <= condition['passUp']:
		qualify['LLPassLevel'][0] = True
	if condition['passLow'] <= qualify['LRPassLevel'][1] <= condition['passUp']:
		qualify['LRPassLevel'][0] = True

	# Diff
	if 0 <= qualify['Diff'][1] <= condition['diff']:
		qualify['Diff'][0] = True

	return qualify


def AverageGray(img):
	"""

	:param img: BGR Image
	:return: Average gray value
	"""
	b_scale = 0.114
	g_scale = 0.587
	r_scale = 0.299

	scale = np.array([[b_scale],
	                  [g_scale],
	                  [r_scale]])
	ave_gray = float(np.mean(img.dot(scale)))
	return round(ave_gray, 4)


def CornerImage(img, ROI_size):
	"""
	Get four corner images.
	Upper Left, Upper Right, Lower Left, Lower Right

	:param img: The target image
	:param img_shape: The shape of the image. (h, w, c = bgr)
	:param ROI_size: ROI size for four corner. It should be proportion of pixel. (len_h, len_w)
	:return: four corner images
	"""
	img_shape = img.shape
	H = int(ROI_size[0] * img_shape[0])
	W = int(ROI_size[1] * img_shape[1])

	nextH = img_shape[0] - H
	nextW = img_shape[1] - W

	UL_img = img[0:H, 0:W]
	UR_img = img[0:H, nextW:img_shape[1]]
	LL_img = img[nextH:img_shape[0], 0:W]
	LR_img = img[nextH:img_shape[0], nextW:img_shape[1]]

	return UL_img, UR_img, LL_img, LR_img


def CenterGrayValue(img, partition, ROI_size):
	"""
	Calculate the largest gray value in the center region.
	:param img: The target image
	:param partition: The region would be examined. Defined it by propotion of h, w.
	:param ROI_size: ROI size for center region. It should be proportion of pixel. (len_h, len_w)
	:return:
	"""
	maxgray = 0.0

	startH = int((1 / 2 - 1 / (2 * partition)) * img.shape[0])
	startW = int((1 / 2 - 1 / (2 * partition)) * img.shape[1])
	endH = int((1 / 2 + 1 / (2 * partition)) * img.shape[0])
	endW = int((1 / 2 + 1 / (2 * partition)) * img.shape[1])

	roiH = int(ROI_size[0] * img.shape[0])
	roiW = int(ROI_size[1] * img.shape[1])

	loopH = endH - startH - roiH
	loopW = endW - startW - roiW

	for h in range(startH, startH + loopH):
		for w in range(startW, startW + loopW):
			gray = AverageGray(img[h:h + roiH, w:w + roiW])
			if maxgray <= gray:
				maxgray = gray
				maxgray_img = img[h:h + roiH, w:w + roiW]

	return maxgray