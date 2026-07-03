document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // LIVE SEARCH (District page)
    // ==========================

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            let value = this.value.toLowerCase();

            document.querySelectorAll("#districtTable tr").forEach(function(row){

                row.style.display =
                    row.innerText.toLowerCase().includes(value)
                    ? ""
                    : "none";

            });

        });

    }

    // ==========================
    // EDIT DISTRICT MODAL
    // ==========================

    document.addEventListener("click", function(e){

        if(e.target.classList.contains("editBtn")){

            document.getElementById("editId").value=e.target.dataset.id;
            document.getElementById("editName").value=e.target.dataset.name;
            document.getElementById("editState").value=e.target.dataset.state;

            new bootstrap.Modal(
                document.getElementById("editModal")
            ).show();

        }

    });

    // ==========================
    // SAVE DISTRICT
    // ==========================

    const saveBtn=document.getElementById("saveEdit");

    if(saveBtn){

        saveBtn.addEventListener("click",function(){

            fetch("/adminpanel/districts/update/",{

                method:"POST",

                headers:{
                    "X-CSRFToken":getCookie("csrftoken"),
                    "Content-Type":"application/x-www-form-urlencoded"
                },

                body:new URLSearchParams({

                    id:document.getElementById("editId").value,
                    name:document.getElementById("editName").value,
                    state:document.getElementById("editState").value

                })

            }).then(()=>location.reload());

        });

    }

    // ==========================
    // DELETE DISTRICT
    // ==========================

    document.addEventListener("click",function(e){

        if(e.target.classList.contains("deleteBtn")){

            let id=e.target.dataset.id;

            if(confirm("Delete this district?")){

                fetch("/adminpanel/districts/delete/",{

                    method:"POST",

                    headers:{
                        "X-CSRFToken":getCookie("csrftoken"),
                        "Content-Type":"application/x-www-form-urlencoded"
                    },

                    body:new URLSearchParams({
                        id:id
                    })

                })

                .then(res=>res.json())

                .then(data=>{

                    document.getElementById("row-"+id)?.remove();

                    let total=document.querySelector(".districts h2");

                    if(total){

                        total.innerText=data.total_districts;

                    }

                });

            }

        }

    });

});

// ==========================
// CSRF
// ==========================

function getCookie(name){

    let cookieValue=null;

    if(document.cookie && document.cookie!==""){

        document.cookie.split(";").forEach(function(cookie){

            cookie=cookie.trim();

            if(cookie.startsWith(name+"=")){

                cookieValue=decodeURIComponent(
                    cookie.substring(name.length+1)
                );

            }

        });

    }

    return cookieValue;

}