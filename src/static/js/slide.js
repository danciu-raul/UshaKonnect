//Functions for the animation on the auth page
function toggleSignUp() {
  const container = document.querySelector('.container');

  container.innerHTML = `
        <div class="signup">
            <h2>Hello!</h2>
            <p>If you already have an account, sign in here.</p>
            <button class="signup-button" onclick="toggleSignIn()">SIGN IN</button>
            <script src="../../static/js/slide.js"></script>
        </div>
        <div class="signin">
            <h1>Sign Up</h1>
            <input type="name" placeholder="Name" required>
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <button class="signin-button">SIGN IN</button>
        </div>   
        `;

  const signup = document.querySelector('.signup');

  signup.style.borderTopLeftRadius = '0px';
  signup.style.borderBottomLeftRadius = '0px';
  signup.style.borderBottomRightRadius = '70px';
  signup.style.borderTopRightRadius = '70px';

  const signinbt = document.querySelector('.signin-button');
  signinbt.style.margin = '30px';
}

function toggleSignIn() {
  const container = document.querySelector('.container');

  container.innerHTML = `
        <div class="signin">
            <h1>Sign In</h1>
            <input type="email" placeholder="Email" required>
            <input type="password" placeholder="Password" required>
            <a href="#" class="forgot-password">Forget your password?</a>
            <button class="signin-button">SIGN IN</button>
        </div>
        <div class="signup">
            <h2>Hello!</h2>
            <p>If you are not already registered, create an account here.</p>
            <button class="signup-button" onclick="toggleSignUp()" >SIGN UP</button>
            <script src="../../static/js/slide.js"></script>
        </div>

`;

  //bordure
  const signup = document.querySelector('.signup');

  signup.style.borderTopLeftRadius = '70px';
  signup.style.borderBottomLeftRadius = '70px';
  signup.style.borderBottomRightRadius = '0px';
  signup.style.borderTopRightRadius = '0px';
  //margin signin 

  const signinbt = document.querySelector('.signin-button');
  signinbt.style.margin = '0px';

}
