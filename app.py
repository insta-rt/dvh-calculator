import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

import utils


# Initial code from here: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
# Run this from >> streamlit run app.py


def display_dvh(df, structures):
    if not structures:
        st.error("Please select at least one structure.")
    else:
        data = df.loc[structures]
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["Dose"]).rename(
            columns={"index": "Dose", "value": "Dose Volume Histogram"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="Dose:T",
                y=alt.Y("Dose Volume Histogram:Q", stack=None),
                color="variable:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)


def instructions():
    st.write("# DVH Calculator! 👋")
    st.sidebar.success("Select an option above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [insta-rt.github.io](https://insta-rt.github.io) for more info
        - Reach out back to us at [insta-rt.github.io/contact](https://insta-rt.github.io/contact)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


def calculate_dvh():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")

    st.markdown(f"## Step 1: Upload dose distribution volume and mask files")
    st.markdown(f"Look [here](https://pyradise.readthedocs.io) to format your files into NIfTI format using Pyradise.")
    dose_file = st.file_uploader("Upload a dose distribution volume (in .nii.gz)", type=['nii', 'gz'])

    mask_files = st.file_uploader("Upload mask volumes (in .nii.gz)", accept_multiple_files=True, type=['nii', 'gz'])

    files_uploaded = (dose_file is not None) and (len(mask_files) > 0)

    if files_uploaded:
        st.markdown(f"Both dose and mask files are uploaded. Click the button below to proceed.")
        x = st.button("Compute")

        st.divider()

        if x:
            st.markdown(f"## Step 2: Choose structures")
            df = utils.dvh_from_files(dose_file, mask_files)
            structures = st.multiselect(
                "Choose structures", list(df.index), list(df.index)
            )
            display_dvh(df, structures)


page_names_to_funcs = {
    "Instructions": instructions,
    "Calculate DVH": calculate_dvh
}

task_selection = st.sidebar.selectbox("Choose a task:", page_names_to_funcs.keys())
page_names_to_funcs[task_selection]()