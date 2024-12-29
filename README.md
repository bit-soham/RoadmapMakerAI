This is a project made by me and Soham T Umbare
# Roadmap Generator AI: Generates a Roadmap according to the student input data
It is the rag based ai model which leverages the misteral-7b model to generate the roadmap for the student information provided. 

## How to run the model

Run the following in the terminal to run the code
    git clone https://github.com/theSohamTUmbare/RoadmapMakerAI.git
    pip install -r requirements.txt
    Get a hugging face inference api token and put it as the token variable in llm.py
    python roadmap.py


## Key Features
- User-friendly GUI for entering student details
- Roadmap tailored to the user using best events/workshops from accross the world

## Usage
    Academic Planning: Helps students create a structured roadmap for academic success, aligning their goals with relevant events, competitions, and opportunities.
    Time Management: Enables students to effectively plan their participation in various extracurricular activities, improving time management and productivity.
    Career Development: Assists students in identifying skill-building opportunities that enhance their resumes and career prospects.
    Personalized Guidance: Provides tailored recommendations based on individual interests and academic progress, fostering personal and professional growth.
    Opportunity Awareness: Raises awareness about available opportunities that students might otherwise overlook, maximizing engagement.
## File Descriptions:
    1. embedders.py: The embedders.py file defines an Embedding_Generator class that generates and saves embeddings for file names and contexts using the Facebook DPR model. It handles loading existing embeddings from disk or creating new ones if unavailable.
    2. gui.py: The gui.py file implements a user information form using CustomTkinter, featuring multiple tabs for personal details, academics, family details, interests, and activities. Upon submission, it validates the input, formats the collected data, and generates a PDF document containing the user's information.
    3. llm.py: The llm.py file defines a class for interacting with a Large Language Model (LLM) via the Hugging Face Hub, including methods for sending queries, receiving responses, and decoding streamed data. It features robust logging for error tracking and can handle retries in case of communication failures.
    4. prompts.py: The prompts.py file contains a Prompt_Generator class that constructs tailored prompts for a student roadmap based on their input, events, and progress, utilizing a language model to suggest relevant sectors and events. It also includes a RoadMapGenerator class to generate a comprehensive roadmap detailing monthly tasks, guidelines, and strategies for maintaining balance and achieving the student’s goals.
    5. roadmap.py: The roadmap.py file integrates the GUI, LLM model, and embedding generator to create a personalized student roadmap based on input data, generated prompts, and events. It appends the generated roadmap to an existing PDF file, formatting the content appropriately before combining it with previous data.
