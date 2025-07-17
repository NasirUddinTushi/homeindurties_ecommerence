document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/api/account/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      localStorage.setItem("user_id", data.user_id);

      alert("Login successful!");

      // 🔁 Redirect to profile.html
      window.location.href = "profile.html";
    } else {
      alert(data.message || "Login failed. Please check credentials.");
    }
  } catch (err) {
    console.error(err);
    alert("Something went wrong. Try again later.");
  }
});
