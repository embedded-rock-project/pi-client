
# import the opencv library
import cv2
import asyncio
from typing import Optional

from requests_toolbelt import MultipartEncoder
from http_reqs import defaultMaker
from io import BytesIO
import time

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
        self._sync_nowait = self.loop.run_in_executor


    def __enter__(self):
        self.enabled = True
        #self.check_if_enabled()
        self.event_task = self._sync_nowait(None, self.check_if_enabled)


    def __exit__(self, exc_type, exc_value, traceback):
        self.enabled = False
        self.shutdown = True
        self.event_task.cancel()
        self.vid.release()
        cv2.destroyAllWindows()


    def enable_camera(self):
        self.enabled = True

    def disable_camera(self):
        self.enabled = False


    # Displays edited video footage resembling security camera
    def standard_survelliance(self):
        print('Loading Camera Feed...')
        while self.enabled:
            # read frame off of video
            ret, frame = self.vid.read()

            # convert BGR color scheme (default) to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # apply a gaussian blur to mimic old-time camera effect
            frame_gray_blur = cv2.GaussianBlur(frame_gray, (21,21),0)

            # display frame to screen
            cv2.imshow('Cam Feed', frame_gray_blur)

            # wait one millisecond, if break key occurs break from loop
            # want to remove this, broke when I did -R
            if cv2.waitKey(1) == 27:
                break  # esc to quit




    def facial_recognition(self):

        # set variables outside of loop
        detect_faces = False
        offset = 0
        while self.enabled:

            #read frame
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
            cv2.imshow('face_detect', frame)

            # check if length of faces (if any were detected) is same as previous runthrough.
            # this is a buffer system to detect false switches from detecting face to not, or vice cersa
            if (len(faces) > 0) != detect_faces:

                # if they don't match, add count of not matching.
                offset += 1

                # if ten in a row don't match, run this.
                if offset > 10:

                    # change detect_faces to current bool of if face is detected
                    detect_faces = (len(faces) > 0)

                    # encode raw bytes to png format
                    #is_success, buffer = cv2.imencode(".png",frame)

                    # create bytesIO stream object to be sent as multipart form data
                    # this is an http requirement.
                    #output_bytes = BytesIO(buffer)

                    # properly encode data to send to discord here.
                    #req_data = MultipartEncoder(fields={ "file": ("test.png", output_bytes, "image/png"), "payload_json": '{{"content":"{}","tts":false}}'.format("Person detected" if detect_faces else "Person left.").encode() })

                    # report to webhook.
                    #defaultMaker.discord_report(headers={"content-type": req_data.content_type}, data=req_data.to_string())

                    # reset offset so checks can begin again.
                    offset = 0
                
            # if current mode DOES match, reset offset.
            else:
                offset = 0

            # I want to remove this.
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break


    # this is more complicated and I can't explain this *that* well. -R
    # note: threshold seems to be doing almost nothing.
    def motion_blur(self):

        # create variable outside of loop.
        background = None
        while self.enabled:

            # read frame from camera
            ret, frame = self.vid.read()

            # if fail, break
            if not ret:
                break

            # convert color scheme to grayscale for processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # apply gaussian blur for some reason
            gray = cv2.GaussianBlur(gray, (21,21), 0)

            # this is ran once: gets first frame as reference. Otherwise skips.
            if background is None:
                background = gray
                continue

            # accquire differences in pixels between current frame and background
            # returns pixels that demonstrate that difference
            subtraction = cv2.absdiff(background, gray)

            # pick out pixels that differ above a certain threshhold.
            retval, threshold = cv2.threshold(subtraction, 25, 255, cv2.THRESH_BINARY)

            # increase size of image
            threshold = cv2.dilate(threshold, None, iterations = 2)

            # create copy of new threshold to continue processing, save original for display
            contourimg = threshold.copy()

            # find contour of currently differing objects.
            outlines, heirarchy = cv2.findContours(contourimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # remove outlines that are insiginificant (too small, possible false positives)
            notable_outlines = [c for c in outlines if cv2.contourArea(c) > 500]

            # debug length of lines, use to report movement
            print(len(notable_outlines))

            # apply rectangles to image.
            for c in notable_outlines:
                
                # get rectangle coordinates
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)


            # display all four cameras.
            cv2.imshow("Camera", frame)
            cv2.imshow("Threshold", threshold)
            cv2.imshow("Subtraction", subtraction)
            cv2.imshow("Contour", contourimg)

            # set new background to compare to.
            background = gray

            # check for break key. I want to remove this.
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break


    def check_if_enabled(self):
        while not self.shutdown:
            if self.enabled and not bool(self.sensor_event):
                self.sensor_event = self._sync_nowait(None, self.camera_modes[self.camera_mode_choice])
            elif not self.enabled and bool(self.sensor_event):
                self.sensor_event.cancel()
                self.sensor_event = None

            time.sleep(0.1)


if __name__ == "__main__":
    import time
    cam = Camera(2)
    with cam:
        time.sleep(30)
