import streamlit as st
import scraping


def show_cv_data(cv_file, cv_path):
    if 'save_buttons' not in st.session_state:
        st.session_state['save_buttons'] = []

    # Habrá que ver si es necesario guardar el pdf en local para trabajar con él (puede
    # que para guardar el propio file_uploader tenga una opción integrada, pero si no está esta):

    with open(cv_path, "wb") as f:  # Donde wb es write binary
        f.write(cv_file.read())
    st.write("File saved to:", cv_path)

    reader = scraping.CVReader(cv_path)
    cv_df = reader.read_pdf()

    # Section to Display and Edit DataFrame Data
    st.header("Check Your Data")
    st.write("Edit the data in each cell if needed and press save")

    data_categories = cv_df["category"].unique()

    for category in data_categories:
        if category in st.session_state['save_buttons']:
            continue

        try:
            if st.session_state[f"{category}_button"]:
                st.session_state['save_buttons'].append(category)
                continue

        except KeyError:
            pass

        st.subheader(category)
        category_data = cv_df[cv_df["category"] == f"{category}"]
        editable_category_data = st.data_editor(category_data)

        # Save Button
        if st.button("Save changes", key=f"{category}_button"):
            cv_df.update(editable_category_data)
            st.success("Changes saved!")

        break
