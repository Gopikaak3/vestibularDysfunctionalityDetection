import cv2
import mediapipe as mp
import numpy as np
import pyrealsense2 as rs

#Calculate angle function
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # last
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


#Calculate angle using intel realsense camera
def findTilt():
    #initiation
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # variables
    whileLoopCounter = 0 
    stage = None
    tilt = 0.0
    tiltDirection = ""
    rightShoulder = [0,0,0]
    leftShoulder = [0,0,0]

    # Configure realsense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    pipeline.start(config)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            
            # Recolor image to RGB
            image = cv2.flip(color_image, 1)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)
            
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                #taking Right and Left Shoulder coordinate points
                rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility]
                leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility]

                refferenceShoulder = [0,0]
                # taking reference point on shoulder
                refferenceShoulder [1] = leftShoulder[1] if leftShoulder[1] > rightShoulder[1] else rightShoulder[1]
                refferenceShoulder [0] = rightShoulder [0] if refferenceShoulder[1] == leftShoulder[1] else leftShoulder[0]
                tiltDirection = "Right" if refferenceShoulder [0] == rightShoulder [0] else "Left"

                # Defining first, mid and last points to find the tilt angle
                First = refferenceShoulder
                Mid = rightShoulder if refferenceShoulder[1] == rightShoulder[1] else leftShoulder
                last = rightShoulder if Mid == leftShoulder else leftShoulder
                
                # Calculate angle
                whileLoopCounter +=1
                if(whileLoopCounter == 10):
                    tilt = calculate_angle(First, Mid, last)
                    whileLoopCounter = 0
            except:
                pass

            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (350,80), (0,155,155), -1)
            
            # Rep data
            cv2.putText(image, tiltDirection, (15,50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, ": " + format(tilt, ".2f"), (150,50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

    #        cv2.putText(image, "Visibility : " + format(rightShoulder[2], ".2f") + format(leftShoulder[2], ".2f"), (150,50), 
    #                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )

            imageMirror = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow('Mediapipe Feed', imageMirror)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



#Device not found window
def deviceNotFound():
    # Set the desired image size
    image_width = 1280
    image_height = 720

    # Create a solid color image using NumPy
    color = (150, 150, 0)  # Blue color, change it to your desired color (BGR format)
    image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    image[:] = color

    # Add text to the image
    text = "Sorry! device is not connected or not detected!"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    text_color = (255, 255, 255)  # White color (BGR format)
    text_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, text_thickness)
    text_x = (image_width - text_size[0]) // 2
    text_y = (image_height + text_size[1]) // 2
    cv2.putText(image, text, (text_x, text_y), font, font_scale, text_color, text_thickness, cv2.LINE_AA)
    cv2.imshow("No Device Connected", image)

    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     break
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()


pipeline = rs.pipeline()
ctx = rs.context()

# Get the list of connected RealSense devices
devices = ctx.query_devices()

if len(devices) == 0:
    deviceNotFound()
else:
    findTilt ()
# Release resources
pipeline.stop()