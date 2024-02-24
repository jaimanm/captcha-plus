import cv2
from flask import Flask, Response, render_template
import mediapipe as mp
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

anotherList = []
message = "hello"

@app.route('/')
def index():
    return render_template('index.html', message=message)

@app.route('/stream')
def stream():
    def event_stream():
       while True:
           yield 'data: {}\n\n'.format(message)
    return Response(event_stream(), mimetype="text/event-stream")

def generate_frames():
    global message
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    count = 0
    anotherList = []
    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands = 1) as hands:
      while camera.isOpened():
        
        success, image = camera.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
          for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            list = []
            for i in range(21):
              temp = []
              temp.append(hand_no)
              temp.append(i)
              temp.append(int(hand_landmarks.landmark[mp_hands.HandLandmark(i).value].x * camera.get(3)))
              temp.append(int(hand_landmarks.landmark[mp_hands.HandLandmark(i).value].y * camera.get(4)))
              temp.append(int(hand_landmarks.landmark[mp_hands.HandLandmark(i).value].z * -100))
              list.append(temp)

            #todo: create average of palm points to accurately depict thumb distance
            #identify gesture
            s = ""
            for i in range(5) :
              averagePalmX = (list[0][2] + list[5][2] + list[13][2] + list[17][2]) / 4
              averagePalmY = (list[0][3] + list[5][3] + list[13][3] + list[17][3]) / 4
              dist1 = np.hypot(list[(i + 1) * 4][2] - averagePalmX, list[((i + 1) * 4)][3] - averagePalmY)
              dist2 = np.hypot(list[(i + 1) * 4 - 2][2] - averagePalmX, list[((i + 1) * 4 - 2)][3] - averagePalmY)
              dist3 = np.hypot(list[(i + 1) * 4 - 1][2] - averagePalmX, list[((i + 1) * 4 - 1)][3] - averagePalmY)
              dist4 = np.hypot(list[(i + 1) * 4 - 3][2] - averagePalmX, list[((i + 1) * 4 - 3)][3] - averagePalmY)
              if dist1 < dist2 or dist1 < dist3 or dist1 < dist4:
                s = s + "0"
              else :
                s = s + "1"
            dec_number = int(s[::-1], 2)
            anotherList.append(dec_number)
        else :
            anotherList.append(-1)


        if count >= 10:
            mode = max(set(anotherList), key = anotherList.count)
            # print(mode)
            anotherList = []
            message = str(mode)
            stream()
            count = 0
        count += 1

        # Flip the image horizontally for a selfie-view display.
        # For simplicity, we'll just encode it as JPEG
        ret, buffer = cv2.imencode('.jpg', cv2.flip(image, 1)) # flip horizontally for a selfie-view display
        image = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

@app.route('/video-stream')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
