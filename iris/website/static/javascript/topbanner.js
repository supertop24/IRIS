window.onload = function() {
  const element = document.getElementById("name");
  element.innerText = "test";

  const searchInput = document.getElementById('search');
  const resultsList = document.getElementById('search-result');

  searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    if (query.length > 0) {
      fetch(`/search?q=${query}`)
        .then(response => response.json())
        .then(userlist => {
          resultsList.innerHTML = '';
          userlist.forEach(user => {
            const li = document.createElement('li');
            li.textContent = user.name;
            li.addEventListener('click', () => {
                                //showProductDetails(game.title, game.description, game.game_id);
                            });
            resultsList.appendChild(li);
          });
          resultsList.style.display = 'block';
          if (resultsList== empty)
          {
            resultsList.style.display = 'none';
          }
        })
        .catch(error => {
          console.error('Error fetching search results:', error);
        });
    } else {
      resultsList.innerHTML = '';
      resultsList.style.display = 'none';
    }
  });
};

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
