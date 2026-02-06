document.addEventListener('DOMContentLoaded', function () {
    console.log('UMatter - Virasat se Vikas tak Theme Loaded');
});

/* Navigation Logic */
function startTest() {
    // Simple redirect
    window.location.href = "/trauma-assessment/";
}

/* Trauma Assessment Logic */
function calculateTrauma() {
    let scores = {
        family: 0,
        financial: 0,
        career: 0,
        love: 0,
        none: 0
    };

    let answerFound = false;
    let selectedRadios = document.querySelectorAll('input[type="radio"]:checked');

    // In case the user hasn't answered 4 questions (since we might have multiple questions)
    // The user's original code checked for answers.length < 4. 
    // We will relax this check slightly or ensure the HTML matches.
    if (selectedRadios.length < 4) {
        alert("Please answer all questions to get an accurate result.");
        return;
    }

    selectedRadios.forEach(answer => {
        if (scores.hasOwnProperty(answer.value)) {
            scores[answer.value]++;
        }
    });

    // Find Logic
    let maxType = 'none';
    let maxCount = -1;
    for (const [type, count] of Object.entries(scores)) {
        if (count > maxCount) {
            maxCount = count;
            maxType = type;
        }
    }

    let resultText = "";
    let resultColor = "";

    switch (maxType) {
        case "family":
            resultText = "You are experiencing Family Trauma. Consider family counseling and emotional support.";
            resultColor = "#D32F2F";
            break;
        case "financial":
            resultText = "You are experiencing Financial Stress. Financial planning and stress management may help.";
            resultColor = "#FF9933";
            break;
        case "career":
            resultText = "You are experiencing Career Anxiety. Career guidance and mindfulness are recommended.";
            resultColor = "#000080";
            break;
        case "love":
            resultText = "You are experiencing Love/Relationship Trauma. Emotional healing and therapy can help.";
            resultColor = "#E91E63";
            break;
        default:
            resultText = "You seem to be managing well. Keep practicing self-care.";
            resultColor = "#4CAF50";
    }

    const resultDiv = document.getElementById("result");
    resultDiv.style.display = 'block';
    resultDiv.style.padding = '20px';
    resultDiv.style.marginTop = '20px';
    resultDiv.style.borderRadius = '8px';
    resultDiv.style.backgroundColor = 'rgba(255,255,255,0.9)';
    resultDiv.style.borderLeft = `5px solid ${resultColor}`;
    resultDiv.innerHTML = `<h3 style="color:${resultColor}">Result</h3><p>${resultText}</p>`;

    resultDiv.scrollIntoView({ behavior: "smooth" });
}

/* Account Logic */
function enableEdit() {
    document.getElementById("nameInput").disabled = false;
    document.getElementById("emailInput").disabled = false;
    // Visual cue
    document.getElementById("nameInput").focus();
}

function saveProfile() {
    // Lock inputs
    document.getElementById("nameInput").disabled = true;
    document.getElementById("emailInput").disabled = true;

    // Update Display Card (User's request)
    const newName = document.getElementById("nameInput").value;
    const newEmail = document.getElementById("emailInput").value;

    document.getElementById("username").innerText = newName;
    document.getElementById("emailDisplay").innerText = newEmail; // Changed ID to avoid conflict with input

    alert("Profile updated successfully!");
}

function logout() {
    if (confirm("Are you sure you want to logout?")) {
        alert("You have been logged out.");
        window.location.href = "/";
    }
}

/* Self Care Logic */
function showHelp() {
    alert(
        "If you are in immediate danger, please contact:\n\n" +
        "• National Mental Health Helpline\n" +
        "• Local Emergency Services\n\n" +
        "You matter. Help is available."
    );
}

/* Progress Logic */
function saveMood(mood) {
    const display = document.getElementById("moodResult");
    display.innerText = "Today's mood recorded: " + mood + " 💙";
    display.style.color = "var(--progress-blue)";
}
