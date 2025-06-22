window.onload = function() {
  const subject = document.getElementById('subject');
  const message = document.getElementById('messagetext');
  if(subject) subject.value = "";
  if(message) message.value = "";
  const user_id=document.getElementById('user_id').value;
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

  fetch(`/message_list?id=${encodeURIComponent(user_id)}`)
  .then(res => res.json())
  .then(data => {
    const listContainer = document.getElementById('list_container');
    listContainer.innerHTML = ''; // Clear any previous content

    if (!data || data.length === 0) {
      // If no messages, show fallback text
      const noMessageDiv = document.createElement('div');
      noMessageDiv.textContent = 'No messages.';
      noMessageDiv.className = 'no_messages'; // Optional: for styling
      listContainer.appendChild(noMessageDiv);
      return;
    }

    data.forEach(message => {
      const messageItem = document.createElement('div');
      messageItem.className = 'list_message_container';

      const top = document.createElement('div');
      top.className = 'list_message_container_top';

      const name = document.createElement('div');
      name.className = 'list_name';
      name.textContent = message.name || 'Unknown';

      const date = document.createElement('div');
      date.className = 'list_date';
      date.textContent = message.date || '';

      top.appendChild(name);
      top.appendChild(date);

      const bottom = document.createElement('div');
      bottom.className = 'list_message_container_bottom';
      bottom.textContent = message.title || '';

      messageItem.appendChild(top);
      messageItem.appendChild(bottom);

      // Optional click handler
      messageItem.addEventListener('click', () => {
        changeDisplay('read')
        document.getElementById('message_read').textContent=message.message;
        document.getElementById('message_title').textContent=message.title;
      });

      listContainer.appendChild(messageItem);
    });
  })
  .catch(error => {
    console.error('Error fetching messages:', error);
  });


};


function changeDisplay(id)
{
    if (id=='message')
    {
        document.getElementById('message').style.display='grid';
        document.getElementById('list').style.display='none';
        document.getElementById('read').style.display='none';
    }
    else if (id=="list") {
        document.getElementById('message').style.display='none';
        document.getElementById('list').style.display='grid';
        document.getElementById('messages').style.display='grid';
        document.getElementById('read').style.display='none';
    } 
    else if (id=="messages")
    {
        document.getElementById('messages').style.display='grid';
        document.getElementById('read').style.display='none';
    }
    else if (id=="read")
    {
        document.getElementById('read').style.display='grid';
        document.getElementById('messages').style.display='none';
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