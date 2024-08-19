import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError


# Initial code from here: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
# Run this from >> streamlit run app.py

def intro():
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


def data_frame_demo():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")

    st.markdown(f"# Step 1: Upload dose distribution volume and mask files")
    st.markdown(f"Look at []() to format your files into NIfTI format using Pyradise.")
    dose_file = st.file_uploader("Upload a dose distribution volume (in .nii.gz)", type=['nii', 'nii.gz'])

    mask_file = st.file_uploader("Upload mask volumes (in .nii.gz)", type=['nii', 'nii.gz'])
    if (dose_file != None) and (mask_files != None):
        st.markdown(f"Both dose and mask files are uploaded")

    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.
        (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
        """
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "—": intro,
    "Calculate DVH": data_frame_demo
}

demo_name = st.sidebar.selectbox("Choose a task:", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()