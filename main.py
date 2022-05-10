import sys
import numpy as np
import cv2 as cv
import argparse

colours = [0, 0, 0]
colours_hsv = [0, 0, 0]

colour_r = 0
colour_g = 0
colour_b = 0

lower_red_first = np.array([0, 80, 50])
upper_red_first = np.array([10, 255, 255])
lower_red_second = np.array([170, 80, 50])
upper_red_second = np.array([180, 255, 255])

lower_blue = np.array([90, 50, 70])
upper_blue = np.array([128, 255, 255])

lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])

lower_yellow = np.array([20, 50, 70])
upper_yellow = np.array([35, 255, 255])

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_video", help="path to the (optional) video file")
args = vars(ap.parse_args())


def main():
    global colours, colours_hsv

    if not args.get("input_video", False):
        video = cv.VideoCapture(0)
    else:
        video = cv.VideoCapture(args["input_video"])

    video = cv.VideoCapture('C:\\Users\\szymo\\Desktop\\MWR\\rgb_ball_720.mp4')

    if video.isOpened() == False:
        print('Error opening video')
        sys.exit()

    while video.isOpened():
        # Capture frame-by-frame
        _, frame = video.read()

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('p'):
            cv.waitKey(-1)

        red_mask = hsv_red(frame)
        blue_mask = hsv(frame, lower_blue, upper_blue)
        green_mask = hsv(frame, lower_green, upper_green)
        yellow_mask = hsv(frame, lower_yellow, upper_yellow)

        mask = red_mask + blue_mask + green_mask + yellow_mask

        # Bitwise-AND mask and original image
        res = cv.bitwise_and(frame, frame, mask=mask)

        cv.setMouseCallback('frame', on_mouse_click, frame)

        if np.array_equal(np.greater(colours_hsv, lower_red_first), np.less(colours_hsv, upper_red_first)):
            contour(mask=red_mask, frame=frame)

        if np.array_equal(np.greater(colours_hsv, lower_green), np.less(colours_hsv, upper_green)):
            contour(mask=green_mask, frame=frame)

        if np.array_equal(np.greater(colours_hsv, lower_blue), np.less(colours_hsv, upper_blue)):
            contour(mask=blue_mask, frame=frame)

        if np.array_equal(np.greater(colours_hsv, lower_yellow), np.less(colours_hsv, upper_yellow)):
            contour(mask=yellow_mask, frame=frame)

        cv.imshow('frame', frame)
        # cv.imshow('mask', mask)
        # cv.imshow('res', res)

    video.release()
    cv.destroyAllWindows()


def on_mouse_click(event, x, y, flags, frame):
    global colours, colours_hsv, colour_r, colour_b, colour_g
    if event == cv.EVENT_LBUTTONDOWN:
        colours = cv.COLOR_BGR2RGB
        colour_r = int(frame[y, x, 0])
        colour_g = int(frame[y, x, 1])
        colour_b = int(frame[y, x, 2])
        colours = frame[y, x]
        # print(colours)
        # print("r ", colour_r, " g ", colour_g, " b ", colour_b)
        # print("BGR colours ", colours)
        colours_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        print("HSV colours ", colours_hsv[y, x])
        colours_hsv = colours_hsv[y, x]


def contour(mask, frame):
    global colour_r, colour_b, colour_g
    # Creating contour to track red color
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for pic, _contour in enumerate(contours):
        area = cv.contourArea(_contour)
        if (area > 100):
            x, y, w, h = cv.boundingRect(_contour)
            frame = cv.rectangle(frame, (x, y), (x + w, y + h), (colour_r, colour_g, colour_b), 2)


def hsv_red(frame):
    global lower_red_first, upper_red_first, lower_red_second, upper_red_second
    # Convert BGR to HSV
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Threshold the HSV image to get only red colors
    mask1 = cv.inRange(hsv_frame, lower_red_first, upper_red_first)
    mask2 = cv.inRange(hsv_frame, lower_red_second, upper_red_second)
    mask = mask1 + mask2

    return mask


def hsv(frame, lower, upper):
    global lower_green, upper_green
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv_frame, lower, upper)

    return mask


if __name__ == '__main__':
    main()
