# Importing required libraries
import cv2
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Opening camera as default
cap = cv2.VideoCapture(0)

# SMTP Server credentials for sending email
smtp_server =
smtp_port = 587
smtp_username =
smtp_password =

# Email addresses for sending and receiving email
email_from =
email_to =

# Haarcascades for face and body detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Initialization of detection and timer variables
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# Frame size and codec for recording
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Start of video capturing loop
while True:
    # Reading the frame from camera
    _, frame = cap.read()

    # Converting frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting faces and bodies in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Saving the frame as an image
    cv2.imwrite('captura.jpg', frame)

    # Creating email message with the captured image as an attachment
    msg = MIMEMultipart()
    msg['From'] =
    msg['To'] =
    msg['Subject'] = 'Movement detected'
    with open('captura.jpg', 'rb') as f:
            img = MIMEImage(f.read())
            msg.attach(img)

    # Sending email message with attachment using SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login()
            smtp.send_message(msg)

    # Checking if there are any detected faces or bodies in the frame
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            # Starting video recording if detection starts
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")
    elif detection:
        # Checking if the time limit for recording has expired
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                # Stopping recording and resetting detection variables
                detection = False
                timer_started = False
                out.release()
                print('Stop Recording!')
        else:
            # Starting timer for recording limit
            timer_started = True
            detection_stopped_time = time.time()

    # Write frame
    if detection:
        out.write(frame)

    # for (x, y, width, height) in faces:
    #    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()