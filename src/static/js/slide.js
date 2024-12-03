//Functions for the animation on the auth page
function toggleSignUp() {
  const signinC = document.querySelector('.loginContainer');
  const signupC = document.querySelector('.signupContainer');

  signinC.style.display = 'none';
  signupC.style.display = 'flex';

}

function toggleSignIn() {
  const signinC = document.querySelector('.loginContainer');
  const signupC = document.querySelector('.signupContainer');

  signinC.style.display = 'flex';
  signupC.style.display = 'none';
}
