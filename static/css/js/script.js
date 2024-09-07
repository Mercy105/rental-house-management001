
// JavaScript to toggle dropdown menu
function toggleDropdown() {
    var dropdown = document.getElementById("property-dropdown");
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}
