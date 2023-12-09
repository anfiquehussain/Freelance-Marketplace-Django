 // Get references to the button and the message paragraph by class name
 var buttons = document.getElementsByClassName("continue-button");
 var messages = document.getElementsByClassName("message");

 // Loop through each button element and add a click event listener
 for (var i = 0; i < buttons.length; i++) {
   buttons[i].addEventListener("click", function () {
     // Find the corresponding message paragraph
     var index = Array.prototype.indexOf.call(buttons, this);
     if (index >= 0 && index < messages.length) {
       // Display the corresponding message paragraph when the button is clicked
       messages[index].style.display = "block";
     }
   });
 }