import os
import json
from flask import Flask, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI()

@app.route('/answer', methods=['GET'])
def answer():
    assistant_file_path = 'assistant.json'

    # If there is an assistant.json file already, then load that assistant
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
            
            # Retrieve the assistant object to check if retrieval tool is enabled
            assistant = client.beta.assistants.retrieve(assistant_id)
            
            if 'retrieval' not in assistant.tools:
                # Update the assistant to enable retrieval tool
                assistant = client.beta.assistants.update(assistant_id, tools=[{"type": "retrieval"}])
                print("Retrieval tool enabled for the assistant.")
    else:
        file = client.files.create(file=open("my-cv.docx", "rb"),
                                purpose='assistants')
        # Create an assistant for joke-telling
        assistant = client.beta.assistants.create(
            name="HR Assistant",
            description="You are an organization HR support, and you have assistant document to help you with sample CV, you also give advice",
            model="gpt-4-1106-preview",  # Use the cheapest model
            tools=[{"type": "retrieval"}],  # Enable the retrieval tool
            file_ids=[file.id]
        )
        # Create a new assistant.json file to load on future runs
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

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

    # # Add the user's message to the thread
    # client.beta.threads.messages.create(thread_id=thread.id,
    #                                   role="user",
    #                                   content="write me a poem on joke")

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_input)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                            assistant_id=assistant_id)

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                    run_id=run.id)
        # print(f"Run status: {run_status.status}")
        if run_status.status == 'completed':
            break
        elif run_status.status == 'requires_action':
            # Handle the function call
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "create_lead":
                    # Process lead creation
                    arguments = json.loads(tool_call.function.arguments)
                    output = functions.create_lead(arguments["name"], arguments["phone"],
                                                    arguments["address"])
                    client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                                run_id=run.id,
                                                                tool_outputs=[{
                                                                    "tool_call_id":
                                                                    tool_call.id,
                                                                    "output":
                                                                    json.dumps(output)
                                                                }])
                    
        time.sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[-1].content[0].text.value
    print(response)

    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)
