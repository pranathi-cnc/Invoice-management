const usernameGroup = document.getElementById("username-group");
const confirmGroup = document.getElementById("confirm-group");

const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");

const loginBtn = document.getElementById("loginBtn");
const loginMessage = document.getElementById("login-message");

const toggleLink = document.getElementById("toggleLink");
const toggleMessage = document.getElementById("toggleMessage");
const formSubtitle = document.getElementById("formSubtitle");

let signupMode = false;

// =========================
// Toggle Login / Signup
// =========================

toggleLink.addEventListener("click", (e) => {

    e.preventDefault();

    signupMode = !signupMode;

    if (signupMode) {

        usernameGroup.style.display = "block";
        confirmGroup.style.display = "block";

        loginBtn.textContent = "Create Account";

        formSubtitle.textContent = "Create your account";

        toggleMessage.textContent = "Already have an account?";

        toggleLink.textContent = "Login";

        loginMessage.textContent = "";

    }

    else {

        usernameGroup.style.display = "none";
        confirmGroup.style.display = "none";

        loginBtn.textContent = "Login";

        formSubtitle.textContent = "Sign in to continue";

        toggleMessage.textContent = "Don't have an account?";

        toggleLink.textContent = "Sign Up";

        loginMessage.textContent = "";

    }

});

// =========================
// Login / Signup
// =========================

loginBtn.addEventListener("click", async () => {

    loginMessage.textContent = "";

    if (signupMode) {

        if (
            username.value.trim() === "" ||
            email.value.trim() === "" ||
            password.value === "" ||
            confirmPassword.value === ""
        ) {

            loginMessage.style.color = "red";
            loginMessage.textContent = "Please fill all fields.";
            return;

        }

        if (password.value !== confirmPassword.value) {

            loginMessage.style.color = "red";
            loginMessage.textContent = "Passwords do not match.";
            return;

        }

        try {

            const response = await fetch("http://127.0.0.1:8000/auth/signup", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    username: username.value.trim(),

                    email: email.value.trim(),

                    password: password.value,

                    confirmPassword: confirmPassword.value

                })

            });

            const result = await response.json();

            if (response.ok) {

                loginMessage.style.color = "green";
                loginMessage.textContent = "Account created successfully.";

                username.value = "";
                email.value = "";
                password.value = "";
                confirmPassword.value = "";

                signupMode = false;

                usernameGroup.style.display = "none";
                confirmGroup.style.display = "none";

                loginBtn.textContent = "Login";

                formSubtitle.textContent = "Sign in to continue";

                toggleMessage.textContent = "Don't have an account?";

                toggleLink.textContent = "Sign Up";

            }

            else {

                loginMessage.style.color = "red";
                loginMessage.textContent = result.detail;

            }

        }

        catch {

            loginMessage.style.color = "red";
            loginMessage.textContent = "Unable to connect to server.";

        }

    }

    else {

        if (email.value.trim() === "" || password.value === "") {

            loginMessage.style.color = "red";
            loginMessage.textContent = "Please enter Email and Password.";
            return;

        }

        try {

            const response = await fetch("http://127.0.0.1:8000/auth/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    email: email.value.trim(),

                    password: password.value

                })

            });

            const result = await response.json();

            if (response.ok) {

                localStorage.setItem("token", result.token);

                localStorage.setItem("user", JSON.stringify(result.user));

                loginMessage.style.color = "green";

                loginMessage.textContent = "Login Successful.";

                setTimeout(() => {

                    window.location.href = "index.html";

                }, 1000);

            }

            else {

                loginMessage.style.color = "red";

                loginMessage.textContent = result.detail;

            }

        }

        catch {

            loginMessage.style.color = "red";

            loginMessage.textContent = "Unable to connect to server.";

        }

    }

});