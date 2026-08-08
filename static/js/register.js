document.getElementById("registerForm").addEventListener("submit", async function(e){

    e.preventDefault();

    const full_name = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    if(password !== confirm_password){
        alert("Passwords do not match");
        return;
    }

    const response = await fetch("/register",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            full_name,
            email,
            password
        })
    });

    const data = await response.json();

    alert(data.message);

    if(data.message==="User Registered Successfully"){
        window.location.href="/login-page";
    }

});