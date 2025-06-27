//pastoral background function
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

//Listens for custom pastoral event
window.addEventListener('pastoral', function() {
    pastoral_background('list');
});

//Document ready functions
document.addEventListener("DOMContentLoaded", () => {
    //Handling custom dropdown for add form
    handleCustomDropdown();
    
    //Handling add buttons
    handleAddButtons();
    
    //Handling filter and sort functionality
    handleFiltersAndSorts();
    
    //Handling form submission
    handleFormSubmission();
});

//Custom dropdown functionality for both merit and incident forms
function handleCustomDropdown() {
    //Handling merit dropdown
    const meritSelectedOption = document.getElementById("meritSelectedOption");
    const meritDropdownList = document.getElementById("meritDropdownOptionList");
    const meritSelectedValue = document.getElementById("meritSelectedValue");

    if (meritSelectedOption && meritDropdownList && meritSelectedValue) {
        meritSelectedOption.addEventListener("click", () => {
            meritDropdownList.style.display = meritDropdownList.style.display === "block" ? "none" : "block";
        });

        meritDropdownList.querySelectorAll(".dropdown-option").forEach(option => {
            option.addEventListener("click", () => {
                const imgSrc = option.getAttribute("data-img");
                const text = option.getAttribute("data-text");
                const value = option.getAttribute("data-value");
                
                if (imgSrc) {
                    meritSelectedOption.innerHTML = `<img src="${imgSrc}" alt="${text}" style="width: 16px; height: 16px; margin-right: 8px;"><span>${text}</span>`;
                } else {
                    meritSelectedOption.innerHTML = `<span>${text}</span>`;
                }

                meritSelectedValue.value = value || text; //Using value if available otherwise using text
                meritDropdownList.style.display = "none";
            });
        });
    }

    //Handling incident dropdown
    const incidentSelectedOption = document.getElementById("incidentSelectedOption");
    const incidentDropdownList = document.getElementById("incidentDropdownOptionList");
    const incidentSelectedValue = document.getElementById("incidentSelectedValue");

    if (incidentSelectedOption && incidentDropdownList && incidentSelectedValue) {
        incidentSelectedOption.addEventListener("click", () => {
            incidentDropdownList.style.display = incidentDropdownList.style.display === "block" ? "none" : "block";
        });

        incidentDropdownList.querySelectorAll(".dropdown-option").forEach(option => {
            option.addEventListener("click", () => {
                const imgSrc = option.getAttribute("data-img");
                const text = option.getAttribute("data-text");
                const value = option.getAttribute("data-value");

                if (imgSrc) {
                    incidentSelectedOption.innerHTML = `<img src="${imgSrc}" alt="${text}" style="width: 16px; height: 16px; margin-right: 8px;"><span>${text}</span>`;
                } else {
                    incidentSelectedOption.innerHTML = `<span>${text}</span>`;
                }
                
                incidentSelectedValue.value = value || text; //Using value if available otherwise using text
                incidentDropdownList.style.display = "none";
            });
        });
    }

    //Closing dropdowns when clicking outside
    document.addEventListener("click", (e) => {
        if (meritSelectedOption && meritDropdownList && 
            !meritSelectedOption.contains(e.target) && !meritDropdownList.contains(e.target)) {
            meritDropdownList.style.display = "none";
        }
        if (incidentSelectedOption && incidentDropdownList && 
            !incidentSelectedOption.contains(e.target) && !incidentDropdownList.contains(e.target)) {
            incidentDropdownList.style.display = "none";
        }
    });
}

//Handling add buttons
function handleAddButtons() {
    const addMeritButton = document.getElementById("addMeritButtn");
    const addIncidentButton = document.getElementById("addIncidentButtn");

    if (addMeritButton) {
        addMeritButton.addEventListener("click", () => {
            pastoral_background('addMerit');
        });
    }

    if (addIncidentButton) {
        addIncidentButton.addEventListener("click", () => {
            pastoral_background('addIncident');
        });
    }
}

