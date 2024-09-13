import cv2
import numpy as np

# Load the old photo
image = cv2.imread('C:\Users\YASHSONI\OneDrive\Desktop\Index.html\images\Merc.png')

# Step 1: Convert to grayscale (if necessary)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Apply Non-Local Means Denoising to reduce noise
denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

# Step 3: Inpainting to remove scratches and damaged parts
# Create a mask where we want to inpaint (assume white scratches on black background)
_, thresh = cv2.threshold(denoised, 240, 255, cv2.THRESH_BINARY_INV)

# Inpaint the image using the mask
inpainted = cv2.inpaint(denoised, thresh, 3, cv2.INPAINT_TELEA)

# Step 4: Histogram Equalization for contrast enhancement
equalized = cv2.equalizeHist(inpainted)

# Step 5: Sharpening the image using a kernel
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
sharpened = cv2.filter2D(equalized, -1, kernel)

# Step 6: Show the results
cv2.imshow("Original", image)
cv2.imshow("Restored Photo", sharpened)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the restored photo
cv2.imwrite('restored_photo.jpg', sharpened)
