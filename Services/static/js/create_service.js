const steps = document.querySelectorAll('.step');
const nextBtns = document.querySelectorAll('.next-step');
const prevBtns = document.querySelectorAll('.prev-step');
let currentStep = 0;

function showStep(stepIndex) {
  steps.forEach((step, index) => {
    if (index === stepIndex) {
      step.classList.add('active');
    } else {
      step.classList.remove('active');
    }
  });
}

nextBtns.forEach((btn, index) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    currentStep++;
    showStep(currentStep);
  });
});

prevBtns.forEach((btn, index) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    currentStep--;
    showStep(currentStep);
  });
});

showStep(currentStep);