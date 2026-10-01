const task = document.getElementById("task");
const input = document.getElementById("inputText");
const label = document.getElementById("inputLabel");
const button = document.getElementById("submitBtn");
const errorBox = document.getElementById("error");
const resultPanel = document.getElementById("resultPanel");
const result = document.getElementById("result");
const resultTitle = document.getElementById("resultTitle");
const copyBtn = document.getElementById("copyBtn");

const meta = {
  qa: ["Your question", "Example: Which is the largest ocean?"],
  explain: ["Topic to explain", "Example: Explain the Pythagoras theorem"],
  quiz: ["Passage or topic", "Paste a passage or enter a topic for 3 MCQs."],
  summarize: ["Text to summarize", "Paste your educational notes here."],
  learn: ["Topic for learning path", "Example: SQL"]
};

task.addEventListener("change", () => {
  const [newLabel, placeholder] = meta[task.value];
  label.textContent = newLabel;
  input.placeholder = placeholder;
  input.value = "";
  resultPanel.hidden = true;
  errorBox.hidden = true;
});

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[ch]));
}

async function runTask() {
  const value = input.value.trim();
  if (!value) {
    errorBox.textContent = "Please enter some content first.";
    errorBox.hidden = false;
    return;
  }

  errorBox.hidden = true;
  resultPanel.hidden = true;
  button.disabled = true;
  button.textContent = "Generating...";

  const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
  };

  const bodyKey = task.value === "qa" ? "question"
    : task.value === "learn" ? "topic"
    : "text";

  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [bodyKey]: value })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The server returned an error.");

    renderResult(task.value, data);
    resultPanel.hidden = false;
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.hidden = false;
  } finally {
    button.disabled = false;
    button.textContent = "Generate Answer";
  }
}

function renderResult(type, data) {
  resultTitle.textContent = {
    qa: "Answer",
    explain: "Explanation",
    quiz: "Quiz",
    summarize: "Summary",
    learn: "Learning Path"
  }[type];

  if (type !== "quiz") {
    result.textContent = data.answer || data.explanation || data.summary || data.learning_path || "";
    return;
  }

  result.innerHTML = "";
  const questions = data.questions || [];
  const scoreBox = document.createElement("div");
  scoreBox.className = "quiz-score";
  scoreBox.textContent = "Score: 0 / " + questions.length;
  result.appendChild(scoreBox);

  let score = 0;
  questions.forEach((q, index) => {
    const card = document.createElement("div");
    card.className = "quiz-card";
    card.innerHTML = `<h3>${index + 1}. ${escapeHtml(q.question)}</h3>`;

    q.options.forEach(option => {
      const labelEl = document.createElement("label");
      labelEl.className = "quiz-option";
      labelEl.innerHTML = `<input type="radio" name="q${index}" value="${escapeHtml(option)}"> ${escapeHtml(option)}`;
      labelEl.addEventListener("click", () => {
        if (card.dataset.answered) return;
        card.dataset.answered = "true";
        const feedback = document.createElement("div");
        feedback.className = "quiz-feedback";
        if (option === q.correct_answer) {
          score += 1;
          feedback.textContent = "Correct!";
        } else {
          feedback.textContent = "Not quite. Correct answer: " + q.correct_answer;
        }
        card.appendChild(feedback);
        scoreBox.textContent = `Score: ${score} / ${questions.length}`;
      });
      card.appendChild(labelEl);
    });
    result.appendChild(card);
  });
}

button.addEventListener("click", runTask);

copyBtn.addEventListener("click", async () => {
  await navigator.clipboard.writeText(result.innerText);
  copyBtn.textContent = "Copied";
  setTimeout(() => copyBtn.textContent = "Copy", 1200);
});
