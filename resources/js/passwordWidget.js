// TODO: Based on the rules here, return an object with a properties `className` and `message`
//
// - A password with length less than 6 has `message` 'Short' and `className` 'short'
//
// Otherwise, we assign the password a score representing its strength. The
// score starts at 0 and will be incremented by one for each of the following
// conditions the password satisfies:
//
// - The password has length longer than 7
// - The password has at least one capital and lowercase letter
// - The password has at least one letter and at least one number
// - The password contains at two or more symbols
//
// We define symbols to be the following characters:
//    '!', '%', '&', '@', '#', '$', '^', '*', '?', '_', '~'
//
// Based on the value from the rules above, return the object with the correct
// values from the corresponding table:
//
// | Score | Class Name | Message         |
// |-------+------------+-----------------|
// | s < 2 | weak       | Weak Password   |
// | s = 2 | good       | Good Password   |
// | s > 2 | strong     | Strong Password |
function checkStrength(password) {
  // TODO: Change this.
  if (password.length < 6) {
    return {
      message: 'Short',
      className: 'short'
    };
  } else {
    // initialize score if length is greater than 6
    let s = 0;
    
    // greater than 7
    if (password.length > 7) {
      s = s+1;
    }

    // capital and lowercase check
    // referenced from: https://bobbyhadz.com/blog/javascript-find-all-uppercase-characters-in-string
    const onlyUpper = password.match(/[A-Z]/);
    const onlyLower = password.match(/[a-z]/);

    if (onlyUpper !== null && onlyLower !== null) {
      s = s+1;
    }

    // letter & number
    const onlyNumber = password.match(/[0-9]/);
    if ((onlyUpper !== null || onlyLower !== null) && onlyNumber !== null) {
      s = s+1;
    }

    // referenced from: https://stackoverflow.com/questions/37896484/multiple-conditions-for-javascript-includes-method
    const symbols = ['!', '%', '&', '@', '#', '$', '^', '*', '?', '_', '~'];
    let x = 0
    for (let i = 0; i < password.length; i+=1) {
      // symbol check
      if (symbols.indexOf(password[i]) !== -1) {
        x = x + 1;
      }

      if (x === 2) {
        s = s + 1;
      }
    }

    // check score
    console.log(s);

    // return
    if (s < 2) {
      return {
        message: 'Weak Password',
        className: 'weak'
      };
    } else if (s === 2) {
      return {
        message: 'Good Password',
        className: 'good'
      };
    } else if (s > 2) {
      return {
        message: 'Strong Password',
        className: 'strong'
      };
    }
  }
}

// You do not need to change this function. You may want to read it -- as you will find parts of it helpful with
// the countdown widget.
function showResult(password) {

  const { message, className } = checkStrength(password);

  if(!message || !className) {
    console.error("Found undefined message or className");
    console.log("message is", message);
    console.log("className is", className);
  }

  // This gets a javascript object that represents the <span id="pwdresult"></span> element
  // Using this javascript object we can manipulate the HTML span by
  // changing it's class and text content
  const resultElement = document.getElementById("pwdresult");

  // This sets the class to one specific element (since you can have multiple classes it's a list)
  resultElement.classList = [className];
  // This sets the text inside the span
  resultElement.innerText = message;
}

// Add a listener for the strength checking widget
function addPasswordListener() {
  let passwordEntry = document.getElementById('password');
  passwordEntry.addEventListener("keyup", () => {
    const password = passwordEntry.value;
    showResult(password);
  });
}

addPasswordListener();
