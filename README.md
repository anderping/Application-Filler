[Check the implementation of the app in Hugging Face Spaces](https://huggingface.co/spaces/anderping/Application-Filler)

__"Application Filler"__ is a tool made out of the weariness of having to fill out manually individual profile sites to 
apply for different jobs.

Its purpose is to save all those troubles by just having to upload your CV in PDF format or LinkedIn profile URL and 
letting the program make the rest of the work.

The __program workflow__ is as follows:

__*FIRST DRAFT*__

1. The user uploads his CV in PDF or image (.png or .jpg) format or (WIP) indicates his LinkedIn profile URL. The image is read through OCR.
2. OpenAi gpt-4o-mini LLM reads it, classifies all the data, which is then saved into a Data Frame.
3. The user is given the option to edit the data afterwards.
4. The user is asked for his job preferences.

__*WIP*__

5. With the profile data and the job preferences the search is conducted.
6. The offers matching the user data and preferences are shown to the user for last verification.
7. The program fills out the application sites.
8. The application sites are shown to the user for revision and approval.

<br>

### Follow the steps to execute the program locally
1. Copy .env.example file to .env on the root folder: 

        # Windows command prompt
        copy .env.example .env

        # macOS and Linux terminal
        cp .env.example .env
    
2. Activate virtual environment:

        # Windows command prompt
        .venv\Scripts\activate.bat
    
        # macOS and Linux
        source .venv/bin/activate

3. Run to execute:

        py src/main.py
