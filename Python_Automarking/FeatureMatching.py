import numpy as np
import cv2
from matplotlib import pyplot as plot

MinimumMatchCount = 10

def keyPointFinderORB(image):
	"Finds key points based on an input image using ORB feature detection"
	image = cv2.imread(image,0)
	orb = cv2.ORB_create()
	keyPoints = orb.detect(image,None)
	keyPoints, descriptors = orb.compute(image,keyPoints)
	output = cv2.drawKeypoints(image, keyPoints, None, color=(0,255,0), flags=0)
	plot.imshow(output), plot.show()
	return keyPoints, descriptors

def keyPointFinderSIFT(image):
	image = cv2.imread(image,0)
	sift = cv2.SIFT()
	keyPoints, descriptors = sift.detectAndCompute(image,None)
	output = cv2.drawKeypoints(image, keyPoints, None, color=(0,255,0), flags=0)
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
	outputImage = cv2.drawMatches(inputImage,inputKeyPoints,comparisonImage,comparisonKeyPoints,matches[:10], flags=2)
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
	good = []
	for m,n in matches:
    	if m.distance < 0.7*n.distance:
        	good.append(m)
        	
    if len(good)>MinimumMatchCount:
    	if len(good)>MIN_MATCH_COUNT:
		    src_pts = np.float32([ inputKeyPoints[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
		    dst_pts = np.float32([ comparisonKeyPoints[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
		    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
		    matchesMask = mask.ravel().tolist()
		    h,w,d = inputImage.shape
		    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
		    dst = cv2.perspectiveTransform(pts,M)
		    outputImage = cv2.polylines(outputImage,[np.int32(dst)],True,255,3, cv2.LINE_AA)
		else:
		    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
		    matchesMask = None
		draw_params = dict(
					matchColor = (0,255,0), # draw matches in green color
            		singlePointColor = None,
            		matchesMask = matchesMask, # draw only inliers
            		flags = 2)

	outputImage = cv2.drawMatchesKnn(inputImage,inputKeyPoints,outputImage,comparisonKeyPoints,good,None,**draw_params)
	plot.imshow(outputImage, 'gray'),plot.show()