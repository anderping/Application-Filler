import streamlit as st
import Scraping


# TODO 1: Se pedirá subir el CV del usuario en PDF o que indique su perfil de Linkedin
# (si no es primer uso se muestra último CV y se ofrece actualizar)
# (se ofrece iniciar nueva instancia si la búsqueda es para un puesto totalmente diferente)

st.title("CV Application Filler")

# File Upload Section
st.header("Submit Your CV")
cv_file = st.file_uploader("Upload your CV as a PDF file", type=["pdf"])

if cv_file:
    st.success(f"File uploaded: {cv_file.name}")
    cv_path = f"Saved CV/{cv_file.name}"

    # Habrá que ver si es necesario guardar el pdf en local para trabajar con él (puede
    # que para guardar el propio file_uploader tenga una opción integrada, pero si no está esta):

    with open(cv_path, "wb") as f:  # Donde wb es write binary
        f.write(cv_file.read())
    st.write("File saved to:", cv_path)

    reader = Scraping.CVReader(cv_path)
    cv_df = reader.read_pdf()

    # Section to Display and Edit DataFrame Data
    st.header("Check Your Data")
    st.write("Edit the data in each cell if needed")

    data_categories = cv_df["category"].unique()

    for category in data_categories:
        st.subheader(category)
        category_data = cv_df[cv_df["category"] == f"{category}"]
        editable_category_data = st.data_editor(category_data)

        # Save Button
        if st.button("Save changes", key=category):
            cv_df.update(editable_category_data)
            st.success("Changes saved!")



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

