const microphoneBtn = document.getElementById('microphone-btn');
const statusElement = document.getElementById('status');
const taskList = document.getElementById('task-list');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
    statusElement.textContent = "Your browser does not support the Web Speech API. Please try Chrome.";
    microphoneBtn.disabled = true;
} else {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    microphoneBtn.addEventListener('click', () => {
        statusElement.textContent = "Listening...";
        microphoneBtn.disabled = true;
        recognition.start();
    });

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        statusElement.textContent = `Heard: "${speechResult}"`;
        addTask(speechResult);
    };

    recognition.onend = () => {
        statusElement.textContent = "Click the microphone to start speaking...";
        microphoneBtn.disabled = false;
    };

    recognition.onerror = (event) => {
        microphoneBtn.disabled = false;
        statusElement.textContent = `Error: ${event.error}. Click the microphone to try again.`;
        console.error('Speech recognition error:', event.error);
        if (event.error === 'not-allowed') {
            statusElement.textContent += " Please allow microphone access.";
        }
    };

    function addTask(text) {
        if (text.trim() === '') {
            statusElement.textContent = "No valid task recognized. Please try again.";
            return;
        }

        const listItem = document.createElement('li');

        // Create Checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.addEventListener('change', () => {
            listItem.classList.toggle('completed', checkbox.checked); // Add/remove 'completed' class based on checkbox state
        });
        listItem.appendChild(checkbox);

        // Create Task Text Span
        const taskTextSpan = document.createElement('span');
        taskTextSpan.textContent = text;
        taskTextSpan.classList.add('task-text'); // Add a class for specific text styling
        listItem.appendChild(taskTextSpan);

        // Create Delete Button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'delete-btn';
        deleteButton.onclick = () => {
            taskList.removeChild(listItem);
        };
        listItem.appendChild(deleteButton);

        taskList.prepend(listItem); // Add new tasks to the top
    }
}