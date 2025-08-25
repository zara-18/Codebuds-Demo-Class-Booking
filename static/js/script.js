const select_box=document.querySelector(".options"),
search_box=document.querySelector(".search-box"),
input_box=document.querySelector('.phone')
selected_opt=document.querySelector('.dropdown-opt')

let options=document.querySelectorAll(".option");

selected_opt.addEventListener("click",()=>{
    select_box.classList.toggle("active");
    selected_opt.classList.toggle("active");
});

function selectOption(){
    const icon=this.querySelector(".iconify").cloneNode(true);
    phone_code=this.querySelector("strong").cloneNode(true);
    selected_opt.innerHTML="";
    selected_opt.append(icon);
    input_box.value = phone_code.innerText;
    select_box.classList.remove("active");
    selected_opt.classList.remove("active");
    search_box.value="";
    opt.classList.remove("hidden")
    
}
function search_country_code() {
    let code = input_box.value.trim();
    
    for (let opt of options) {
        let country_code = opt.querySelector("strong").innerText.trim();
        
        if (country_code === code) {
            let icon1 = opt.querySelector(".iconify").cloneNode(true);
            selected_opt.innerHTML = "";
            selected_opt.append(icon1);
            select_box.classList.remove("active");
            selected_opt.classList.add("active");
            return; 
        }
    }
}
function search_country(){
    let search_query = search_box.value.toLowerCase();
    for(opt of options){
    let is_matched=opt.querySelector(".country-name").innerText.toLowerCase().includes(search_query);
    opt.classList.toggle("hidden", !is_matched);
    }
}



options.forEach(option=>option.addEventListener("click",selectOption)); 
search_box.addEventListener("input",search_country)
input_box.addEventListener("input",search_country_code)

    
 