//Showing individual report function
function showIndividualReport(element) {
    //Getting data from the clicked element
    const reportData = {
        id: element.dataset.id,
        author: element.dataset.author,
        date: element.dataset.date,
        time: element.dataset.time,
        location: element.dataset.location,
        type: element.dataset.type,
        students: element.dataset.students,
        staff: element.dataset.staff,
        note: element.dataset.note,
        title: element.dataset.title,
        parentCommunication: element.dataset.parentCommunication,
        disciplinaryActions: element.dataset.disciplinaryActions,
        resolutionStatus: element.dataset.resolutionStatus
    };

    //Determining if it's a merit or incident report and populating
    if (element.classList.contains('meritReportBox')) {
        populateViewMeritReport(reportData);
        pastoral_background('viewMerit');
    } else if (element.classList.contains('incidentReportBox')) {
        populateViewIncidentReport(reportData);
        pastoral_background('viewIncident');
    }
}

//Populating view merit report section with data
function populateViewMeritReport(data) {
    document.getElementById("reportDate").textContent = data.date || 'N/A';
    document.getElementById("reportTime").textContent = data.time || 'N/A';
    document.getElementById("reportLocation").textContent = data.location || 'N/A';
    
    //Includes the image with the title
    const reportTitleElement = document.getElementById("reportTitleType");
    reportTitleElement.innerHTML = getTypeImageWithText(data.title || 'N/A');

    document.getElementById("reportStudents").textContent = data.students || 'N/A';
    document.getElementById("reportStaff").textContent = data.staff || 'N/A';
    document.getElementById("reportAuthor").textContent = data.author || 'N/A';
    document.getElementById("reportNote").textContent = data.note || 'N/A';
}

//Populating view incident report section with data
function populateViewIncidentReport(data) {
    document.getElementById("incidentReportDate").textContent = data.date || 'N/A';
    document.getElementById("incidentReportTime").textContent = data.time || 'N/A';
    document.getElementById("incidentReportLocation").textContent = data.location || 'N/A';
    
    //Includes the image with the title
    const incidentReportTitleElement = document.getElementById("incidentReportTitleType");
    incidentReportTitleElement.innerHTML = getTypeImageWithText(data.title || 'N/A');

    document.getElementById("incidentReportStudents").textContent = data.students || 'N/A';
    document.getElementById("incidentReportStaff").textContent = data.staff || 'N/A';
    document.getElementById("incidentReportAuthor").textContent = data.author || 'N/A';
    document.getElementById("incidentReportNote").textContent = data.note || 'N/A';
    document.getElementById("incidentReportParentCommunication").textContent = data.parentCommunication || 'N/A';
    document.getElementById("incidentReportDisciplinaryActions").textContent = data.disciplinaryActions || 'N/A';
    document.getElementById("incidentReportResolutionStatus").textContent = data.resolutionStatus || 'N/A';
}

//Function to get the image with text for report types
function getTypeImageWithText(titleType) {
    if (!titleType || titleType === 'N/A') {
        return 'N/A';
    }
    
    const lowerTitleType = titleType.toLowerCase();
    
    if (lowerTitleType === 'teamwork') {
        return '<img src="/static/images/icons/teamwork.png" alt="Teamwork" class="reportTypeIcon" style="width: 16px; height: 16px; margin-right: 8px; vertical-align: middle;"> Teamwork';
    } else if (lowerTitleType === 'respect') {
        return '<img src="/static/images/icons/respect.jpg" alt="Respect" class="reportTypeIcon" style="width: 16px; height: 16px; margin-right: 8px; vertical-align: middle;"> Respect';
    } else if (lowerTitleType === 'behavioural') {
        return '<img src="/static/images/icons/behavioural.png" alt="Behavioural" class="reportTypeIcon" style="width: 16px; height: 16px; margin-right: 8px; vertical-align: middle;"> Behavioural';
    } else if (lowerTitleType === 'property') {
        return '<img src="/static/images/icons/property.png" alt="Property" class="reportTypeIcon" style="width: 16px; height: 16px; margin-right: 8px; vertical-align: middle;"> Property';
    }
    
    //Default for unknown types
    return titleType;
}

