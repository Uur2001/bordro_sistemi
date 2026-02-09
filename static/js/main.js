
function goToStep(stepNumber) {
    const allSteps = document.querySelectorAll('.step-content');
    allSteps.forEach(step => step.classList.remove('active'));
    const allButtons = document.querySelectorAll('.wizard-steps .step-button');
    allButtons.forEach(btn => btn.classList.remove('active'));
    const targetStep = document.getElementById('step' + stepNumber);
    if (targetStep) {
        targetStep.classList.add('active');
    }

    const targetButton = document.querySelector(`.wizard-steps .step-button[data-step="${stepNumber}"]`);
    if (targetButton) {
        targetButton.classList.add('active');
    }

    const stepText = document.getElementById('currentStepText');
    if (stepText) {
        stepText.textContent = stepNumber;
    }

    allButtons.forEach(btn => {
        const btnStep = parseInt(btn.getAttribute('data-step'));
        if (btnStep < stepNumber) {
            btn.classList.add('completed');
        } else if (btnStep > stepNumber) {
            btn.classList.remove('completed');
        }
    });

    console.log('Adım değişti:', stepNumber);
}

document.addEventListener('DOMContentLoaded', function() {
    const stepButtons = document.querySelectorAll('.wizard-steps .step-button');
    stepButtons.forEach(button => {
        button.addEventListener('click', function() {
            const step = parseInt(this.getAttribute('data-step'));
            goToStep(step);
        });
    });

    const toggleSwitches = document.querySelectorAll('.toggle-switch input');
    toggleSwitches.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const formGroup = this.closest('.form-group');
            if (formGroup) {
                const label = formGroup.querySelector('label');
                if (label) {
                    const status = this.checked ? 'Hesaplansın' : 'Hesaplanmasın';
                    console.log(label.textContent + ': ' + status);
                }
            }
        });
    });

    const moneyInputs = document.querySelectorAll('input[id*="Ucret"], input[id*="Matrahi"]');
    moneyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            let value = this.value.replace(/[^\d,]/g, '');
            if (value) {
                this.value = value + ' ₺';
            }
        });
    });

    const calculateBtns = document.querySelectorAll('.btn-calculate');
    calculateBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            alert('Bordro hesaplama işlevi henüz aktif değil. Bu özellik yakında eklenecek!');
        });
    });

    console.log('Sayfa yüklendi, wizard hazır.');
});

