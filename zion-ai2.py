from flask import Flask, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI()

@app.route('/answer', methods=['GET'])
def answer():
    # Create an assistant for joke-telling
    assistant = client.beta.assistants.create(
        name="Joke Teller",
        description="You are a famous comedian, known for making jokes about dogs.",
        model="gpt-4-1106-preview",  # Use the cheapest model
        tools=[],
        file_ids=[]
    )

    # Upload assistant documents (PDFs, Word docs, etc.)
    # assistant.documents.create(
    #     file="./my-cv.pdf",  # Specify the path to your PDF document
    #     purpose="assistant"  # Specify the purpose as "assistant"
    # )
    # assistant.documents.create(
    #     file="./my-cv.docx",  # Specify the path to your Word document
    #     purpose="assistant"  # Specify the purpose as "assistant"
    # )

    # Create a thread with a user message requesting a joke about cats
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Tell a joke about cats",
                "file_ids": []  # You can include file IDs if needed
            }
        ]
    )

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Retrieve the response from the Assistant's run
    response = run['data'][0]['message']['content']

    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)
