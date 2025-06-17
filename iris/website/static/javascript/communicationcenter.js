window.addEventListener('load', function() {
  const searchInput = document.getElementById('usersearch');
  const resultsList = document.getElementById('usersearch-result');

  if (searchInput && resultsList) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      if (query.length > 0) {
        fetch(`/searchUser?q=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(userlist => {
            resultsList.innerHTML = '';
            userlist.forEach(user => {
              const li = document.createElement('li');
              li.textContent = user.name;
              li.addEventListener('click', () => {
                document.getElementById('target_id').value=user.id;
                document.getElementById('target_name').textContent='Send message to: '+user.name;
                document.getElementById('toggle_search').checked=false;
                document.getElementById('target_lock').checked=true;
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

function changeDisplay(id)
{
    if (id=='message')
    {
        document.getElementById('message').style.display='grid';
        document.getElementById('list').style.display='none';
        document.getElementById('view').style.display='none';
    }
    else if (id=="list") {
        document.getElementById('message').style.display='none';
        document.getElementById('list').style.display='grid';
        document.getElementById('view').style.display='none';
    } 
    else 
    {
        document.getElementById('message').style.display='none';
        document.getElementById('list').style.display='none';
        document.getElementById('view').style.display='grid';
    }
}