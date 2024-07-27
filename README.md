# Notecraft

Notecraft is an online platform that transforms users' images and PDFs of their notes into structured study materials. The website uses OCR technology to extract text and processes this text with AI to generate summaries, notes, flashcards, and tests.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- **File Upload**: Users can upload images or PDFs of their notes.
- **Text Extraction**: OCR technology extracts text from the uploaded files.
- **Content Generation**: AI generates a title, summary, notes, and flashcards.
- **Interactive Tests**: Users can take tests based on the generated study materials.
- **User Authentication**: Secure registration and login system.
- **Study Material Management**: Users can view, sort, and manage their study materials.
- **Responsive Design**: Accessible on various devices with a responsive UI.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Database**: MySQL
- **APIs**: OCR Space API, ChatGPT API
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
   python manage.py makemigrations
   python manage.py migrate
   
6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   
7. **Run the server**:
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
