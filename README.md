import cv2

src = cv2.imread("./sample.jpg")
dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=350, param2=40, minRadius=20, maxRadius=100)

for circle in circles [0] :
  x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
  cv2.circle(dst, (x, y), r, (255, 255, 255), 5)

cv2.imshow("Detected Circles", dst)
cv2.waitKey(0)
cv2.destrovAllWindows ()
