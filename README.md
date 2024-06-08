# Application Setup and Run Instructions

```bash
https://rabyte.streamlit.app/
```

## Setup Environment

Before running the application, ensure that you install all the necessary dependencies:

```bash
pip install -r requirements.txt
```
This command will install all the required Python packages listed in requirements.txt.

## Running the Streamlit Interface

To run the Streamlit interface which provides a graphical user interface for the application, use the following command:

```
streamlit run streamlit_app.py
```

This will start the Streamlit server, and you should see a URL in the terminal where you can access the web interface.

## Running the API

For the API that handles the functionality directly, you need to run app.py. Execute the following command to start the Flask server:

```
python app.py
```

Once the server is running, you can access the API at:
```
http://localhost:5000/rabyte-translation
```

### Using the API
To use the API, you need to send a POST request to http://localhost:5000/ravigate-translation with an MP4 file as input. You must include two parameters:

- **remove_profanity**: Set this to 'Yes' to remove profanity from the translations, or 'No' to leave the content as is.
- **language**: Specify one of the 29 languages you want the output to be translated into.


# DEMO
https://github.com/bhavikakaliya/compass-hackathon-rabyte/blob/main/rabyte.mp4
https://rabyte.streamlit.app/



