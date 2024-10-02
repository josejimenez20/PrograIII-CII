document.addEventListener('DOMContentLoaded', event => {
    mnxAcademica.addEventListener('click', e => {
        e.preventDefault();
        let form = e.target.dataset.form;
        console.log(form);
    });
});