   document.addEventListener('DOMContentLoaded', function() {
    function showSection(sectionId) {
        const sections = ['register-welcome', 'register-user', 'register-body', 'register-activity-level', 'register-username'];
        for (const section of sections) {
            document.getElementById(section).style.display = section === sectionId ? 'block' : 'none';
        }
    }

    showSection('register-welcome');

    document.getElementById('continue-register-welcome').addEventListener('click', function() {
        showSection('register-user');
    });

    document.getElementById('next-register-user').addEventListener('click', function() {
        if (validateUserSection()) {
            showSection('register-body');
        }
    });

    document.getElementById('next-register-body').addEventListener('click', function() {
        if (validateBodySection()) {
            showSection('register-activity-level');
        }
    });

    document.getElementById('next-register-activity').addEventListener('click', function() {
        if (validateActivitySection()) {
            showSection('register-username');
        }
    });

    document.getElementById('previous-register-user').addEventListener('click', function() {
        showSection('register-welcome');
    });

    document.getElementById('previous-register-body').addEventListener('click', function() {
        showSection('register-user');
    });

    document.getElementById('previous-register-activity').addEventListener('click', function() {
        showSection('register-body');
    });

    document.getElementById('username').addEventListener('keyup', function() {
        updateHiddenFields();
    });

    const passwordInput = document.getElementById('user-password');
    const registerButton = document.getElementById('register-everything');

    passwordInput.addEventListener('keyup', function() {
        const passwordValue = passwordInput.value;
        registerButton.disabled = passwordValue.length < 8;
    });

    const confirmPassword = document.getElementById('confirm-password');
    confirmPassword.addEventListener('keyup', function() {
        registerButton.disabled = passwordInput.value !== confirmPassword.value;
    });
});


function validateUserSection() {
    const firstName = document.getElementById('first-name').value;
    const gender = getSelectedGender();
    const bday = document.getElementById('bday').value;

    if (firstName && gender && bday) {
        updateHiddenFields();
        return true;
    } else {
        alert('Please fill in all the fields in the current section.');
        return false;
    }
}

function validateBodySection() {
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;
    const goalWeight = document.getElementById('goalweight').value;

    if (height && weight && goalWeight) {
        updateHiddenFields();
        return true;
    } else {
        alert('Please fill in all the fields in the current section.');
        return false;
    }
}

function validateActivitySection() {
    const activityLevel = getSelectedActivityLevel();

    if (activityLevel !== null) {
        updateHiddenFields();
        return true;
    } else {
        alert('Please select an activity level in the current section.');
        return false;
    }
}

function updateHiddenFields() {
    document.getElementById('user-name').value = document.getElementById('first-name').value;
    document.getElementById('user-sex').value = getSelectedGender();
    document.getElementById('user-bday').value = document.getElementById('bday').value;
    document.getElementById('user-height').value = document.getElementById('height').value;
    document.getElementById('user-weight').value = document.getElementById('weight').value;
    document.getElementById('user-goalweight').value = document.getElementById('goalweight').value;
    document.getElementById('user-activity').value = getSelectedActivityLevel();
}

function getSelectedGender() {
    const maleRadioButton = document.getElementById('sex-male');
    const femaleRadioButton = document.getElementById('sex-female');

    if (maleRadioButton.checked) {
        return 'male';
    } else if (femaleRadioButton.checked) {
        return 'female';
    } else {
        return null;
    }
}

function getSelectedActivityLevel() {
    const activityLevels = document.getElementsByName('activity-level');

    for (let i = 0; i < activityLevels.length; i++) {
        if (activityLevels[i].checked) {
            return i;
        }
    }

    return null;
}