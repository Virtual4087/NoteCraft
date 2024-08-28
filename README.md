# Notecraft

Notecraft is an innovative web application designed to transform users' images and PDFs of their notes into structured, comprehensive study materials. The platform leverages OCR technology to extract text from images and PDFs and utilizes AI to generate summaries, notes, flashcards, and interactive tests. This application aims to simplify the study process by providing a seamless and efficient way for users to create study aids from their existing notes.

## Table of Contents

- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Distinctiveness and Complexity

### Distinctiveness

Notecraft stands out from other projects in its innovative approach to generating study materials from user-provided images and PDFs. Unlike typical social networks or e-commerce sites, Notecraft focuses on educational content transformation using advanced technologies such as Optical Character Recognition (OCR) and AI-based natural language processing. This project does not resemble any other project in this course and is far removed from the old CS50W Pizza project. The primary goal of Notecraft is to enhance the study experience by automatically creating structured learning materials, which is distinct from other web applications that might focus on social interactions or online transactions.

### Complexity

The complexity of Notecraft arises from several aspects:
1. **Integration of OCR and AI**: Notecraft combines OCR technology to extract text from images and PDFs with AI to generate summaries, notes, and flashcards. This involves complex data processing and API integrations.
2. **Interactive Test Creation**: The platform allows users to generate and take interactive tests based on their study materials. This feature requires dynamic content generation, user interaction handling, and real-time feedback.
3. **Data Storage and Retrieval**: Efficiently storing and retrieving user-generated content and ensuring data consistency and integrity add to the project's complexity.
4. **Mobile-Responsive Design**: Ensuring the application is fully responsive and accessible on various devices requires careful planning and design.

## Features

- **File Upload**: Users can upload images or PDFs of their notes.
- **Text Extraction**: OCR technology extracts text from the uploaded files.
- **Content Generation**: AI generates a title, summary, notes, and flashcards.
- **Interactive Tests**: Users can take tests based on the generated study materials.
- **User Authentication**: Secure login system.
- **Study Material Management**: Users can view, sort, and manage their study materials.
- **Responsive Design**: Accessible on various devices with a responsive UI.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Database**: SQLite
- **APIs**: OCR Space API, Openai API, Gemini API, Antrhopic API
- **Version Control**: Git

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/notecraft.git
   cd notecraft
   
2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
5. **Set up the database**:
   ```bash
   python manage.py makemigrations notecraft
   python manage.py migrate
   
6. **Setting Up the `.env` File**

   To configure your environment variables, create a `.env` file in the root directory of your project and add the following keys:
   
   ```plaintext
   DJANGO_SECRET_KEY=''
   OCR_API_KEY='' # Can be obtained for free from OCR.space
   AI_API_KEY=''  # Use either GEMINI_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY
   ```

   ### Required Keys:
   
   - **DJANGO_SECRET_KEY**: The secret key for your Django project.
   - **OCR_API_KEY**: API key from OCR.space, used for Optical Character Recognition (OCR).
   - **AI_API_KEY**: You must provide one API key for an AI service (choose either **GEMINI_API_KEY**, **ANTHROPIC_API_KEY**, or **OPENAI_API_KEY**).

   ### Optional Configuration:
   
   You can switch between different AI services by navigating to the appropriate lines in the code:

   - To change the AI service for generating study aids: Modify [here](https://github.com/Virtual4087/NoteCraft/blob/main/notecraft/views.py#L174).
   - To change the AI service for generating test questions: Modify [here](https://github.com/Virtual4087/NoteCraft/blob/main/notecraft/views.py#L223).
     
   If you want to change the model within the same AI service, navigate to the api_services directory in the notecraft app directory and adjust the model 
   configuration for each service individually.
   
8. **Run the server**:
   ```bash
   python manage.py runserver

## Usage

1. **Register an account or log in**.
2. **Upload images or PDFs** on the homepage.
3. **Generate study materials** by processing the uploaded files.
4. **View and manage** the generated study materials.
5. **Start tests** based on the study materials.
6. **Review test results** and study further.

## Contributing

1. **Fork the repository**.

2. **Create a new branch**:
   ```bash
   git checkout -b feature-branch
   
3. **Commit your changes**:
   ```bash
   git commit -m 'Add new feature'
   
4. **Push to the branch**:
   ```bash
   git push origin feature-branch
   
5. **Open a Pull Request**.
