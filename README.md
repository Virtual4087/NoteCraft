# NoteCraft

Notecraft is an innovative web application designed to transform users' images and PDFs of their notes into structured, comprehensive study aids. The platform leverages OCR technology to extract text from images and PDFs and utilizes AI to generate summaries, notes, flashcards, and interactive tests. This application aims to simplify the study process by providing a seamless and efficient way for users to create study aids from their existing notes.

## Table of Contents

- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Distinctiveness and Complexity

Notecraft is a project that differs significantly from usual course projects, particularly ones that resemble social networks or e-commerce systems. Notecraft's primary goal is to help students study more effectively by automating the development of study aids from printed or digital text sources. This emphasis on educational productivity, rather than user interaction or commercial transactions, distinguishes it from similar efforts that may simply mimic current models such as social media or online shopping.

Notecraft's ability to combine cutting-edge AI models with Optical Character Recognition (OCR) technology to produce study aids is one of its primary differentiators. Notecraft uses a pipeline for text extraction, artificial intelligence processing, and content creation, in contrast to an e-commerce site, which focuses largely on handling products, transactions, and user interactions. This calls for knowledge of AI and OCR technologies in addition to the ability to smoothly incorporate them into a dependable and user-friendly online application.

The complexity of Notecraft is heightened by its requirement to manage a variety of input data formats, including PDFs and images of book pages, and to provide meaningful and practical study materials, including summaries, notes, and flashcards. This isn't limited to social networks, where managing data and facilitating user interaction are usually the main problems. The difficulty with Notecraft is that the content it creates needs to be accurate and relevant, which calls for sophisticated AI model tuning and algorithms.

Additionally, Notecraft helps students with a particular problem they face: the time and effort needed to make study tools that work. An e-commerce site or social network concentrates on enabling transactions, whereas Notecraft offers a useful tool that has a direct influence on learning. This educational focus, which represents a profound comprehension of the particular needs of its target users, marks a considerable shift from more general-purpose apps.

In summary, Notecraft stands apart from other projects because of its specific focus on creating educational content, the incorporation of cutting-edge technology like AI and OCR, and the particular difficulties involved in processing and creating study aids. Its complexity comes from the clever conversion of unprocessed data into priceless teaching tools rather than from user interaction or transactional procedures. Because of this, Notecraft stands out in the field of educational technology solutions and is also a very creative solution.

## Features

- **File Upload**: Users can upload images or PDFs of their notes.
- **Text Extraction**: OCR technology extracts text from the uploaded files.
- **Content Generation**: AI generates a title, summary, notes, and flashcards.
- **Interactive Tests**: Users can take tests based on the generated study aids.
- **User Authentication**: Secure login system.
- **Study Aid Management**: Users can view, sort, and manage their study aids.
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
   python -m venv .venv

   # For Git bash:
   source .venv/Scripts/activate

   # For Powershell:
   .venv\\Scripts\\activate   
   
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
5. **Set up the database**:
   ```bash
   python manage.py makemigrations notecraft
   python manage.py migrate
   
6. **Set Up the `.env` File**

   To configure your environment variables, create a `.env` file in the root directory of your project and add the following keys:
   
   ```plaintext
   DJANGO_SECRET_KEY=''
   OCR_API_KEY='' # Can be obtained for free from OCR.space

   #(Use any one of these)
   GEMINI_API_KEY=''
   ANTHROPIC_API_KEY=''
   OPENAI_API_KEY=''
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
3. **Generate study aids** by processing the uploaded files.
4. **View and manage** the generated study aids.
5. **Start tests** based on the study aids.
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
