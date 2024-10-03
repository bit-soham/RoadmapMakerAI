from llm import llm
import numpy as np # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

class Prompt_Generator:
    def __init__(self, embedder,  student_input, files_dict, month, year):
        self.student_input = student_input
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.No_of_events = 0
        self.events = ""
        self.year = year
        self.files_dict = files_dict
        self.files = list(files_dict.keys())
        self.current_month = month - 1
        self.current_date = f'{self.months[self.current_month]} {self.year}'
        self.starting_date = f'{self.months[month - 1]} {year}'
        self.No_to_text = {
                            0 : 'first',
                            1 : 'second',
                            2 : 'third',
                            3 : 'fourth',
                            4 : 'fifth',
                            5 : 'sixth',
                            6 : 'seventh',
                            7 : 'eighth',
                            8 : 'ninth',
                            9 : 'tenth',
                            10 : 'eleventh',
                            11 : 'twelfth',
                            12 : 'thirteenth',
                            13 : 'fourteenth',
                            14 : 'fifteenth',
                            15 : 'sixteenth',
                            16 : 'seventeenth',
                            17 : 'eighteenth',
                            18 : 'nineteenth',
                            19 : 'twentieth'
                        }
        self.embedder = embedder
        self.device = self.embedder.device
        
        self.done_events = {}
        self.best_events = []

    def query_embd(self, query):
        query_inputs = self.embedder.question_tokenizer(query, return_tensors="pt", max_length=512, truncation=True).to(self.device)
        query_embedding = self.embedder.question_encoder(**query_inputs).pooler_output
        return query_embedding

    def increment_month(self):
        if self.months[self.current_month] == 'December':
            self.year = str(int(self.year) + 1)
            self.current_month = 0
        else:
            self.current_month += 1
        self.current_date = f'{self.months[self.current_month]} {self.year}'

    def similarity_check(self, query, context_embeddings):
        similarities = cosine_similarity(
            query.detach().cpu().numpy(),
            context_embeddings.detach().cpu().numpy()
        )
        # print("Similarities:", similarities)
        return similarities

    def generate_file_prompt(self):
        epsilon = 1 if self.No_of_events == 0 else 0.6
        a = np.random.rand()

        if a < epsilon:
            original_query_for_file = f"""
                        You are the professional roadmap guide, according to the given student info as follows {self.student_input}
                        you are generating a roadmap for the student. Now you are providing the task to the student for the
                        {self.No_to_text[self.No_of_events]} month of their road map you will suggest him the task for this month
                        while considering his interests goals and events he has already done in previous months. The student has
                        done {self.No_of_events} events till now which are: {self.events}
                        Now please suggest the student a sector among these 16 sectors {self.files}
                        the student should choose for the current month's task according to his current progress as per the roadmap
                        and according to his interests and skills and long-term goals. Your answer should only contain the sector name and nothing else.
                        Do not say anything else.
                        """
            print("Same: ", end='')
            epsilon -= 0.9 * epsilon
        else:
            print("Diff: ", end='')
            original_query_for_file = f"""
                        You are the professional roadmap guide, according to the given student info as follows {self.student_input}
                        you are generating a roadmap for the student. Now you are providing the task to the student for the
                        {self.No_to_text[self.No_of_events]} month of their road map you will suggest him the task for this month
                        while considering his interests goals and events he has already done in previous months. The student has
                        done {self.No_of_events} events till now which are: {self.events}
                        Now please suggest the student a sector among these 16 sectors {self.files} other than {self.file_header}
                        the student should choose for the current month's task according to his current progress as per the roadmap
                        and according to his interests and skills and long-term goals. Your answer should only contain the sector name and nothing else.
                        Do not say anything else.
                        """
            epsilon += 0.4 * epsilon
        prompt = """
        You are a knowledgeable professor who is very knowledgeable on matters of students' careers. You will help your student choose the best sector for them while deciding their roadmap. You will just tell the student the name of the sector most suitable for them.
        """
        response = llm(original_query_for_file, prompt)
        response_embedding = self.query_embd(response)

        # print("This is the response we get:- ",response)

        similiarites = self.similarity_check(response_embedding, self.embedder.filenames_embeddings)
        self.file_header = self.files[np.argmax(similiarites)]
        print("This is the file_header afterr similarity check:- ", self.file_header)



    def generate_event_prompt(self):

        query_for_llm = f"""
                        You are the professional roadmap guide, according to the given student info {self.student_input} on {self.starting_date} you are generating a
                        one-year roadmap for the student. The roadmap began at {self.starting_date} and now is {self.months[self.current_month]}, Now you have to give him a perfect hypothetical event for the student for their
                        {self.No_to_text[self.No_of_events]} month of their road map you will suggest him the most suitable event for this month while considering the
                        events he has already done in previous months his interests and his skills and the hypothetical event dates should be in the current month of the event. Till now the student has already done {self.No_of_events} events till now which are:
                        {self.events} The event you decide for him should be from {self.file_header} setor . Make sure you don't include the events he already did and don't say anything extra other than event fields.
                    """
        example_answers = []
        prompt = """You are a helpful professional roadmap guide.
        Provide an example tasks to the given sector that you will suggest from from the information in the question."""

        for i in range(5):
            example_answers.append(self.query_embd(llm(query_for_llm, prompt)))


        query_embedding = self.query_embd(query_for_llm)
        similarities = np.array([(np.zeros(self.embedder.context_embeddings[self.file_header].size(0)))])
        print(self.file_header, len(similarities[0]))

        for i in range(5):
            similarities += self.similarity_check(example_answers[i], self.embedder.context_embeddings[self.file_header])


        if self.file_header not in self.done_events.keys():
            self.done_events[self.file_header] = []

        for event in self.done_events[self.file_header]:
            print("Already Done" , self.files_dict[self.file_header].iloc[event])
            similarities[0][event] = -1

        most_relevant_idx = np.argmax(similarities)
        self.done_events[self.file_header] += [most_relevant_idx]

        df = self.files_dict[self.file_header]
        best_event = df.iloc[most_relevant_idx]

        self.increment_month()

        print(best_event)
        return best_event



    def generate_prompt(self, count):

        for i in range(count):
            self.generate_file_prompt()
            best_event = self.generate_event_prompt()

            # columns = ['Title', 'Description', 'Details', 'Highlights', 'Cost' 'Website', 'website']
            event = ''
            event += f'On {self.current_date} the students does his {i + 1}th event  from the {self.file_header} sector It\'s details are: \n '
            for idx, (column, value) in enumerate(best_event.items()):
                  event += f"{chr(idx + 97)}) The {str(column)} of the event is {str(value)}\n"

            self.best_events.append(best_event)
            self.events += event
            self.No_of_events += 1

        return self.events


