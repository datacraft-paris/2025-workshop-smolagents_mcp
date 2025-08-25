# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# # Datacraft Events Assistant – Querying a Local Database with Natural Language
#
# Welcome to this hands-on notebook!  
# The goal is to build an intelligent assistant that can answer questions like (using a database of events extracted from Datacraft’s internal calendar):
#
# > *"What are the upcoming events in French?"*  
# > *"How many workshops are related to AI?"*
#
# All of that by querying a **local database** using a **natural language interface** powered by an LLM (Large Language Model).
#
#
# ## What You'll Learn
#
# In this notebook, you will:
#
# Connect a natural language agent to a local SQLite database  
# Define a tool that lets the agent run SQL queries  
# Ask real questions and get structured answers
#
# You’ll also learn how to use the [`smolagents`](https://github.com/smol-ai/smolagent) framework to combine tools with LLMs like GPT-4.
#
#
# ## The `events` Database
#
# The agent will query a local database of events extracted from Datacraft’s internal calendar.  
# The database is a simple SQLite file called `events.db`, and it contains a single table: **`evenements`**.
#
# Each row represents one event (a workshop, talk, or training session).
#
# ### Main columns:
#
# | Column         | Description                                        |
# |----------------|----------------------------------------------------|
# | `nomenclature` | Unique code for the event (e.g. `0706-AI-Intro`)   |
# | `titre`        | Event title (e.g. `"Intro to Generative AI"`)      |
# | `description`  | Full description of the event                      |
# | `date`         | Date of the event (as text, e.g. `2024-06-03`)     |
# | `horaire`      | Time range (e.g. `"9h00 - 17h30"`)                 |
# | `tag`          | Topics or tags (e.g. `#AI`, `#DataGouv`)           |
# | `langue`       | Language of the event (e.g. `"français"`, `"english"`) |
#
#
# ## Technologies Used
#
# This notebook uses:
#
# - `smolagent` – to manage the agent and tools
# - `OpenAI` – to interpret your questions
# - `SQLAlchemy` – to connect to the database
#
#
# ## Expected Outcome
#
# By the end of this notebook, you’ll be able to write:
#
# ```python
# agent.run("List all French events after July 1st.")

# +
import os
from smolagents import tool, CodeAgent, OpenAIServerModel
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv(override=True)
# -

# ## Getting more info about the database column names

engine = create_engine("sqlite:///../../data/events.db")
inspector = inspect(engine)
for col_info in inspector.get_columns("evenements"):
    print(col_info["name"])


# ### Defining a Tool for the Agent: `query_events_db`
#
# In `smolagent`, a **tool** is a Python function that the agent can call to interact with the outside world — such as querying a database, calling an API, reading a file, or performing calculations.
#
# #### Why define a tool?
#
# LLMs like GPT-4 don't have direct access to your local environment or files.  
# By wrapping a function with the `@tool` decorator, you allow the agent to **"see" and use** that function when it decides it's relevant to the user’s question.
#
#
# #### What does a tool need?
#
# A tool in `smolagent` is simply a Python function, but it must follow these **three key rules**:
#
# 1. **A clear and unique name**  
#    The name of the function is how the agent will refer to it internally. It should describe the action it performs.
#
# 2. **A well-written docstring**  
#    The agent reads the docstring to understand:
#    - what the tool does
#    - how to use it
#    - what arguments it accepts
#    - what it returns  
#    
#    Without a good docstring, the agent will either ignore the tool or misuse it.
#
# 3. **A simple and reliable interface**  
#    The tool should expect only standard Python types as arguments (`str`, `int`, `float`, etc.) and return a string or JSON-serializable output.
#
# #### Our example: `query_events_db`
#
# This tool allows the agent to send **raw SQL queries** to the `evenements` table in our local database.
#
# You can ask the agent:
# - `"What are the events in French?"`
# - `"List all events that mention AI."`
# - `"How many events are scheduled after July?"`
#
# The agent will translate your question into SQL, run the query using this tool, and return the results in plain text.

@tool
def query_events_db(query: str) -> str:
    """
    Allows querying the `evenements` table, which contains cleaned information about workshops and events.

    Table: evenements

    Available columns include:
    - nomenclature: unique identifier or code for the event (e.g. "0706-MiniFormation-Capdigital")
    - titre: title of the event (e.g. "Introduction to Generative AI")
    - description: detailed description of the event
    - date: date of the event, stored as text (e.g. "2024-06-03")
    - horaire: time slot or duration of the event (e.g. "9h00 - 17h30")
    - tag: optional topic tags (e.g. "#DataGouv", "#IA")
    - langue: language of the event (e.g. "français", "anglais")

    You can write SQL queries such as:
    - SELECT titre FROM evenements WHERE langue = 'français';
    - SELECT COUNT(*) FROM evenements WHERE tag LIKE '%IA%';
    - SELECT DISTINCT langue FROM evenements;
    - SELECT * FROM evenements ORDER BY date DESC;

    Note: the `date` column is stored as text. If you need to sort or filter by date,
    you can use SQL date functions (e.g. `STRFTIME`) or cast the column as needed.

    Args:
        query: A valid SQL query string to execute on the `evenements` table.

    Returns:
        A string containing the query results in plain text format.
    """
    engine = create_engine("sqlite:///../../data/events.db")
    output = ""
    with engine.connect() as con:
        rows = con.execute(text(query))
        for row in rows:
            output += "\n" + str(row)
    return output


# We now set up the model that will power the agent.
# We’re using OpenAI’s API to access the model gpt-4o.

model = OpenAIServerModel(
    model_id="gpt-4o",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)

#
# Now that we have:
#
# - a model (`gpt-4o` via OpenAI),
# - a tool (`query_events_db`) that knows how to query the event database,  
#
# we can combine them into a single `CodeAgent`.
#
# The `CodeAgent` is the core component of the `smolagent` framework.  
# It takes a list of tools and a language model, and automatically decides:
#
# - When to call a tool
# - How to use it
# - What answer to return to the user
#

agent = CodeAgent(
    tools=[query_events_db],
    model=model,
)

# let's try it ! 

question = "What are the different types of events organized?"
agent.run(question)
