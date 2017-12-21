import cv2
import imutils
import numpy as np


def disease(filename):
    image = cv2.imread(filename)
    ratio = image.shape[0] / 300.0
    orig = image.copy()

    image = imutils.resize(image, height=300)
    orig = image.copy()

    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3
    ret, label, center = cv2.kmeans(Z, K, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))

    # cv2.imshow('res2', res2)

    image = res2.copy()


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bilateralFilter(image, 11, 15, 17)
    edged = cv2.Canny(gray, 30, 200)
    # cv2.imshow("grayed", gray)

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # edged = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    circle = 0
    square = 0
    square_countour_list = []
    countour_list = []

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        area = cv2.contourArea(c)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if(len(approx) > 8 and (area > 5)):
            circle += 1
            countour_list.append(c)
        elif (area > 10):
            square += 1
            square_countour_list.append(c)

    print circle
    print square
    if square >= circle:
        return "square disease"
    else:
        return "circular disease"

    # cv2.drawContours(orig, square_countour_list, -1, (0, 255, 0), 3)
    # cv2.drawContours(orig, countour_list, -1, (255, 0, 0), 3)
    # cv2.imshow('objects detected', orig)
    # cv2.waitKey(0)
