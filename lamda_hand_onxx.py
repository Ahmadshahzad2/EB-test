import json
import onnxruntime as ort
import numpy as np
import base64
from PIL import Image
from io import BytesIO

def preprocess_input(image):
    # Resize the image to the required size (224x224)
    image = image.resize((224, 224))
    
    # Convert image to numpy array and transpose to (1, 3, 224, 224)
    image_array = np.array(image).astype(np.float32).transpose(2, 0, 1).reshape(1, 3, 224, 224)
    
    # Normalize the image data to the range [0, 1]
    image_array /= 255.0
    
    return image_array

def lambda_handler(event, context):
    # Extract the model type from the event    
    
    model_path = '/mnt/redLantern/image.onnx'
    
    # Load the ONNX model
    session = ort.InferenceSession(model_path)

    # Extract base64 image data from the event
    base64_image = event['body']
    
    # Decode the base64 string to bytes
    image_bytes = base64.b64decode(base64_image)
    
    # Convert the bytes to an image
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Preprocess the input data
    image_array = preprocess_input(image)

    # Run inference
    input_name = session.get_inputs()[0].name
    result = session.run(None, {input_name: image_array})

    # Prepare the result
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'result': result[0].tolist()
        })
    }

    return response