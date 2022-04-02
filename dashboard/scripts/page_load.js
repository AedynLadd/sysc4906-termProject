

if (window.localStorage.getItem("visited-SYSC4906-dashboard") == null){
    document.getElementById("landing_page").className = "landing_page"
    document.getElementById("main_animation_body").className = "main_animation_body"
} else{
    document.getElementById("landing_page").className = "landing_page_hiding"
    document.getElementById("main_animation_body").className = "main_animation_body_shown"
}

function hideLandingPage(){
    window.localStorage.setItem("visited-SYSC4906-dashboard", "visited")
    document.getElementById("landing_page").className = "landing_page_hiding"
    document.getElementById("main_animation_body").className= "main_animation_body_shown"
}
