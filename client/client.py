from ollama import Client

client = Client(host="http://10.10.110.25:11434")

def chat(prompt,stream_status):
    stream = client.generate(
        model="llama3",
        prompt=prompt,
        stream=stream_status  # this enables streaming
        # logprobs=True
    )
    return stream

