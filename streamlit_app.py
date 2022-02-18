import streamlit as st

from segments import SegmentsClient
from segments.huggingface import release2dataset

query_params = st.experimental_get_query_params()
prefilled_owner = query_params['owner'][0] if 'owner' in query_params else 'jane'
prefilled_dataset = query_params['dataset'][0] if 'dataset' in query_params else 'flowers'
prefilled_release = query_params['release'][0] if 'release' in query_params else 'v0.1'

st.write('Export your Segments.ai dataset to the HuggingFace hub.')

def show_code_block():
    code = f'''
from segments import SegmentsClient
from segments.huggingface import release2dataset

segments_api_key = "{segments_api_key}"
client = SegmentsClient(api_key)
release = client.get_release("{segments_dataset_owner}/{segments_dataset_name}", "{segments_release}")

dataset = release2dataset(release, True)
dataset.push_to_hub("{hf_dataset_owner}/{hf_dataset_name}")
'''

    st.code(code, language='python')

def export_dataset():
    try:
        # TODO: redirect the stdout of these functions to st.write(): https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602
        # TODO: hide the form once the button is clicked, possibly adding another button to reset at that time.
        client = SegmentsClient(segments_api_key)
        release = client.get_release(f'{segments_dataset_owner}/{segments_dataset_name}', f'{segments_release}')
        dataset = release2dataset(release, True)
        dataset.push_to_hub(f'{hf_dataset_owner}/{hf_dataset_name}', token=hf_api_key)

        # Success!
        st.balloons()
    except:
        st.write('Something went wrong.')

with st.form(key='my_form'):
    st.subheader('Segments.ai')
    segments_api_key = st.text_input('Segments.ai API key', help="Get your Segments.ai API key [here](https://segments.ai/account)")
    col1, col2, col3 = st.columns(3)
    with col1:
        segments_dataset_owner = st.text_input('Dataset owner', prefilled_owner, key="segments_dataset_owner")
    with col2:
        segments_dataset_name = st.text_input('Dataset name', prefilled_dataset, key="segments_dataset_name")
    with col3:
        segments_release = st.text_input('Release', prefilled_release)

    # st.write('---')

    st.subheader('HuggingFace')
    hf_api_key = st.text_input('HuggingFace API key', help="Get your HuggingFace API key [here](https://huggingface.co/settings/token)")
    col1, col2, col3 = st.columns(3)
    with col1:
        hf_dataset_owner = st.text_input('Dataset owner', prefilled_owner, key="hf_dataset_owner")
    with col2:
        hf_dataset_name = st.text_input('Dataset name', prefilled_dataset, key="hf_dataset_name")

    submit_button = st.form_submit_button(label='Start export')

if submit_button:
    show_code_block()
    export_dataset()