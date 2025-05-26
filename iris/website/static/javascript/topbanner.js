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
