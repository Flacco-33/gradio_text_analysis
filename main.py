# Import necessary libraries
import google.generativeai as genai
import json
import gradio as gr
# Configure the API key
import os
apiKey =(os.getenv('Api_GEMINI'))
genai.configure(api_key=apiKey)

#instructions 
modelInstructions ="You will analyze the sentences that I propose to you, which will be in Spanish. Your task consists of six parts:\n1. Emotions: Analyze each sentence and identify the emotions present: joy, sadness, anger, neutrality, anguish, fear, surprise, and frustration. Assign a percentage of intensity to each emotion, making sure that the total sum is 1. The result should be a JSON with this structure: {\"joy\": 0.0, \"sadness\": 0.1, \"anger\": 0.2, \"neutrality\": 0.1, \"anguish\": 0.1, \"fear\": 0.0, \"surprise\": 0.0, \"frustration\": 0.5}.\n2. Professor Analysis: Determine whether the sentence expresses a positive, negative, or neutral opinion about the professor.\n3. ID Extraction:\n3.1 Teacher_ID: Extracts the teacher_id, which is at the end of the sentence after a comma (e.g., \"sentence_text, 20TE0164\").\n3.1 Student_ID: Extracts the student_id, which is at the beginning of the sentence before the colon (e.g., \"20AVC: sentence, idTeacher\").\n4. Sentence Text: Include the full sentence text in the output by removing the teacher_id.\n5. Output Format: Returns a JSON with the following structure:\n{\n\"emotions\": {emotions_result},\n\"sentiment\": {teacher_analysis_result},\n\"teacher_id\": \"teacher_id\",\n\"student_id\": \"student_id\",\n\"comment\": \"sentence_text\"\n}\n6. Response Format: Provides the response in RAW format, without using Markdown.",

# Create the model configuration
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

def analize_text(prompt):
    # Create the GenerativeModel object
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro', # or gemini-1.5-pro or flash
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction=modelInstructions
        )  
    # Generate content from the prompt
    response = model.generate_content([prompt], stream=True)

    # Initialize a buffer to store the response parts
    buffer = []
    # Iterate over the response chunks
    for chunk in response:
        # Iterate over the parts of each chunk
        for part in chunk.parts:
            # Append the text of each part to the buffer
            buffer.append(part.text)
        # clear_output()
        # display(Markdown(''.join(buffer)))
    # Concatenate the buffer to get the complete JSON response
    result_json = ''.join(buffer)
    
    print (result_json)
    # Try to decode the JSON response
    try:
        result_dict = json.loads(result_json)
        if any(value == "" or value is None for value in result_dict.values()):
            return "Error: Empty field found in result_dict"
        #verify result_dict not fields empty
        # Verify if any field is empty in result_dict
        
    # Handle JSON decoding errors
    except json.JSONDecodeError as e:
        result_dict = {}
        return(f"Error al decodificar JSON: {e}")
    # Print the decoded JSON dictionary
    return (result_dict)

# Create the Gradio interface for the model with a text input field and a text output field in json format
gr.Interface(fn=analize_text, inputs="text", outputs="text", title="Gemini API", description="Analyze the sentences that I propose to you, which will be in Spanish. Your task consists of six parts:").launch()
