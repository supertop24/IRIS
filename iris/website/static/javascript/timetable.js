window.onload = function() {
    const view = document.querySelectorAll('.viewed');
    const modify = document.querySelectorAll('.modified');
    view.forEach(target => {
        target.classList.add('active');
    });
    modify.forEach(target => {
        target.classList.remove('active');
    });
    viewed();
}
function viewed()
{
    for (let start = 11; start <= 51; start += 10) {
        for (let i = start; i < start + 5; i++) {
            document.getElementById('v'+i).textContent=document.getElementById(i).value;
            document.getElementById('m'+i).value=document.getElementById(i).value;
        }
    }
}
function modified()
{
    let button = document.getElementById('modify');
    button.classList.toggle('active');
    if(button.classList.contains('active'))
    {
        const view = document.querySelectorAll('.viewed');
        const modify = document.querySelectorAll('.modified');
        view.forEach(target => {
            target.classList.remove('active');
        });
        modify.forEach(target => {
            target.classList.add('active');
        });
    }
    else
    {
        for (let start = 11; start <= 51; start += 10) {
        for (let i = start; i < start + 5; i++) {
            document.getElementById(i).value=document.getElementById('m'+i).value;
            document.getElementById('v'+i).textContent=document.getElementById('m'+i).value;
        }}
        const view = document.querySelectorAll('.viewed');
        const modify = document.querySelectorAll('.modified');
        view.forEach(target => {
            target.classList.add('active');
        });
        modify.forEach(target => {
            target.classList.remove('active');
        });
    }
}
