import cv2
import mediapipe as mp

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Rock Paper Scissors", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

def recognize_gesture(hand_landmarks):
    # Finger tip and pip landmarks
    tips = {
        'thumb': mp_hands.HandLandmark.THUMB_TIP,
        'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
        'pinky': mp_hands.HandLandmark.PINKY_TIP,
    }
    pips = {
        'thumb': mp_hands.HandLandmark.THUMB_IP,
        'index': mp_hands.HandLandmark.INDEX_FINGER_PIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_PIP,
        'pinky': mp_hands.HandLandmark.PINKY_PIP,
    }

    finger_up = {}

    # Determine if thumb is up (extended to the side). 
    thumb_tip = hand_landmarks.landmark[tips['thumb']]
    thumb_ip = hand_landmarks.landmark[pips['thumb']]
    finger_up['thumb'] = thumb_tip.x > thumb_ip.x

    # Check if other fingers are up (tip above pip in y-axis)
    for finger in ['index', 'middle', 'ring', 'pinky']:
        tip = hand_landmarks.landmark[tips[finger]]
        pip = hand_landmarks.landmark[pips[finger]]
        finger_up[finger] = tip.y < pip.y

    # Check gestures
    if all(finger_up[f] for f in finger_up):  # Paper
        return "paper"
    if not any(finger_up[f] for f in finger_up):  # Rock
        return "rock"
    if finger_up['index'] and finger_up['middle'] and not finger_up['ring'] and not finger_up['pinky'] and not finger_up['thumb']:  # Scissors
        return "scissors"
    return None

