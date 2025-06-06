/* Toggle nav state */
function toggleNav() {
    const sideNav = document.getElementById("mySideNav");
    const content = document.getElementById("content");

    if (sideNav.classList.contains("collapsed")) {
        // Opsens nav and restores styling
        sideNav.classList.remove("collapsed");
        content.classList.remove("navCollapsed");

        // Resetting any inline styles the might interfere
        sideNav.style.width = "";
        content.style.marginLeft = "";
    }
    else {
        //Closes nav
        sideNav.classList.add("collapsed");
        content.classList.add("navCollapsed");

        // Resetting any inline styles that might interfere
        sideNav.style.width = "";
        content.style.marginLeft = "";
    }
}
function studentProfile(id)
{
    window.location.href = `/studentProfile/${id}`;
}
/* Changing side nav's width and the content's left margin when nav is closed */
function closeNav() {
    
}
