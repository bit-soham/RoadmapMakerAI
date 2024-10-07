import os
import torch # type: ignore
import pickle
from transformers import ( # type: ignore
    DPRQuestionEncoder,
    DPRContextEncoder,
    DPRQuestionEncoderTokenizer,
    DPRContextEncoderTokenizer,
)

class Embedding_Generator:
    def __init__(self, files_dict):
        self.files = list(files_dict.keys())
        self.files_dict = files_dict
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.context_embeddings = None
        loaded = False


        self.question_encoder = DPRQuestionEncoder.from_pretrained(
            "facebook/dpr-question_encoder-single-nq-base"
        )
        self.question_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(
            "facebook/dpr-question_encoder-single-nq-base"
        )
        self.question_encoder = self.question_encoder.to(self.device)
        
        directory = 'Data\\file_embeddings'
        
        filename1 = 'file_embeddings.pth'
        filename2 = 'file_embeddings.pkl'
        
        file_path1 = os.path.join(directory, filename1)
        file_path2 = os.path.join(directory, filename2)
        print(file_path1)
        if os.path.isfile(file_path1):
            self.filenames_embeddings = torch.load(file_path1, map_location=self.device, weights_only=True)
        elif os.path.isfile(file_path2):
            with open(file_path2, 'rb') as f:
                self.filenames_embeddings = pickle.load(f)
        else:
            # Load the context encoder and its corresponding tokenizer
            print("hellodss")
            if not loaded:
                context_encoder = DPRContextEncoder.from_pretrained(
                    "facebook/dpr-ctx_encoder-single-nq-base"
                )
                self.context_tokenizer = DPRContextEncoderTokenizer.from_pretrained(
                    "facebook/dpr-ctx_encoder-single-nq-base"
                )
                self.context_encoder = context_encoder.to(self.device)            
                loaded = True   
            
            self.filenames_embeddings = self.filename_embd()
        
        
        filename1 = 'context_embeddings.pth'
        filename2 = 'context_embeddings.pkl'
        
        file_path1 = os.path.join(directory, filename1)
        file_path2 = os.path.join(directory, filename2)
        
        if os.path.isfile(file_path1):
            self.context_embeddings = torch.load(file_path1, map_location=self.device, weights_only=True)
        elif os.path.isfile(file_path2):
            with open(file_path2, 'rb') as f:
                self.context_embeddings = pickle.load(f)
        else:
            print("hello")
            # Load the context encoder and its corresponding tokenizer
            if not loaded:
                context_encoder = DPRContextEncoder.from_pretrained(
                    "facebook/dpr-ctx_encoder-single-nq-base"
                )
                self.context_tokenizer = DPRContextEncoderTokenizer.from_pretrained(
                    "facebook/dpr-ctx_encoder-single-nq-base"
                )
                self.context_encoder = context_encoder.to(self.device)            
                loaded = True
            
            self.context_embeddings = self.context_embd()

    def concatenate_row(self, row):
        return ', '.join(f'{col}: {row[col]}' for col in row.index)

    def filename_embd(self):
        context_embeddings = []

        for file_name in self.files:
            # print(file_name)
            context_inputs = self.context_tokenizer(file_name, return_tensors="pt").to(self.device)
            context_embedding = self.context_encoder(**context_inputs).pooler_output
            context_embeddings.append(context_embedding)
        file_embeddings = torch.cat(context_embeddings, dim=0)
        
        torch.save(file_embeddings, 'file_embeddings.pth')
        with open('file_embeddings.pkl', 'wb') as f:
            pickle.dump(file_embeddings, f)
        return file_embeddings

    def context_embd(self):
        context_embeddings = {}
        for file_header in self.files:
            event_embeddings = []
            data = self.files_dict[f"{file_header}"]
            columns_to_remove = ['Website', 'website', 'No', 'No.']
            data = data.drop(columns=[col for col in columns_to_remove if col in data.columns])
            data['concatenated'] = data.apply(self.concatenate_row, axis=1)

            for idx, row in data.iterrows():
                event_inputs = self.context_tokenizer(row['concatenated'], return_tensors="pt").to(self.device)
                event_embedding = self.context_encoder(**event_inputs).pooler_output
                event_embeddings.append(event_embedding)

            context_embeddings[file_header] = torch.cat(event_embeddings, dim=0)

        torch.save(context_embeddings, 'context_embeddings.pth')
        with open('context_embeddings.pkl', 'wb') as f:
            pickle.dump(context_embeddings, f)

        return context_embeddings
