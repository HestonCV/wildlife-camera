import cv2  
import requests
import time
import os
import os
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'



camera_token = 'cd98db92'
camera_paired = False


def capture_image():
  vidcap = cv2.VideoCapture(0)

  if vidcap.isOpened():
    ret, frame = vidcap.read()
    if ret:
      #crop to match size expected by machine learning model
      cropped_frame = frame[0:448, 0:448]
      cv2.imshow('frame', cropped_frame)

      _, buffer = cv2.imencode('.jpg', cropped_frame)

      image_as_bytes = buffer.tobytes()

      print(str(server_access_token))
      headers = {'Authorization': f'Bearer {server_access_token}'}
      files = {'image': ('image.jpg', image_as_bytes, 'image/jpeg')}

      response = requests.post(
        'http://192.168.1.140:5000/images',
        headers=headers,
        files=files)
      print(str(response.json()))
    else: 
      print('Error: could not capture frame')
  else: 
    print('Error: could not open camera')

def arm_camera():
  # loop here and wait for motion, then take image and send to server
  print("Camera Armed")
  cv2.namedWindow("dummy")
  while True:
        # Your other code here
        key = cv2.waitKey(1) & 0xFF  # Wait for 1 ms and get the key pressed
        if key == ord('p'):  # Check if the key is 'p'
            capture_image()
  

while not camera_paired:
  response = requests.get(f'http://192.168.1.140:5000/cameras/{camera_token}/check_pair')
  if response.status_code == 201:
    # store access token on device here
    camera_paired = True
    data = response.json()
    print(str(response.json()))
    server_access_token = data.get('data').get('access_token')
    print(server_access_token)
    arm_camera()
  else:
    print(str(response.json()))
    time.sleep(10)

