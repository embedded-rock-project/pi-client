import cv2
import numpy as np
import time
import pandas
from datetime import datetime

class UseCamera:
    def Surveillance(self):
        print('Loading Camera Feed...')
        cam = cv2.VideoCapture(0)#, cv2.CAP_DSHOW)
        firstFrame=cam.read()
        cv2.imshow("frame", firstFrame)
        firstFrameGray =cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
        firstFrameGrayBlur = cv2.GaussianBlur(firstFrameGray, (21,21),0)
        while True:
            Frame = cam.read() #[1]
            FrameGray=cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
            FrameGrayBlur= cv2.GaussianBlur(FrameGray, (21,21),0)

            cv2.imshow('Cam Feed', FrameGrayBlur)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        cv2.destroyAllWindows()
        cam.release()

    def ShowFeed(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 420)

        # import cascade file for facial recognition
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while True:
            success, img = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Getting corners around the face
            faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)  # 1.3 = scale factor, 5 = minimum neighbor
            # drawing bounding box around face
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            cv2.imshow('face_detect', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyWindow('face_detect')

    def MotionBlur(self):
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

            time.sleep(0.015)

            if key == ord('s'):
                break

        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    UseCamera().Surveillance()



# import cv2

# class Camera:
#     def __init__(self):
#         self.FirstFrameGray = None
#         self.FirstFrame = None
#         self.Frame = None
#         self.Cam = None

        
#     def Surveillance(self):
#         print('Loading Camera Feed...')
#         self.Cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#         self.FirstFrame=self.Cam.read()[1]
#         #self.FirstFrameGray =cv2.cvtColor(self.FirstFrame, cv2.COLOR_BGR2GRAY)
#         self.FirstFrameGrayBlur = cv2.GaussianBlur(self.FirstFrameGray, (21,21),0)
#         while True:
#             self.Frame = self.Cam.read()[1]
#             #self.FrameGray=cv2.cvtColor(self.Frame, cv2.COLOR_BGR2GRAY)
#             self.FrameGrayBlur= cv2.GaussianBlur(self.FrameGray, (21,21),0)
            
#             cv2.imshow('Cam Feed', self.FrameGrayBlur)
#             if cv2.waitKey(1) == 27: 
#                 break  # esc to quit
#         cv2.destroyAllWindows()
#         self.Cam.release()
#     def ShowFeed(self):
#         self.Cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#         while True:
#             self.Frame = self.Cam.read()[1]
#             cv2.imshow('Cam Feed', self.Frame)
#             if cv2.waitKey(1) == 27: 
#                 break  # esc to quit
#         cv2.destroyAllWindows()
#         self.Cam.release()


# if(__name__=='__main__'):
#     Camera().Surveillance()

