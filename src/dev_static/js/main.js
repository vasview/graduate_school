setTimeout(function () {
    const alertList = document.querySelectorAll('.alert_close_btn')
    alertList.forEach(function (alert) {
      alert.click()
    })
}, 5000);