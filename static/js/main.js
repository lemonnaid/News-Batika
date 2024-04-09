function validate_form() {
  if (validate_firstname() && validate_lastname() && validate_username() && validate_password() && compare_passwords()) {
    return true;
  }
  return false;
}

function validate_firstname() {
  let first_name = document.getElementById("firstname").value;
  let fn_regex = /^[A-Za-z ]+$/;

  if (!fn_regex.test(first_name)) {
    alert("Firstname should have only alphabet");
    document.getElementById("firstname").focus();
    return false;
  }
  return true;
}

function validate_lastname() {
  let last_name = document.getElementById("lastname").value;
  let ln_regex = /^[A-Za-z ]+$/;

  if (!ln_regex.test(last_name)) {
    alert("Lastname should have only alphabet separated by space");
    document.getElementById("lastname").focus();
    return false;
  }
  return true;
}

function validate_username() {
  let user_name = document.getElementById("username").value;
  let user_regex = /^[A-Za-z0-9]+$/;

  if (!user_regex.test(user_name)) {
    alert("Username should have only alphabet.");
    document.getElementById("username").focus();
    return false;
  }
  return true;
}

function validate_password() {
  let user_password = document.getElementById("password").value;
  password_regex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[+=@#%$^*/-]).{8,}$/;
  if (!password_regex.test(user_password)) {
    alert("Password Policy failed. Password should have lowercase, uppercase, digit, special character and atleast 8 character long");
    document.getElementById("password").focus();
    return false;
  }
  return true;
}

function compare_passwords() {
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("password_confirm").value;

  if (password != confirmPassword) {
    alert("Password do not match");
    document.getElementById("password_confirm").focus();
    return false;
  }
  return true;
}


function openNewsAndRefresh(newsId) {
  // Open news source in new tab
  // window.open("http://url-to-news-source.com", "_blank");

  // Fetch similar news using AJAX
  $.ajax({
      url: `http://127.0.0.1:8000/similar_news/${newsId}/`,
      type: 'GET',
      success: function(data) {
          // Update home news content with similar news
          $('.home-news-container').html(data);
      },
      error: function(xhr, status, error) {
          console.error('Failed to fetch similar news:', error);
      }
  });
}
