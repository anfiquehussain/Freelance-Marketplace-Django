document.addEventListener("DOMContentLoaded", function () {
    const basicButton = document.getElementById("basic-button");
    const standardButton = document.getElementById("standard-button");
    const premiumButton = document.getElementById("premium-button");

    const basicDetails = document.getElementById("basic-details");
    const standardDetails = document.getElementById("standard-details");
    const premiumDetails = document.getElementById("premium-details");

    basicButton.addEventListener("click", function () {
      basicDetails.style.display = "block";
      standardDetails.style.display = "none";
      premiumDetails.style.display = "none";

      // Change button background colors
      basicButton.style.backgroundColor = "var(--background)" 

      standardButton.style.backgroundColor = "";
      premiumButton.style.backgroundColor = "";

      basicButton.style.color = "var(--text)";
      standardButton.style.color = "";
      premiumButton.style.color = "";

    });

    standardButton.addEventListener("click", function () {
      basicDetails.style.display = "none";
      standardDetails.style.display = "block";
      premiumDetails.style.display = "none";

      // Change button background colors
      basicButton.style.backgroundColor = "";
      standardButton.style.backgroundColor = "var(--background)";  // Change to your desired color
      premiumButton.style.backgroundColor = "";

      basicButton.style.color = "";
      standardButton.style.color = "var(--text)";
      premiumButton.style.color = "";
    });

    premiumButton.addEventListener("click", function () {
      basicDetails.style.display = "none";
      standardDetails.style.display = "none";
      premiumDetails.style.display = "block";

      // Change button background colors
      basicButton.style.backgroundColor = "";
      standardButton.style.backgroundColor = "";
      premiumButton.style.backgroundColor = "var(--background)";  // Change to your desired color
      basicButton.style.color = "";
      standardButton.style.color = "";
      premiumButton.style.color = "var(--text)";
    });

    // Show basic details by default
    basicDetails.style.display = "block";
    basicButton.style.backgroundColor = "var(--background)";  // Change to your desired color
    basicButton.style.color = "var(--text)";
  });

  