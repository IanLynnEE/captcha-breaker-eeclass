# eeclass Captcha Breaker

Try to break it by OpenCV and Tesseract with traineddata from [Shreeshrii](https://github.com/Shreeshrii). 

The idea is to utilize the fact that captcha answer will not change in one session. Thus, collecting 10 or more images for prediction and voting on the answer can solve the problem of distortion. 

Noise is removed by two steps of `cv2.dilate()`.