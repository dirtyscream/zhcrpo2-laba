jQuery(document).ready(function() {

    jQuery("html").on("dragover", function(e) {
        e.preventDefault();
        e.stopPropagation();
        jQuery('.upload_area_text').html('Drop here');
    });
    
    jQuery(document).on("dragleave", function(e) {
        if((e.target.localName == 'html' || e.target.localName == 'main') && e.originalEvent.screenX == 0 && e.originalEvent.screenY == 0) {
            e.preventDefault();
            e.stopPropagation();
            jQuery('.upload_area_text').html('Choose file or drag&drop');
        }
    });

    jQuery("html").on("drop", function(e) {
        e.preventDefault();
        e.stopPropagation();
        jQuery('.upload_area_text').html('Choose file or drag&drop');
    });

    jQuery('.upload_area').on('dragenter', function(e) {
        e.stopPropagation();
        e.preventDefault();
        jQuery('.upload_area_text').html('Drop');
    });

    jQuery('.upload_area').on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
        jQuery('.upload_area_text').html('Drop');
    });

    jQuery('.upload_area').on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
        let list = new DataTransfer();
        let file = new File([e.originalEvent.dataTransfer.files[0]], e.originalEvent.dataTransfer.files[0].name);
        list.items.add(file);
        jQuery("#uploadfile").prop("files", list.files);
        jQuery('.chosen_file').html(e.originalEvent.dataTransfer.files[0].name);
        jQuery('.upload_area_text').html('Choose file or drag&drop');
    });

    jQuery('#uploadfile').on('change', function(element) {
		jQuery('.chosen_file').html(element.target.files[0].name);
	});

	const uploadForm = document.getElementById('upload_form');
    const input_file = document.getElementById('uploadfile');
    const progress_bar = document.getElementById('progress');

    jQuery("#upload_form").submit(function(e){
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        const media_data = input_file.files[0];
        // if(media_data.size > 4 * 1024 * 1024) {
        //     input_file.value = "";
        //     jQuery('.chosen_file').html('<span style="color: red;">max file size 4MB</span>');
        //     setTimeout(function() {
        //         jQuery('.chosen_file').empty();
        //     }, 5000);
        //     return;
        // }
        if(media_data != null){
            //console.log(media_data);
            jQuery('.header .progress').css('display', 'flex');
        }
        jQuery('#uploadbutton').prop("disabled", true);

        jQuery.ajax({
            type: 'POST',
            url:'/drive/upload',
            data: formData,
            beforeSend: function() {},
            xhr:function() {
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', e => {
                    if(e.lengthComputable){
                        const percentProgress = ((e.loaded/e.total)*100 / 2).toFixed(2);
//                        console.log(percentProgress);
                        jQuery('.header .progress').attr('aria-valuenow', percentProgress);
                        jQuery('.header .progress-bar').css('width', percentProgress + '%');
                        jQuery('.header .progress-bar').html(percentProgress + '%');
                    }
                });
                return xhr
            },
            success: function(response) {
                location.reload();
                //console.log(response);
            },
            error: function(err) {
                //console.log(err);
            },
            xhrFields: {
                onprogress: function(e) {
                    let response = e.currentTarget.response;
                    let arr = response.split(" ");
                    let percentProgress = (parseFloat(arr[arr.length - 2]) + 50).toFixed(2);
                    jQuery('.header .progress').attr('aria-valuenow', percentProgress);
                    jQuery('.header .progress-bar').css('width', percentProgress + '%');
                    jQuery('.header .progress-bar').html(percentProgress + '%');
                }
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });

    jQuery('#pin-tab').on('click', function(e) {
        e.preventDefault();
        jQuery('#drive-tab-pane').removeClass('show active');
        jQuery('#pin-tab-pane').addClass('show active');
        jQuery('#drive-tab-pane').css('display','none');
        jQuery('#pin-tab-pane').css('display','inline');
        jQuery('#drive-tab').removeClass('active');
        jQuery('#pin-tab').addClass('active');
        localStorage.setItem('currentPage', 1);
    });

    jQuery('#drive-tab').on('click', function(e) {
        e.preventDefault();
        jQuery('#drive-tab-pane').addClass('show active');
        jQuery('#pin-tab-pane').removeClass('show active');
        jQuery('#drive-tab-pane').css('display','inline');
        jQuery('#pin-tab-pane').css('display','none');
        jQuery('#drive-tab').addClass('active');
        jQuery('#pin-tab').removeClass('active');
        localStorage.setItem('currentPage', 0);
    });

    let savedPage = localStorage.getItem('currentPage');

    if(savedPage) {
        if(savedPage == 1) {
            jQuery('#drive-tab-pane').removeClass('show active');
            jQuery('#pin-tab-pane').addClass('show active');
            jQuery('#drive-tab-pane').css('display','none');
            jQuery('#pin-tab-pane').css('display','inline');
            jQuery('#drive-tab').removeClass('active');
            jQuery('#pin-tab').addClass('active');
        }
    }

    jQuery('.delete_file_req').on('click', function() {
        jQuery.ajax({
            type: 'GET',
            url: jQuery(this).attr('value'),
            data: {"1dbfb090cac3446b9fa93805f3a694f0":198190},
            success: function(response) {
                location.reload();
                //console.log(response);
            },
            error: function(err) {
                //console.log(err);
            },
        });
    });
    jQuery('.delete_pin_req').on('click', function() {
        jQuery.ajax({
            type: 'GET',
            url: jQuery(this).attr('value'),
            data: {"93c5272130ea44dba67e8dcc0107b8f7":14583209},
            success: function(response) {
                location.reload();
                //console.log(response);
            },
            error: function(err) {
                //console.log(err);
            },
        });
    });
    $('#create_pin').on('click', function() {
        window.location.href = '/pin/create';
    });
});