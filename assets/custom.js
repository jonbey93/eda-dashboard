function autoResizeBoxes() {
    const boxes = document.querySelectorAll('textarea[id*="view-code-box"]');
    boxes.forEach(box => {
        box.style.height = 'auto';
        box.style.height = box.scrollHeight + 'px';
    });
}

document.addEventListener('DOMContentLoaded', autoResizeBoxes);

// Resize again after any button click (for toggling visibility)
document.addEventListener('click', (e) => {
    if (e.target && e.target.innerText.includes('View Code')) {
        setTimeout(autoResizeBoxes, 50);  // Delay to allow DOM update
    }
});