let myBtn = document.getElementById('myBtn')

window.onscroll = function(){scrollFunction()}

function scrollFunction(){
    if(document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
        myBtn.style.display = "block";
    }else{
        myBtn.style.display = "none";
    }
}

function topFunction(){
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0
}