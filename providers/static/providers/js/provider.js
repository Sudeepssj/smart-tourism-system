const toggleBtn = document.getElementById("sidebarToggle");
const sidebar = document.querySelector(".provider-sidebar");

toggleBtn.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
});


// const toggleBtn = document.getElementById("sidebarToggle");
// const sidebar = document.querySelector(".provider-sidebar");

// // ===== LOAD SAVED STATE =====
// if (localStorage.getItem("sidebarState") === "open") {
//     sidebar.classList.remove("collapsed");
// } else {
//     sidebar.classList.add("collapsed");
// }

// // ===== TOGGLE SIDEBAR =====
// toggleBtn.addEventListener("click", function () {

//     sidebar.classList.toggle("collapsed");

//     // SAVE STATE
//     if (sidebar.classList.contains("collapsed")) {
//         localStorage.setItem("sidebarState", "closed");
//     } else {
//         localStorage.setItem("sidebarState", "open");
//     }

// });