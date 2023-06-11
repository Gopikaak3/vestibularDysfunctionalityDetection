#taking Right and Left Shoulder coordinate points
rightShoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
leftShoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

# taking reference point on shoulder
refferenceShoulder [1] = leftShoulder[1] if leftShoulder[1] > rightShoulder[1] else rightShoulder[1]
refferenceShoulder [0] = rightShoulder [0] if refferenceShoulder[1] == leftShoulder[1] else leftShoulder[0]
tiltDirection = "Right" if refferenceShoulder [0] == rightShoulder [0] else "Left"

# Defining first, mid and last points to find the tilt angle
First = refferenceShoulder
Mid = rightShoulder if refferenceShoulder[1] == rightShoulder[1] else leftShoulder
last = rightShoulder if mid == leftShoulder else leftShoulder