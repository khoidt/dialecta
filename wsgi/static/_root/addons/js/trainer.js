(function($) {
	
	var processing_request = false;
	function ajax_request(req_type, req_data){
		//var text_id = window.location.pathname;
		if (processing_request == true) {
			console.log('processing previous request, please wait'); // Error to log
			return false;
		};
		processing_request = true;
		$.ajax({  //Call ajax function sending the option loaded
			url: "../../ajax/",  //This is the url of the ajax view where you make the search 
			//contentType: "application/json; charset=utf-8",
			type: 'POST',
			data: {'request_type' : req_type, 'request_data' : req_data},
			timeout: 50000,
			error: function(x, t, m) {
				console.log(x, t, m);
				processing_request = false;
			},
			success: function(response) {
				result = $.parseJSON(response);  // Get the results sended from ajax to here
				processing_request = false
				if (result.error) { // If the function fails
					console.log(result.error_text); // Error to log
				} else {
					if (req_type == 'training_data_load_req') {
						var training_dict = result['training_dict'];
						console.log(training_dict);
						return training_dict;
						//var exceptions_arr = result.exceptions_arr;
					}
					if (req_type == 'trt_annot_req') {
						suggestions_lst = result.result
						//console.log(suggestions_lst);
						if (suggestions_lst !== undefined) {
							$('#rus_normalization_input').val(suggestions_lst[0][0]);
						}
					}
				}
			}
		});
	};
	
	function nextInDOM(_selector, _subject) {
		var next = getNext(_subject);
		while(next.length != 0) {
			var found = searchFor(_selector, next);
			if(found != null) return found;
			next = getNext(next);
		}
		return null;
	};
	function getNext(_subject) {
		if(_subject.next().length > 0) return _subject.next();
		return getNext(_subject.parent());
	};
	function searchFor(_selector, _subject) {
		if(_subject.is(_selector)) return _subject;
		else {
			var found = null;
			_subject.children().each(function() {
				found = searchFor(_selector, $(this));
				if(found != null) return false;
			});
			return found;
		}
		return null; // will/should never get here
	};
	
	function activateTrainingExample(training_dict, except_arr) {
		
		//console.log('looking for next example');
		if (!document.getElementById("training_example")) {
			var next_valid_trt = $('.annot_wrapper').first().find('trt:first');
		}
		else {
			//console.log($('trt#training_example').text());
			var next_valid_trt = nextInDOM('trt', $('trt#training_example'));
		};
		activateTRT(next_valid_trt, training_dict, except_arr);
	};
	
	function activateTRT(trt_tag, training_dict, except_arr) {
		
		$('trt#training_example').removeAttr('id');
		trt_tag.attr('id', 'training_example');
		if (!training_dict[trt_tag.text()] && except_arr.indexOf(trt_tag.text())==-1) {
			$('trt.focused').removeClass('focused');
			trt_tag.addClass('focused');
			activateContext($('trt.focused').closest('.annot_wrapper'));
			ajax_request('trt_annot_req', {'trt' : trt_tag.text(),});
		}
		else {
			activateTrainingExample(training_dict, except_arr);
		}
	};
	
	function activateContext(context_tag) {
		$('.active_annot_t').css('display', 'none');
		$('.active_annot_t').removeClass('active_annot_t');
		//fragment.css({'display':'block', 'position': 'fixed', 'padding-top': '15%', 'padding-left': '3%','opacity':0.5});
		context_tag.addClass('active_annot_t');
		context_tag.css('display', 'inline-flex');
	};
	
	$(document).ready(function() {
		$('.annot_wrapper').css('display', 'none');
		$('.participant').css('display', 'none');
		$('nrm').css('display', 'none');
		$('lemma').css('display', 'none');
		$('morph').css('display', 'none');
		$('token').css('margin', '20pt');
		$('trt').css({'font-size': '300%', 'font-color':'grey',});
		$('tech').css({'font-size': '300%'});
		//$('button').css({'width': '500%', 'height': '500%'});
		
		var training_dict = $('#examples').data('dictionary');
		var except_arr = $('#exceptions').data('array');
		$('#counter_status').text(Object.keys(training_dict).length);
		activateTrainingExample(training_dict, except_arr);
		
		$('#skipbutton').click(function(e) {
			except_arr.push($('trt.focused').text());
			//console.log(except_arr);
			activateTrainingExample(training_dict, except_arr)
		});
		$('#addbutton').click(function(e) {
			//console.log('trying to save examples');
			var values = [$('#bel_normalization_input').val(), $('#rus_normalization_input').val()];
			training_dict[$('trt.focused').text()] = values;
			$('#counter_status').text(Object.keys(training_dict).length);
			//console.log(training_dict);
			activateTrainingExample(training_dict, except_arr);
		});
		$('#savebutton').click(function(e) {
			ajax_request('save_model_req', {'trd' : JSON.stringify(training_dict), 'exr' : JSON.stringify(except_arr),});
		});
	});
})(django.jQuery);













