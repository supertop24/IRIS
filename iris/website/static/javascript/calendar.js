function formatDateToISO(dateObj) {
    return dateObj.toISOString().split('T')[0];
}

function loadSchedule(date = null) {
  const queryDate = date || formatDateToISO(new Date());

  fetch(`/api/daily-schedule?date=${queryDate}`)
    .then(response => response.json())
    .then(data => {
      renderCalendar(data); // You’ll implement this function to display the sessions
    })
    .catch(error => {
      console.error("Error loading schedule:", error);
    });
}

// Maybe later add scheduleDatePicker method, or week-toggle method

document.addEventListener('DOMContentLoaded', function () {
  loadSchedule(); // This is loading today’s schedule
//  setupDatePicker(); // Maybe add later
});

function renderCalendar(data) {
    const gridItems = document.querySelectorAll('.calendarContentGrid .girdItem')
    gridItems.forEach(item => item.textContent = '');

    data.forEach((session, index) => {
        const colGroup = Math.floor(index / 5); 
        const row = index % 5;

        const baseIndex = row * 6 + colGroup * 3;

        gridItems[baseIndex].textContent = session.time || '';
        gridItems[baseIndex + 1].textContent = session.preiod || '';
        gridItems[baseIndex + 2].textContent = session.class_code || '';
    });
}

