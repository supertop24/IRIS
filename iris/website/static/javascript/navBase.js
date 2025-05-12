/* Toggle nav state */
function openNav() {
    const sideNav = document.getElementById("mySideNav");
    const content = document.getElementById("content");

    // Removes collapsed class to restore styling
    sideNav.classList.remove("collapsed");
    content.classList.remove("navCollapsed");

    // Resetting any inline styles the might interfere
    sideNav.style.width = "";
    content.style.marginLeft = "";
}

/* Changing side nav's width and the content's left margin when nav is closed */
function closeNav() {
   const sideNav = document.getElementById("mySideNav");
    const content = document.getElementById("content");


    // Adds collapsed class
    sideNav.classList.add("collapsed");
    content.classList.add("navCollapsed");

    // Resetting any inline styles that might interfere
    sideNav.style.width = "";
    content.style.marginLeft = "";
}
