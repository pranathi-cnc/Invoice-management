// =============================
// Authentication
// =============================

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

// =============================
// Elements
// =============================

const fileInput = document.getElementById("file-input");
const fileNameDisplay = document.getElementById("file-name");
const submitBtn = document.getElementById("submit-btn");
const uploadStatus = document.getElementById("upload-status");
const progressContainer = document.getElementById("progress-container");
const progressBar = document.getElementById("progress-bar");
const fileGallery = document.getElementById("file-gallery");
const searchInput = document.getElementById("search-input");

const backend = "http://127.0.0.1:8000";

let allFiles = [];

// =============================
// Load Files
// =============================

window.addEventListener("DOMContentLoaded", () => {

    fetchGalleryFiles();

});

// =============================
// Search
// =============================

searchInput.addEventListener("input", (event) => {

    const searchText = event.target.value.toLowerCase().trim();

    const filtered = allFiles.filter(file =>
        file.filename.toLowerCase().includes(searchText)
    );

    renderFiles(filtered);

});

// =============================
// File Selection
// =============================

fileInput.addEventListener("change", () => {

    if (fileInput.files.length === 0) {

        fileNameDisplay.textContent = "No file selected";

        submitBtn.disabled = true;

        return;

    }

    fileNameDisplay.textContent =
        fileInput.files[0].name;

    submitBtn.disabled = false;

});

// =============================
// Upload Invoice
// =============================

submitBtn.addEventListener("click", () => {

    const file = fileInput.files[0];

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    submitBtn.disabled = true;

    progressContainer.style.display = "block";

    progressBar.style.width = "0%";

    progressBar.textContent = "0%";

    uploadStatus.style.display = "block";

    uploadStatus.style.color = "#2563eb";

    uploadStatus.innerHTML =
        "⬆ Uploading file...";

    const xhr = new XMLHttpRequest();

    xhr.open(
        "POST",
        `${backend}/upload`,
        true
    );

    // ---------------- Upload Progress ----------------

    xhr.upload.onprogress = (event) => {

        if (!event.lengthComputable)
            return;

        const percent = Math.round(
            (event.loaded / event.total) * 100
        );

        progressBar.style.width = percent + "%";

        progressBar.textContent =
            percent + "%";

    };

    // ---------------- Upload Completed ----------------

    xhr.upload.onload = () => {

        uploadStatus.style.color = "#f59e0b";

        uploadStatus.innerHTML = `
            ⏳ Upload completed.<br>
            Processing invoice...<br>
            <small>
            OCR is extracting text and AI is understanding the invoice.
            </small>
        `;

    };

    // ---------------- Server Response ----------------

    xhr.onload = () => {

        progressContainer.style.display = "none";

        const response = JSON.parse(xhr.responseText);

        if (xhr.status === 200) {

            uploadStatus.style.color = "#16a34a";

            uploadStatus.innerHTML = `
                ✅ Invoice processed successfully.<br>
                <small>
                Invoice details have been extracted and stored successfully.
                </small>
            `;

            fileInput.value = "";

            fileNameDisplay.textContent =
                "No file selected";

            submitBtn.disabled = true;

            fetchGalleryFiles();

        }

        else {

            uploadStatus.style.color = "#dc2626";

            uploadStatus.innerHTML =
                "❌ " + response.detail;

            submitBtn.disabled = false;

        }

    };

    // ---------------- Network Error ----------------

    xhr.onerror = () => {

        progressContainer.style.display = "none";

        uploadStatus.style.color = "#dc2626";

        uploadStatus.innerHTML =
            "❌ Unable to connect to the server.";

        submitBtn.disabled = false;

    };

    xhr.send(formData);

});

// =============================
// Fetch Files From Backend
// =============================

async function fetchGalleryFiles() {

    try {

        const response = await fetch(`${backend}/files`);

        if (!response.ok)
            throw new Error("Unable to fetch files.");

        allFiles = await response.json();

        renderFiles(allFiles);

    }

    catch (error) {

        console.error(error);

        fileGallery.innerHTML = `
            <div class="empty-state">
                Unable to connect to backend.
            </div>
        `;

    }

}

// =============================
// Format File Size
// =============================

function formatFileSize(bytes) {

    if (bytes < 1024)
        return bytes + " Bytes";

    if (bytes < 1024 * 1024)
        return (bytes / 1024).toFixed(2) + " KB";

    if (bytes < 1024 * 1024 * 1024)
        return (bytes / (1024 * 1024)).toFixed(2) + " MB";

    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + " GB";

}

// =============================
// Format Upload Date
// =============================

function formatDate(dateString) {

    const date = new Date(dateString);
    date.setMinutes(date.getMinutes() + 330);
    return date.toLocaleString("en-IN", {

        day: "2-digit",

        month: "short",

        year: "numeric",

        hour: "2-digit",

        minute: "2-digit"

    });

}
// =============================
// Render Repository Files
// =============================

function renderFiles(filesArray) {

    fileGallery.innerHTML = "";

    if (filesArray.length === 0) {

        fileGallery.innerHTML = `
            <div class="empty-state">
                No uploaded files found.
            </div>
        `;

        return;

    }

    filesArray.forEach(file => {

        let icon = "📄";

        if (file.file_type.toLowerCase() === "pdf")
            icon = "📕";

        else if (
            file.file_type.toLowerCase() === "png" ||
            file.file_type.toLowerCase() === "jpg" ||
            file.file_type.toLowerCase() === "jpeg"
        )
            icon = "🖼️";

        else if (
            file.file_type.toLowerCase() === "doc" ||
            file.file_type.toLowerCase() === "docx"
        )
            icon = "📘";

        const row = document.createElement("div");

        row.className = "repo-file-card";

        row.innerHTML = `

            <div class="file-meta-block">

                <div class="extension-icon-box">

                    ${icon}

                </div>

                <div class="file-details">

                    <div class="file-title-text">

                        ${file.filename}

                    </div>

                    <div class="file-info">

                        ${file.file_type}

                        •

                        ${formatFileSize(file.file_size)}

                    </div>

                    <div class="upload-time">

                        Uploaded :
                        ${formatDate(file.uploaded_at)}

                    </div>

                </div>

            </div>

            <a
    href="${file.url}"
    target="_blank"
    class="download-action-anchor"
    title="Download File"
>
    <svg xmlns="http://www.w3.org/2000/svg"
         fill="none"
         viewBox="0 0 24 24"
         stroke-width="2"
         stroke="currentColor">

        <path stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 3v12m0 0l4-4m-4 4l-4-4M5 21h14"/>

    </svg>
</a>

        `;

        fileGallery.appendChild(row);

    });

}