from PIL import Image
from io import BytesIO
import base64

init_image = None

with open("images_scaled/beach_bike.jpg", "rb") as conditioning_image:
    init_image = base64.b64encode(conditioning_image.read()).decode("utf8")

print(init_image[:100])
print(len(init_image))

# with open("images_scaled/beach_bike.text", "w") as text_file:
#     text_file.write(init_image)

# with open("images_scaled/beach_bike.text", "r") as text_file:
#     read_image = text_file.read()    
    
image = Image.open(BytesIO(base64.b64decode(init_image)))
image.show()