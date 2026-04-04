document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const overlay = document.getElementById("sidebar-overlay");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("active");
            overlay.classList.toggle("active");
        });
    }

    if (overlay) {
        overlay.addEventListener("click", function () {
            sidebar.classList.remove("active");
            overlay.classList.remove("active");
        });
    }

});


// manage_district 
// Live Search
document.getElementById("searchInput")?.addEventListener("keyup", function () {
    let value = this.value.toLowerCase();
    document.querySelectorAll("#districtTable tr").forEach(function (row) {
        row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
    });
});


// Open Edit Modal
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("editBtn")) {

        document.getElementById("editId").value = e.target.dataset.id;
        document.getElementById("editName").value = e.target.dataset.name;
        document.getElementById("editState").value = e.target.dataset.state;

        new bootstrap.Modal(document.getElementById("editModal")).show();
    }
});


// Save Edit
document.getElementById("saveEdit")?.addEventListener("click", function () {

    fetch("/adminpanel/districts/update/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            id: document.getElementById("editId").value,
            name: document.getElementById("editName").value,
            state: document.getElementById("editState").value
        })
    }).then(() => location.reload());

});


// Delete District
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("deleteBtn")) {

        let id = e.target.dataset.id;

        if (confirm("Are you sure?")) {

            fetch("/adminpanel/districts/delete/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({ id: id })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("row-" + id).remove();

                // Live Dashboard Update
                let totalCard = document.querySelector(".districts h2");
                if (totalCard) {
                    totalCard.innerText = data.total_districts;
                }
            });
        }
    }
});


// CSRF Helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(function (cookie) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
