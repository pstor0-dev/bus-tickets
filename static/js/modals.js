const open_modal = document.getElementById('open-modal');
const close_modal = document.getElementById('close-modal');
const modal_container = document.getElementById('modal-container');

if (open_modal && close_modal) {
    open_modal.addEventListener('click', () => {
        modal_container.classList.add('show');
    });    

    close_modal.addEventListener('click', () => {
        modal_container.classList.remove('show');
    });
}