import mediapipe as mp 
import cv2

class GestureDetector:
    def __init__(self):
        self.init_recognition()
        
        self.detection_result = []
        self.results = []
        self.output_image = None
        self.timestamp = 0
        
    def results_listener(self, result, output_image, timestamp):
        if len(result.gestures) > 0 and len(self.detection_result) < 2:
            self.detection_result.append(result)
            
            self.output_image = output_image
            self.timestamp = timestamp
    
    def parse_results(self):
        
        try:
            if len(self.detection_result) == 0:
                self.results = []
                return
        except Exception as e:
            print(e)
            print(self.detection_result)
            return
        results = []
        hand_count = len(self.detection_result)
        
        print("hand count: ", hand_count)
        # print("results: ", self.detection_result)
        # print("gestures: ", result.gestures)
        # print("handeness: ", result.handedness)
        # print("gesture 0: ", result.gestures[0][0])
        # print("landmark 0: ", result.hand_landmarks[0][0])
        # print("category name: ", result.gestures[0][0].category_name)
        
        # result format: {'type': 'action_type', 'hand': 'handness', 'top_left': (x, y), 'bottom_right': (x, y)}
        for i in range(hand_count):
            parsed_result = {}
            
            parsed_result["type"] = self.detection_result[i].gestures[0][0].category_name 
            parsed_result["hand"] = self.detection_result[i].handedness[0][0].category_name
            
            # TODO: fix dummy
            # get top_left and bottom_right from mediapipe result
            
            # get all landmarks
            landmarks_x = [ landmark.x for landmark in self.detection_result[i].hand_landmarks[0] ]
            landmarks_y = [ landmark.y for landmark in self.detection_result[i].hand_landmarks[0] ]
            
            top_left = (min(landmarks_x), min(landmarks_y))
            bottom_right = (max(landmarks_x), max(landmarks_y))
            
            parsed_result["top_left"] = top_left
            parsed_result["bottom_right"] = bottom_right
            
            print("result: ", parsed_result)
        
            results.append(parsed_result)
        print("results: ", results)
        self.results = results 
        self.detection_result.clear()
        
    def init_recognition(self):
        BaseOptions = mp.tasks.BaseOptions
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path='assets/gesture_recognizer.task'),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.results_listener,
            min_hand_presence_confidence=0.3
        )
        
        self.gesture_recognizer = GestureRecognizer.create_from_options(options)
    
    
    
    def detect(self, frame, timestamp):
        # convert frame to mediapipe image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        result = self.gesture_recognizer.recognize_async(mp_image, timestamp)
    
    def fetch_results(self):
        return self.results, self.output_image, self.timestamp