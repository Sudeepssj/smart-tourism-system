document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const overlay = document.getElementById("sidebar-overlay");
    const mainContent = document.getElementById("main-content");

    /* =========================
       SIDEBAR TOGGLE (ONLY BUTTON)
    ========================= */
    toggleBtn.addEventListener("click", function () {

        if (window.innerWidth <= 992) {
            // MOBILE → only show/hide
            sidebar.classList.toggle("active");
            overlay.classList.toggle("active");
        } else {
            // DESKTOP → collapse mode
            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("expanded");
        }

    });

    /* =========================
       OVERLAY CLOSE (MOBILE)
    ========================= */
    overlay?.addEventListener("click", function () {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    });

    /* =========================
       🔥 FIX: CONTROL BOOTSTRAP COLLAPSE
    ========================= */
    document.querySelectorAll('[data-bs-toggle="collapse"]').forEach(link => {

        link.addEventListener("click", function (e) {

            const isCollapsed = sidebar.classList.contains("collapsed");

            if (isCollapsed) {
                // ❌ STOP bootstrap completely
                e.preventDefault();
                e.stopImmediatePropagation();

                alert("Expand sidebar to use menu");
                return false;
            }

        }, true); // 🔥 IMPORTANT (capture phase)
    });

    /* =========================
       NORMAL LINKS → DO NOTHING
    ========================= */
    document.querySelectorAll("#sidebar a:not([data-bs-toggle])").forEach(link => {
        link.addEventListener("click", function () {
            // allow navigation normally
        });
    });

    /* =========================
       LIVE SEARCH
    ========================= */
    document.getElementById("searchInput")?.addEventListener("keyup", function () {
        let value = this.value.toLowerCase();

        document.querySelectorAll("#districtTable tr").forEach(function (row) {
            row.style.display = row.innerText.toLowerCase().includes(value) ? "" : "none";
        });
    });

    /* =========================
       EDIT MODAL
    ========================= */
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("editBtn")) {

            document.getElementById("editId").value = e.target.dataset.id;
            document.getElementById("editName").value = e.target.dataset.name;
            document.getElementById("editState").value = e.target.dataset.state;

            new bootstrap.Modal(document.getElementById("editModal")).show();
        }
    });

    /* =========================
       SAVE EDIT
    ========================= */
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

    /* =========================
       DELETE DISTRICT
    ========================= */
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

                    let totalCard = document.querySelector(".districts h2");
                    if (totalCard) {
                        totalCard.innerText = data.total_districts;
                    }
                });
            }
        }
    });

});

/* =========================
   CSRF HELPER
========================= */
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