const studyMaterial = document.querySelector('#studMatBlock');
const test = document.querySelector('#testBlock');
const questions = document.querySelector('#questions');
const nextButton = document.querySelector('#nextButton');
const prevButton = document.querySelector('#prevButton');
const submitButton = document.querySelector('#submitButton');
let questionSet = {};
let selected = {};
let index = 0;
// Switching between study material and test
function switchToTest(event, token, id){
    event.target.disabled = true;
    event.target.innerHTML = "Loading...";
    fetch("/test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            id: id,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        if (data.success == true) {
            Object.entries(data.questions.MCQ).forEach(([key, value]) => {
                questionSet[key] = value;
                selected[key] = null;
                const question = document.createElement('div');
                question.dataset.q = key;
                question.classList.add('hidden');
                question.innerHTML += `<div>${key}</div>`;
                Object.entries(value).forEach(([key1, value1]) => {
                    question.innerHTML += `<div data-choice="${key1}" onclick="select(event)">${key1}</div>`
                });
                questions.appendChild(question);

            });

            Object.entries(data.questions.TOF).forEach(([key, value]) => {
                questionSet[key] = value;
                selected[key] = null;
                const question = document.createElement('div');
                question.dataset.q = key;
                question.classList.add('hidden');
                question.innerHTML += `<div>${key}</div>`;
                question.innerHTML += `<div data-choice="true" onclick="select(event)">True</div>`;
                question.innerHTML += `<div data-choice="false" onclick="select(event)">False</div>`;
                questions.appendChild(question);
            });

            questions.children[index].classList.remove('hidden');
            studyMaterial.classList.add('hidden');
            test.classList.remove('hidden');
        } else {
            alert("Some error occured");
        }
        event.target.disabled = false;
        event.target.innerHTML = "Start Test";
    });
}

// For Study Material
function flip(event) {
    event.target.classList.toggle("bg-gray-200");
    event.target.children[0].classList.toggle("hidden");
    event.target.children[1].classList.toggle("hidden");
}

// For test
function next(){
    if (index < 9){
        prevButton.disabled = false;
        questions.children[index].classList.add('hidden');
        index++;
        questions.children[index].classList.remove('hidden');
        if (index == 9){
            nextButton.disabled = true;
            submitButton.classList.remove('hidden');
        }
    }
}

function prev(){
    if (index > 0){
        nextButton.disabled = false;
        submitButton.classList.add('hidden');
        questions.children[index].classList.add('hidden');
        index--;
        questions.children[index].classList.remove('hidden');
        if (index == 0){
            prevButton.disabled = true;
        }
    }
}

function select(event){
    const selection = event.target;
    selected[selection.parentElement.dataset.q] = selection.dataset.choice;
    Array.from(event.target.parentElement.children).forEach((element) => {
        element.classList.remove('bg-gray-200');
    });
    selection.classList.add('bg-gray-200');
}

function submitAnswers(){
    console.log(questionSet);
    console.log(selected);
    marks = 0;
    Object.entries(selected).forEach(([key, value]) => {
        if (selected[key]){
            try{
                if (questionSet[key][value] == true || JSON.parse(questionSet[key]) == true){
                    marks++;
                }
            }            
            catch (e){
            }
        }
    });
    console.log(marks);
}