/* Toggle nav state */
function open()
{
    window.dispatchEvent(new CustomEvent("sidebarOpen"));
}
function close()
{
    window.dispatchEvent(new CustomEvent("sidebarCollapse"));
}
function toggleNav() {
    const sideNav = document.getElementById("mySideNav");
    const content = document.getElementById("content");
    if (sideNav.classList.contains("collapsed")) {
        open();
        // Opsens nav and restores styling
        sideNav.classList.remove("collapsed");
        content.classList.remove("navCollapsed");
        // Resetting any inline styles the might interfere
        sideNav.style.width = "";
        content.style.marginLeft = "";
    }
    else {
        close();
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
