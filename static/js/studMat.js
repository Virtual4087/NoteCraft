const studyMaterial = document.querySelector('#studMatBlock');
const test = document.querySelector('#testBlock');
const questions = document.querySelector('#questions');
const nextButton = document.querySelector('#nextButton');
const prevButton = document.querySelector('#prevButton');
const submitButton = document.querySelector('#submitButton');
const score = document.querySelector('#scoreBlock');
const questionsPreview = document.querySelector("#questionsPreview");
const finalScore = document.querySelector("#finalScore");
let questionSet = {};
let selected = {};
let index = 0;
// Switching between study material and test
function switchToTest(event, token, id){
    event.target.disabled = true;
    event.target.innerHTML = "Generating questions...";
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
            Object.entries(data.questions).forEach(([key, value]) => {
                questionSet[key] = value;
                selected[key] = null;
                const question = document.createElement('li');
                question.dataset.q = key;
                question.className = "flex flex-col gap-2 hidden";
                question.innerHTML += `<span class="font-semibold text-lg my-2">${key}</span>`;
                Object.entries(value).forEach(([key1, value1]) => {
                    question.innerHTML += `<div data-choice="${key1}" onclick="select(event)" class="px-6 py-2 rounded bg-gray-100">${key1}</div>`
                });
                questions.appendChild(question);

            });
            
            questions.children[index].classList.remove('hidden');
            studyMaterial.classList.add('hidden');
            test.classList.remove('hidden');
        } else {
            alert("Some error occured");
            event.target.innerText = "Start Test";

        }
        event.target.disabled = false;
        event.target.innerText = "Start Test";
    });
}

// For Study Material
function flip(event) {
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
        element.classList.remove('bg-blue-200');
    });
    selection.classList.add('bg-blue-200');
}

function submitAnswers(){
    console.log(questionSet);
    console.log(selected);
    marks = 0;
    let success = Object.entries(selected).some(([key, value]) => {
        if (selected[key]){
            if (questionSet[key][value] == true){
             marks++;
        }         
        }else{
            alert("Please answer all questions");
            marks = 0;
            return true;
        }
    });

    if (!success){
        test.classList.add('hidden');
        score.classList.remove('hidden');
        finalScore.innerText = `${marks}/10`;
        let count = 1;
        Object.entries(questionSet).forEach(([key, value]) => {
            const questionBox = document.createElement('div');
            questionBox.className = "flex flex-col gap-2"
            questionBox.innerHTML = `<div class="font-semibold my-1">${count}. ${key}</div>`
            Object.entries(value).forEach(([key1, value1]) => {     
                if (value1 == true){
                    questionBox.innerHTML += `<div class="px-3 py-1 text-sm rounded bg-green-100 flex justify-between">
                        <span>${key1}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-check" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="#00b341" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M5 12l5 5l10 -10" />
                        </svg>
                    </div>`
                } 
                
                else if (key1 == selected[key]){
                    questionBox.innerHTML += `<div class="px-3 py-1 text-sm rounded bg-red-100 flex justify-between">
                        <span>${key1}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-x" width="20" height="20" viewBox="0 0 24 24" stroke-width="2" stroke="#ff2825" fill="none" stroke-linecap="round" stroke-linejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                            <path d="M18 6l-12 12" />
                            <path d="M6 6l12 12" />
                        </svg>
                    </div>`
                }

                else{
                    questionBox.innerHTML +=  `<div class="px-3 py-1 text-sm rounded bg-gray-100">${key1}</div>`
                }
            })
            questionsPreview.appendChild(questionBox);
            count++;
        })
    }
}

function goBack() {
    if (window.history.length > 1 && document.referrer.includes(window.location.origin)) {
        window.history.back();
    } else {
        window.location.href = "/";
    }
}

function switchTostudMat(){
    studyMaterial.classList.remove('hidden');
    test.classList.add('hidden');
    questions.innerHTML = "";
    index = 0;
    questionSet = {};
    selected = {};
    nextButton.disabled = false;
    prevButton.disabled = true;
    submitButton.classList.add('hidden');
}