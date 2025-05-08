/* Changing side nav's width and the container's left margin when nav is open */
function openNav() {
    document.getElementById("mySideNav").style.width = "320px";
    document.getElementById("container").style.marginLeft = "320px";
}

/* Changing side nav's width and the container's left margin when nav is closed */
function closeNav() {
    document.getElementById("mySideNav").style.width = "0";
    document.getElementById("container").style.marginLeft = "0";
}
