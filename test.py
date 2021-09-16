
# # import the opencv library
import cv2
import time
  
  
# # define a video capture object
# vid = cv2.VideoCapture(0)
# # vid.set(3, 640)
# # vid.set(4, 420)

# # import cascade file for facial recognition
# faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# while(True):
      
#     # Capture the video frame
#     ret, frame = vid.read()

#     grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Getting corners around the face
#     faces = faceCascade.detectMultiScale(grayFrame, 1.3, 5)  # 1.3 = scale factor, 5 = minimum neighbor
    
#     # drawing bounding box around face
#     print(faces)
#     for (x, y, w, h) in faces:
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
#     cv2.imshow('face_detect', frame)


#     # grayFrameBlurred = cv2.GaussianBlur(grayFrame, (21,21), 0)
#     # # Display the resulting frame
#     # cv2.imshow('frame', grayFrameBlurred)
      
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()


def MotionBlur():
    camera = cv2.VideoCapture(0)

    background = None

    while True:
        grabbed, frame = camera.read()

        if not grabbed:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)

        if background is None:
            background = gray
            continue

        subtraction = cv2.absdiff(background, gray)
        threshold = cv2.threshold(subtraction, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations = 2)
        contourimg = threshold.copy()

        outlines, heirarchy = cv2.findContours(contourimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in outlines:
            if cv2.contourArea(c) < 500:
                continue

            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        cv2.imshow("Camera", frame)
        cv2.imshow("Threshold", threshold)
        cv2.imshow("Subtraction", subtraction)
        cv2.imshow("Contour", contourimg)

        key = cv2.waitKey(1) & 0xFF

        # time.sleep(0.015)

        if key == ord('s'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    MotionBlur()