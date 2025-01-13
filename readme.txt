"Application Filler" is a tool made out of the weariness of having to fill out manually individual profile sites to apply for different jobs.

Its purpose is to save all those troubles by just having to upload your CV in PDF format or LinkedIn profile URL and letting the program make the rest of the work.

The program workflow is as follows:

    FIRST DRAFT
    1. The user uploads his CV in PDF format or indicates his LinkedIn profile URL.
    2. OpenAi gpt-4o-mini LLM reads it, classifies all the data, which is then saved into a Data Frame.
    3. The user is given the option to edit the data afterwards.
    4. The user is asked for his job preferences.

    TBD
    5. With the profile data and the job preferences the search is conducted.
    6. The offers matching the user data and preferences are shown to the user for last verification.
    7. The program fills out the application sites.
    8. The application sites are shown to the user for revision and approval.


Run the following before execution:

    - Copy .env.example file to .env on the root folder. You can type "copy .env.example .env" if using command prompt Windows or "cp .env.example .env" if using terminal Ubuntu.
