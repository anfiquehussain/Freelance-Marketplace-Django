function myFunction() {
    var readmore = document.getElementById("read-more");
    var btnText = document.getElementById("myBtn");
    if (readmore.style.display === "none") {
        readmore.style.display = "inline"
        btnText.innerHTML = "Hide";
    } else {
        readmore.style.display = "none";
        btnText.innerHTML = "Show";

    }

}