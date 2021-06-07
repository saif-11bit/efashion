let myBtn = document.getElementById('myBtn')

window.onscroll = function () { scrollFunction() }

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        myBtn.style.display = "block";
    } else {
        myBtn.style.display = "none";
    }
}
myBtn.addEventListener('click', function topFunction() {
    console.log('Clicked')
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0
})
