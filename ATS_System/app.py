from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import openai

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_openai_response(input_text, pdf_content, prompt):
    """
    Generate response using OpenAI's GPT-4o model for resume analysis
    """
    try:
        # Prepare the image content
        base64_image = pdf_content[0]["data"]

        # Construct the messages for the API call
        messages = [
            {
                "role": "system",
                "content": "You are an experienced Technical Human Resource Manager analyzing a resume."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Job Description: {prompt}\n\nAnalysis Request: {input_text}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        # Make API call to OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "Error processing the resume"


def input_pdf_setup(uploaded_file):
    """
    Convert uploaded PDF to base64 encoded image
    """
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit App Configuration
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input Areas
input_text = st.text_area("Copy and paste your job description from LinkedIn or anywhere ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

# Button Definitions
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# Prompts
input_prompt1 = """ You are an experienced Technical Human Resource Manager with a keen understanding of assessing candidate profiles against job requirements. Your task is to thoroughly review the provided resume and evaluate the candidate's alignment with the job description."
"Please provide a detailed and professional assessment of the applicant’s qualifications, skills, and experiences in relation to the specified role."
"Your evaluation should address the following points:"
"Core Alignment: Assess whether the candidate's technical and professional skills match the job's core requirements. Highlight specific qualifications or experiences that demonstrate suitability.",
"Strengths: Identify and elaborate on the candidate's key strengths, including technical competencies, soft skills, certifications, achievements, and notable projects, that make them stand out for the role.",
"Gaps and Weaknesses: Point out any missing skills, qualifications, or experiences that may hinder the candidate's ability to perform the job effectively. Suggest areas for improvement or development.",
"Relevance: Evaluate the relevance of the candidate’s past roles, projects, and accomplishments to the responsibilities of the job.",
"Cultural Fit: Consider the candidate's values, interests, and extracurricular activities in determining their potential cultural alignment with the company or team.",
"Growth Potential: Analyze the candidate’s ability to grow into the role and their potential for long-term success within the organization.",
"Final Recommendation: Conclude with your overall impression of the candidate’s suitability for the role. Include whether you would recommend them for further consideration or suggest they be considered for a different position better suited to their qualifications."
"Provide clear, specific, and actionable insights to ensure your evaluation aids in making an informed decision."""

input_prompt3 = """
You are a highly skilled ATS (Applicant Tracking System) scanner with in-depth expertise in data science and ATS functionalities. Your task is to evaluate the uploaded resume against the provided job description and provide a detailed assessment.",
"Your evaluation should include the following key points:"
"Match Percentage:Analyze the resume to determine the percentage of alignment with the job description. Consider factors such as skills, qualifications, relevant experience, and keywords. Provide a clear percentage score as the primary output.",
"Missing Keywords:Identify and list the specific keywords, phrases, or competencies from the job description that are missing in the resume. Highlight these gaps to offer actionable insights for improvement.",
"Final Thoughts:Share your final assessment of the resume’s overall quality and suitability for the role. Mention whether the candidate’s profile demonstrates strong alignment, partial alignment, or weak alignment with the job requirements. Provide recommendations for further action, such as refining the resume or proceeding with the application.",
Ensure your evaluation is precise, detailed, and provides valuable feedback to enhance the applicant's chances of success. Focus on both technical and soft skills while ensuring a holistic match with the job description.
"""

# Processing Submissions
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")