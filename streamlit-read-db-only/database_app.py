import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, select

# Streamlit app title
st.title("Database Connection and Management")

# Sidebar for database connection parameters
with st.sidebar:
    st.header("Database Connection")
    database_type = st.selectbox("Database Type", ["mysql", "postgresql", "sqlite"])
    database_url = st.text_input("Database URL/Host")
    database_name = st.text_input("Database Name")
    database_username = st.text_input("Username")
    database_password = st.text_input("Password", type="password")
    port = st.number_input("Port", value=3306 if database_type == "mysql" else 5432)

# Add connect button
if st.sidebar.button("Connect"):
    # Create connection string based on database type
    if database_type == "sqlite":
        connection_string = f"sqlite:///{database_url}"
    else:
        connection_string = f"{database_type}://{database_username}:{database_password}@{database_url}:{port}/{database_name}"

    # Connect to database
    try:
        engine = create_engine(connection_string)
        connection = engine.connect()
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Store connection in session state
        st.session_state['engine'] = engine
        st.session_state['connection'] = connection
        st.session_state['metadata'] = metadata
        
        st.success("Connected to database successfully!")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")

# If connected, show disconnect button and database interface
if 'engine' in st.session_state:
    if st.sidebar.button("Disconnect"):
        st.session_state['connection'].close()
        del st.session_state['engine']
        del st.session_state['connection']
        del st.session_state['metadata']
        st.success("Disconnected successfully!")
        st.experimental_rerun()
    
    # Show available tables
    tables = st.session_state['metadata'].tables.keys()
    selected_table = st.selectbox("Select a table", tables)
    
    if selected_table:
        table = Table(selected_table, st.session_state['metadata'], autoload_with=st.session_state['engine'])
        st.subheader(f"Table: {selected_table}")
        
        # Display table data
        query = select(table)
        df = pd.read_sql(query, st.session_state['connection'])
        st.dataframe(df)
        
        # Data input section
        st.subheader("Insert Data")
        columns = table.columns.keys()
        input_data = {}
        
        for col in columns:
            if col != "id":  # Skip auto-incrementing IDs
                input_data[col] = st.text_input(f"Enter {col}")
        
        if st.button("Insert Data"):
            if all(input_data.values()):
                with st.session_state['engine'].connect() as conn:
                    ins = table.insert().values(**input_data)
                    conn.execute(ins)
                    conn.commit()
                st.success("Data inserted successfully!")
                st.experimental_rerun()  # Refresh the table view
            else:
                st.error("Please fill all fields")
