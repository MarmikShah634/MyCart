document.getElementById("subBtn").addEventListener("click", (e)=>{
    e.preventDefault();
    let description = document.getElementById("description");
    if (description.value === ''){
        description.classList.add("is-invalid");
        return false;
    }
    else{
        description.classList.remove("is-invalid");
        document.getElementById("contactForm").submit();
    }
});