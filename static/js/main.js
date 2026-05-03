
// ── EMOTION EMOJI MAP ──
const emojiMap = {
    happy: "😊", sad: "😢", angry: "😠", fear: "😨",
    disgust: "🤢", surprise: "😲", neutral: "😐", calm: "😌"
};

// ── AUTH ──
const authModal = document.getElementById("authModal");
const authTitle = document.getElementById("authTitle");
const authEmail = document.getElementById("authEmail");
const authPassword = document.getElementById("authPassword");
const authName = document.getElementById("authName");
const authSubmitBtn = document.getElementById("authSubmitBtn");
const authToggle = document.getElementById("authToggle").querySelector("span");
const authError = document.getElementById("authError");
const logoutBtn = document.getElementById("logoutBtn");

let isLogin = true;

window.onload = () => {
    const token = localStorage.getItem("token");
    if (token) {
        authModal.style.display = "none";
        logoutBtn.style.display = "inline-block";
        loadHistory();
    } else {
        authModal.style.display = "flex";
        logoutBtn.style.display = "none";
    }
};

authToggle.addEventListener("click", () => {
    isLogin = !isLogin;
    authTitle.textContent = isLogin ? "Welcome back" : "Create account";
    authSubmitBtn.textContent = isLogin ? "Login" : "Register";
    authName.style.display = isLogin ? "none" : "block";
    authToggle.textContent = isLogin ? "Register" : "Login";
    authError.textContent = "";
});

authSubmitBtn.addEventListener("click", async () => {
    const email = authEmail.value.trim();
    const password = authPassword.value.trim();
    const name = authName.value.trim();
    authError.textContent = "";

    if (!email || !password) { authError.textContent = "Email and password are required"; return; }
    if (!isLogin && !name) { authError.textContent = "Name is required"; return; }

    const body = isLogin ? { email, password } : { name, email, password };
    const url = isLogin ? "/auth/login" : "/auth/register";

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem("token", data.token);
            authModal.style.display = "none";
            logoutBtn.style.display = "inline-block";
        } else {
            authError.textContent = data.error;
        }
    } catch {
        authError.textContent = "Could not connect to server.";
    }
});

logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    authModal.style.display = "flex";
    logoutBtn.style.display = "none";
    document.getElementById("resultCard").classList.remove("visible");
    statusBar.textContent = "Ready — choose to record or upload an audio file";
    audioBlob = null;
    submitBtn.disabled = true;
    recordBtn.textContent = "⏺ Start Recording";
    recordBtn.classList.remove("recording");
    waveform.classList.remove("active");
});

// ── RECORDING ──
let mediaRecorder, audioChunks = [], audioBlob;
const recordBtn = document.getElementById("recordBtn");
const submitBtn = document.getElementById("submitBtn");
const statusBar = document.getElementById("statusBar");
const waveform = document.getElementById("waveform");

recordBtn.addEventListener("click", async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.start();
        recordBtn.textContent = "⏹ Stop Recording";
        recordBtn.classList.add("recording");
        waveform.classList.add("active");
        statusBar.textContent = "Recording... speak naturally";
        submitBtn.disabled = true;
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            submitBtn.disabled = false;
            waveform.classList.remove("active");
            statusBar.textContent = "Recording complete — click Analyze";
        };
    } else {
        mediaRecorder.stop();
        recordBtn.textContent = "⏺ Start Recording";
        recordBtn.classList.remove("recording");
    }
});

submitBtn.addEventListener("click", () => analyzeAudio(audioBlob, "recording.webm"));

// ── UPLOAD ──
const uploadZone = document.getElementById("uploadZone");
const fileInput = document.getElementById("fileInput");
const uploadFilename = document.getElementById("uploadFilename");
const uploadAnalyzeBtn = document.getElementById("uploadAnalyzeBtn");
let uploadedFile = null;

uploadZone.addEventListener("click", () => fileInput.click());

uploadZone.addEventListener("dragover", e => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
});

uploadZone.addEventListener("dragleave", () => uploadZone.classList.remove("dragover"));

uploadZone.addEventListener("drop", e => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) setUploadFile(file);
});

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) setUploadFile(fileInput.files[0]);
});

function setUploadFile(file) {
    uploadedFile = file;
    uploadFilename.textContent = "📎 " + file.name;
    uploadAnalyzeBtn.disabled = false;
    statusBar.textContent = `File ready: ${file.name}`;
}

uploadAnalyzeBtn.addEventListener("click", () => {
    if (uploadedFile) analyzeAudio(uploadedFile, uploadedFile.name);
});

// ── SHARED ANALYZE FUNCTION ──
async function analyzeAudio(blob, filename) {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", blob, filename);

    statusBar.textContent = "Analyzing your emotion...";
    document.getElementById("resultCard").classList.remove("visible");

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Authorization": "Bearer " + token },
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            const emotion = data.emotion.toLowerCase();
            document.getElementById("emotionEmoji").textContent = emojiMap[emotion] || "🎯";
            document.getElementById("emotionText").textContent = data.emotion.toUpperCase();
            document.getElementById("feedbackText").textContent = data.feedback;
            document.getElementById("resultCard").classList.add("visible");
            statusBar.textContent = "Analysis complete ✓";
            loadHistory();
        } else {
            statusBar.textContent = "Error: " + data.error;
        }
    } catch {
        statusBar.textContent = "Could not connect to server.";
    }
}
async function loadHistory() {
    const token = localStorage.getItem("token");
    if (!token) return;

    const res = await fetch("/history", {
        headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();

    const tbody = document.getElementById("historyTableBody");
    if (!tbody) return;

    tbody.innerHTML = "";
    data.history.reverse().forEach(record => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${new Date(record.timestamp).toLocaleDateString()}</td>
            <td>${new Date(record.timestamp).toLocaleTimeString()}</td>
            <td>${record.emotion.toUpperCase()}</td>
            <td>${record.feedback.slice(0, 60)}...</td>
        `;
        tbody.appendChild(tr);
    });
}