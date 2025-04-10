import ast
from sqlalchemy import create_engine, text, inspect

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


from dotenv import load_dotenv

from app.database.database import engine


load_dotenv()

model = ChatOpenAI()


def get_all_tables_and_schemas():
    
    # Use the inspector to get metadata about the database
    inspector = inspect(engine)
    
    # Get all schemas
    schemas = inspector.get_schema_names()
    
    all_tables = {}
    
    # Iterate over all schemas and get tables in each schema
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        all_tables[schema] = tables
    
    return all_tables


def get_all_tables_and_columns():
    # Use the inspector to get metadata about the database
    inspector = inspect(engine)
    
    # Get all schemas
    schemas = inspector.get_schema_names()
    
    all_tables = {}
    
    # Iterate over all schemas and get tables and their columns in each schema
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        
        # Iterate over tables to get their columns
        schema_tables = {}
        for table in tables:
            columns = inspector.get_columns(table_name=table, schema=schema)
            schema_tables[table] = columns
        
        all_tables[schema] = schema_tables
    
    return all_tables

def table_selector(schema, question):
    prompt = """
    You are best database manager you need to understand user question and provide table and schema which needs to user for get data.
    
    Here is database schema : {schema}
    
    Here is user question : {question}
    
    Note : you need to provide relevant table and schema if need join or anything else for get relevant data so you need to provide that both tables as well.
    """
    
    prompt_template = ChatPromptTemplate.from_template(prompt)
    parser = StrOutputParser()
    chain = prompt_template | model | parser
    response = chain.invoke({"schema": schema, "question": question})
    return response


def graph_requirement_check(final_schema, question):
    prompt = """
    You are best data analyst you need to understand final schema and user question and provide detail that is graph is need to replresent that data or not.
    
    Here is final schema : {final_schema}
    
    Here is user question : {question}
    
    Note : you need to give answer in yes or no only as below.
    
    if graph is executable then you need to say yes or you need to say no and remember you graph will be create by plotly, seaborn, and matplotlib so give answer to keep that in mind.
    
    """
    
    prompt_template = ChatPromptTemplate.from_template(prompt)
    parser = StrOutputParser()
    chain = prompt_template | model | parser
    response = chain.invoke({"final_schema": final_schema, "question": question})
    return response

def get_table(final_schema, question):
    prompt = """
    You are best data engineer you need to provide table name based on user question from final schema so user can perform further operations.
    
    Here is final schema : {final_schema}
    
    Here is user question : {question}
    
    Note : you need to provide table name only in string do not add any single word or alphabet extra. response should be like that 'movie name' this is example not give this exact name and do not add any symbols like '/', '\' or anything only give name of movie.
    
    """
    
    prompt_template = ChatPromptTemplate.from_template(prompt)
    parser = StrOutputParser()
    chain = prompt_template | model | parser
    response = chain.invoke({"final_schema": final_schema, "question": question})
    return response 

# Function to generate code using LLM
# def generate_code_using_llm(schema, user_query, attempt_number=1):
#     schema_description = ", ".join([f"{col} ({dtype})" for col, dtype in schema.items()])
#     prompt = (
#         f"Attempt #{attempt_number}: Given the following DataFrame schema: {schema_description}, "
#         f"generate Python code using Seaborn to {user_query}. "
#         "do not create any sample dataframe you need to use only given dataframe"
#         "You need to utilize matplotlib axis and fig to show and store graph."
#         "Ensure the code creates a visually appealing plot with labels, titles, and appropriate colors. "
#         "Remember this thing also : Passing palette without assigning hue is deprecated and will be removed in v0.14.0. Assign the x variable to hue and set legend=False for the same effect."
#         "Use 'hue' and 'pelette' for create more interactive and better graph."
#         "The plot should be stored in a variable named 'fig'."
#         "And remember you do not need to show graph so do not add 'plt.show()' this code."
#         "do not use 'ax.legend_.remove()' in code"
#     )
#     response = ChatOpenAI().generate([prompt])  # Pass the prompt as a list
#     generated_code = response.generations[0][0].text  # Access the generated text
#     return generated_code


def generate_code_using_llm(schema, user_query, attempt_number=1):

    """ Function for create sql code from schema for get required data """

    prompt = (
        f"Attempt #{attempt_number}: Given the following schema: {schema}, "
        f"generate sql query suitable for mysql {user_query}. "

        "Note : DO not do any mistake in write query understand query and accordingly execute it for table which belongs to it and do not do any mistake"
        "YOur response should be sql code do not do any mistake in sql query so it give error at the time of execution"
    )
    response = ChatOpenAI().generate([prompt])  # Pass the prompt as a list
    generated_code = response.generations[0][0].text  # Access the generated text
    return generated_code

# Function to verify code syntax
def verify_code_syntax(code):
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)