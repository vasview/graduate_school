var noteEditModal = document.getElementById('noteEditModal')
noteEditModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    var section_title = button.getAttribute('data-section_title')
    var section_name = button.getAttribute('data-section_name')
    var section_id = button.getAttribute('data-section_id')
    var modalBodyTitle = noteEditModal.querySelector('.modal-body-title')
    var model_save_btn = document.getElementById('model_save_btn')

    model_save_btn.dataset.section_name = section_name
    model_save_btn.dataset.section_url = '/postgraduates/explanatory_notes/' + section_id + '/approve'
    modalBodyTitle.textContent = section_title
})


function updateNoteStatus() {
  const csfr = document.querySelector('[name=csrfmiddlewaretoken]').value
  let save_button = document.getElementById('model_save_btn')
  let url = save_button.getAttribute('data-section_url')
  let approval_status = document.querySelector('input[name="approval_status"]:checked').value

  let body = JSON.stringify({
    approval_status: approval_status
  })

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
          let section = document.getElementById('section_status_' + data['section_id'])
          const statusStyles = ['status_info_primary', 'status_info_warning', 'status_info_success']
          let currentStyleClass = statusStyles.some(removeSectionApprovalStyle)
          
          function removeSectionApprovalStyle(value) {
            section.classList.remove(value) 
          }
          
          section.innerHTML = data['approval_status']
          section.classList.remove(currentStyleClass)
          section.classList.add(data['info_status_css'])

          let close_btn = document.getElementById("modal_close_btn");
          close_btn.click();
      })
      .catch(error => {
          console.log(error)
      })
}