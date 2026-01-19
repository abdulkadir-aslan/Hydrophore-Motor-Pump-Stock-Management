$(function () {
    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-book").modal("show");
        },
        success:  function (data) {
          if (data.form_close) {
            window.location.reload()
            // $("#book-table tbody").html(data.html_book_list);  // <-- Replace the table body
            $("#modal-book").modal("hide");
          }
          else {
            $("#modal-book .modal-content").html(data.html_form);
          }

          
        }
        
      });
    };
  
    function loadUpdateForm(book_id) {
      var data_url = "/books/"+book_id+"/update/";
      var btn = $(this);
      $.ajax({
        url: data_url,
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-book").modal("show");
        },
        success: function (data) {
          $("#modal-book .modal-content").html(data.html_form);
        }
      });
    }
  
    var saveCreateFormAndUpdate = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            loadUpdateForm(data.book_id);
          }
          else {
            $("#modal-book .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
    var saveForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            window.location.reload()
            // $("#book-table tbody").html(data.html_book_list);  // <-- Replace the table body
            $("#modal-book").modal("hide");  // <-- Close the modal
          }
          else {
            $("#modal-book .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
    // Create book
    $(".js-create-book").click(loadForm);
    $("#modal-book").on("submit", ".js-book-create-form", saveCreateFormAndUpdate);
  
    // Update book
    $("#book-table").on("click", ".js-update-book", loadForm);
    $("#modal-book").on("submit", ".js-book-update-form", saveForm);
  
    // Delete book
    $("#book-table").on("click", ".js-delete-book", loadForm);
    $("#modal-book").on("submit", ".js-book-delete-form", saveForm);
  
  });
  