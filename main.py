# import streamlit as st
import gradio as gr
# from cv_streamlit import show_cv_data
import scraping
import pandas as pd
import re


# TODO 1: Se pedirá subir el CV del usuario en PDF o que indique su perfil de Linkedin
# (si no es primer uso se muestra último CV y se ofrece actualizar)
# (se ofrece iniciar nueva instancia si la búsqueda es para un puesto totalmente diferente)


# @st.cache_data
# def load_file(file):
#     return file
#
#
# def show_cv_data(cv_file, cv_path):
#     if 'save_buttons' not in st.session_state:
#         st.session_state['save_buttons'] = []
#
#     # Habrá que ver si es necesario guardar el pdf en local para trabajar con él (puede
#     # que para guardar el propio file_uploader tenga una opción integrada, pero si no está esta):
#
#     with open(cv_path, "wb") as f:  # Donde wb es write binary
#         f.write(cv_file.read())
#     st.write("File saved to:", cv_path)
#
#     reader = scraping.CVReader(cv_path)
#     cv_df = reader.read_pdf()
#
#     # Section to Display and Edit DataFrame Data
#     st.header("Check Your Data")
#     st.write("Edit the data in each cell if needed and press save")
#
#     data_categories = cv_df["category"].unique()
#
#     for category in data_categories:
#         if category in st.session_state['save_buttons']:
#             continue
#
#         try:
#             if st.session_state[f"{category}_button"]:
#                 st.session_state['save_buttons'].append(category)
#                 continue
#
#         except KeyError:
#             pass
#
#         st.subheader(category)
#         category_data = cv_df[cv_df["category"] == f"{category}"]
#         editable_category_data = st.data_editor(category_data)
#
#         # Save Button
#         if st.button("Save changes", key=f"{category}_button"):
#             cv_df.update(editable_category_data)
#             st.success("Changes saved!")
#
#         break
#
#
# st.title("CV Application Filler")
#
# # File Upload Section
# st.header("Submit Your CV")
#
# if 'file_uploader' not in st.session_state:
#     st.session_state['file_uploader'] = []
#     cv_file = st.file_uploader("Upload your CV as a PDF file", type=["pdf"])
#
# cv_file_cached = load_file(cv_file)
#
# if cv_file_cached:
#     st.success(f"File uploaded: {cv_file.name}")
#     cv_path = f"Saved CV/{cv_file.name}"
#
#     show_cv_data(cv_file, cv_path)


# TODO 2: Se mostrará al usuario el perfil generado para que pueda modificar algo si lo desea:
#
#   Nombre, titular, descripción, localización, contacto, webs externas, idiomas, experiencia, proyectos,
#   estudios, skills, otros



# TODO 3: Se le pedirá contestar unas preguntas acerca del tipo de trabajo que busca (autorellenadas
# con info del CV para que el usuario compruebe y cambie algo si quiere):

#   Localización, puesto/s, industria (autorrellenado por OpenAI con varias opciones sabido el puesto), rama (autorrellenado
#   por OpenAI con varias opciones sabido el puesto), tipo de puesto (a elegir una o varias: remoto, híbrido, presencial),
#   nivel de experiencia (a elegir una o varias), tipo de contrato (a elegir una o varias),
#   idiomas (autorrellenado de la lectura del CV), skills (autorrellenado de la lectura del CV), salario minimo,
#   disponibilidad para viajar esporádicamente (a elegir sí o no),
#   traslado (a elegir sí o no si localización es diferente al de residencia)
#
#   Si los parámetros no coinciden con los datos de las oferta, esa se descartará

# TODO 4: Se genera una tabla de pandas con esa info.

# TODO 5: Se pregunta cuántas ofertas se desean aplicar en la ejecución.


# Function to handle file upload
def upload_cv(file):
    global cv_df

    destiny_path = f"Saved CV/{re.search(r'([^\\]+)$', file).group(1)}"

    with open(file.name, "rb") as origin:
        with open(destiny_path, "wb") as destiny:
            destiny.write(origin.read())

    reader = scraping.CVReader(destiny_path)
    cv_df = reader.read_pdf()

    return cv_df, destiny_path


# Function to display and edit DataFrame
def edit_dataframe(edited_data):
    global cv_df

    updated_df = pd.DataFrame(edited_data)
    cv_df.update(updated_df)

    return "Data saved successfully!"


# Initialize Gradio App
with gr.Blocks() as app:
    gr.Markdown("# CV Application Filler")

    # File Upload Section

    gr.Markdown("## Upload Your CV")

    ui_file = gr.File(label="Upload a PDF file", file_types=[".pdf"], type='filepath')
    ui_file_path = gr.Textbox(label="File Path", show_copy_button=True)

    ui_df = gr.Dataframe(interactive=True,
                             render=False)

    ui_file.change(upload_cv, inputs=ui_file, outputs=[ui_df, ui_file_path])

    @gr.render(inputs=ui_file_path)
    def success(file_path):
        if len(file_path) > 0:
            gr.Markdown("_CV Read Successfully!_")

    gr.Markdown("## Check Your Data")
    gr.Markdown("### Edit the data in each cell if needed and then press save")
    gr.Markdown("Do not modify NaN cells!")
    ui_df.render()

    @gr.render(inputs=ui_file_path)
    def save(file_path):
        if len(file_path) > 0:
            global ui_df

            save_button = gr.Button(f"Save Data")
            category_status = gr.Textbox(label="Status", container=False, render=False)
            save_button.click(edit_dataframe,
                              inputs=ui_df,
                              outputs=category_status)
            category_status.render()

# Launch Gradio App
app.launch(share=True)
