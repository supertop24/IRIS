function formatDateToISO(dateObj) {
    return dateObj.toISOString().split('T')[0];
}

function loadSchedule(date = null) {
  const queryDate = date || formatDateToISO(new Date());

  fetch(`/api/daily-schedule?date=${queryDate}`)
    .then(response => response.json())
    .then(data => {
      renderCalendar(data); 
    })
    .catch(error => {
      console.error("Error loading schedule:", error);
    });
}

// function loadSchedule(date = null) { // alternative function to display "tomorrow" timetable instead of todays - for easy weekend testing of timetable 
//   const tomorrow = new Date();
//   tomorrow.setDate(tomorrow.getDate() + 1);
  
//   const queryDate = date || formatDateToISO(tomorrow);

//   fetch(`/api/daily-schedule?date=${queryDate}`)
//     .then(response => response.json())
//     .then(data => {
//       renderCalendar(data); 
//     })
//     .catch(error => {
//       console.error("Error loading schedule:", error);
//     });
// }



document.addEventListener('DOMContentLoaded', function () {
  loadSchedule(); 
//  setupDatePicker(); // Add later to let user select date for calendar view
});

function renderCalendar(scheduleData) {
    // Clearing all existing class information before rendering, preventing overloading 
    const classInfoItems = document.querySelectorAll('.class-info');
    classInfoItems.forEach(item => {
        item.textContent = '';
    });

    // Mapping period codes to period identifiers
    const periodMapping = {
        'P1': '1',
        'P2': '2', 
        'P3': '3',
        'P4': '4',
        'P5': '5',
        'TUT': 'tut',
        'SOD': 'sod',
        'EOD': 'eod',
        'INT': 'int', 
        'LUN': 'lun'
    };

    scheduleData.forEach(session => {
        console.log('Processing session:', session); //
        
        let periodCode = session.period_label || `P${session.period_id}`;
        let targetPeriod = periodMapping[periodCode.toUpperCase()] || periodCode.toLowerCase();
        
        const targetElement = document.querySelector(`.class-info[data-period="${targetPeriod}"]`);
        
        if (targetElement) { // I've added console logging to check if sessions are being found
            targetElement.textContent = session.class_code || session.subject || 'Class';
            console.log(`Placed ${session.class_code} in period ${targetPeriod}`);
        } else {
            console.warn(`Could not find element for period: ${targetPeriod}`);
        }
    });
}

// Later: add week-toggle method




