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