document.querySelector(".login-form").style.display = "none";
document.querySelector(".login").style.background = "none";

document.querySelector(".login").addEventListener("click", function() {
  document.querySelector(".signup-form").style.display = "none";
  document.querySelector(".login-form").style.display = "block";
  document.querySelector(".signup").style.background = "none";
  document.querySelector(".login").style.background = "#fff";
});

document.querySelector(".signup").addEventListener("click", function() {
  document.querySelector(".signup-form").style.display = "block";
  document.querySelector(".login-form").style.display = "none";
  document.querySelector(".login").style.background = "none";
  document.querySelector(".signup").style.background = "#fff";
});

