import gradio as gr
import scraping
import pandas as pd
import re
# import llm


# TODO 1: Falta añadir la opción de que se suba el CV mediante perfil de LinkedIn
#  (si no es primer uso se muestra último CV y se ofrece actualizar)
#  (se ofrece iniciar nueva instancia si la búsqueda es para un puesto totalmente diferente)


def upload_cv(file):
    """Function to handle file upload and generate de Data Frame."""
    global cv_df

    destiny_path = "saved CV/{}".format(re.search(r'([^/]+)$', file.replace("\\", "/")).group(1))

    with open(file.name, "rb") as origin:
        with open(destiny_path, "wb") as destiny:
            destiny.write(origin.read())

    reader = scraping.CVReader(destiny_path)
    cv_df = reader.read_pdf()

    cv_section = gr.Column(visible=True)

    return cv_df, destiny_path, cv_section


def edit_dataframe(edited_data):
    """Function to save the changes in the Data Frame."""
    global cv_df

    updated_df = pd.DataFrame(edited_data)
    cv_df.update(updated_df)

    return "CV Data Saved Successfully!"


def save_job_specs(location, role, contract, exp_level, job_type):
    """Function to save job specifications."""
    global job_specs

    job_specs = {"location": location,
                 "role": role,
                 "contract": contract,
                 "exp_level": exp_level,
                 "job_type": job_type
                 }

    return "Job Specifications Saved Successfully!"


def search_jobs():
    """Function to execute the job search."""
    global offers_cv, job_specs

    web_scraper = scraping.WebScraper()
    offers_cv = web_scraper.retrieve_offer_data(job_specs)

    return


with gr.Blocks() as app:
    gr.Markdown("# CV Application Filler")
    gr.Markdown("")

    # File upload section

    gr.Markdown("## Upload Your CV")

    # TODO: Pedir a usuario que suba su Cover Letter, si dispone de ella

    ui_file = gr.File(label="Upload a PDF file. Ensure avoiding redundant information or poorly structured data to "
                            "boost the performance of the model:", file_types=[".pdf"], type='filepath')
    ui_file_path = gr.Textbox(label="File Path", show_copy_button=True)

    with gr.Column(visible=False) as cv_section:
        gr.Markdown("_CV Read Successfully!_")

        gr.Markdown("")
        gr.Markdown("## Check Your Data")
        gr.Markdown("### Edit the data in each cell if needed. You can add new rows for the Education, Employment and "
                    "Skills categories, but don't add new categories.\nWhen finished, press save:")
        ui_df = gr.Dataframe(interactive=True,
                             col_count=(6, 'fixed'))

        # TODO: Ajustar tamaño de filas para que la descripción no sea en una sóla línea

        # TODO 2: Se le pedirá contestar unas preguntas acerca del tipo de trabajo que busca (autorellenadas
        #  con info del CV para que el usuario compruebe y cambie algo si quiere):
        #  Localización, puesto/s, *industria (autorrellenado por OpenAI con varias opciones sabido el puesto), *rama (autorrellenado
        #  por OpenAI con varias opciones sabido el puesto), tipo de puesto (a elegir una o varias: remoto, híbrido, presencial),
        #  nivel de experiencia (a elegir una o varias), tipo de contrato (a elegir una o varias),
        #  *idiomas (autorrellenado de la lectura del CV), *skills (autorrellenado de la lectura del CV), *salario minimo,
        #  *disponibilidad para viajar esporádicamente (a elegir sí o no),
        #  *traslado (a elegir sí o no si localización es diferente al de residencia)
        #  Si los parámetros no coinciden con los datos de las oferta, esa se descartará. Excepto las marcadas con asterisco,
        #  solo serán utilizadas para rellenar las aplicaciones

        with gr.Column(render=False) as job_section:
            gr.Markdown("")
            gr.Markdown("## Job Specifications")
            gr.Markdown("### Answer the following questions regarding the jobs you would like to apply to:")

            location = gr.Textbox(label="Location")
            role = gr.Textbox(label="Role")

            # industry_choices = llm.generate_industry_choices(cv_df)
            # gr.Dropdown(label="Industry", choices=[industry_choices])

            contract = gr.CheckboxGroup(label="Contract", choices=["Remote", "On-site", "Hybrid"])
            exp_level = gr.Dropdown(label="Experience level",
                                    choices=["Internship", "Entry Level", "Associate", "Mid-Senior Level", "Director",
                                             "Executive"],
                                    multiselect=True)
            job_type = gr.Dropdown(label="Job Type",
                                   choices=["Full-Time", "Part-Time", "Contract", "Temporary", "Internship", "Other"],
                                   multiselect=True)

            save_job_specs_button = gr.Button("Save Job Specifications")
            success_message_job = gr.Textbox(label="Status", container=False, render=False)
            save_job_specs_button.click(save_job_specs,
                                        inputs=[location, role, contract, exp_level, job_type],
                                        outputs=success_message_job)
            success_message_job.render()

        save_cv_button = gr.Button("Save CV Data")
        success_message_cv = gr.Textbox(label="Status", container=False, render=False)
        save_cv_button.click(edit_dataframe,
                             inputs=ui_df,
                             outputs=success_message_cv)
        success_message_cv.render()

        @gr.render(inputs=success_message_cv)
        def render_job_section(control):
            if len(control) > 0:
                job_section.render()

        @gr.render(inputs=success_message_job)
        def make_last_question(control):
            if control is not None:
                global jobs_to_apply

                gr.Markdown("## One last question:")
                jobs_to_apply = gr.Number(label="How many offers would you like to apply to?",
                                          precision=0)

                search_jobs_button = gr.Button("Start Searching for Jobs!")
                search_jobs_button.click(search_jobs)

    ui_file.change(upload_cv, inputs=ui_file, outputs=[ui_df, ui_file_path, cv_section])

# Launch Gradio App
app.launch(share=False)
