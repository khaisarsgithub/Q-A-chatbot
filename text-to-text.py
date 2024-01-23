import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai 
import os
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import UnstructuredURLLoader, PyPDFLoader

load_dotenv(find_dotenv())

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Define menu options
options = ["Translate", "Text Summary", "Data Analysis", "Metafic.ai"]
icons = ["translate", "book", "search", "question"]

# Create sidebar menu
with st.sidebar:
    selected_option = option_menu(
        menu_title="Navigation",
        options=options,
        icons=icons,
        menu_icon="list",
        default_index=0,
    )

# Display content based on selected option
if selected_option == "Translate":
    st.header("Welcome to the Translator page!")
    st.write("input")
    text = st.text_input("Enter Input")
    target_language = st.text_input("Target Language")
    submit = st.button("Submit")

    if submit:
        st.write(text)
        # Create the prompt for translation
        prompt = f"Please translate '{text}' to '{target_language}.'"
        st.write("Translating...")
        # Generate text with the model
        try:
            response = model.generate_content(prompt)
            st.subheader("Transleted to " + target_language)

            # Extract the translated text from the response
            translated_text = response.text

            # Print the translated text
            print(f"Translated text: {translated_text}")
            st.write(translated_text)
        except Exception as e:
            print(e)
            st.write("We are not in your language yet...")
        

    
elif selected_option == "Text Summary":
    st.header("Text Summarization")
    text = st.text_area("Enter text here", height=250)
    submit = st.button("Submit")

    if submit:
        st.text("Summarizing...")
        prompt = f"Please Summarize the text delimeted by ```  text: ```{text}```  and give a short summary'"
        try:
            response = model.generate_content(prompt)
            print(response.text)
            st.subheader("Summary:")
            st.write(response.text)
        except Exception as e:
            print(e)
            st.write("Some Error Occured...")


elif selected_option == "Data Analysis":
    st.header("Research and QA")
    url_1 = st.text_input("Enter URL1")
    url_2 = st.text_input("Enter URL2")
    url_3 = st.text_input("Enter URL3")
    submit = st.button("Submit")

    if submit:
        urls = [url_1, url_2, url_3]
        loader = UnstructuredURLLoader(urls=urls)
        st.write("Loading the URLs...")
        data = loader.load()
        # print("Data: " + data)
        st.write("Summarizing the content...")
        try:
            prompt = f"Please Summarize the text delimited by ```  text: ```{data}```  and a short summary as well as the give key insights about the text'"
            response = model.generate_content(prompt)
            print(response.text)
            st.write(response.text)
        except Exception as e:
            print(e)
            st.write("Something went wrong ...")
        
    
else:
    st.header("Generate Questions from your Text")
    file = st.file_uploader("Enter a file")
    loader = PyPDFLoader("LangChain_Cheat_Sheet_KDnuggets.pdf")

    submit = st.button("Submit")
    if submit:
        data = loader.load()
        st.write("Generating...")
        data = data[0].page_content
        try:
            prompt = f"List out the questions from the data delimeted by ``` data: ```{data}```'"
            response = model.generate_content(prompt)
            st.subheader("Generated Questions: ")
            print(response.text)
            st.write(response.text)
        except Exception as e:
            print(e)
            st.write("Something went wrong ...")
