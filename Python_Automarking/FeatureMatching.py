import numpy as np
import cv2
from matplotlib import pyplot as plot

def keyPointFinderORB(image):
	"Finds key points based on an input image using ORB feature detection"
	image = cv2.imread(image,0)
	orb = cv2.ORB_create()
	keyPoints = orb.detect(image,None)
	keyPoints, descriptors = orb.compute(image,keyPoints)
	output = cv.drawKeypoints(image, keyPoints, None, color=(0,255,0), flags=0)
	plot.imshow(output), plot.show()
	return keyPoints, descriptors

def keyPointFinderSIFT(image):
	image = cv2.imread(image,0)
	sift = cv2.SIFT()
	keyPoints, descriptors = sift.detectAndCompute(image,None)
	output = cv.drawKeypoints(image, keyPoints, None, color=(0,255,0), flags=0)
	plot.imshow(output), plot.show()
	return keyPoints, descriptors

def bruteForceMatcher(inputImage,comparisonImage):
	"Uses the brute force matcher on two ORB keypoint maps"

	#Get keypoints and descriptors of both images
	inputKeyPoints, inputDescriptors = keyPointFinderORB(inputImage)
	comparisonKeyPoints, comparisonDescriptors = keyPointFinderORB(comparisonImage)

	#Create Matcher
	bfMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = bfMatcher.match(inputDescriptors,comparisonDescriptors)
	matches = sorted(matches, key = lambda x:x.distance)
	# Draw first 10 matches.
	outputImage = cv.drawMatches(inputImage,inputKeyPoints,comparisonImage,comparisonKeyPoints,matches[:10], flags=2)
	plot.imshow(outputImage),plot.show()
	return matches.distance

def FLANNMatcher(inputImage,comparisonImage):
	inputKeyPoints, inputDescriptors = keyPointFinderSIFT(inputImage)
	comparisonKeyPoints, comparisonDescriptors = keyPointFinderSIFT(comparisonImage)

	#FLANN parameters
	FLANN_INDEX_KDTREE = 1
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)

	flann = cv2.FlannBasedMatcher(index_params,search_params)

	matches = flann.knnMatch(inputDescriptors,comparisonDescriptors,k=2)
	matchesMask = [[0,0] for i in xrange(len(matches))]
	for i,(m,n) in enumerate(matches):
		if m.distance < 0.7*n.distance:
			matchesMask[i]=[1,0]

	draw_params = dict(
					matchColor = (0,255,0),
               		singlePointColor = (255,0,0),
                   	matchesMask = matchesMask,
                   	flags = 0)
	outputImage = cv2.drawMatchesKnn(inputImage,inputKeyPoints,outputImage,comparisonKeyPoints,matches,None,**draw_params)
	plot.imshow(outputImage),plot.show()