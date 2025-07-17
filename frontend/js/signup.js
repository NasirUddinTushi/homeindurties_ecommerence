document.querySelector("form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const first_name = document.querySelector("#first-name").value;
  const last_name = document.querySelector("#last-name").value;
  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  const response = await fetch("http://127.0.0.1:8000/api/account/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      first_name,
      last_name,
      email,
      password,
    }),
  });

  const data = await response.json();

  if (response.ok) {
    alert("Account created successfully!");
    window.location.href = "signin.html";
  } else {
    alert(data.message || "Registration failed.");
    console.log(data.errors);
  }
});