class RoadMapGenerator:
    def __init__(self, events, student_input, no_of_events):
        self.events = events
        self.student_input = student_input
        self.no_of_events = no_of_events

    def generate_roadmap(self):
        system_prompt = """
                You are a professional Career and health advisor and you care for students mental strengh but will push them to their limits to achieve there goals
                """
        user_prompt = f"""
              So we created a roadmap of events for this student {self.student_input} where he does the following events {self.events} monthwise
              So using this information that you are given i want you to create a perfect roadmap for the student while considering his mental state and his goals. You can suggest some small extra things that he may need to do like learning some language ,
              going into some social media , doing exercises , taking rests etc and also mention some guidelines to follow while doing these events. Some strict rules he should follow to build self-discipline.
              Roadmap output  Guidelines:

              Personalized advice to help the student maintain a balanced lifestyle, avoid burnout, and stay disciplined.
              Strategies for self-care, mental health, and self-discipline that are relevant to the student's goals and personality.
              Main Checklist for Applications and Preparations:

              Clearly outline what the student needs to accomplish for their upcoming applications and competitions. Include any specific requirements, deadlines, or preparation tips.
              Monthly Tasks:

              For each month, provide a detailed breakdown of activities the student should focus on. This should include:
              Event Preparation: Specific study or skill-building activities needed for upcoming events or competitions. For example, if participating in the American Collegiate Programming Contest (ACPC) in May, outline a study plan focusing on algorithms and problem-solving skills.
              Life Balance: Include activities that promote a healthy work-life balance, such as exercise routines, meditation, social activities, and relaxation techniques.
              Networking and Learning: Suggest networking opportunities with professionals in the student's field of interest and ways to stay updated with the latest developments (e.g., following relevant news, attending webinars).
              Self-Reflection and Adaptation: Encourage regular reflection on what was learned, what can be improved, and how to adapt strategies moving forward.
              Extra Tips and Activities:

              Suggest additional activities that the student could engage in to enhance their skills, such as learning a new language, engaging in online courses, or joining study groups.

                The ouput format should only contain the roadmap and nothing else. and it shold have a format like this and do not use this as an example just see the format
                'Name's Roadmap
                Guidelines -
                1. Before you begin going through your roadmap, keep the following in your mind:
                ....
                .
                .
                .
                .
                Main checklist to complete for application -
                ....

                Monthly Tasks -
                April-
                ..

                website name (for each month)

                May-
                .
                .
                .website name (for each month)
                .
                .
                .
                .
                December-
                ..
                January -
                .
                .
                .
                April

                '
                You must genarate the roadmap for each month that should include what events along with the event's website he should attend what aspects of his life he should take care of and other imp things he can do that month on his own according to the events
                he is attending next month preparing for upcoming events and his goals.
                You must Whenever you are mentioning an event mention the event's website also for each month
                YOU must Do this for {self.no_of_events} months using the data on the events we provided
                """
        response = llm(user_prompt, system_prompt, max_tokens=10000)
        return response
