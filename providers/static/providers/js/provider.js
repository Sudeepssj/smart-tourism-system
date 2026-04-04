const toggleBtn = document.getElementById("sidebarToggle");
const sidebar = document.querySelector(".provider-sidebar");

toggleBtn.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
});