import os 
# from dotenv import load_dotenv


# load_dotenv()


# Set up Postgres database credentials
db_credentials = {
    'dbname'    :   'appseed_db',
    'user'      :   'flask',
    'password'  :   'Tamir4578',
    'host'      :   'localhost',
    'port'      :   5432
}


# Set up OpenAI variables 
OPENAI_API_KEY  =   os.getenv("OPENAI_API_KEY")
AI_MODEL        =   'gpt-3.5-turbo-16k'
# AI_MODEL        =   'gpt-4'



# Max number of tokens permitted within a conversation exchange via OpenAI API
MAX_TOKENS_ALLOWED      =   3000


# Max number of messages to exchange with OpenAI API
MAX_MESSAGES_TO_OPENAI  =   5



# An arbitrary number to provide a buffer to avoid reaching exact token limits
TOKEN_BUFFER            =   100  
