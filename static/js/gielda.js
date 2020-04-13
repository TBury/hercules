var dropdown = document.querySelector('.dropdown');
dropdown.addEventListener('click', function (event) {
    event.stopPropagation();
    dropdown.classList.toggle('is-active');
});

document.querySelector('.sort_by').addEventListener('change', function () {
    const sortForm = document.querySelector(".sort-form");
    sortForm.submit();
});
