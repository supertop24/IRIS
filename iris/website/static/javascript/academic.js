// === Your existing academic_background function ===
function academic_background(id) {
  const targets = document.querySelectorAll('.academic');
  targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }
  });
  section('academic'); // Assuming this function exists
}

// Listen for custom 'academic' event
window.addEventListener('academic', () => {
  academic_background('list');
});

// On page load, set date and type input values
window.onload = function() {
  const today = new Date().toISOString().split('T')[0];
  const dateInput = document.getElementById("submit_form_date");
  if (dateInput) dateInput.value = today;

  const typeInput = document.getElementById("submit_form_type");
  if (typeInput) typeInput.value = "Report";

  // Initialize drag & drop event listeners
  initDragAndDrop();
};

let file_data= null;
// === Drag and Drop File Upload logic ===
function initDragAndDrop() {
  const dropArea = document.getElementById('drop-area');
  if (!dropArea) return; // Exit if no drop area

  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
      e.preventDefault();
      e.stopPropagation();
    }, false);
  });

  // Highlight drop area on dragenter and dragover
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.add('highlight');
    }, false);
  });

  // Remove highlight on dragleave and drop
  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => {
      dropArea.classList.remove('highlight');
    }, false);
  });

  // Handle dropped files
  dropArea.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    handleFiles(files);
  });

  // Optional: handle files selected with file input inside drop area
  const fileInput = dropArea.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.addEventListener('change', () => {
      handleFiles(fileInput.files);
    });
  }
}

// Process and display file list
function handleFiles(files) {
  const fileList = document.getElementById('file-list');
  if (!fileList) return;

  if (files.length === 0) {
    file_data = null;
    return;
  }

  // Only allow PDF files
  const file = files[0];
  if (file.type !== 'application/pdf') {
    alert('Only PDF files are allowed.');
    return;
  }

  file_data = file;

  fileList.innerHTML = ''; // Clear previous files
  [...files].forEach(file => {
    const item = document.createElement('div');
    item.textContent = file.name;
    fileList.appendChild(item);

    // Optional: uploadFile(file);
  });
}


// Optional: example upload function
/*
function uploadFile(file) {
  const url = 'YOUR_UPLOAD_ENDPOINT';
  const formData = new FormData();
  formData.append('file', file);

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(() => alert(`${file.name} uploaded successfully!`))
  .catch(() => alert(`Error uploading ${file.name}`));
}
*/
