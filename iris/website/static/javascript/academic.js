function academic_background(id)
{
    const targets = document.querySelectorAll('.academic');
    targets.forEach(target => {
    target.classList.remove('active');
    if (target.dataset.id === id) {
      target.classList.add('active');
    }});
    section('academic');
}
window.addEventListener('academic', function() {
    academic_background('list');
});