//Handling form submission
function handleFormSubmission() {
    const forms = document.querySelectorAll('#reportForm');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            //Validating form inputs
            const date = this.querySelector('[name="date"]').value.trim();
            const time = this.querySelector('[name="time"]').value.trim();
            const location = this.querySelector('[name="location"]').value.trim();
            const studentsInvolved = this.querySelector('[name="studentsInvolved"]').value.trim();
            const staffInvolved = this.querySelector('[name="staffInvolved"]').value.trim();
            const author = this.querySelector('[name="author"]').value.trim();
            const description = this.querySelector('[name="description"]').value.trim();
            
            //Checking if any required field is empty
            if (!date) {
                alert('Please enter a date.');
                this.querySelector('[name="date"]').focus();
                return;
            }
            if (!time) {
                alert('Please enter a time.');
                this.querySelector('[name="time"]').focus();
                return;
            }
            if (!location) {
                alert('Please enter a location.');
                this.querySelector('[name="location"]').focus();
                return;
            }
            if (!studentsInvolved) {
                alert('Please enter students involved.');
                this.querySelector('[name="studentsInvolved"]').focus();
                return;
            }
            if (!staffInvolved) {
                alert('Please enter staff involved.');
                this.querySelector('[name="staffInvolved"]').focus();
                return;
            }
            if (!author) {
                alert('Please enter the author of the report.');
                this.querySelector('[name="author"]').focus();
                return;
            }
            if (!description) {
                alert('Please enter a description.');
                this.querySelector('[name="description"]').focus();
                return;
            }

            //Getting the student ID
            const studentId = getStudentId();
            
            //Creating FormData object
            const formData = new FormData(this);
            formData.append('student_id', studentId);
            
            let reportType = 'Merit'; //default
            
            //Checking if form is inside addIncident container
            const parentSection = this.closest('.pastoral');
            if (parentSection && parentSection.classList.contains('addIncident')) {
                reportType = 'Incident';
            }
            
            //Looking for incident form elements
            const incidentElements = this.querySelector('#incidentSelectedValue');
            if (incidentElements) {
                reportType = 'Incident';
            }
            
            formData.append('report_type', reportType);
            
            //Submitting the form
            fetch('/add_pastoral_report', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    //Showing success message
                    alert('Report submitted successfully!');
                    // Redirect back to the student profile page
                    window.location.href = `/studentProfile/${studentId}`;
                } else {
                    throw new Error('Failed to submit report');
                }
            })
            .catch(error => {
                console.error('Error submitting report:', error);
                alert('Error submitting report. Please try again.');
            });
        });
    });
}

//Handling filters and sorts
function handleFiltersAndSorts() {
    //Merit reports filters
    const meritFilter = document.getElementById("meritFilter");
    const meritSort = document.getElementById("meritSort");
    
    //Incident reports filters
    const incidentFilter = document.getElementById("incidentFilter");
    const incidentSort = document.getElementById("incidentSort");

    if (meritFilter) {
        meritFilter.addEventListener("change", () => {
            filterReports('Merit', meritFilter.value, meritSort ? meritSort.value : 'latest');
        });
    }

    if (meritSort) {
        meritSort.addEventListener("change", () => {
            filterReports('Merit', meritFilter ? meritFilter.value : '', meritSort.value);
        });
    }

    if (incidentFilter) {
        incidentFilter.addEventListener("change", () => {
            filterReports('Incident', incidentFilter.value, incidentSort ? incidentSort.value : 'latest');
        });
    }

    if (incidentSort) {
        incidentSort.addEventListener("change", () => {
            filterReports('Incident', incidentFilter ? incidentFilter.value : '', incidentSort.value);
        });
    }
}

