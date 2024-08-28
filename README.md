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

Notecraft is a project that stands out distinctly from typical course projects, particularly those that resemble social networks or e-commerce platforms. The primary focus of Notecraft is on enhancing the study process for students by automating the creation of study aids from printed or digital text sources. This focus on educational productivity, rather than on user interaction or commercial transactions, sets it apart from other projects that might merely replicate existing models like social media or online stores.

One of the key aspects that distinguish Notecraft is its integration of Optical Character Recognition (OCR) technology with advanced AI models to generate study aids. Unlike an e-commerce site, which primarily involves managing products, transactions, and user interactions, Notecraft involves a complex pipeline of text extraction, natural language processing, and content generation. This requires not only an understanding of OCR and AI technologies but also the ability to integrate these technologies seamlessly into a web application that is both user-friendly and reliable.

The complexity of Notecraft is further amplified by the need to handle diverse types of input data, such as images of book pages or PDFs, and to produce coherent and useful study materials like summaries, notes, and flashcards. This goes beyond the scope of a social network, where the primary challenges are typically related to user interaction and data management. Notecraft’s challenge lies in the accuracy and relevance of the content it generates, which requires algorithms and careful tuning of the AI models used.

Moreover, Notecraft addresses a specific pain point for students—the time and effort required to create effective study aids. While a social network focuses on connecting users or an e-commerce site on facilitating transactions, Notecraft provides a functional tool that directly impacts the learning process. This educational focus is a significant departure from more general-purpose applications, reflecting a deep understanding of the specific needs of its target users.

In summary, Notecraft is distinct from other projects due to its specialized focus on educational content generation, the integration of advanced technologies like OCR and AI, and the unique challenges associated with processing and generating study aids. Its complexity lies not in user interaction or transactional processes but in the intelligent transformation of raw data into valuable educational resources. This makes Notecraft not only unique but also a highly innovative solution in the realm of educational technology.

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
   python3 -m venv venv
   source venv/bin/activate
   
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
