import cv2
import pyvirtualcam
from gestureDetector import GestureDetector
from animationPlayer import AnimationPlayer

class App:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.raw_frame = None
        self.result_frame = None
        
        self.gestureDetector = GestureDetector()
        self.animationPlayer = AnimationPlayer(self.width, self.height)

    def run(self):
        while True:
            success, self.raw_frame = self.cap.read()            
            if not success:
                break
            
            # horizontal flip
            self.raw_frame = cv2.flip(self.raw_frame, 1)
            
            # get current timestamp
            timestamp = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
            # print("Timestamp: ", timestamp)
            
            # TODO: Add gesture detection code here
            self.gestureDetector.detect(self.raw_frame, timestamp)
            
            self.gestureDetector.parse_results()
            results, output_image, timestamp = self.gestureDetector.fetch_results()
            
            self.result_frame = self.animationPlayer.process_frame(self.raw_frame, results, timestamp)
            
            # show result in cv2
            # TODO: show result in pyvirtualcam with OBS
            cv2.imshow("Frame", self.result_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = App()
    app.run()