import cv2
import numpy as np 

class Animation:
    def __init__(self, path, width, height, x, y, start_time, duration):
        self.animation = None 
        self.animation_mask = None
        
        self.animation_path = path
        self.width = width
        self.height = height
        
        self.x = max(0, x)
        self.y = max(0, y)
        
        self.start_time = start_time
        self.duration = duration
    
        self.load_animation()
    
    def load_animation(self) -> None:
        img = cv2.imread(self.animation_path) 
        # resize image
        img = cv2.resize(img, (self.width, self.height))
        
        self.animation = img
        
        # TODO: animation mask for png animation
        # 1 if pixel is part of animation, 0 otherwise
        # use alpha channel of png image during imread
        # self.animation_mask = None
        
    def fetch_animation(self) -> np.ndarray:
        # overlay animation on frame
        return self.animation
        

class AnimationPlayer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = None
        
        self.animation_size = 100
        
        # actions: Closed_Fist, Open_Palm, Thumb_Up, Thumb_Down, Victory, ILoveYou, Pointing_Up
        self.assets = {
            "Thumb_Up": "assets/thumbs_up.png",
        }
        
        # list of all ongoing animations
        self.current_animations = []
    
    # TODO: instead of overlay, directly use slicing to replace certain areas of the frame (large) with the animation image (Small)
    
    def process_frame(self, raw_frame, classification_result, timestamp) -> np.ndarray: 
        if raw_frame is None:
            return
        
        frame = raw_frame.copy()
        
        # plot hand bounding box
        for result in classification_result:
            # unnormalize the bounding box (x, y)
            top_left = (int(result["top_left"][0] * self.width), int(result["top_left"][1] * self.height))
            bottom_right = (int(result["bottom_right"][0] * self.width), int(result["bottom_right"][1] * self.height))
            
            # check boundary
            top_left = (max(0, top_left[0]), max(0, top_left[1]))
            bottom_right = (min(self.width, bottom_right[0]), min(self.height, bottom_right[1]))
            
            frame = cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            
            result_type = result["type"]
            if result_type not in self.assets:
                continue
            
            # create animation object
            animation = Animation(
                path = self.assets[result_type], 
                width = self.animation_size, 
                height = self.animation_size,
                x = top_left[0] - self.animation_size, 
                y = top_left[1] - self.animation_size, 
                start_time = timestamp, 
                duration = 50
            )
            
            self.current_animations.append(animation)
        
        if len(self.current_animations) == 0:
            return frame
            
        # add animation to frame
        for animation in self.current_animations:
            # check if animation is still ongoing
            if animation.start_time + animation.duration < timestamp:
                self.current_animations.remove(animation)
                continue
            
            # fetch animation
            animation_graphic = animation.fetch_animation()
            
            # replace frame segment with animation
            frame[animation.y:animation.y + self.animation_size, animation.x:animation.x + self.animation_size] = animation_graphic
            
        return frame