import os
from openai import OpenAI
import json
import pandas as pd
import tiktoken

openai_key = os.getenv("OPENAI_API_KEY")


def classify(text):
    """Receives an input text and classifies it per desired types. For example, it gets a full job
    experience and in classifies the text splitting it into location, dates, description, etc."""

    tokenizer = tiktoken.encoding_for_model("gpt-4")
    employment_token = tokenizer.encode("Employment")[0]
    education_token = tokenizer.encode("Education")[0]

    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        # top_p=0.8,
        # frequency_penalty=0.3,
        # presence_penalty=0.1,
        stop=["}\n\n"],
        logit_bias={
            f"{employment_token}": 25,
            f"{education_token}": 25,
        },
        messages=[
            {"role": "system",
             "content":  """
             You are a highly precise machine for extracting and classifying information from text extracted from a CV. 
             Your task is to analyze the input text and return a structured JSON object following the rules below:
             
             1. Your response must only include a valid JSON string with the following key-value pairs structure 
             (values below are examples):
             
             {
                "category": ["Employment"],
                "company/institute": ["Apple"],
                "role/career": ["Software Engineer"]
                "user location": ["United States"],
                "timestamp": ["March 2022 to March 2023"],
                "description": ["Developed and optimized cutting-edge applications and systems, collaborating 
                with cross-functional teams to deliver innovative solutions"]
             }
             
             Where:
                - category: The section or heading of the CV (e.g., User Description, Employment, Education).
                - company/institute: The organization or institution (e.g., employer, school).
                - role/career: The position or degree.
                - location: The specific location associated with the entry.
                - timestamp: The dates or time range associated with the entry. 
                - description: A detailed explanation or associated data for the entry.
                
             2. Always use double quotes in the JSON string, do not use single quotes.
             
             3. Do not return any additional text or comments besides the JSON string. For example, avoid prefixing 
             with "Here is the JSON:" or "json".           
                             
             4. In the JSON string, for the 'category' key each section of the CV could have one of the following names 
             (or either synonyms or similar names to these): 
                - Name: the name of the user, which normally is used as a heading in the CV.
                - User Location: the location of the user, which is normally accompanied by other user data, such as 
                    'Contact'. Do not put any of the User Location data in the 'location' key, place it entirely in 
                    'description'. Only include the location itself.
                - Contact: the contact info of the user. Could be a telephone number or an email.
                - External Links: shall include links to sites such as GitHub, LinkedIn or other portfolio-like sites. 
                    Is is normally included close to other user data, such as 'Location' and 'Contact'. If no links are 
                    present, fill out every key with NaN.
                - User Description
                - Languages: the languages the user knows, which could be specified in an independent section or in 
                    the 'Skills' section depending on the CV.
                - Employment
                - Education
                - Skills
                - Interests and Achievements
                
             Use only these as categories, do not make up any other.
             
             5. For the 'Education', 'Employment' and 'Skills' categories always create a new instance for every entry, 
             even if the category is repeated.
                          
             6. If any required information is missing from the text, always use "NaN" as the placeholder. Do not leave 
             blank spaces.
             
             7. In case of 'Name', 'Location', 'Contact', 'External Links', 'User Description', 'Languages', 'Skills' 
             and 'Interests and Achievements':
                - Only fill the 'description' key with the correspondant information, 
                - All other keys must be filled with "NaN".

             8. Ensure that all lists in the values have the same length. If a value is unavailable for a specific key, 
             fill it with "NaN" to maintain alignment, hence don't leave any blank spaces
             
             9. Do not nest lists within the JSON values. Every value in the JSON should be flat.""",
             },

            {"role": "user", "content": text}
        ]
    )

    # TODO 1: Ver si hace falta incluir el "Titular" en el Data Frame

    # TODO 2: Para Location se rellena la columna location cuando debería ir en description. Puede necesitar corrección
    #  post

    # TODO 3: Ver si ajustar Temperature y otros parámetros en el modelo

    content = completion.choices[0].message.content  # It is generated as a literal json string
    data = json.loads(content)  # To transform into a dictionary

    try:
        return pd.DataFrame(data)
    except ValueError:
        print("Language model may fail to generate a proper Data Frame in some runs. Please re-upload your CV and try "
              "again.")


# def generate_industry_choices(cv_df):
#     cv_df[cv_df["category"] == "Employment"]["company/institute"]
#
#
#     return


def generate_synonyms():

    return


def write_cover_letter():

    return


# def identify_skills(self):
#     pipe = pipeline("token-classification", model="jjzha/jobbert_knowledge_extraction")

#     pipe("TEXTO A CLASIFICAR")



    #                  , in which case always only use one of the
    #                  following indicated names, for example, if "Other Employment" is used in the CV, include it as
    #                  "Professional Experience")
