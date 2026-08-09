import os
import time
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from flask import Flask,render_template, request, jsonify
import mysql.connector
from config import DB_CONFIG,GEMINI_API_KEY
from google import genai
from google.genai.errors import ClientError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
client = genai.Client(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=13334,
        ssl_ca=DB_CONFIG["ssl"]["ca"],
        ssl_verify_cert=True
    )


@app.route("/")
def home():
    return render_template("index.html")


# User Registration
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        print(data)

        full_name = data["full_name"]
        email = data["email"]
        password = data["password"]
        hashed_password = generate_password_hash(password)
        

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (full_name, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (full_name, email, hashed_password))
        conn.commit()
        print("Inserted rows:",cursor.rowcount)

        cursor.close()
        conn.close()

        return jsonify({
            "message": "User Registered Successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html") 

@app.route("/upload")
def upload_page():
    return render_template("upload.html")  

@app.route("/chat")
def chat_page():
    return render_template("chat.html")  

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")
     
    
#user log in
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        email = data["email"]
        password = data["password"]
        

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[3], password):
             return jsonify({
            "message": "Login Successful"
        })
        else:
             return jsonify({
            "message": "Invalid Email or Password"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })  


#create study_note api
@app.route("/add-note", methods=["POST"])
def add_note():
    try:
        data = request.json

        document_id = data["document_id"]
        notes = data["notes"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO study_notes (document_id, notes)
        VALUES (%s, %s)
        """

        cursor.execute(query, (document_id, notes))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Study note added successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

#view study note api
@app.route("/notes", methods=["GET"])
def get_notes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM study_notes")
        notes = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(notes)

    except Exception as e:
        return jsonify({"error": str(e)})    

#ducument upload API
@app.route("/upload-document", methods=["POST"])
def upload_document():
    try:
        data = request.json

        user_id = data["user_id"]
        file_name = data["file_name"]
        file_type = data["file_type"]
        summary = data["summary"]

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO documents
        (user_id, file_name, file_type, summary)
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(query, (user_id, file_name, file_type, summary))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Document uploaded successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })
    
#file upload api
@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"})

    filename = secure_filename(file.filename)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)
    text = extract_text_from_pdf(filepath)

    # Store the extracted PDF text
    app.config["CURRENT_PDF_TEXT"] = text

    print("EXTRACTED TEXT LENGTH:", len(text))
    print("EXTRACTED TEXT:", text[:500])

    summary = generate_summary(text[:50000])

    if summary is None:
        return jsonify({
        "error": "Gemini API request failed."
    })

    import json

    summary = summary.replace("```json", "").replace("```", "").strip()

    summary = json.loads(summary)
        

    return jsonify({
    "message": "PDF uploaded successfully",
    "filename": filename,
    "overview": summary["overview"],
    "important_points": summary["important_points"],
    "technologies": summary["technologies"],
    "key_takeaways": summary["key_takeaways"]
})
  
#Read pdf api
@app.route("/read-pdf", methods=["POST"])
def read_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files["file"]

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return jsonify({
            "message": "PDF read successfully",
            "text": text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }) 

#generate summary    
def generate_summary(text):

    try:
        response = client.models.generate_content(
           model="gemini-3.5-flash",
            contents=f"""
You are StudyMate AI.

Read the following PDF and return ONLY valid JSON.

Do not write explanations.
Do not use Markdown.
Do not use ```json.

IMPORTANT RULES FOR TECHNOLOGIES:

1. List ONLY technologies explicitly mentioned in the PDF.
2. Do NOT guess or invent technologies.
3. Do NOT include general skills such as:
   - Teamwork
   - Communication
   - Problem solving
   - Leadership
   - Time management
4. Do NOT include academic subjects unless they are clearly a technology.
5. Include programming languages, frameworks, libraries, databases,
   development tools, and platforms when explicitly mentioned.
6. If no technologies are mentioned, return an empty array [].

Return exactly this structure:

{{
  "overview": [
    "Sentence 1",
    "Sentence 2"
  ],
  "important_points": [
    "Point 1",
    "Point 2",
    "Point 3"
  ],
  "technologies": [
    "Technology 1",
    "Technology 2"
  ],
  "key_takeaways": [
    "Takeaway 1",
    "Takeaway 2"
  ]
}}

PDF:
{text}
"""
        )

        print("========== RAW GEMINI RESPONSE ==========")
        print(response.text)

        return response.text

    except Exception as e:
        print("========== GEMINI ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        return None

# Ask AI API
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.json

        question = data.get("question")

        if not question:
            return jsonify({
                "error": "Question is required"
            })

        pdf_text = app.config.get("CURRENT_PDF_TEXT", "")

        if not pdf_text:
            return jsonify({
                "error": "Please upload a PDF first."
            })

        import time

        for i in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=f"""
You are StudyMate AI.

Answer the user's question ONLY using the PDF content given below.

If the answer is not available in the PDF, say:
"Information not found in the uploaded PDF."

PDF Content:
{pdf_text}

User Question:
{question}
"""
                )

                return jsonify({
                    "answer": response.text
                })

            except Exception as e:
                if i == 2:
                    return jsonify({
                        "error": str(e)
                    })

                time.sleep(3)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })
    
#generate quiz api
# Generate Quiz API
@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    try:

        # Get uploaded PDF text
        pdf_text = app.config.get("CURRENT_PDF_TEXT", "")

        if not pdf_text:
            return jsonify({
                "error": "Please upload a PDF first."
            })


        # Call Gemini 3.5 Flash
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"""
You are StudyMate AI.

Your task is to generate a quiz ONLY from the uploaded PDF.

IMPORTANT INSTRUCTIONS:

1. Read and understand the complete PDF.
2. Identify all important points, concepts, definitions, formulas,
   keywords, headings, and major topics.
3. Give higher priority to topics that contain more important information.
4. Generate MORE questions from topics that have MORE important points.
5. Generate FEWER questions from topics that have less important information.
6. Do not create questions from information that is not present in the PDF.
7. Do not repeat the same question.
8. Every question must have exactly 4 options.
9. The "answer" must exactly match one of the four options.
10. The number of questions must be dynamic according to the amount
    of important content.

QUESTION COUNT:

- Very small amount of important content: 5 questions
- Small amount of important content: 5-7 questions
- Medium amount of important content: 10 questions
- Large amount of important content: 15 questions
- Very large amount of important content: 20 questions

For example:
If Topic A has 10 important points and Topic B has 3 important points,
generate more questions from Topic A than Topic B.

Return ONLY valid JSON.
Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations before or after the JSON.

JSON FORMAT:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "answer": "Correct option"
        }}
    ]
}}

PDF CONTENT:

{pdf_text}
"""
        )


        # Get Gemini response
        quiz_text = response.text.strip()


        print("========== RAW QUIZ RESPONSE ==========")
        print(quiz_text)


        # Remove Markdown code fences if Gemini adds them
        quiz_text = quiz_text.replace("```json", "")
        quiz_text = quiz_text.replace("```", "")
        quiz_text = quiz_text.strip()


        # Convert JSON string into Python object
        import json

        try:

            quiz = json.loads(quiz_text)

        except json.JSONDecodeError:

            return jsonify({
                "error": "Gemini returned invalid JSON.",
                "response": response.text
            })


        # Check questions
        if "questions" not in quiz:

            return jsonify({
                "error": "Quiz does not contain questions."
            })


        if not quiz["questions"]:

            return jsonify({
                "error": "No questions were generated."
            })


        # Return quiz to JavaScript
        return jsonify({
            "quiz": quiz
        })


    except Exception as e:

        print("========== QUIZ ERROR ==========")
        print(type(e).__name__)
        print(str(e))

        return jsonify({
            "error": str(e)
        })      

if __name__ == "__main__":
    app.run(debug=True)