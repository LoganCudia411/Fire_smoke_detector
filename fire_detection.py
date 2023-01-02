import cv2

#capture video using cv2 (0 is for first webcam)
# put video name to capture video
video = cv2.VideoCapture("video.mov")

#while video is running, we track the frames
while True:
    ret, frame = video.read() 
    frame = cv2.resize(frame, (1000,600))
    if ret == False: 
        break # if video ends

    cv2.imshow("output_window", frame)

    #when anyone preses q in the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#exit out of video
cv2.destroyAllWindows()

video.release() 