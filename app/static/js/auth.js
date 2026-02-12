// Firebase config injected from backend
const firebaseConfig = window.__FIREBASE_CONFIG__;

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

const output = document.getElementById("output");

// ------------------ Utility ------------------

async function getToken() {
  const user = auth.currentUser;
  if (!user) {
    alert("Login first");
    return null;
  }
  return await user.getIdToken();
}

async function createBackendSession(token) {
  const res = await fetch("/auth/session", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  if (!res.ok) {
    const text = await res.text();
    output.textContent = "Session creation failed:\n" + text;
    return false;
  }

  return true;
}

async function authFetch(url, body = null, method = "POST") {
  const token = await getToken();
  if (!token) return null;

  const options = {
    method,
    headers: {
      Authorization: "Bearer " + token,
    },
  };

  if (body) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const res = await fetch(url, options);

  if (!res.ok) {
    const text = await res.text();
    output.textContent = "Error:\n" + text;
    return null;
  }

  return await res.json();
}

// ------------------ Login ------------------

document.getElementById("loginBtn").addEventListener("click", async () => {
  try {
    const provider = new firebase.auth.GoogleAuthProvider();
    const result = await auth.signInWithPopup(provider);

    const token = await result.user.getIdToken();

    // Create backend session
    const sessionCreated = await createBackendSession(token);

    if (!sessionCreated) return;

    output.textContent =
      "Logged in & session created:\n" +
      JSON.stringify(
        {
          uid: result.user.uid,
          email: result.user.email,
          name: result.user.displayName,
        },
        null,
        2
      );
  } catch (err) {
    output.textContent = "Login failed:\n" + err.message;
  }
});

// ------------------ Backend Test ------------------

document.getElementById("backendBtn").addEventListener("click", async () => {
  const res = await fetch("/auth/me");

  if (!res.ok) {
    const text = await res.text();
    output.textContent = text;
    return;
  }

  const data = await res.json();
  output.textContent =
    "Backend response:\n" + JSON.stringify(data, null, 2);
});

// ------------------ Team Create ------------------

document.getElementById("createTeamBtn").addEventListener("click", async () => {
  const name = document.getElementById("teamName").value;
  const data = await authFetch("/team/create", { name });
  if (data) {
    output.textContent = JSON.stringify(data, null, 2);
  }
});

// ------------------ Team Join ------------------

document.getElementById("joinTeamBtn").addEventListener("click", async () => {
  const invite_code = document.getElementById("inviteCode").value;
  const data = await authFetch("/team/join", { invite_code });
  if (data) {
    output.textContent = JSON.stringify(data, null, 2);
  }
});

// ------------------ Start Game ------------------

document.getElementById("startGameBtn").addEventListener("click", () => {
  // Now session handles auth automatically
  window.location.href = "/game/start";
});
