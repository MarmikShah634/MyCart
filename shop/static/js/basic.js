searchBtn.addEventListener("click", ()=>{
    let searchBtn = document.getElementById("searchBtn");
    if (document.getElementById("search").value === ''){
        alert("Please enter somthing to serach.");
        document.getElementById('searchAnchorTag').setAttribute('href', '#');
    }
    else{
        document.getElementById('searchAnchorTag').setAttribute('href', '/shop/search');
    }
});