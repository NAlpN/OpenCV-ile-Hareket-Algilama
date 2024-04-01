import cv2

cap = cv2.VideoCapture('video.mp4')

ret, frame1 = cap.read()
ret, frame2 = cap.read()

object_count = 0
start_time = None
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3) 
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
        object_count += 1
        if start_time is None:
            start_time = cap.get(cv2.CAP_PROP_POS_MSEC)

    cv2.imshow("feed", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

end_time = cap.get(cv2.CAP_PROP_POS_MSEC)
elapsed_time = (end_time - start_time) / 1000
print("Takip Edilen Nesne Sayısı:", object_count)
print("Takip Süresi (saniye):", elapsed_time)

cv2.destroyAllWindows()
cap.release()
