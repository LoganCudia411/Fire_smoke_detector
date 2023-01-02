import cv2
import numpy as np
import smtplib
import playsound
from datetime import datetime
import threading

fire_reported = 0
alarm_status = False
email_status = False
now = datetime.now()
current_time = now.strftime("%h:%m:%S")


#play alarm function
def play_alarm():
    while True:
        playsound.playsound('alarm-sound.mp3', True)

#function to send email
def send_email_function():

    recipientEmail = "Enter_Recipient_Email"
    #input firedepartment email
    recipientEmail = recipientEmail.lower()
    try:
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.ehlo()
       server.starttls()
       server.login("Enter_Your_Email (System Email)", 'Enter_Your_Email_Password (System Email')
       server.sendmail('Enter_Your_Email (System Email)', recipientEmail, "Warning A Fire Accident has been reported on ABC Company")
       print("sent to {}".format(recipientEmail))
       server.close()
    except Exception as e:
     	print(e)


#capture video using cv2 (0 is for first webcam)
# put video name to capture video
video = cv2.VideoCapture("video.MOV")

# while video is running, we track the frames
while True:
    (ret, frame) = video.read()
    if not ret:
        break
    frame = cv2.resize(frame, (960,540))

    #blurring video to remove noises
    blur = cv2.GaussianBlur(frame, (21, 21), 0)

    #converting to HSV color
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #upper and lower color values 
    lower = [18,50,50]
    upper = [35, 255, 255]

    #use numpy to convert flame into some kind of numerical value 
    lower = np.array(lower, dtype='uint8') #int arry
    upper = np.array(upper, dtype='uint8') #int arry


    #create mask to look for sepcific color in range of upper and lower bounds in HSV format
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame,hsv,mask=mask)

    #check if fire by converting the mask into an integer
    fire_size = cv2.countNonZero(mask)
    #if the actual size of the fire is greater than this threshold
    if int(fire_size)>5000:
        fire_reported= fire_reported+1

    cv2.imshow("output_window", output)

    if fire_reported>=1:
            #email fire department and play alarm simultaneously using threading technique
            if alarm_status == False:
                threading.Thread(target=play_alarm).start()
                alarm_status = True

            if email_status == False:
                threading.Thread(target=send_email_function).start()
                email_status = True
    if ret == False: 
        break # if video ends

    #when anyone preses q in the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#exit out of video
cv2.destroyAllWindows()
video.release() 

