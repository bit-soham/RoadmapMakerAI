from fpdf import FPDF
import textwrap

data = """
Guidelines -
1. Maintaining a balanced lifestyle, avoiding burnout, and building self-discipline are key to your success. Remember to prioritize self-care, mental health, and discipline.
2. Establish a consistent routine that includes regular exercise, meditation, social activities, and relaxation techniques. 
3. Monitor your stress levels and take breaks when necessary.
4. Develop good study habits such as setting a study schedule, creating a designated workspace, and avoiding distractions.  
5. Stay organized and keeptrack of deadlines, requirements, and preparations for upcoming events.
6. Make networking a priority. Connect with professionals in your field of interest and stay updated with the latest developments in your chosen subjects.
7. Be proactive in seeking opportunities, such as learning a new language or engaging in online courses.
8. Adapt your strategies and plans regularly based on your learning and experiences.
9. Set clear goals and work towards them with persistence and determination.

Main checklist to complete for application -
- Research and select universities where you wish to study abroad.
- Check eligibility criteria, application deadlines, and required documents for each university.
- Gather all necessary documents, including transcripts, test scores, and letters of recommendation.
- Prepare personal statements that clearly articulate your goals, achievements, and why you are a strong fit for the chosen universities.
- Start applying to your chosen universities as early as possible to increase your chances of admission.

Monthly Tasks -

April -
1. Begin researching study abroad opportunities and select universities that align with your goals. (website: https://www.educationusa.state.gov/)
2. Start preparing personal statements focusing on your goals, achievements, and motivation for studying abroad.
3. Take language exams such as the TOEFL or IELTS as required by your chosen universities.
4. Start gathering all necessary documents such as transcripts, test scores, and letters of recommendation.

May -
1. Register for the SAT or ACT as required by your chosen universities.
2. Review application deadlines for your chosen universities and ensure you have all necessary documents ready.
3. Begin preparing for entrance exams with a focus on subjects relevant to your chosen field of study.
4. Attend Regeneron international sciences and engineering fair(ISEF) to showcase your talent and engage with like-minded individuals. (website: https://www.societyforscience.org/isef)

June -
1. Finalize your university applications.
2. Review all application materials to ensure accuracy and completeness.
3. Network with professionals in your field of interest and stay updated with the latest developments.
4. Participate in Plan International to make a positive impact on the world and showcase your commitment to community service. (website: https://planinternational.org/)

July -
1. Attend the Global Social Leaders World Summit to hone your leadership and social entrepreneurship skills. (website: https://www.globalsocialleaders.com)
2. Brainstorm business ideas and start researching potential markets.
3. Continue preparing for entrance exams with a focus on math, science, and critical-thinking skills.
4. Take a break and engage in relaxation and social activities to avoid burnout.

August -
1. Register for the Biogenius competition to showcase your skills in the field of biotechnology. (website: https://www.biogenius.de)
2. Hone your presentation skills and prepare for competition presentations.
3. Attend networking events and conferences to meet industry professionals.
4. Take a break and engage in physical activities to stay healthy.

September -
1. Register for the American Collegiate Programming Contest (ACPC) regional competition. (website: https://www.acsl.org)    
2. Review algorithms and problem-solving strategies to prepare for the upcoming competition.
3. Connect with professionals in the field of computer science and seek advice on potential career paths.
4. Participate in AIESEC to gain cross-cultural leadership experience and volunteer opportunities. (website: https://www.aiesec.org/)

October -
1. Attend the American Collegiate Programming Contest (ACPC) regional competition.
2. Review feedback from the regional competition and adjust strategies as necessary.
3. Attend relevant webinars and online courses to stay updated on the latest developments in computer science.
4. Network with professionals in the field of entrepreneurship and seek advice on how to launch a business.

November -
1. Register for the World Trade Organization (WTO) Model to gain experience in trade negotiations and dispute resolution. (website: https://www.wto.org)
2. Review economic theories and global trade agreements to prepare for the competition.
3. Attend the Young Entrepreneurs Challenge pitch competition to gain experience in presenting business ideas. (website: https://yechallenge.com)
4. Take a break and engage in self-reflection, setting new goals for personal and professional growth.

December -
1. Attend the Biogenius competition for a chance to showcase your skills in biotechnology.
2. Review feedback from the Biogenius competition and adjust strategies as necessary.
3. Network with professionals in the field of biotechnology and seek advice on potential career paths.
4. Take a break and enjoy the holiday season, recharging your mind and body for the upcoming year.

January -
1. Register for the Regeneron international sciences and engineering fair(ISEF) to showcase your talent and engage with like-minded individuals. (website: https://www.societyforscience.org/isef)
2. Review applications for scholarships and fellowships.
3. Network with professionals in your field of interest and seek advice on potential career paths.
4. Attend relevant online courses to stay updated on the latest developments in your chosen subjects.

February -
1. Attend the Codingame platform to participate in coding competitions and develop programming skills. (website: https://www.codingame.com)
2. continued networking and learning opportunities will be available throughout the year, ensuring you stay at the forefront of your field and connected with professionals.
3. Take a break and engage in self-reflection, setting new goals for personal and professional growth.
4. Establish a consistent routine for exercise and self-care to maintain optimal mental and physical health.
"""

# Split data by newlines to preserve original paragraph structure
data_lines = data.split('\n')

# Create a new PDF object
pdf = FPDF()
pdf.add_page()

# Add a title
pdf.set_font("Arial", 'B', size=20)
pdf.cell(0, 10, 'Student Roadmap', ln=True, align='C')
pdf.ln(10)

# Set font for content
pdf.set_font("Arial", size=12)

# Function to add text to the PDF with word wrapping and preserving newlines
def add_wrapped_text(pdf, text, width, is_month=False):
    if is_month:
        pdf.set_font("Arial", style='B', size=12)  # Set bold font for month
        pdf.ln(5)  # Larger margin above
    wrapped_text = textwrap.fill(text, width=width)
    pdf.multi_cell(0, 10, wrapped_text)
    if is_month:
        pdf.ln(5)  # Larger margin below
        pdf.set_font("Arial", size=12)  # Reset to regular font

# Define a list of month names
months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December",
          "january", "february", "march", "april", "may", "june", 
          "july", "august", "september", "october", "november", "december"]

# Loop through each line in data_lines, wrap and add it to the PDF
for line in data_lines:
    if line.strip():  # Non-empty lines
        # Check if the line starts with a month name
        if any(month in line for month in months):
            add_wrapped_text(pdf, line, 103, is_month=True)
        else:
            add_wrapped_text(pdf, line, 103, is_month=False)
    else:
        pdf.ln(0)  # Add a small line break for empty lines (paragraph breaks)

# Output the PDF to a file
temp_pdf_file = "temp_page.pdf"
pdf.output(temp_pdf_file)