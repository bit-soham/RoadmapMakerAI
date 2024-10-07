import pandas as pd # type: ignore
import torch # type: ignore
import os
from llm import llm
from gui import GUI
from embedder import Embedding_Generator
from prompts import Prompt_Generator, RoadMapGenerator
from fpdf import FPDF

root_directory = '/python_project/'

# List all files and directories in the root directory
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

user_interface = GUI()
student_data = user_interface.get_data()



# Load the question encoder and its corresponding tokenizer


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


# student_input = """
#                 Lakshya Tanwar is a 12th-grade student from Bhopal, India, born on 5th July 2008. His gender is male.
#                  He studies under the CBSE board in the PCM stream, with 80% in 10th grade and 82% in 11th grade.
#                  Preparing for IIT-JEE, Lakshya aims to pursue Computer Science at IIT Bombay.
#                  He is catching up on Chemistry due to missed lessons and finds both Chemistry and Physics challenging.
#                  His long-term goal is to become a Software Engineer at Google, with interests in
#                  AI, web development, sports (Football, Basketball, Chess), community service, and entrepreneurship.
#                 Lakshya’s father earns INR 500,000 annually. Lakshya has skills in communication, marketing, Python,
#                 and web development. His extracurriculars include founding "Needy Binders" (providing food to the needy),
#                 interning as a Marketing Intern at "Cross The Skylimits," and co-founding "Nutrifido" (dog care and medication).
#                 He also aspires to launch AI-related startups and contribute to Ed-tech and animal welfare.
#                 """
month = 4
year = '2023'


embedder = Embedding_Generator(files_dict)

for file_names in files_dict.keys():
    print(file_names, embedder.context_embeddings[file_names].shape)

t = embedder.filenames_embeddings
t.size()

torch.save(embedder.context_embeddings, 'context_embeddings.pth')



prompt_generator = Prompt_Generator(embedder, student_input, files_dict, month, year)
prompt = prompt_generator.generate_prompt(12)

# TODO Make a prompt to generate the prompt for the events and make

# prompt = prompt_generator.generate_prompt(12)


no_of_events = prompt_generator.No_of_events

print(prompt)



Roadmap_Generator = RoadMapGenerator(prompt, student_input, no_of_events)
roadmap = Roadmap_Generator.generate_roadmap()


print(f"{roadmap=}")
# Create a PDF file
pdf = FPDF()
pdf.add_page()

# Add a title
pdf.set_font("Arial", 'B', size=20)  # Set font for title (bold, larger size)
pdf.cell(0, 10, 'Student Information', ln=True, align='C')  # Left align the title
pdf.ln(10)  # Add a line break after the title

# Set fonts for the content
pdf.set_font("Arial", size=12)

# Parse the data and write it to the PDF in the desired format
data = roadmap.split('\n')

for line in data:
    if ':' in line:
        # Separate label and value
        label, value = line.split(':', 1)

        # Write the label in bold
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(50, 10, f"{label.strip()}:", ln=0)  # Set a fixed width for the label cell
        
        # Write the value in regular font
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"{value.strip()}", ln=1)  # Remaining width for the value cell

# Save the PDF with the name 'Roadmap.pdf'
pdf.output("Roadmap.pdf")

# reader = PdfReader('Roadmap.pdf')
# writer = PdfWriter()

# # Add all pages from the existing PDF to the writer
# for page in reader.pages:
#     writer.add_page(page)

# # Create a new page for the content you want to append
# pdf = FPDF()
# pdf.add_page()

# # Add a title to the new page
# pdf.set_font("Arial", 'B', size=20)  # Set font for title (bold, larger size)
# pdf.cell(0, 10, 'Suggested Roadmap', ln=True, align='C')  # Center align the title
# pdf.ln(10)  # Add a line break after the title

# # Set fonts for the content
# pdf.set_font("Arial", size=12)

# # Write the new content directly to the PDF
# for line in content_to_append.split('\n'):
#     if ':' in line:
#         # Separate label and value
#         label, value = line.split(':', 1)

#         # Write the label in bold
#         pdf.set_font("Arial", style='B', size=12)
#         pdf.cell(50, 10, f"{label.strip()}:", ln=0)  # Set a fixed width for the label cell
        
#         # Write the value in regular font
#         pdf.set_font("Arial", size=12)
#         pdf.cell(0, 10, f"{value.strip()}", ln=1)  # Remaining width for the value cell

# # Save the new page to a temporary file
# temp_pdf_file = "temp_page.pdf"
# pdf.output(temp_pdf_file)

# # Read the temporary file to append it
# new_reader = PdfReader(temp_pdf_file)
# for page in new_reader.pages:
#     writer.add_page(page)

# # Write out the combined PDF
# with open(existing_pdf_file, "wb") as output_pdf:
#     writer.write(output_pdf)

# # Clean up the temporary file
# import os
# os.remove(temp_pdf_file)
