/* Toggle nav state */
function openNav() {
    const sideNav = document.getElementById("mySideNav");
    const container = document.getElementById("container");

    // Removes collapsed class to restore styling
    sideNav.classList.remove("collapsed");
    container.classList.remove("navCollapsed");

    // Resetting any inline styles the might interfere
    sideNav.style.width = "";
    container.style.marginLeft = "";
}

/* Changing side nav's width and the container's left margin when nav is closed */
function closeNav() {
   const sideNav = document.getElementById("mySideNav");
    const container = document.getElementById("container");


    // Adds collapsed class
    sideNav.classList.add("collapsed");
    container.classList.add("navCollapsed");

    // Resetting any inline styles that might interfere
    sideNav.style.width = "";
    container.style.marginLeft = "";
}
