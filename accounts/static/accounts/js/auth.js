const loginBtn = document.getElementById("loginBtn");
const userBtn = document.getElementById("userSignupBtn");
const providerBtn = document.getElementById("providerSignupBtn");

const slider = document.querySelector(".form-slider");

loginBtn.addEventListener("click", () => {
    slider.style.transform = "translateX(0%)";
    setActive(loginBtn);
});

userBtn.addEventListener("click", () => {
    slider.style.transform = "translateX(-33.3333%)";
    setActive(userBtn);
});

providerBtn.addEventListener("click", () => {
    slider.style.transform = "translateX(-66.6666%)";
    setActive(providerBtn);
});

function setActive(button) {
    document.querySelectorAll(".auth-toggle button")
        .forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
}

/* PASSWORD TOGGLE */
document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", function () {
        const target = document.getElementById(this.dataset.target);
        if (target.type === "password") {
            target.type = "text";
            this.classList.replace("fa-eye", "fa-eye-slash");
        } else {
            target.type = "password";
            this.classList.replace("fa-eye-slash", "fa-eye");
        }
    });
});
