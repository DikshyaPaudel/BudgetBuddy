const usernameField = document.querySelector("#username");
const feedbackField = document.querySelector(".invalid_feedback");
const emailfeedbackField = document.querySelector(".email-feedback");
// const emailField = document.querySelector("#email");
const emailField = document.querySelector("#email");
const passwordField = document.querySelector("#password");
const showPassword = document.querySelector(".showpassword");
const submitButton = document.querySelector(".submit-btn");
showPassword.addEventListener("click", (e) => {
  if (showPassword.textContent === "SHOW") {
    showPassword.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPassword.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
});

emailField.addEventListener("keyup", (e) => {
  // console.log("222", 222);
  const emailvalue = e.target.value;

  emailField.classList.remove("is-invalid");
  emailfeedbackField.style.display = "none";

  if (emailvalue.length > 0) {
    fetch("/authentication/validate-email/", {
      body: JSON.stringify({
        email: emailvalue,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          emailField.classList.add("is-invalid");
          emailfeedbackField.style.display = "block";
          emailfeedbackField.innerHTML = `<p>${data.email_error}</p>`;
          submitButton.disabled = true;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {

  const usernamevalue = e.target.value;

  //to remove error when again rewriting the input
  usernameField.classList.remove("is-invalid");
  feedbackField.style.display = "none";

  if (usernamevalue.length > 0) {
    fetch("/authentication/validate-username/", {
      body: JSON.stringify({
        username: usernamevalue,
      }), //turn js object into correct json
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
       
        if (data.username_error) {
          usernameField.classList.add("is-invalid");
          feedbackField.style.display = "block";
          feedbackField.innerHTML = `<p>${data.username_error}</p>`;
          submitButton.disabled = true;
        } else {
          submitButton.removeAttribute("disabled");
        }
      });
  }
});
