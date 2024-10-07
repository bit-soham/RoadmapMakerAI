import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter as ctk
from fpdf import FPDF

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("User Information Form")
        self.geometry("700x600")
        self.formatted_data = ''  # To store the formatted data string

        # Set appearance mode and color theme

        
        ctk.set_appearance_mode("dark")  # "dark" or "light"
        ctk.set_default_color_theme("dark-blue")  # You can also use "green" or "dark-blue"
        
        
        # Set up a notebook to hold multiple tabs (one tab for each form page)
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(expand=True, fill="both")

        # Adding pages to the notebook
        self.notebook.add("Personal Details")  # Adding tabs without the 'text' keyword argument
        self.notebook.add("Academics")
        self.notebook.add("Family Details")
        self.notebook.add("Interests")
        self.notebook.add("Activities")

        # Access the pages by tab name
        self.page1 = self.notebook.tab("Personal Details")
        self.page2 = self.notebook.tab("Academics")
        self.page3 = self.notebook.tab("Family Details")
        self.page4 = self.notebook.tab("Interests")
        self.page5 = self.notebook.tab("Activities")

        # Create form fields for each page
        self.create_page1()
        self.create_page2()
        self.create_page3()
        self.create_page4()
        self.create_page5()
        
    def toggle_mode(self):
        if ctk.get_appearance_mode() == "light":
            ctk.set_appearance_mode("dark")
            self.mode_switch.configure(text="Light Mode")
        else:
            ctk.set_appearance_mode("light")
            self.mode_switch.configure(text="Dark Mode")

        

    def create_page1(self):
        # Personal Details Form (Page 1)
        page1_frame = ctk.CTkFrame(self.notebook.tab("Personal Details"))  # Correct way to access the tab
        page1_frame.pack(expand=True, fill="both")
        
        content_frame = ctk.CTkFrame(page1_frame, fg_color='transparent')
        content_frame.pack(expand=True)     # This frame will take up all available space
        
        ctk.CTkLabel(content_frame, text="Full Name:").pack(pady=1,  padx=90, anchor='w')
        self.full_name = ctk.CTkEntry(content_frame, width=500)
        self.full_name.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Gender:").pack(pady=1,  padx=90, anchor='w')
        self.gender = ctk.CTkComboBox(content_frame, values=["Male", "Female", "Other"])
        self.gender.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Date of Birth (DD-MM-YYYY):").pack(pady=1,  padx=90, anchor='w')
        self.dob = ctk.CTkEntry(content_frame)
        self.dob.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Country:").pack(pady=1,  padx=90, anchor='w')
        self.country = ctk.CTkEntry(content_frame, width=500)
        self.country.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="City:").pack(pady=1,  padx=90, anchor='w')
        self.city = ctk.CTkEntry(content_frame, width=500)
        self.city.pack(pady=5,  padx=90, anchor='w')

    def create_page2(self):
        page2_frame = ctk.CTkFrame(self.notebook.tab("Academics"))  # Correct way to access the tab
        page2_frame.pack(expand=True, fill="both")
        
        content_frame = ctk.CTkFrame(page2_frame, fg_color='transparent')
        content_frame.pack(expand=True)  
        # Academics Form (Page 2)
        ctk.CTkLabel(content_frame, text="Class:").pack(pady=1,  padx=90, anchor='w')
        self.academic_class = ctk.CTkEntry(content_frame, width=500)
        self.academic_class.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Educational Board:").pack(pady=1,  padx=90, anchor='w')
        self.education_board = ctk.CTkEntry(content_frame, width=500)
        self.education_board.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="10th Marks (%):").pack(pady=1,  padx=90, anchor='w')
        self.marks_10 = ctk.CTkEntry(content_frame)
        self.marks_10.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="11th Marks (%):").pack(pady=1,  padx=90, anchor='w')
        self.marks_11 = ctk.CTkEntry(content_frame)
        self.marks_11.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Stream:").pack(pady=1,  padx=90, anchor='w')
        self.stream = ctk.CTkEntry(content_frame)
        self.stream.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Are you preparing for any entrance examination?").pack(pady=1,  padx=90, anchor='w')
        self.exam_prep = ctk.CTkEntry(content_frame, width=500)
        self.exam_prep.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Do you want to study abroad?").pack(pady=1,  padx=90, anchor='w')
        self.abroad_study = ctk.CTkComboBox(content_frame, values=["Yes", "No"])
        self.abroad_study.pack(pady=5,  padx=90, anchor='w')

    def create_page3(self):
        page2_frame = ctk.CTkFrame(self.notebook.tab("Family Details"))  # Correct way to access the tab
        page2_frame.pack(expand=True, fill="both")
        
        content_frame = ctk.CTkFrame(page2_frame, fg_color='transparent')
        content_frame.pack(expand=True)  
        # Family Details Form (Page 3)
        ctk.CTkLabel(content_frame, text="Father's Name:").pack(pady=1,  padx=90, anchor='w')
        self.father_name = ctk.CTkEntry(content_frame, width=500)
        self.father_name.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Mother's Name:").pack(pady=1,  padx=90, anchor='w')
        self.mother_name = ctk.CTkEntry(content_frame, width=500)
        self.mother_name.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Father's Occupation:").pack(pady=1,  padx=90, anchor='w')
        self.father_occupation = ctk.CTkEntry(content_frame, width=150)
        self.father_occupation.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Mother's Occupation:").pack(pady=1,  padx=90, anchor='w')
        self.mother_occupation = ctk.CTkEntry(content_frame, width=150)
        self.mother_occupation.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Father's Annual Income:").pack(pady=1,  padx=90, anchor='w')
        self.father_income = ctk.CTkEntry(content_frame, width=500)
        self.father_income.pack(pady=5,  padx=90, anchor='w')

    def create_page4(self):
        page4_frame = ctk.CTkFrame(self.notebook.tab("Interests"))  # Correct way to access the tab
        page4_frame.pack(expand=True, fill="both")
        
        content_frame = ctk.CTkFrame(page4_frame, fg_color='transparent')
        content_frame.pack(expand=True)  
        # Interests Form (Page 4)
        ctk.CTkLabel(content_frame, text="What do you want to become in the future?").pack(pady=1,  padx=90, anchor='w')
        self.future_goal = ctk.CTkEntry(content_frame, width=500)
        self.future_goal.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Interest Field Areas:").pack(pady=1,  padx=90, anchor='w')
        self.interest_areas = ctk.CTkEntry(content_frame, width=500)
        self.interest_areas.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Sports:").pack(pady=1,  padx=90, anchor='w')
        self.sports = ctk.CTkEntry(content_frame, width=500)
        self.sports.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="CS Interests:").pack(pady=1,  padx=90, anchor='w')
        self.cs_interests = ctk.CTkEntry(content_frame, width=500)
        self.cs_interests.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Community Service that you have offered:").pack(pady=1,  padx=90, anchor='w')
        self.community_service = ctk.CTkEntry(content_frame, width=500)
        self.community_service.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Entrepreneurship Interests:").pack(pady=1,  padx=90, anchor='w')
        self.entrepreneurship_interests = ctk.CTkEntry(content_frame, width=500)
        self.entrepreneurship_interests.pack(pady=5,  padx=90, anchor='w')


    def create_page5(self):
        page5_frame = ctk.CTkFrame(self.notebook.tab("Activities"))  # Correct way to access the tab
        page5_frame.pack(expand=True, fill="both")
        
        content_frame = ctk.CTkFrame(page5_frame, fg_color='transparent')
        content_frame.pack(expand=True)  
        # Interests Form (Page 4)
        ctk.CTkLabel(content_frame, text="What skills do you have?").pack(pady=1,  padx=90, anchor='w')
        self.skills = ctk.CTkEntry(content_frame, width=500)
        self.skills.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Can you List  out any 3 activities where you used above skills-").pack(pady=1,  padx=90, anchor='w')
        ctk.CTkLabel(content_frame, text="Activity 1:").pack(pady=1,  padx=90, anchor='w')
        self.activity1= ctk.CTkEntry(content_frame, width=500)
        self.activity1.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Activity 2:").pack(pady=1,  padx=90, anchor='w')
        self.activity2 = ctk.CTkEntry(content_frame, width=500)
        self.activity2.pack(pady=5,  padx=90, anchor='w')

        ctk.CTkLabel(content_frame, text="Activity 3:").pack(pady=1,  padx=90, anchor='w')
        self.activity3 = ctk.CTkEntry(content_frame, width=500)
        self.activity3.pack(pady=5,  padx=90, anchor='w')
        
        # A submit button
        submit_button = ctk.CTkButton(content_frame, text="Submit", command=self.submit_form, width=150, height=30)
        submit_button.pack(pady=20)
        

    

    def submit_form(self):
        # Gather all the input data and format it into a string
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
            f"Community Service that you have offered: {self.community_service.get()}\n"
            f"Entrepreneurship Interests: {self.entrepreneurship_interests.get()}\n"
        )
        
        activities = (
            f"Skills: {self.skills.get()}\n"
            f"Activity1: {self.activity1.get()}\n"
            f"Activity2: {self.activity2.get()}\n"
            f"Activity3: {self.activity3.get()}\n"
        )

        # Combine all the data into one formatted string
        self.formatted_data = (
            personal_details + academics + family_details + interests + activities
        )

        # Close the window and stop the main loop
        self.destroy()

    from fpdf import FPDF

    def get_data(self):
        # Start the main loop when this method is called
        self.mainloop()
        print(self.formatted_data)


        # After the main loop ends, return the formatted data
        
        
        return self.formatted_data



if __name__ == "__main__":
    app = GUI()
    app.get_data()