//Awards background function
function awards_background(id) {
  const targets = document.querySelectorAll('.awards');
  targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }
  });
  section('awards');
}

window.addEventListener('awards', () => {
  awards_background('list');
});

//Upload function for awards - called when user clicks
function upload() {
  console.log('Upload function called');
  //Getting input fields - Check if elements exist first
  const termElement = document.getElementById('termMenu');
  const typeElement = document.querySelector('.awards.add .inputAwardType');
  const titleElement = document.querySelector('.awards.add .inputAwardTitle');
  const gradeElement = document.getElementById('gradeMenu');
  const subjectElement = document.querySelector('.awards.add .inputAwardSubject');
  
  // Debug: Check which elements are found
  console.log('Elements found:', {
    term: termElement,
    type: typeElement,
    title: titleElement,
    grade: gradeElement,
    subject: subjectElement
  });
  
  if (!termElement || !typeElement || !titleElement || !gradeElement || !subjectElement) {
    alert('Error: Could not find all form elements. Check the console for details.');
    return;
  }
  
  const term = termElement.value;
  const type = typeElement.value;
  const title = titleElement.value;
  const grade = gradeElement.value;
  const subject = subjectElement.value;

  // Debug: Check what values we're getting
  console.log('Form values:', {
    term: term,
    type: type,
    title: title,
    grade: grade,
    subject: subject
  });

  //Getting the year that the award was uploaded - for filtering the display
  const currentYear = new Date().getFullYear();

  //Validation to ensure user fills in all sections
  if (term === 'empty' || grade === 'empty') {
    alert('Please select both the Term and Year Level');
    return;
  }

  if (!type.trim() || !title.trim()) {
    alert('Please fill in Award Type and Award Title');
    return;
  }

  //Creating the data object to send to the sever
  const awardData = {
    term: term,
    type: type.trim(),
    title: title.trim(), //'Note' in the datbase for consistency
    grade: grade,
    subject: subject.trim(),
    year: currentYear,
    student_id: getCurrentStudentID()
  };

  //Sending the data to the sever
  fetch('/uploadAward', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(awardData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('Award uploaded successfully!');
      clearForm();
      awards_background('list'); //Switching back to the list section
      //Refreshing the page to show the new report
      window.location.reload();
    } else {
      alert('Error uploading the award: ' + (data.message || 'Unkown error'));
    }
  })
  //Error handling
  .catch(error => {
    console.error('Error:', error);
    alert('Error uploading award. Please try again.');
  });
}

//Function that clears the form after a successful upload
function clearForm() {
    document.getElementById('termMenu').value = 'empty';
    document.querySelector('.inputAwardType').value = '';
    document.querySelector('.inputAwardTitle').value = '';
    document.getElementById('gradeMenu').value = 'empty';
    document.querySelector('.inputAwardSubject').value = '';
}

//Getting the student_id and saving it to the form
function getCurrentStudentID() {
//Getting student_id via URL
const path = window.location.pathname;
const match = path.match(/\/studentProfile\/(\d+)/);
if (match) {
  console.log('Found student ID: ', parseInt(match[1])); //Debug log
  return parseInt(match[1]);
}

//Error handling - if for some reason the url cannot be passed
console.error('Could not extract student ID from URL: ', path);
alert('Error: Could not determine which student to add award to');
return null;
}