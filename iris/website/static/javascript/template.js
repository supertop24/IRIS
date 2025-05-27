function sidebarOpen() {
    const content = document.getElementById('content');
    content.classList.remove('collapsed');
}

function sidebarCollapse() {
    const content = document.getElementById('content');
    content.classList.add('collapsed');
}

window.addEventListener('sidebarOpen', sidebarOpen);
window.addEventListener('sidebarCollapse', sidebarCollapse);