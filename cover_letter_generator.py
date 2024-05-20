import dbConnection as dbConn
from snowflake.snowpark import Session
import streamlit as st
import snowflake.connector as snconn
import json

def chatbot():
    instructions = "Be concise. Do not hallucinate"
    st.write(st.session_state.job_description)
    st.write(st.session_state.additional_info)
    # Initialize message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                'role': 'assistant',
                'content': "Hello! I'm here to help you generate a cover letter. Please upload files and provide job description to get started."
                # 'content': st.session_state.fetched_data if len(st.session_state.fetched_data) > 0 else "No files uploaded yet. Please upload files to generate cover letter."
            }
        ]
    # User input prompt
    prompt = st.chat_input("Type your message", key="chat_input")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.isFirstPrompt = True

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):  
            context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
            response = cortex.Complete('mistral-large', f"Instructions:{instructions}, context:{context}, Prompt:{prompt}",session = st.session_state.new_session)
            st.markdown(response)

            st.session_state.messages.append({
                'role': 'assistant',
                'content': response
            })


        # Scroll to the last message
        st.write('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)
        st.write('<script>var element = document.body; element.scrollTop = element.scrollHeight;</script>', unsafe_allow_html=True)


def generate_cover_letter(user_data, job_description, additional_info):
    # # Step 1: Extract relevant details from user data and job description
    st.write('Hello')
    print(st.session_state.database_conn_token)
    # personal_info = extract_personal_info(user_data,job_description,dbConnUserInfo)
    # st.write(personal_info)
    
    # # Step 2: Use the Snowflake Arctic model to generate each section
    # personal_profile = generate_personal_profile(personal_info)
    # experience_mapping = generate_experience_mapping(skills, experience, job_description)
    # gap_addressing = address_gaps(skills, job_description)
    # conclusion = generate_conclusion(personal_info)

    # Step 3: Combine all sections into a single cover letter
    # cover_letter = f"{personal_profile}\n\n{experience_mapping}\n\n{gap_addressing}\n\n{conclusion}"
    # return cover_letter
    return

def extract_personal_info(user_data, job_description, dbConnUserInfo):
    # Create a prompt to extract relevant personal information according to the job description
    prompt = [
        {
            'role': 'system',
            'content': 'You are a helpful AI assistant. Extract the relevant personal information from the user data according to the job description.'
        },
        {
            'role': 'user',
            'content': user_data
        }
    ]

    options = {
        'temperature': 0.7,
        'max_tokens': 10
    }
    # Define the parameters
    params = {
        'prompt': json.dumps(prompt),
        'options': json.dumps(options)
    }

    # Use Snowflake to generate relevant personal information
    cur = dbConnUserInfo.cursor()
    try:
        query="SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s, %s)"
        cur.execute(query, ('snowflake-arctic', params['prompt'], params['options']))
        
        result = cur.fetchall()
        print(result)
        relevant_info = result[0][0] if result else ""
    finally:
        cur.close()

    return relevant_info


# def extract_skills_experience(user_data):
#     # Extract skills and experience logic here
#     return user_data['skills'], user_data['experience']

# def generate_personal_profile(personal_info):
#     # Use Snowflake Arctic to generate personal profile
#     return f"Dear Hiring Manager,\n\nMy name is {personal_info[0]}..."

# def generate_experience_mapping(skills, experience, job_description):
#     # Use Snowflake Arctic to map skills and experience
#     return f"Based on your job description, I have the following relevant experience..."

# def address_gaps(skills, job_description):
#     # Identify and address gaps
#     return "While my experience does not directly include..., I have demonstrated..."

# def generate_conclusion(personal_info):
#     # Generate concluding paragraph
#     return "Thank you for considering my application..."

# f"Given the applicant's resume and the job description, generate a cover letter that includes the following sections: \n\n"
# f"1. Personal Profile Building Story: Introduce the applicant and highlight their core strengths and unique qualities. \n\n"
# f"2. Experience Mapping: Link the applicant's experiences and skills to the job description. Use scenarios to demonstrate impact. \n\n"
# f"3. Address Gaps: If there are gaps between the resume and job description, acknowledge and explain them. \n\n"
# f"4. Conclusion: Summarize the applicant's suitability for the role and express enthusiasm for the position. \n\n"
# f"Resume: {resume_data}\n\n"
# f"Job Description: {job_description}\n\n"
# f"Cover Letter:"
