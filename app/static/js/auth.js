// Firebase config injected from backend
const firebaseConfig = window.__FIREBASE_CONFIG__;

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

const output = document.getElementById("output");

document.getElementById("loginBtn").addEventListener("click", async () => {
  try {
    const provider = new firebase.auth.GoogleAuthProvider();
    const result = await auth.signInWithPopup(provider);

    output.textContent =
      "Logged in (Firebase):\n" +
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

document.getElementById("backendBtn").addEventListener("click", async () => {
  const user = auth.currentUser;
  if (!user) {
    alert("Login first");
    return;
  }

  const token = await user.getIdToken();

  const res = await fetch("/auth/me", {
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const data = await res.json();
  output.textContent =
    "Backend response:\n" + JSON.stringify(data, null, 2);
});

async function authFetch(url, body) {
  const user = auth.currentUser;
  if (!user) {
    alert("Login first");
    return;
  }

  const token = await user.getIdToken();

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  output.textContent = JSON.stringify(data, null, 2);
}

document.getElementById("createTeamBtn").addEventListener("click", () => {
  const name = document.getElementById("teamName").value;
  authFetch("/team/create", { name });
});

document.getElementById("joinTeamBtn").addEventListener("click", () => {
  const invite_code = document.getElementById("inviteCode").value;
  authFetch("/team/join", { invite_code });
});
