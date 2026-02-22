document.addEventListener("DOMContentLoaded", function () {

  const modalElement = document.getElementById("modal-book");
  const modal = new bootstrap.Modal(modalElement);

  // Edit butonuna tıklama
  document.addEventListener("click", function (e) {
    const button = e.target.closest(".js-update-book");
    if (!button) return;

    const url = button.getAttribute("data-url");

    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
    .then(response => response.json())
    .then(data => {
      modalElement.querySelector(".modal-content").innerHTML = data.html_form;
      modal.show();
    })
    .catch(() => {
      alert("Form yüklenirken hata oluştu.");
    });
  });

  // Modal içindeki form submit
  // modalElement.addEventListener("submit", function (e) {
  //   if (!e.target.classList.contains("js-book-update-form")) return;

  //   e.preventDefault();

  //   const form = e.target;
  //   const formData = new FormData(form);

  //   fetch(form.action, {
  //     method: "POST",
  //     body: formData,
  //     headers: {
  //       "X-Requested-With": "XMLHttpRequest"
  //     }
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     if (data.form_is_valid) {
  //       modal.hide();
  //       window.location.reload();
  //     } else {
  //       modalElement.querySelector(".modal-content").innerHTML = data.html_form;
  //     }
  //   })
  //   .catch(() => {
  //     alert("Kaydetme sırasında hata oluştu.");
  //   });
  // });

});

document.addEventListener("DOMContentLoaded", function () {
  // Geri git butonuna tıklama
  document.addEventListener("click", function (e) {
    const backButton = e.target.closest(".js-go-back");
    if (!backButton) return;

    // Yönlendirme yapılacak URL'yi al
    const url = backButton.getAttribute("data-href");
    if (confirm("Bu İş Emri Önceki Adıma Dönecek Onaylıyormusunuz!")) {
      // Yönlendirme işlemini gerçekleştir
      window.location.href = url;
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Geri git butonuna tıklama
  document.addEventListener("click", function (e) {
    const backButton = e.target.closest(".js-delete");
    if (!backButton) return;

    // Yönlendirme yapılacak URL'yi al
    const url = backButton.getAttribute("data-href");
    if (confirm("Bu kaydı silmek istediğinizden emin misiniz?")) {
      // Yönlendirme işlemini gerçekleştir
      window.location.href = url;
    }
  });
});