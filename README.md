# Financial_Chatbot

- Clone github repository for get full project source code `https://github.com/pratikrathod08/Financial_Chatbot.git`

- Clone via git or download zip and store to local folder. 

- Go to main folder you will see backend and frontend folders. 

- Go to backend root folder.

`Open Terminal and got to directory of application and move to backend folder `
```bash 
cd backend
```

## Create VENV

```bash 
python -m venv venv 
```

- Activate venv 
```bash 
venv\scripts\activate  ## For windows
source venv/bin/activate ## For linux
```

## Install requiremts and create packages 

```bash 
pip install -r requirements.txt
```

- Go to backend root folder.

`Run below command to terminal `
```bash  
deactivate  ## For deactivate backend venv
```

```bash
cd ..
## For come back in root folder
```

```bash 
cd frontend ## Go to frontend folder
```

```bash  
python -m venv venv1  ## For install frontend lib like streamlit if using node or other tech it id not required
```

```bash 
venv1\scripts\activate  ## For windows
source venv1/bin/activate ## For linux
```

```bash 
pip install -r requirements.txt ## Install frontend dependencies
```

- Create .env to backend folder and store below secret credentials 
```bash
OPENAI_API_KEY=""  ## Put here your openai api key
UPLOAD_DIR="app/data/uploads"   ## Upload directory to store data
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY=""  ## Langsmith key for tracing and observability
DB_PATH="app/faiss_index"   ## Vector db path
DB_URI=""   ## Sql database uri

```

- Go to backend folder and run application 
`Make sure to activate virtual environment before run application`
```bash 
uvicorn app.main:app --reload ## Your app will run on localhost:8000 port
```

- Go to frontend folder and run application
`Make sure to activate virtual environment before run application`
```bash 
streamlit run app.py  ## You will get fronend url from terminal after run app 
```

- Go to fronend url and browse your files and upload you will get success message after successfully upload all files. 

- Ask your question from uploaded data. 

- Check logs for uploaded files and chat history from `UPLOAD_DIR=app/data/uploads` this path.
- Also check logs for error and success from log folder inside backend folder.