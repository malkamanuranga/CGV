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
import random

def play_game():
    global previous_gesture, previous_computer_gesture, previous_result_text
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
                gesture = recognize_gesture(landmarks)

                if gesture and gesture != previous_gesture:
                    previous_gesture = gesture
                    comp = random.choice(['rock', 'paper', 'scissors'])
                    previous_computer_gesture = comp

                    # Determine result
                    if gesture == comp:
                        previous_result_text = "It's a tie!"
                    elif (gesture == 'rock' and comp == 'scissors') or \
                         (gesture == 'scissors' and comp == 'paper') or \
                         (gesture == 'paper' and comp == 'rock'):
                        previous_result_text = "You win!"
                    else:
                        previous_result_text = "Computer wins!"
        # Displaying text continuously
        cv2.putText(frame, f'Your gesture: {previous_gesture or "Waiting..."}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Computer: {previous_computer_gesture or "Waiting..."}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f'Result: {previous_result_text or "Waiting..."}', (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Rock Paper Scissors", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

cv2.putText(frame, f'Your gesture: {previous_gesture or "Waiting..."}', (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
cv2.putText(frame, f'Computer: {previous_computer_gesture or "Waiting..."}', (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(frame, f'Result: {previous_result_text or "Waiting..."}', (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

if result.multi_hand_landmarks:
    for landmarks in result.multi_hand_landmarks:
        # Process landmarks if hands are detected
else:
    # Handle case where no hands are detected
    cv2.putText(frame, "No hand detected", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# More precise conditions for paper (all fingers extended)
if all(finger_up[f] for f in finger_up):
    return "paper"

# Reduce the frequency of hand landmark processing if necessary for performance
if frame_counter % 5 == 0:
    result = hands.process(rgb_frame)
    
round_count = 0

max_rounds = 5

 

if round_count >= max_rounds:

   cv2.putText(frame, "Game Over!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

if previous_result_text == "You win!":
    # Add animation for winning (e.g., text flashing)
    cv2.putText(frame, "You Win!", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
