// Get references to the popup and open button
var popup = document.getElementById("popup");
var openButton = document.getElementsByName("openPopupButton")[0];

// Get reference to the close button inside the popup
var closeButton = document.getElementById("closePopup");

// Function to open the popup
function openPopup() {
    popup.style.display = "block";
}

// Function to close the popup
function closePopup() {
    popup.style.display = "none";
}

// Event listeners
openButton.addEventListener("click", openPopup);
closeButton.addEventListener("click", closePopup);
