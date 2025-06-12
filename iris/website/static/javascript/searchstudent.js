window.addEventListener('load', function() {
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