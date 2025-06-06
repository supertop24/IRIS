function sidebarOpen() {
    const banner = document.getElementById('banner');
    banner.style.width = 'calc(100% - 16%)';
    banner.style.marginLeft = '16%';
}

function sidebarCollapse() {
    const banner = document.getElementById('banner');
    banner.style.width = 'calc(100% - 4%)';
    banner.style.marginLeft = '4%';
}

window.addEventListener('sidebarOpen', sidebarOpen);
window.addEventListener('sidebarCollapse', sidebarCollapse);

function selected(id) {
  const buttons = document.querySelectorAll('button');
  buttons.forEach(button => {
    button.classList.remove('active');
    if (button.dataset.id === id) {
      button.classList.add('active');
    }
  });
  window.dispatchEvent(new CustomEvent(id));
}
function userByID(id)
{
  const element = document.getElementById("name");
  if (id==0)
  {
    return element.innerText = "No student is selected";
  }
  fetch(`/searchID?id=${encodeURIComponent(id)}`)
    .then(res => res.json())
    .then(user => {
      if (element) {
        element.innerText = user.name;
      }
    });
}
window.addEventListener('load', function() {
  userByID(parseInt(document.getElementById('studentId').value));

  const searchInput = document.getElementById('search');
  const resultsList = document.getElementById('search-result');

  if (searchInput && resultsList) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      if (query.length > 0) {
        fetch(`/search?q=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(userlist => {
            resultsList.innerHTML = '';
            userlist.forEach(user => {
              const li = document.createElement('li');
              li.textContent = user.name;
              li.addEventListener('click', () => {
                window.location.href = `/studentProfile/${user.id}`;
              });
              resultsList.appendChild(li);
            });
            if (resultsList.children.length > 0) {
              resultsList.style.display = 'block';
            } else {
              resultsList.style.display = 'none';
            }
          })
          .catch(error => {
            console.error('Error fetching search results:', error);
            resultsList.style.display = 'none';
          });
      } else {
        resultsList.innerHTML = '';
        resultsList.style.display = 'none';
      }
    });
  }
});