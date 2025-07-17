document.getElementById("logout-btn").addEventListener("click", async () => {
  const refresh = localStorage.getItem("refresh_token");

  const response = await fetch("http://127.0.0.1:8000/api/account/logout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access_token")}`,
    },
    body: JSON.stringify({ refresh }),
  });

  if (response.ok) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    alert("Logged out successfully!");
    window.location.href = "signin.html";
  } else {
    alert("Logout failed.");
  }
});
