import time
from roboflow import Roboflow

# Start measuring time
start = time.time()

# Initialize the Roboflow client with your API key
import detect

# Use parse_opt and main from detect.py
opt = detect.parse_opt()



# Save the prediction results to an output image

# Calculate and print the time taken for the sequential processing
print("Time for sequential processing: ")
print(time.time() - start)
