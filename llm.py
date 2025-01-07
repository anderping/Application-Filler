from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import pandas as pd

load_dotenv('.env')
openai_key = str(os.getenv("OPENAI_API_KEY"))


def classify(text):
    """Receives an input text and classifies it per desired types. For example, it gets a full job
    experience and in classifies the text splitting it into location, dates, description, etc"""

    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "temperature": 0,
             "content":  """You are a machine for word type classification that receives a text extracted from a CV 
             as input and retrieves the following pieces of data: category, name, role, location, date and 
             description from it following the next set of rules:
             
             1. Your response shall include a valid JSON string with the following key-value pairs format 
             (in this case values are examples):
             
             {
                "category": ["Employment"],
                "company/institute": ["Apple"],
                "role/career": ["Software Engineer"]
                "location": ["United States"],
                "timestamp": ["March 2022 to March 2023"],
                "description": ["Developed and optimized cutting-edge applications and systems, collaborating 
                with cross-functional teams to deliver innovative solutions"]
             }
             
             2. Don't return anything else but the JSON string, don't include any other text (for example, "json").
             
             3. Always use double quotes in the JSON string, don't use single quotes.
                             
             4. In the JSON string 'category' is the category or heading of each section of the CV, which could 
             have one of the following names (or synonyms to these: User Description, Employment, Education, Skills, Interests 
             and Achievements.
             
             5. Always include a new instance of category, even if it's repeated.
             
             6. If you can't find information from the text regarding any of the keys in any of the 'category' 
             values then always fill it with 'NaN'.
             
             7. In case of 'User Description', 'Skills' and 'Interests' only fill the 'description' key with the 
             correspondant information, fill the rest of the keys with NaN.

             8. All lists in the values must be of the same length, hence don't leave any blank spaces, in that 
             case fill with 'NaN'.
             
             9. Never create lists inside the lists indicated in the JSON string for the values.""",
             },
            {"role": "user", "content": text}
        ]
    )

    #                  , in which case always only use one of the
    #                  following indicated names, for example, if "Other Employment" is used in the CV, include it as
    #                  "Professional Experience")

    content = completion.choices[0].message.content  # Esto se genera como un literal json string, no vale como un JSON normal
    data = json.loads(content)  # Para transformarlo en diccionario

    return pd.DataFrame(data)


def generate_synonyms(self):

    return


def write_cover_letter(self):

    return


# def identify_skills(self):
#     pipe = pipeline("token-classification", model="jjzha/jobbert_knowledge_extraction")

#     pipe("TEXTO A CLASIFICAR")
