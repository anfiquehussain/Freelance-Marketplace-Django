function showProfileIncompleteMessage(message) {
    alert(message);
}

const cardTitles = document.getElementsByClassName('card-title');
const maxCharacters = 15; // Adjust this to your desired character limit

Array.from(cardTitles).forEach(cardTitle => {
    if (cardTitle.textContent.length > maxCharacters) {
        const truncatedText = cardTitle.textContent.substring(0, maxCharacters) + '...';
        cardTitle.textContent = truncatedText;
    }
});

