function toggleCategories() {
    // Get all columns with the class 'col-6' inside the row with the id 'CtgListRow'
    var cols = document.querySelectorAll('#CtgListRow .col-6');

    // Toggle the 'd-none' class of each column
    cols.forEach(function (col) {
        col.classList.toggle('d-none');
    });
}

// console.log("hallo")
document.addEventListener('DOMContentLoaded', function () {
    titlediplay();

    function titlediplay() {
        const cardTitles = document.getElementsByClassName('card-title');
        const maxCharacters = 50; // Adjust this to your desired character limit

        Array.from(cardTitles).forEach(cardTitle => {
            if (cardTitle.textContent.length > maxCharacters) {
                const truncatedText = cardTitle.textContent.substring(0, maxCharacters) + '...';
                cardTitle.textContent = truncatedText;
            }
        });
    }
});