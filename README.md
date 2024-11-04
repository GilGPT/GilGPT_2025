# Welcome to GilGPT

0. Download source files
1. Install a virtual environment:
~~~
python -m venv .venv
~~~
2. Activate the virtual environment:
~~~
.venv/Scripts/activate
~~~
3. Install packages via requirements.txt
~~~
pip install -r requirements.txt
~~~
4. Insert your OpenAI API and Unstructured API Key in the .env file located at the root directory
5. Insert your desired .pdf files into a *new folder* and change the name of the variable **file_path** in **agent_pool.py** to the name of the folder
6. Run the Streamlit application locally:
~~~
streamlit run app.py
~~~
7. Once started the chosen .pdf file in your newly created folder (see 5.) will be turned into vectores and loaded into your knowledge base
8. A new window will open in your browser
9. Now you can interact with Gillie
10. To terminate the GilGPT application use CTRL+C
