document.addEventListener('DOMContentLoaded',function(){
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if(toggle && nav){
    toggle.addEventListener('click',()=>{nav.style.display = nav.style.display === 'block' ? '' : 'block'});
  }

  // Simple demo JS for progress tracker page
  const progressInputs = document.querySelectorAll('.progress-input');
  progressInputs.forEach(input => {
    input && input.addEventListener('input', (e) => {
      const bar = document.querySelector(`#bar-${input.dataset.for}`);
      if(bar) bar.style.width = `${e.target.value}%`;
    });
  });
});