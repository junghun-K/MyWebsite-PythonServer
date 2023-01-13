function autoSuggest() {
  let email = document.getElementById('email');
  let username = document.getElementById('user');

  updateValue(username, email.value);
  
  // referenced from: https://flaviocopes.com/how-to-find-character-string-javascript/#:~:text=Nov%2013%202020-,How%20do%20you%20find%20a%20character%20in%20a%20string%2C%20using,one%20(or%20more)%20characters.&text=If%20there%20are%20more%20than,finds%2C%20starting%20from%20the%20left.
  function updateValue(username,email) {
    if (username.value === "" && email.includes('@')) {
      console.log(email);
      username.value = email.slice(0, email.indexOf('@'));
    }
  }
}

function concernChecked() {
  let concern = document.getElementById('concern');
  let popup = document.getElementById('concernbox');
  // referenced from: https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration/setProperty
  if (concern.checked) {
    popup.style.setProperty('display', 'inline-block');
  } else {
    popup.style.setProperty('display', 'none');
  }
}

// referenced from: lecture code
document.querySelector('#email').addEventListener('input', autoSuggest);

document.querySelector('#concern').addEventListener('click', concernChecked);
document.querySelector('#question').addEventListener('click', concernChecked);
document.querySelector('#comment').addEventListener('click', concernChecked);

