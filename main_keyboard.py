import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Key,Controller

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize hand detector
detector = HandDetector(maxHands=1, detectionCon=0.85)
keyboard = Controller()  # Simulate keyboard input

# Virtual keyboard keys
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

final_text = ""  # Store typed text

# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create button objects
button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button([100 * j + 50, 100 * i + 50], key))

# Function to draw buttons
def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        # cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)  # Rounded rectangle
        cv2.rectangle(img, button.pos, (x + w, y + h), (128, 128, 128), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
    return img

# Main loop
while True:
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1)  # Flip for mirror effect

    # Detect hands
    hands, img = detector.findHands(img, draw=True)

   
    img = draw_all(img, button_list)

    # Process hand tracking
    if hands:
        hand = hands
        bbox = hands[0]['bbox']

        x1,x2,x3,x4 = bbox
        area = (x3 * x4)
        # print(area)

        

        lm_list = hands[0]["lmList"]  # Get first hand's landmark list
        index_finger_x, index_finger_y = lm_list[8][0], lm_list[8][1]  # Index finger tip position

        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if(85000<area<110000):
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

                # Check if index finger is on a button
                if x < index_finger_x < x + w and y < index_finger_y < y + h:
                    # Highlight button
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

                    # Extract x, y coordinates for distance check
                    x1, y1, _ = lm_list[8]   # Index finger tip
                    x2, y2, _ = lm_list[12]  # Middle finger tip
                    
                    length, _, _ = detector.findDistance((x1, y1), (x2, y2))  # Pass (x, y) only

                    if length < 50:  # If fingers are close, register key press
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
                        final_text += button.text
                        sleep(0.25)  # Prevent multiple presses

    # Display typed text
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, final_text, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Show webcam feed
    cv2.imshow("Virtual Keyboard", img)

    # Quit when 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
