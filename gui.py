import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter as ctk
from fpdf import FPDF

# Constants for reusability and maintainability
PADDING = 90
WIDTH = 500

class GUI(ctk.CTk):
    """User Information Form GUI using CustomTkinter."""
    def __init__(self):
        super().__init__()
        self.title("User Information Form")
        self.geometry("700x600")
        self.formatted_data = ''  # To store the formatted data string

        # Setting appearance mode and color theme
        ctk.set_appearance_mode("dark")  # "dark" or "light"
        ctk.set_default_color_theme("dark-blue")

        # Create notebook (tabs container)
        self.create_notebook()

        # Create tabs for each form section
        self.create_page1()
        self.create_page2()
        self.create_page3()
        self.create_page4()
        self.create_page5()

    def create_notebook(self):
        """Initialize the notebook to hold multiple tabs."""
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(expand=True, fill="both")

        # Add tabs for each form section
        for tab_name in ["Personal Details", "Academics", "Family Details", "Interests", "Activities"]:
            self.notebook.add(tab_name)

    def create_label_and_entry(self, parent, text, entry_var_name):
        """Helper method to create label and entry field."""
        ctk.CTkLabel(parent, text=text).pack(pady=1, padx=PADDING, anchor='w')
        entry_var = ctk.CTkEntry(parent, width=WIDTH)
        entry_var.pack(pady=5, padx=PADDING, anchor='w')
        setattr(self, entry_var_name, entry_var)

    def create_label_and_combo_box(self, parent, text, values, combo_var_name):
        """Helper method to create label and combobox field."""
        ctk.CTkLabel(parent, text=text).pack(pady=1, padx=PADDING, anchor='w')
        combo_var = ctk.CTkComboBox(parent, values=values)
        combo_var.pack(pady=5, padx=PADDING, anchor='w')
        setattr(self, combo_var_name, combo_var)

    def create_page1(self):
        """Create the Personal Details form (Page 1)."""
        page_frame = self.create_page_frame("Personal Details")
        self.create_label_and_entry(page_frame, "Full Name:", "full_name")
        self.create_label_and_combo_box(page_frame, "Gender:", ["Male", "Female", "Other"], "gender")
        self.create_label_and_entry(page_frame, "Date of Birth (DD-MM-YYYY):", "dob")
        self.create_label_and_entry(page_frame, "Country:", "country")
        self.create_label_and_entry(page_frame, "City:", "city")

    def create_page2(self):
        """Create the Academics form (Page 2)."""
        page_frame = self.create_page_frame("Academics")
        self.create_label_and_entry(page_frame, "Class:", "academic_class")
        self.create_label_and_entry(page_frame, "Educational Board:", "education_board")
        self.create_label_and_entry(page_frame, "10th Marks (%):", "marks_10")
        self.create_label_and_entry(page_frame, "11th Marks (%):", "marks_11")
        self.create_label_and_entry(page_frame, "Stream:", "stream")
        self.create_label_and_entry(page_frame, "Entrance Exam Preparation:", "exam_prep")
        self.create_label_and_combo_box(page_frame, "Study Abroad:", ["Yes", "No"], "abroad_study")

    def create_page3(self):
        """Create the Family Details form (Page 3)."""
        page_frame = self.create_page_frame("Family Details")
        self.create_label_and_entry(page_frame, "Father's Name:", "father_name")
        self.create_label_and_entry(page_frame, "Mother's Name:", "mother_name")
        self.create_label_and_entry(page_frame, "Father's Occupation:", "father_occupation")
        self.create_label_and_entry(page_frame, "Mother's Occupation:", "mother_occupation")
        self.create_label_and_entry(page_frame, "Father's Annual Income:", "father_income")

    def create_page4(self):
        """Create the Interests form (Page 4)."""
        page_frame = self.create_page_frame("Interests")
        self.create_label_and_entry(page_frame, "What do you want to become in the future?", "future_goal")
        self.create_label_and_entry(page_frame, "Interest Field Areas:", "interest_areas")
        self.create_label_and_entry(page_frame, "Sports:", "sports")
        self.create_label_and_entry(page_frame, "CS Interests:", "cs_interests")
        self.create_label_and_entry(page_frame, "Community Service that you have offered:", "community_service")
        self.create_label_and_entry(page_frame, "Entrepreneurship Interests:", "entrepreneurship_interests")

    def create_page5(self):
        """Create the Activities form (Page 5)."""
        page_frame = self.create_page_frame("Activities")
        self.create_label_and_entry(page_frame, "What skills do you have?", "skills")
        self.create_label_and_entry(page_frame, "Activity 1:", "activity1")
        self.create_label_and_entry(page_frame, "Activity 2:", "activity2")
        self.create_label_and_entry(page_frame, "Activity 3:", "activity3")

        # Submit button and warning text box
        submit_button = ctk.CTkButton(page_frame, text="Submit", command=self.submit_form, width=150, height=30)
        submit_button.pack(pady=20)
        self.message_box = ctk.CTkTextbox(page_frame, height=2, width=WIDTH, state='disabled')
        self.message_box.pack(pady=5)

    def create_page_frame(self, tab_name):
        """Helper method to create frame for each tab."""
        page_frame = ctk.CTkFrame(self.notebook.tab(tab_name))
        page_frame.pack(expand=True, fill="both")
        content_frame = ctk.CTkFrame(page_frame, fg_color='transparent')
        content_frame.pack(expand=True)
        return content_frame

    def submit_form(self):
        """Collect form data, format it, and generate a PDF."""
        try:
            # Check if all fields are filled
            if not all([
                self.full_name.get(),
                self.gender.get(),
                self.dob.get(),
                self.country.get(),
                self.city.get(),
                self.academic_class.get(),
                self.education_board.get(),
                self.marks_10.get(),
                self.marks_11.get(),
                self.stream.get(),
                self.exam_prep.get(),
                self.abroad_study.get(),
                self.father_name.get(),
                self.mother_name.get(),
                self.father_occupation.get(),
                self.mother_occupation.get(),
                self.father_income.get(),
                self.future_goal.get(),
                self.interest_areas.get(),
                self.sports.get(),
                self.cs_interests.get(),
                self.community_service.get(),
                self.entrepreneurship_interests.get(),
                self.skills.get(),
                self.activity1.get(),
                self.activity2.get(),
                self.activity3.get(),
            ]):
                self.message_box.configure(state='normal')  # Enable the text box
                self.message_box.delete(1.0, tk.END)  # Clear previous messages
                self.message_box.insert(tk.END, "Please fill all the fields before submitting.")
                self.message_box.configure(state='disabled')  # Disable the text box
                return  # Exit if validation fails

            # If all fields are filled, clear any error messages
            self.message_box.configure(state='normal')  # Enable the text box
            self.message_box.delete(1.0, tk.END)  # Clear previous messages
            self.message_box.insert(tk.END, "Form submitted successfully!")  # You can update this message as needed
            self.message_box.configure(state='disabled')  # Disable the text box


            personal_details = (
                f"Full Name: {self.full_name.get()}\n"
                f"Gender: {self.gender.get()}\n"
                f"Country: {self.country.get()}\n"
                f"City: {self.city.get()}\n"
                f"Date of Birth: {self.dob.get()}\n"
            )

            academics = (
                f"Class: {self.academic_class.get()}\n"
                f"Educational Board: {self.education_board.get()}\n"
                f"10th Marks: {self.marks_10.get()}%\n"
                f"11th Marks: {self.marks_11.get()}%\n"
                f"Stream: {self.stream.get()}\n"
                f"Entrance Exam Preparation: {self.exam_prep.get()}\n"
                f"Study Abroad: {self.abroad_study.get()}\n"
            )

            family_details = (
                f"Father's Name: {self.father_name.get()}\n"
                f"Mother's Name: {self.mother_name.get()}\n"
                f"Father's Occupation: {self.father_occupation.get()}\n"
                f"Mother's Occupation: {self.mother_occupation.get()}\n"
                f"Father's Annual Income: {self.father_income.get()}\n"
            )

            interests = (
                f"Future Goal: {self.future_goal.get()}\n"
                f"Interest Field Areas: {self.interest_areas.get()}\n"
                f"Sports: {self.sports.get()}\n"
                f"CS Interests: {self.cs_interests.get()}\n"
                f"Community Service: {self.community_service.get()}\n"
                f"Entrepreneurship Interests: {self.entrepreneurship_interests.get()}\n"
            )

            activities = (
                f"Skills: {self.skills.get()}\n"
                f"Activity 1: {self.activity1.get()}\n"
                f"Activity 2: {self.activity2.get()}\n"
                f"Activity 3: {self.activity3.get()}\n"
            )

            # Combine all sections
            self.formatted_data = personal_details + academics + family_details + interests + activities
            print(self.formatted_data)
            #Generate and save a PDF from the collected form data.
            pdf = FPDF()
            pdf.add_page()

            # Set font and margins
            pdf.set_font("Arial", size=12)

            # Add formatted data to the PDF
            for line in self.formatted_data.split("\n"):
                if ':' in line:
                    # Split into label and value
                    label, value = line.split(':', 1)
                    
                    # Dynamically calculate the width for the label based on its length
                    label_width = pdf.get_string_width(f"{label.strip()}:") + 8 

                    # Write the label in bold
                    pdf.set_font("Arial", style='B', size=12)
                    pdf.cell(label_width, 10, f"{label.strip()}:", ln=0)  # Dynamically set label width
                    
                    # Write the value in regular font
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, f"{value.strip()}", ln=1)  # Move to next line after value
                else:
                    # If no colon, write the line as-is
                    pdf.cell(190, 10, line, ln=1)


            # Save the PDF to a file
            pdf.output("Roadmap.pdf")

        except Exception as e:
            print(f"Error: {e}")
        # Close the window and stop the main loop
        self.destroy()
        return
            
    def get_data(self):
        # Start the main loop when this method is called
        self.mainloop()
        print(self.formatted_data)
        # After the main loop ends, return the formatted data
        return self.formatted_data           

if __name__ == "__main__":
    app = GUI()
    app.mainloop()

