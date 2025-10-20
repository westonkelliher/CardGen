import base64
from openai import OpenAI

with open(".key") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)


img = client.images.generate(
    model="dall-e-2",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024"
)

print(img.created)
print(img.output_format)
print(img.quality)
print(img.size)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)
