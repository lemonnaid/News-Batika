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

//Search box field part of code

function toggleSearch() {
  let searchField = document.getElementById("searchField");
  if (searchField.style.display === "none") {
    searchField.style.display = "inline-block";
    searchField.focus();
  } else {
    searchField.style.display = "none";
  }
}

function open_link_and_get_similar_news(redirect_url, news_id, authenticated) {
  // Open a new window with the specified redirect URL
  window.open(redirect_url, "_blank");

  if (authenticated == "True") {
    console.log("Getting similar news");
    window.location.href = `http://localhost:8000/similar_news/${news_id}`;
  }
}

function search_news() {
  let search_text = document.getElementById("searchField").value;
  if (search_text) {
    console.log(search_text);
    window.location.href = `http://localhost:8000/search/${search_text}`;
  }
}

