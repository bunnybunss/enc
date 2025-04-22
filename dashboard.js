// static/dashboard.js

const token = localStorage.getItem("jwt_token");
if (!token) {
  window.location.href = "/login";
}

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

document.getElementById("encryptButton").addEventListener("click", async () => {
  const file = document.getElementById("encryptFile").files[0];
  const password = document.getElementById("encryptPassword").value;
  const status = document.getElementById("status");

  if (!file || !password) {
    status.innerText = "⚠️ Please select a file and enter a password.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("password", password);

  const res = await fetch("/encrypt", {
    method: "POST",
    headers: { "x-access-token": token },
    body: formData
  });

  if (res.ok) {
    const blob = await res.blob();
    triggerDownload(blob, "encrypted_" + file.name);
    status.innerText = "✅ File encrypted and downloaded.";
  } else {
    const error = await res.json();
    status.innerText = "❌ " + (error.message || "Encryption failed.");
  }
});

document.getElementById("decryptButton").addEventListener("click", async () => {
  const file = document.getElementById("decryptFile").files[0];
  const password = document.getElementById("decryptPassword").value;
  const status = document.getElementById("status");

  if (!file || !password) {
    status.innerText = "⚠️ Please select a file and enter a password.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("password", password);

  const res = await fetch("/decrypt", {
    method: "POST",
    headers: { "x-access-token": token },
    body: formData
  });

  if (res.ok) {
    const blob = await res.blob();
    triggerDownload(blob, "decrypted_" + file.name);
    status.innerText = "✅ File decrypted and downloaded.";
  } else {
    const error = await res.json();
    status.innerText = "❌ " + (error.message || "Decryption failed.");
  }
});

document.getElementById("logoutLink").addEventListener("click", (e) => {
  e.preventDefault();
  localStorage.removeItem("jwt_token");
  window.location.href = "/login";
});
