/* Changing side nav's width and the container's left margin when nav is open */
function openNav() {
    document.getElementById("mySideNav").style.width = "320px";
    document.getElementById("container").style.marginLeft = "320px";


    /* Shows links when nav is open */
    const navText = document.querySelectorAll(".navItem span");
    navText.forEach(text => text.style.display = "block");

    // Show elements that should be visible in open state
    document.querySelector(".userProfile").style.display = "flex";
    document.querySelector(".irisLogo").style.display = "block";

    // Remove collapsed class
    document.getElementById("mySideNav").classList.remove("collapsed");
}

/* Changing side nav's width and the container's left margin when nav is closed */
function closeNav() {
    document.getElementById("mySideNav").style.width = "78px";
    document.getElementById("container").style.marginLeft = "78px";


    /* Hides links when nav is closed */
    const navTexts = document.querySelectorAll(".navItem span");
    navTexts.forEach(text => text.style.display = "none");

    // Hide elements that should be hidden in collapsed state
    document.querySelector(".userProfile").style.display = "none";
    document.querySelector(".irisLogo").style.display = "none";
    
    // Add collapsed class
    document.getElementById("mySideNav").classList.add("collapsed");
}
