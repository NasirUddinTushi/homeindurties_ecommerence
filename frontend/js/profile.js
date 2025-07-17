document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");

  if (!token) {
    alert("You are not logged in!");
    window.location.href = "signin.html";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/api/account/profile/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) throw new Error("Unauthorized");

    const data = await res.json();
    document.querySelector("#profile-name").innerText =
      data.data.first_name + " " + data.data.last_name;
    document.querySelector("#profile-email").innerText = data.data.email;
  } catch (err) {
    alert("Please login again.");
    window.location.href = "signin.html";
  }
});
