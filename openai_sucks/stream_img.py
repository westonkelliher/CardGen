from openai import OpenAI

client = OpenAI()

stream = client.images.generate(
    model="dall-e-2",
    prompt="A cute baby sea otter",
    n=1,
    size="1024x1024",
    stream=True
)

for event in stream:
    print(event)
