import ollama

response = ollama.chat(
    model='mistral',
    messages=[
        {'role': 'user', 'content': 'Write a cold email to a Web3 influencer for a product collaboration.'}
    ]
)

print(response['message']['content'])
