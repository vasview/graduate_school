var workEditModal = document.getElementById('workEditModal')
workEditModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var work_id = button.getAttribute('data-work_id')
    var work_title = button.getAttribute('data-work_title')
    var work_completion = button.getAttribute('data-work_completion')
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalBodyTitle = workEditModal.querySelector('.modal-body-title')
    var modalSlider = document.getElementById('modal_slider')
    var modalSliderValue = workEditModal.querySelector('.modal_slider_value')
    // var modalBodyInput = exampleModal.querySelector('.modal-body input')

    var model_save_btn = document.getElementById('model_save_btn')
    model_save_btn.dataset.work_id = work_id

    modalBodyTitle.textContent = work_title
    modalSlider.value = work_completion
    modalSliderValue.textContent = work_completion
    
})


var slider = document.getElementById("modal_slider");
var output = document.getElementById("modal_slider_val");
output.innerHTML = slider.value;

slider.oninput = function() {
    output.innerHTML = this.value;  
    // output.value = this.value;
}

function updateWorkPercentage() {
    const csfr = document.querySelector('[name=csrfmiddlewaretoken]').value
    let save_button = document.getElementById('model_save_btn')
    let work_id = save_button.getAttribute('data-work_id')
    let url = '/study_plans/works/' + work_id
    let modal_slider_val = document.getElementById('modal_slider_val')
    let change_value = modal_slider_val.innerHTML
    let body = JSON.stringify({completion: change_value})


    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'X-CSRFToken': csfr
    }

    fetch(url, {
            method: 'post',
            headers: headers,
            body: body
    })
        .then(response => {
            if(response.ok) {
                return response.json()
            } else {
                throw Error
            }
        })
        .then(data => {
            let completion_work_id = "completion_work_" + work_id;
            let left_work_id = 'left_work_' + work_id;
            let change_work_id = 'change_work_' + work_id;

            let completion_work_el = document.getElementById(completion_work_id);
            let left_work_el = document.getElementById(left_work_id);
            let change_work_btn = document.getElementById(change_work_id)

            completion_work_el.style.width = data['completion'] + '%'
            left_work_el.style.width = data['left'] + '%'
            completion_work_el.innerHTML =  data['completion']
            change_work_btn.dataset.work_completion = data['completion']

            let close_btn = document.getElementById("modal_close_btn");
            close_btn.click();
        })
        .catch(error => {
            console.log(error)
        })
}
