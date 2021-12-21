# # Import packages
# import cv2
# import numpy as np
# img = cv2.imread(r'D:\gil\demo\UOB smart project demo\object detection\output.jpg')
# print(img.shape) # Print image shape
# cv2.imshow("original", img)
# cropped_image = img[:, 280:]
# # Display cropped image
# cv2.imshow("cropped", cropped_image)
# # Save the cropped image
# cropped_image=cv2.resize(cropped_image,(400,400))
# print(cropped_image.shape)
# cv2.imwrite("Cropped Image.jpg", cropped_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import os

# dir=os.listdir(r"static\detection images")
list_images=[]
start='2021-11-26-17-19-18'
end='2021-11-26-17-27-55'
for i in os.listdir(r"static\detection images"):
    if start<=i.split('_')[0]<=end:
        list_images.append(i)