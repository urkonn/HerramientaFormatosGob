var typeFile;
$("#feedback").hide();
checkVisible();

function iconType(el) {
  typeFile = el.getAttribute("data-type");
  $("input[name=format_to]").val(typeFile);
  $(".icon").removeClass("button-higlight");
  $(el).addClass("button-higlight");
  $( "#submitButton" ).prop( "disabled", false );
};

function disabledElementsFalse(){
  $( ".icon-disabled" ).prop( "disabled", false );
  $( ".disabled-elem" ).removeClass( "opacity-text" );
  $( ".icon-select" ).removeClass( "icon-disabled" ).addClass( "icon" ).attr("onclick","iconType(this);");
};
function checkVisible(){
  if ( $('.dz-file-preview').length ) {
    //$( "#submitButton" ).prop( "disabled", false );
    $( ".disabled-elem" ).removeClass( "opacity-text" );
    $( ".icon-disabled" ).prop( "disabled", false );
    $( ".icon-select" ).removeClass("icon-disabled").addClass('icon');
  } else {
    $( "#submitButton" ).prop( "disabled", true );
    $( ".disabled-elem" ).addClass( "opacity-text" );
    $( ".icon-select" ).addClass( "icon-disabled" ).removeAttr("onclick").removeClass("button-higlight");
    $( ".icon-disabled" ).prop( "disabled", true );
  }
}

// Dropzone
Dropzone.autoDiscover = false;

var dropzone = new Dropzone('#my-awesome-dropzone', {
  //previewTemplate: document.querySelector('#preview-template').innerHTML,
  // The configuration we've talked about above
  acceptedFiles: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel",
  url: '.',
  autoProcessQueue: false,
  uploadMultiple: false,
  paramName: 'xls_file',
  maxFiles: 1,
  parallelUploads: 1,
  thumbnailHeight: 120,
  thumbnailWidth: 120,
  maxFilesize: 10000,
  filesizeBase: 1000,
  hiddenInputContainer: "#myform",
  dictFallbackMessage: "Tu navegador no soporta 'drag and drop' para subir archivos.",
  dictFileTooBig: "El tamaño del archivo es muy grande: ({{filesize}}Mb). Máximo permitido: {{maxFilesize}}Mb.",
  dictInvalidFileType: "Tipo de archivo no permitido.",
  dictResponseError: "Respuesta del servidor: {{statusCode}}.",
  dictCancelUpload: "Cancelar",
  dictCancelUploadConfirmation: "¿Quieres cancelar el envío del archivo?",
  dictMaxFilesExceeded: "No puedes subir más archivos.",

  // The setting up of the dropzone
  init: function() {
    var myDropzone = this;
    this.on("maxfilesexceeded", function(file) {
      this.removeAllFiles();
      this.addFile(file);
    });

    this.on("addedfile", function(file) {
      var _this = this;
      // Create the remove button
      var removeButton = Dropzone.createElement("<a href='javascript:void(0)' id='remove-button'>Eliminar archivo</a>");

      // Listen to the click event
      removeButton.addEventListener("click", function(e) {
        // Make sure the button click doesn't submit the form:
        e.preventDefault();
        e.stopPropagation();

        // Remove the file preview.
        _this.removeFile(file);
        // If you want to the delete the file on the server as well,
        // you can do the AJAX request here.
        checkVisible();
      });

      // Add the button to the file preview element.
      file.previewElement.appendChild(removeButton);
    });

    this.on('sending', function(file, xhr, formData){
      formData.append('format_to', $("input[name=format_to]").val());
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    });

    var interval_id = null,
        link_interval = null,
        count_error = 0;

    function progress_show(){
      $.post(link_interval).success(function(response){
          if(response.status === 'PROGRESS'){
            $('.percent').find('h4').html("% " + response.progress.current.toString())
          } else if (response.status === 'SUCCESS'){
            swal({
              confirmButtonText: "DESCARGAR",
              title: "Éxito",
              text: "Archivo convertido correctamente",
              type: "success" },
            function(){
              window.open(response.link,'_blank');
            });
            $('.loading-document').css('display', 'none');
            clearInterval(interval_id);
          } else if (response.status === 'ERROR'){
            count_error ++;
            if (count_error > 3){
              clearInterval(interval_id);
              swal({
              confirmButtonText: "OK",
              title: "Error",
              text: response.error,
              type: "error" });
              $('.loading-document').css('display', 'none');
            }
          }
      });
    }


    this.on("success", function(file, response, e) {
      if(response.status === 'ok'){
        link_interval = response.link
        $('.percent').find('h4').html("% 0")
        interval_id = setInterval(progress_show, 1000)
      }

      if(response.status === 'error'){
        swal({
          confirmButtonText: "OK",
          title: "Error",
          text: response.error,
          type: "error" }); 
      }

      $("#feedback").hide();
      myDropzone.removeFile(file);
      checkVisible();
    });

    // First change the button to actually tell Dropzone to process the queue.
    //this.element.querySelector("button[type=submit]").addEventListener("click", function(e) {
    $('#submitButton').on("click", function(e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();
      myDropzone.processQueue();
      $("#feedback").show().text("Por favor espera... Tu documento está siendo analizado y transformado");
      $("#remove-button").hide();
      $('.loading-document').css('display', 'block');
    });

  },

  thumbnail: function(file, dataUrl) {
    if (file.previewElement) {
      file.previewElement.classList.remove("dz-file-preview");
      var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
      for (var i = 0; i < images.length; i++) {
        var thumbnailElement = images[i];
        thumbnailElement.alt = file.name;
        thumbnailElement.src = dataUrl;
      }
      setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
    }
  }

});

$(function(){
    jQuery('img.svg').each(function(){
        var $img = jQuery(this);
        var imgID = $img.attr('id');
        var imgClass = $img.attr('class');
        var imgURL = $img.attr('src');

        jQuery.get(imgURL, function(data) {
            // Get the SVG tag, ignore the rest
            var $svg = jQuery(data).find('svg');
            // Add replaced image's ID to the new SVG
            if(typeof imgID !== 'undefined') {
                $svg = $svg.attr('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if(typeof imgClass !== 'undefined') {
                $svg = $svg.attr('class', imgClass+' replaced-svg');
            }
            // Remove any invalid XML tags as per http://validator.w3.org
            $svg = $svg.removeAttr('xmlns:a');
            // Check if the viewport is set, else we gonna set it if we can.
            if(!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
                $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
            }
            // Replace image with new SVG
            $img.replaceWith($svg);
        }, 'xml');
    });
});