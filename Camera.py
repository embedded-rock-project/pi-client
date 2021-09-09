import cv2

class Camera:
    def Surveillance(self):
        print('Loading Camera Feed...')
        self.Cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.FirstFrame=self.Cam.read()[1]
        self.FirstFrameGray =cv2.cvtColor(self.FirstFrame, cv2.COLOR_BGR2GRAY)
        self.FirstFrameGrayBlur = cv2.GaussianBlur(self.FirstFrameGray, (21,21),0)
        while True:
            self.Frame = self.Cam.read()[1]
            self.FrameGray=cv2.cvtColor(self.Frame, cv2.COLOR_BGR2GRAY)
            self.FrameGrayBlur= cv2.GaussianBlur(self.FrameGray, (21,21),0)
            
            cv2.imshow('Cam Feed', self.FrameGrayBlur)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()
        self.Cam.release()
    def ShowFeed(self):
        self.Cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            self.Frame = self.Cam.read()[1]
            cv2.imshow('Cam Feed', self.Frame)
            if cv2.waitKey(1) == 27: 
                break  # esc to quit
        cv2.destroyAllWindows()
        self.Cam.release()
if(__name__=='__main__'):
    Camera()

