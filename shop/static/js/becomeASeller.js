document.getElementById("subBtn").addEventListener("click", ()=>{
    let business_name = document.getElementById("business_name");
    let business_email = document.getElementById("business_email");
    let business_phone_no = document.getElementById("business_phone_no");
    let business_address = document.getElementById("business_address");
    let items_to_sell = document.getElementById("items_to_sell");
    if (business_name.classList.contains('is_invalid')){
        business_name.focus();
        return false;
    }
    if (business_email.classList.contains('is_invalid')){
        business_email.focus();
        return false;
    }
    if (business_phone_no.classList.contains('is_invalid')){
        business_phone_no.focus();
        return false;
    }
    if (business_address.classList.contains('is_invalid')){
        business_address.focus();
        return false;
    }
    if (items_to_sell.classList.contains('is_invalid')){
        items_to_sell.focus();
        return false;
    }

    if (business_name.value == '' || business_email.value == '' || business_phone_no.value == '' || business_address.value == '' || items_to_sell.value == ''){
        alert("All fields are required. Please fill all the fields.");
        return false;
    }
    return true;
});
