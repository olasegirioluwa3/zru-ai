from flask import Flask, request, jsonify
from docx import Document
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()
# Initialize OpenAI client
openai_client = OpenAI()

# Extract text content from the Word document
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

# Path to the Word document
docx_file_path = 'my-cv.docx'

# Extract text content from the Word document
document_text = extract_text_from_docx(docx_file_path)

# Define a route to handle user input
@app.route('/ask', methods=['GET'])
def ask():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={ "type": "json_object" },
        max_tokens=50,
        # messages=[
        #     {"role": "system", "content": "You are a helpful assistant designed to output answer in an educational way for Zion Reborn University students."},
        #     {"role": "user", "content": "Who is the world richest man in 2018,2019,2020?"}
        # ]
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to help Zion Reborn University (ZRU) students with tasks, understand if the student intent to make payment, learn about courses offered or academic programs in this json format. example intent: payment|course|program."},
            {"role": "assistant", "content": "if intent is payment: ask a followup question the department and program the student is or aspiring for at Zion Reborn University then generate a tuition fee for the user."},
            {"role": "user", "content": "How much is the university tuition fee?"}
        ]
    )
    print(response.choices[0].message.content)
    # Return the response
    return jsonify({'response': response.choices[0].message.content})

if __name__ == '__main__':

    app.run(debug=True)
