document.getElementById('item_owner_grade').addEventListener('change', function () {
    const selectedGrade = this.value;
    const userOptions = document.querySelectorAll('#item_owner option');

    userOptions.forEach(option => {
        if (option.value === '') {
            option.hidden = false;
            return;
        }

        option.hidden = selectedGrade &&
            option.dataset.grade !== selectedGrade;
    });

    document.getElementById('item_owner').value = '';
});
