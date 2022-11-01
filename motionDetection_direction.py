import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
ret, frame3 = cap.read()

print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    diff2 = cv2.absdiff(frame2, frame3)
    gray2 = cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY)
    blur2 = cv2.GaussianBlur(gray2, (5,5), 0)
    _, thresh2 = cv2.threshold(blur2, 20, 255, cv2.THRESH_BINARY)
    dilated2 = cv2.dilate(thresh2, None, iterations=3)
    contours2,_ = cv2.findContours(dilated2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    itCents = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 2500:
            continue
        itCents.append((x+w/2,y+h/2))
        #cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 255, 255), 3)

    itCents2 = []
    for contour in contours2:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 2500:
            continue
        itCents2.append((x+w/2,y+h/2))
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 3)

    if len(itCents)>0 and len(itCents2)>0:
        print("000000000000000000000",itCents[0][1])
        print("111111111111111111111",itCents2[0][1])
        if itCents2[0][1] - itCents[0][1] > 0:
            print("down")
            cv2.putText(frame1, 'Downwards', (int(itCents[0][0]), int(itCents[0][1])), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 3)
        else:
            print("up")
            cv2.putText(frame1, 'Upwards', (int(itCents[0][0]), int(itCents[0][1])), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 3)

    image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    frame2 = frame3
    ret, frame3 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
