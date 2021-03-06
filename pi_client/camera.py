from concurrent.futures import ThreadPoolExecutor
import nest_asyncio
nest_asyncio.apply()



import cv2
import asyncio
from typing import Optional
from requests_toolbelt import MultipartEncoder
from io import BytesIO
import time
import numpy as np
from http_reqs import defaultMaker
#import traceback




class Camera:

    # Initialization
    def __init__(self, camera_mode_choice: int, camera: int = 0, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.enabled = False
        self.sensor_event = None
        self.vid = None
        self.camera = camera
        self.camera_mode_choice = camera_mode_choice
        self.loop = loop if loop else asyncio.get_event_loop()

        # Get default OpenCV image recognition model
        self.cv2Cascades = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        # set possible camera modes
        self.camera_modes = [self.standard_survelliance, self.facial_recognition, self.motion_blur_clean]
        
    # Enter as enabled by default. This is so switch camera mode works.
    def __enter__(self):
        self.enabled = True

    # Call disable camera on exit of class.
    def __exit__(self, exc_type, exc_value, traceback):
        self.disable_camera()

    # getter for mode.
    def get_mode(self):
        return self.camera_mode_choice

    # enable camera. Avoids seg faults from OpenCV attempting to access camera on multiple threads.
    def enable_camera(self):
        if not self.enabled:
            self.enabled = True
            self.vid = cv2.VideoCapture(self.camera)
            if not bool(self.sensor_event):
                self.sensor_event = self.loop.run_in_executor(None, self.camera_modes[self.camera_mode_choice])

    # Disable camera. Avoid calling NoneTypes and destroys openCV windows.
    def disable_camera(self):
        if self.enabled:
            self.enabled = False
            if bool(self.sensor_event):  
                self.sensor_event.cancel()
                self.sensor_event = None
            if (self.vid):
                self.vid.release()
            cv2.destroyAllWindows()

    # Switch camera mode. Input int to choose which mode.
    def switch_camera_mode(self, choice: int):
        # if choice != self.camera_mode_choice:
        self.camera_mode_choice = choice
        self.disable_camera()
        self.enable_camera()

    # unused for demo. Would report data + image to discord.
    def _report_to_discord(self, frame, message):

        # encode raw bytes to jpg format
        is_success, buffer = cv2.imencode(".jpg", frame)

        # create bytesIO stream object to be sent as multipart form data
        output_bytes = BytesIO(buffer)

        # properly encode data to send to discord here.
        req_data = MultipartEncoder(fields={"file": ("test.jpg", output_bytes, "image/jpeg"), "payload_json": '{{"content":"{}","tts":false}}'.format(message).encode()})
        
        # report to webhook.
        #defaultMaker.discord_report(headers={"content-type": req_data.content_type}, data=req_data.to_string())


    def standard_survelliance(self):
        while self.enabled:

            # read frame off of video
            ret, frame = self.vid.read()

            # convert BGR color scheme (default) to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # apply a gaussian blur to mimic old-time camera effect
            frame_gray_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

            # display frame to screen
            hello, image = cv2.imencode('.jpg', frame_gray_blur)
            img = np.array(image).tobytes()
            defaultMaker.ws_img_feed_send(img)

            # wait one millisecond, if break key occurs break from loop
            # want to remove
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        # cv2.destroyWindow("survelliance")


    def facial_recognition(self):
        # set variables outside of loop
        detect_faces = False
        offset = 0
        while self.enabled:

            # read frame
            ret, frame = self.vid.read()

            # convert to grayscale to be used for image detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # using preloaded xmls for cv2, detect matching patterns
            # in this case, detect forward facing facial features. (alliteration)
            faces = self.cv2Cascades.detectMultiScale(gray_frame, 1.3, 5)

            # for each rectangle detected, draw rectangle onto original frame
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # display edited frame
            hello, image = cv2.imencode('.jpg', frame)
            img = np.array(image).tobytes()
            defaultMaker.ws_img_feed_send(img)
            # check if length of faces (if any were detected) is same as previous runthrough.
            # this is a buffer system to detect false switches from detecting face to not, or vice cersa
            if (len(faces) > 0) != detect_faces:

                # if they don't match, add count of not matching.
                offset += 1

                # if ten in a row don't match, run this.
                if offset > 10:

                    # change detect_faces to current bool of if face is detected
                    detect_faces = (len(faces) > 0)

                    # report to website
                    result = ("camera", True, 1) if detect_faces else ("camera", True, 0)
                    defaultMaker.ws_server_report(*result)

                    # reset offset so checks can begin again.
                    offset = 0

            # if current mode DOES match, reset offset.
            else:
                offset = 0

            # I want to remove this.
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


    def motion_blur(self):
        # create variable outside of loop.
        background = None
        detected_movement = False
        offset = 0
        while self.enabled:
            try:
                # read frame from camera
                ret, frame = self.vid.read()

                # convert color scheme to grayscale for processing
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # apply gaussian blur to display motion blur to detection process.
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                # this is ran once: gets first frame as reference. Otherwise skips.
                if background is None:
                    background = gray
                    continue

                # accquire differences in pixels between current frame and background
                # returns pixels that demonstrate that difference
                subtraction = cv2.absdiff(background, gray)

                # pick out pixels that differ above a certain threshhold.
                retval, threshold = cv2.threshold(
                    subtraction, 25, 255, cv2.THRESH_BINARY)

                # increase size of image
                threshold = cv2.dilate(threshold, None, iterations=2)

                # create copy of new threshold to continue processing, save original for display
                contourimg = threshold.copy()

                # find contour of currently differing objects.
                outlines, heirarchy = cv2.findContours(
                    contourimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # remove outlines that are insiginificant (too small, possible false positives)
                notable_outlines = list(
                    filter(lambda c: cv2.contourArea(c) > 500, outlines))

                if (len(notable_outlines) > 0) != detected_movement:

                    # if they don't match, add count of not matching.
                    offset += 1

                    # if ten in a row don't match, run this.
                    if offset > 5:
                        detected_movement = (len(notable_outlines) > 0)
                        if detected_movement:
                            defaultMaker.ws_server_report("There was movement!")
                            defaultMaker.ws_img_feed_send(frame)
                        offset = 0
                else:
                    offset = 0

                # draw rectangles on image.
                for c in notable_outlines:

                    # get rectangle coordinates
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Send data over webhook.
                hello, image = cv2.imencode('.jpg', frame)
                img = np.array(image).tobytes()
                defaultMaker.ws_img_feed_send(img)

                # set new background to compare to.
                background = gray

                # check for break key. I want to remove this.
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    break

            except ConnectionResetError:
                print("connection lost")
                break
            except cv2.error:
                #traceback.print_exc()
                break



    #same code as above just compact
    def motion_blur_clean(self):
            background = None
            detected_movement = False
            offset = 0
            while self.enabled:
                try:
                    #background
                    ret, frame = self.vid.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)
                    if background is None:
                        background = gray
                        continue
                        
                    #sets up the contour finding and motion detection
                    subtraction = cv2.absdiff(background, gray)
                    retval, threshold = cv2.threshold(subtraction, 25, 255, cv2.THRESH_BINARY)
                    outlines, heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    notable_outlines = list(filter(lambda c: cv2.contourArea(c) > 500, outlines))
                    
                    #motion detection using outline regcognition and magnitude of change over a period of time
                    if (len(notable_outlines) > 0) != detected_movement:
                        offset += 1
                        if offset > 5:
                            detected_movement = (len(notable_outlines) > 0)
                            result = ("camera", "report", "Motion detected") if detected_movement else ("camera", "report", "Motion stopped")
                            defaultMaker.ws_server_report(*result)
                            offset = 0
                    else:
                        offset = 0
                        
                    #puts a frame around any notable movement areas drawn on the image sent to the website
                    for c in notable_outlines:
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    hello, image = cv2.imencode('.jpg', frame)
                    img = np.array(image).tobytes()
                    defaultMaker.ws_img_feed_send(img)
                    background = gray
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        break
                except ConnectionResetError:
                    print("connection lost")
                    break
                except cv2.error:
                    #traceback.print_exc()
                    break
                    #continue
