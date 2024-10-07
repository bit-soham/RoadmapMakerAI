""" 
    Here are  we are putting all the things together (GUI, LLM model, embedder, prompts created and generating the actual
roadmap for the student which will then added to the the roadmap.pdf file
"""

from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
import pandas as pd # type: ignore
import torch # type: ignore
import os
from llm import llm
from gui import GUI
from embedder import Embedding_Generator
from prompts import Prompt_Generator, RoadMapGenerator
from fpdf import FPDF

root_directory = '/python_project/'

# List of all files and directories in the root directory
for root, dirs, files in os.walk(root_directory):
    for file in files:
        print(os.path.join(root, file))

existing_path = "Data/"
files_dict = {
    "Art and Music Extracurriculars and Art Competitions":  pd.read_csv(f"{existing_path}Art_Music_Extracurriculars_Art_Competitions.csv"),
    "Computer Science Extracurriculars and Competitions" :  pd.read_csv(f"{existing_path}computer_science_extracurricular.csv"),
    "Physics and Astronomy Extracurriculars" :  pd.read_csv(f"{existing_path}phy_astr_extracurricular.csv"),
    "Computer Science Extracurricular and Competitions" :  pd.read_csv(f"{existing_path}computer_science_extracurricular.csv"),
    "Advanced research journals" : pd.read_csv(f"{existing_path}advanced__research_journals.csv"),
    "Law and Economic competitions" : pd.read_csv(f"{existing_path}law_economic_comptetions.csv"),
    "Camp Programs" : pd.read_csv(f"{existing_path}camp_programs.csv"),
    "Awards" : pd.read_csv(f"{existing_path}Awards.csv"),
    "Biology Competitions and Extracurriculars" : pd.read_csv(f"{existing_path}biology_competitions_extracurriculars.csv"),
    "International Math Competitions" : pd.read_csv(f"{existing_path}math_comp_international.csv"),
    "Volunteering Non Government Organizations" : pd.read_csv(f"{existing_path}ngos.csv"),
    "Music Competitions" : pd.read_csv(f"{existing_path}music_competitions.csv"),
    "Highschool Research Journals" : pd.read_csv(f"{existing_path}highschool_research_journal.csv"),
    "Art and Music Extracurriculars and Art Competitions" : pd.read_csv(f"{existing_path}Art_Music_Extracurriculars_Art_Competitions.csv"),
    "Physics and Astronomy Extracurriculars" : pd.read_csv(f"{existing_path}phy_astr_extracurricular.csv"),
    "Business and entrepreneurship Opportunities" : pd.read_csv(f"{existing_path}business_entrepreneurship.csv"),
    "Scholarships" : pd.read_csv(f"{existing_path}scholarships.csv"),
    "Sports extracurriculars" : pd.read_csv(f"{existing_path}Sports_extracurriculars.csv"),
    "Summer Camps" : pd.read_csv(f"{existing_path}summer_camps.csv")
}

# initiationg the gui
user_interface = GUI()
# getting the data from the gui
student_data = user_interface.get_data()


# checking the availablity 
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



def conv_input_to_text(student_data):
    user_prompt = f""" The student details are {student_data}
                """
    system_prompt = """You only output what the user asks you to nothing extra and you can compress information without losing any information
                     and you now how to highlight and distribute important features about that can be important when creating roadmap for a student
                    You will be given a query that contains student information in a field-wise format. Your task is to convert this structured data into a single,
                    coherent paragraph that presents all the student information clearly and accurately.
                    Ensure that the paragraph is well-organized, and includes all relevant details about the student. Only output the paragraph and nothing else
                    """
    return llm(user_prompt, system_prompt)

student_input = conv_input_to_text(student_data)

# start month and year
month = 4
year = '2023'

# generating the embedding for the data files
embedder = Embedding_Generator(files_dict)

for file_names in files_dict.keys():
    print(file_names, embedder.context_embeddings[file_names].shape)

t = embedder.filenames_embeddings


# getting the prompt 
prompt_generator = Prompt_Generator(embedder, student_input, files_dict, month, year)
prompt = prompt_generator.generate_prompt(12)

# getting the number of events done
no_of_events = prompt_generator.No_of_events

# initializing the RoadMapGenerator
Roadmap_Generator = RoadMapGenerator(prompt, student_input, no_of_events)
# getting roadmap from the generator
roadmap = Roadmap_Generator.generate_roadmap()

print(roadmap)

#gettinng the roadmap text to append in the pdf
content_to_append = roadmap
existing_pdf_file = 'Roadmap.pdf'

# read from the existing Roadmap.pdf
reader = PdfReader(existing_pdf_file)
# initialize the writer
writer = PdfWriter()

# Add all pages from the existing PDF to the writer
for page in reader.pages:
    writer.add_page(page)

# Create a new page for the content to append
pdf = FPDF()
pdf.add_page()

# Add a title
pdf.set_font("Arial", 'B', size=20)  
pdf.cell(0, 10, 'Student Roadmap', ln=True, align='C')  
# Add a line break after the title
pdf.ln(10)  

# Set fonts for the content
pdf.set_font("Arial", size=12)

# Parse the data and write it to the PDF in the desired format
data = roadmap.split('\n')

for line in data:
    if ':' in line:
        # Split into label and value
        label, value = line.split(':', 1)
        
        # Dynamically calculate the width for the label based on its length
        label_width = pdf.get_string_width(f"{label.strip()}:") + 2  # Add some padding

        # Write the label in bold
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(label_width, 10, f"{label.strip()}:", ln=0)  # Dynamically set label width
        
        # Write the value in regular font
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"{value.strip()}", ln=1)  # Move to next line after value
    else:
        # If no colon, write the line as-is
        pdf.cell(190, 10, line, ln=1)

# generator the temperory pdf file to write the roadmap info
temp_pdf_file = "temp_page.pdf"
pdf.output(temp_pdf_file)

# Read the temporary file to append it 
new_reader = PdfReader(temp_pdf_file)
for page in new_reader.pages:
    writer.add_page(page)

# Write out the combined PDF [student info that he provided and the Roadmap for him]
with open(existing_pdf_file, "wb") as output_pdf:
    writer.write(output_pdf)


# Clean up the temporary file
try:
    os.remove(temp_pdf_file)
except OSError as e:
    print(f"Error removing file: {e}")