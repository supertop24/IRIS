function sidebarOpen() {
    const content = document.getElementById('content');
    content.classList.remove('collapsed');
}

function sidebarCollapse() {
    const content = document.getElementById('content');
    content.classList.add('collapsed');
}
function section(id)
{
    const targets = document.querySelectorAll('.section');
    targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }});
}

window.addEventListener('sidebarOpen', sidebarOpen);
window.addEventListener('sidebarCollapse', sidebarCollapse);
window.addEventListener('profile', function() {
  section('profile');
});

window.addEventListener('pastoral', function() {
  section('pastoral');
});

window.addEventListener('academic', function() {
  section('academic');
});

window.addEventListener('awards', function() {
  section('awards');
});

window.addEventListener('extracurrilars', function() {
  section('extracurrilars');
});

window.addEventListener('timetable', function() {
  section('timetable');
});