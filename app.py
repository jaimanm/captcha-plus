# # mediapipe hand tracking test
# import cv2

# cap = cv2.VideoCapture(0)

# # show the video
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()


import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Process the frame as needed (e.g., apply filters)
            # For simplicity, we'll just encode it as JPEG
            # overlay a rectangle before encoding the frame
            cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video-stream')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
