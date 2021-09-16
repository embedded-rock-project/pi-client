
# import the opencv library
import cv2
import asyncio
from typing import Optional
from http_reqs import defaultMaker



class Camera:
    def __init__(self, camera_mode_choice: int, camera: int = 0, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.shutdown = False
        self.enabled = False
        self.camera = camera
        self.vid = cv2.VideoCapture(self.camera)
        self.cv2Cascades = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.camera_mode_choice = camera_mode_choice
        self.camera_modes = [self.standard_survelliance, self.facial_recognition, self.motion_blur]
        self.event_task = None
        self.sensor_event = None
        self.loop = loop if loop else asyncio.get_event_loop()
        self._await = self.loop.run_until_complete
        self._nowait = self.loop.create_task


    def __enter__(self):
        self.enabled = True
        self.event_task = self.loop.run_in_executor(None, self.camera_modes[self.camera_mode_choice])


    def __exit__(self, exc_type, exc_value, traceback):
        self.enabled = False
        self.shutdown = True
        self.event_task.cancel()
        self.vid.release()
        cv2.destroyAllWindows()


    def standard_survelliance(self):
        print('Loading Camera Feed...')
        while True:
            ret, frame = self.vid.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray_blur = cv2.GaussianBlur(frame_gray, (21,21),0)
            cv2.imshow('Cam Feed', frame_gray_blur)
            if cv2.waitKey(1) == 27:
                break  # esc to quit




    def facial_recognition(self):
        detect_faces = False
        offset = 0
        while self.enabled:
            ret, frame = self.vid.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.cv2Cascades.detectMultiScale(gray_frame, 1.3, 5)
            for (x, y, w, h) in faces:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.imshow('face_detect', frame)
            if (len(faces) > 0) != detect_faces:
                offset += 1
                if offset > 10:
                    detect_faces = (len(faces) > 0)
                    defaultMaker.discord_report(json={"content": "There was a pressure change!"})
                    offset = 0
            else:
                offset = 0
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


    def motion_blur(self):
        background = None
        while self.enabled:
            grabbed, frame = self.vid.read()
            if not grabbed:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21), 0)

            if background is None:
                background = gray
                continue

            subtraction = cv2.absdiff(background, gray)
            retval, threshold = cv2.threshold(subtraction, 255, 255, cv2.THRESH_BINARY)
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


    def check_if_enabled(self):
        while not self.shutdown:
            if self.enabled and not bool(self.sensor_event):
                self.sensor_event = self.loop.run_in_executor(None, self.camera_modes[self.camera_mode_choice])
            elif not self.enabled and bool(self.sensor_event):
                self.sensor_event = None
            time.sleep(0.1)


if __name__ == "__main__":
    import time
    cam = Camera(2)
    with cam:
        time.sleep(30)
 
    print("bye")
