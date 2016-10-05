/*(function($) {
	
	$(document).ready(function() {
		//$('#id_string_id').after('<button>generate id</button>')
		$('#id_recording_date').change(function(){
			generate_string_id()
			});
		$('#id_to_speakers').change(function(){
			generate_string_id()
			});
			
		//$().
		//<input type="checkbox" name="rename_files" value="Bike">
	});
	
	function generate_string_id() {
		var date_str = $('#id_recording_date').val().replace(/\-/g, '');
		var speaker_str = get_speaker_str($('#id_to_speakers :selected').text());
		if (speaker_str != '' && date_str != '') {
			//$('#id_string_id').val(date_str + '_' + speaker_str);
			ajax_request('string_id_update', {'date' : date_str, 'speaker' : speaker_str});
		};
	};
	
	function set_string_id(string_id) {
		$('#id_string_id').val(string_id);
	};
	
	function get_speaker_str(speaker_raw_str) {
		var speaker_str = ''
		for (var i = 0, len = speaker_raw_str.length; i < len; i++) {
			if (speaker_raw_str[i] == speaker_raw_str[i].toUpperCase() && speaker_raw_str[i].match(/[^\- .,_]/)){
				speaker_str += speaker_raw_str[i];
			};
		};
		return speaker_str
	};
	
	function ajax_request(req_type, req_data){
	
		$.ajax({  //Call ajax function sending the option loaded
			url: "/admin/corpora/recording/ajax/",  //This is the url of the ajax view where you make the search 
			//contentType: "application/json; charset=utf-8",
			type: 'POST',
			data: {'request_type' : req_type, 'request_data' : req_data, 'modelID' : $(location).attr('href').split('/').reverse()[2]},
			timeout: 50000,
			error: function(x, t, m) {
				console.log(x, t, m);
			},
			success: function(response) {
				result = $.parseJSON(response);  // Get the results sended from ajax to here
				if (result.error) { // If the function fails
					console.log(result.error_text); // Error to log
				} else {
					set_string_id(result.result);
				}
			}
	});
	};
		
})(django.jQuery);*/