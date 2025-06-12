function pastoral_background(id) {
  const targets = document.querySelectorAll('.pastoral');
  targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }
  });
  section('pastoral');
}

// Listen for custom 'academic' event
window.addEventListener('pastoral', () => {
  pastoral_background('reportList');
});








// Custom dropdown menu code 
document.addEventListener("DOMContentLoaded", () => {
    const selectedOption = document.getElementById("selectedOption");
    const dropdownOptionList = document.getElementById("dropdownOptionList");
    const selectedValue = document.getElementById("selectedValue");

    if (selectedOption && dropdownOptionList && selectedValue) {
        selectedOption.addEventListener("click", () => {
            dropdownOptionList.style.display = dropdownOptionList.style.display === "block" ? "none" : "block";
        });

        document.querySelectorAll(".dropdownOption").forEach(option => {
            option.addEventListener("click", () => {
                const imgSrc = option.getAttribute("data-img");
                const text = option.getAttribute("data-text");
                const value = option.getAttribute("data-value");

                selectedOption.innerHTML = `<img src="${imgSrc}" alt="${text}"><span>${text}</span>`;
                selectedValue.value = value;
                dropdownOptionList.style.display = "none";
            });
        });

        //Close dropdown if clicked outside of box
        document.addEventListener("click", (e) => {
            if (!e.target.closest(".dropdownContainer")) {
                dropdownOptionList.style.display = "none";
            }
        });
    }
});

//Individual report 
function showIndividualReport(element) {
    const reportData = {
        date: element.dataset.date,
        time: element.dataset.time,
        location: element.dataset.location,
        type: element.dataset.type,
        students: element.dataset.students,
        staff: element.dataset.staff,
        author: element.dataset.author,
        note: element.dataset.note,
    };

    //Filling in the report section
    document.querySelector('#reportDate').textContent = reportData.date;
    document.querySelector('#reportTime').textContent = reportData.time;
    document.querySelector('#reportLocation').textContent = reportData.location;
    document.querySelector('#reportType').textContent = reportData.type;
    document.querySelector('#reportStudents').textContent = reportData.students;
    document.querySelector('#reportStaff').textContent = reportData.staff;
    document.querySelector('#reportAuthor').textContent = reportData.author;
    document.querySelector('#reportNote').textContent = reportData.note;

    //Note fields - will seperate after testing
    document.querySelectorAll('.reportNote').forEach(el => el.textContent = reportData.note);

    //Displaying the individual report section
    pastoral_background('individualReport');
}