window.onload = function() {
  const subject = document.getElementById('subject');
  const message = document.getElementById('messagetext');
  if(subject) subject.value = "";
  if(message) message.value = "";

  const targetLock = document.getElementById('target_lock');
  if(targetLock) targetLock.checked = false;

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
                document.getElementById('target_id').value = user.id;
                document.getElementById('target_name').textContent = 'Send message to: ' + user.name;
                document.getElementById('toggle_search').checked = false;
                document.getElementById('target_lock').checked = true;
              });
              resultsList.appendChild(li);
            });
            resultsList.style.display = resultsList.children.length > 0 ? 'block' : 'none';
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
};


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
function searchon()
{
  document.getElementById('target_lock').checked=false;
}
function send()
{
  const targetID= document.getElementById('target_id').value;
  const userID= document.getElementById('user_id').value;
  const subject=document.getElementById('subject').value;
  const message=document.getElementById('messagetext').value;
  if (subject.trim() === "") {
    alert("Please write a subject!");
    return;
  }
  if (message.trim() === "") {
    alert("Please write the message!");
    return;
  }
  const formData = new FormData();
  formData.append('sender_id', userID);
  formData.append('target', subject);
  formData.append('target_id', targetID);
  formData.append('sender', subject);
  formData.append('message', message);
  fetch('/sendMessage', {
    method: 'POST',
    body: formData,
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
  alert("Message succesfully uploaded!");
  window.onload();
}