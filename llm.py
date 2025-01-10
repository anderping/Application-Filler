from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import pandas as pd

load_dotenv('.env')
openai_key = str(os.getenv("OPENAI_API_KEY"))


def classify(text):
    """Receives an input text and classifies it per desired types. For example, it gets a full job
    experience and in classifies the text splitting it into location, dates, description, etc."""

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
                             
             4. In the JSON string, 'category' is the category or heading of each section of the CV, which could 
             have one of the following names (or similar/synonyms to these): Name, Location, Contact, External Links, 
             User Description, Languages, Employment, Education, Skills, Interests and Achievements. Use only these as 
             categories, do not make up any other.
             
             5. 'Name' is the name of the user, which normally is used as a heading in the CV.
             
             6. 'Location' is the location of the user, which is normally accompanied by other user data, such as 
             'Contact'. Don't put any of the location data in the 'location' key, place it entirely in 'description'. 
             Only include the location itself.
             
             7. 'Contact' is the contact info of the user. Could be a telephone number or an email.
             
             8. 'External Links' shall include links to sites such as GitHub, Linkedin or other portfolio-like sites. 
             Is is normally included close to other user data, such as 'Location' and 'Contact'. If no links are 
             present, fill out every key with NaN.
             
             9. 'Languages' are the languages the user knows, which could be specified in an independent section or in 
             the 'Skills' section.
             
             10. For the 'Education', 'Employment' and 'Skills' categories always include a new instance in the 
             'category' key, even if it's repeated.
                          
             11. If you can't find information from the text regarding any of the keys in any of the 'category' 
             values then always fill it out with 'NaN'.
             
             12. In case of 'Name', 'Location', 'Contact', 'External Links', 'User Description', 'Languages', 'Skills' 
             and 'Interests' only fill out the 'description' key with the correspondant information, fill out the 
             rest of the keys with NaN.

             13. All lists in the values must be of the same length, hence don't leave any blank spaces, in that case 
             fill out with 'NaN'.
             
             14. Never create lists inside the lists indicated in the JSON string for the values.""",
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
