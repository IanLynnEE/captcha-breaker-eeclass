# eeclass Captcha Breaker

## Feasibility

To utilize the fact that captcha answer will not change in one session, we can collect 10 or more images first. Then, noise can be removed by two steps of `cv2.dilate()`. Eventually, by Tesseract with trained data from [Shreeshrii](https://github.com/Shreeshrii), the answer can be predicted by majority vote. 

## DL

The steps above require 10 images and Tesseract, and loading them take ages. Trained model for this specific purpose is needed. The project [lanpa/NTHUAIScaptcha](https://github.com/lanpa/NTHUAIScaptcha) has shown that CNNs can do a great job. We hope the similar network can work here as well.

