<script type="text/javascript"></script>
const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.loginlink');
const signupLink = document.querySelector('.signuplink');

signupLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
}); 