//Filter reports function
function filterReports(reportType, titleFilter, sortBy) {
    const studentId = getStudentId();
    
    //Building query parameters
    const params = new URLSearchParams({
        filterType: reportType,
        titleFilter: titleFilter,
        sortBy: sortBy
    });

    //Making AJAX request to filter endpoint
    fetch(`/filter_reports/${studentId}?${params}`)
        .then(response => response.json())
        .then(data => {
            updateReportsList(data, reportType);
        })
        .catch(error => {
            console.error('Error filtering reports:', error);
        });
}

//Updating reports list with filtered data
function updateReportsList(reports, reportType) {
    const containerId = reportType === 'Merit' ? 'meritContentContainer' : 'incidentContentContainer';
    const container = document.querySelector(`.${containerId}`);
    
    if (!container) return;

    //Finding the existing reports container
    const existingReports = container.querySelectorAll('.meritReportBox, .incidentReportBox');
    existingReports.forEach(report => report.remove());

    //Adding filtered reports after the header
    const headerContainer = container.querySelector('.headerContainer');
    
    reports.forEach(report => {
        const reportItem = createReportItem(report, reportType);
        headerContainer.insertAdjacentElement('afterend', reportItem);
    });
}

//Creating report item element
function createReportItem(report, reportType) {
    const div = document.createElement('div');
    div.className = reportType === 'Merit' ? 'meritReportBox' : 'incidentReportBox';
    div.onclick = () => showIndividualReport(div);
    
    //Setting data attributes
    div.dataset.id = report.id;
    div.dataset.author = report.author;
    div.dataset.date = report.date;
    div.dataset.time = report.time;
    div.dataset.location = report.location;
    div.dataset.type = report.reportType;
    div.dataset.students = report.studentsInvolved;
    div.dataset.staff = report.staffInvolved;
    div.dataset.note = report.note;
    div.dataset.title = report.titleType;
    div.dataset.parentCommunication = report.parentCommunication || '';
    div.dataset.disciplinaryActions = report.disciplinaryActions || '';
    div.dataset.resolutionStatus = report.resolutionStatus || '';

    //Function getting the image for report based on report title
    function getTypeImage(titleType) {
        const lowerTitleType = titleType.toLowerCase();

        if (lowerTitleType === 'teamwork') {
            return '<img src="/static/images/icons/teamwork.png" alt="Teamwork" class="reportTypeIcon">';
        } else if (lowerTitleType === 'respect') {
            return '<img src="/static/images/icons/respect.jpg" alt="Respect" class="reportTypeIcon">';
        } else if (lowerTitleType === 'behavioural') {
            return '<img src="/static/images/icons/behavioural.png" alt="Behavioural" class="reportTypeIcon">'; // ← ADDED class="reportTypeIcon" here
        } else if (lowerTitleType === 'property') {
            return '<img src="/static/images/icons/property.png" alt="Property" class="reportTypeIcon">';
        }
        return '';
    }

    //Setting content
    div.innerHTML = `
        <p class="titleWithImage">
            ${getTypeImage(report.titleType)}
            ${report.titleType}
        </p>
        <p>${report.author}</p>
        <p>${report.date}</p>
    `;

    return div;
}

//Getting student ID from URL
function getStudentId() {
    const pathParts = window.location.pathname.split('/');
    
    //Looking for studentProfile in the path
    const studentProfileIndex = pathParts.indexOf('studentProfile');
    if (studentProfileIndex !== -1 && pathParts[studentProfileIndex + 1]) {
        return pathParts[studentProfileIndex + 1];
    }
    
    const pastoralIndex = pathParts.indexOf('pastoral');
    if (pastoralIndex !== -1 && pathParts[pastoralIndex + 1]) {
        return pathParts[pastoralIndex + 1];
    }
    
    return null;
}

//Navigating functions back to list view
function goBackToList() {
    pastoral_background('list');
}