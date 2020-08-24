/*
 +--------------------------------------------------------------------------------------------------+
 |	SNUH(서울대학교병원 프로젝트) 자바스크립트 컴포넌트													|
 +--------------------------------------------------------------------------------------------------+
 |																									|
 |	버전 	: v1.0.0																				|
 |	목록 	: getUUID																				|
 |			  isArrayLike																			|
 | 			  isFileApiSupport																		|
 | 			  optional																				|
 | 			  escapeSelector																		|
 |	      	  alignListIndex																		|
 |	      	  selectChain																			|
 |	      	  ajaxSelectChain																		|
 |	      	  ajaxChain																				|
 |			  maxlength																				|
 |			  enhancedSubmit																		|
 |			  getLength																				|
 |			  previewImage																			|
 |			  pagerBuilder																			|
 |																									|
 |	의존성	: "jquery": ">= 1.12.4"																	|
 |																									|
 |	개정이력																							|
 |		- 2017-05-26 최초 생성																		|
 |																									|
 |																		created by PCN (2017-05-26)	|
 +--------------------------------------------------------------------------------------------------+
*/

/*
	getUUID
	
	타입: function 타입
	설명: UUID 생성
*/
function getUUID() {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
		var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
		return v.toString(16);
	});
}

/*
	isArrayLike

	타입: function 타입
	설명: Array 타입으로 변환이 가능한 속성을 모두 가지고 있는지 확인
*/
function isArrayLike(arr) {

	if (typeof arr !== 'object' || jQuery.isWindow(arr)) {
		return false;
	}

	var length = !!arr && "length" in arr && arr.length,
		type = jQuery.type(arr);

	return type === "array" || length === 0 ||
		typeof length === "number" && length > 0 && (length - 1) in arr;
}


/*
	isFileApiSupport
	타입: function 타입
	설명: 해당 브라우저에서 FILE API를 지원하는지 확인
*/
var isFileApiSupport = (function() {
	
	var __currentBrowser;
	
	function isFileApiSupport() {
		if (__currentBrowser === undefined) {
			var fileApiProps = ['File', 'FileReader', 'FileList', 'Blob'];
			for (var i in fileApiProps) {
				if (!(fileApiProps[i] in window)) {
					return (__currentBrowser = false);
				}
			}
			return (__currentBrowser = true);
		}
		else {
			return __currentBrowser;
		}
	}
	
	return isFileApiSupport;
	
})();

/*
	optional

	타입: object 타입
	설명: optional design pattern
*/
var optional = (function() {

	var CONST_EMPTY_OPTIONAL_FACTOR = 'CONST_EMPTY_OPTIONAL_FACTOR', 
		CONST_EMPTY_OPTIONAL, 
		CONST_FN_EXTEND, 
		CONST_STR_EXTEND, 
		CONST_OBJ_EXTEND, 
		CONST_ARR_EXTEND, 
		CONST_FILE_EXTEND, 
		optionalFactors;

	function resolveFallback(fallback) {
		if (typeof fallback === 'object' && typeof fallback['provide'] === 'function') {
			return fallback['provide'].call(null);
		}
		if (!!fallback) {
			return fallback
		}
		else {
			throw new Error('incorrect value');
		}
	}

	function findOptionalFactor(value) {
		for (var name in optionalFactors) {
			if (optionalFactors[name].validate(value)) {
				return optionalFactors[name];
			}
		}
		return CONST_EMPTY_OPTIONAL_FACTOR;
	}

	function makeOptional(value, optionalFactor) {

		if (CONST_EMPTY_OPTIONAL_FACTOR === optionalFactor) {
			return CONST_EMPTY_OPTIONAL;
		}

		var __correct = optionalFactor.validate(value);
		var __value = __correct ? optionalFactor.resolveValue(value) : value;

		var optional = {
			'get': function() {
				if (__correct) {
					return __value;
				}
				else if (arguments[0]) {
					return resolveFallback(arguments[0]);
				}
				else {
					throw optionalFactor.error();
				}
			}, 
			'ifCorrect': function(consumer) {
				if (__correct) {
					consumer.call(this, __value);
				}
			}, 
			'isCorrect': function() {
				return __correct;
			}, 
			'map': function(mapper) {
				if (__correct) {
					var result = mapper.call(this, __value);
					return makeOptional(result, findOptionalFactor(result));
				}
				return optionalFactor.extend(CONST_EMPTY_OPTIONAL);
			}, 
			'filter': function(filter) {
				if (__correct) {
					var filtered = filter.call(this, __value);
					if (filtered) {
						return makeOptional(__value, optionalFactor);
					}
				}
				return optionalFactor.extend(CONST_EMPTY_OPTIONAL);
			}, 
			'getOrError': function(error) {
				if (__correct) {
					return __value;
				}
				if (typeof error === 'function') {
					error = error.call(value);
				}
				throw error || optionalFactor.error();
			}
		};

		return optionalFactor.extend(optional);
	}

	CONST_EMPTY_OPTIONAL = {
		'get': function() {
			if (arguments[0]) {
				return resolveFallback(arguments[0]);
			}
			else {
				throw new Error('empty');
			}
		}, 
		'ifCorrect': function(consumer) {
			//do nothing..
		}, 
		'isCorrect': function() {
			return false;
		}, 
		'map': function(mapper) {
			return this;
		}, 
		'filter': function(filter) {
			return this;
		}, 
		'getOrError': function() {
			throw new Error('empty');
		}
	};

	CONST_FN_EXTEND = {
		'call': function() {
			var result;
			var args = [].slice.call(arguments);
			this.ifCorrect(function(fn) {
				result = fn.call.apply(fn, args);
			});
			return makeOptional(result, findOptionalFactor(result));
		}, 
		'apply': function() {
			var result;
			var context = arguments[0];
			var args = arguments[1];
			this.ifCorrect(function(fn) {
				result = fn.apply(context, args);
			});
			return makeOptional(result, findOptionalFactor(result));
		}, 
		'bind': function() {
			var result;
			var args = [].slice.call(arguments);
			this.ifCorrect(function(fn) {
				result = fn.bind.apply(fn, args);
			});
			return makeOptional(result, findOptionalFactor(result));
		}
	};

	CONST_STR_EXTEND = {
		'hasText': function() {
			return this.filter(function(str) {
				return str.trim().length > 0;
			});
		}, 
		'getOrEmptyString': function() {
			if (this.isCorrect()) {
				return this.get();
			}
			else {
				return '';
			}
		}
	};

	CONST_OBJ_EXTEND = {
		'requireProperty': function() {
			var propertyNames = isArrayLike(arguments[0]) ? arguments[0] : [].slice.call(arguments);
			return this.filter(function(obj) {
				for (var i in propertyNames) {
					if (!(propertyNames[i] in obj)) {
						return false;
					}
				}
				return true;
			});
		}, 
		'getProperty': function(propertyName) {
			var value = this.get();
			var result = value[propertyName];
			return makeOptional(result, findOptionalFactor(result));
		}
	};

	CONST_ARR_EXTEND = {
		'notEmpty': function() {
			return this.filter(function(arr) {
				return arr.length > 0;
			});
		}, 
		'filterArr': function(filterer) {
			var result;
			this.ifCorrect(function(arr) {
				if (typeof arr.filter === 'function') {
					result = arr.filter.call(arr, filterer);
				}
				else {
					result = [];
					for (var i = 0; i < arr.length; i++) {
						if (filterer.call(arr, arr[i], i, arr)) {
							result.push(arr[i]);
						}
					}
				}
			});
			return optional.arr(result);
		}, 
		'mapArr': function(mapper) {
			var result;
			this.ifCorrect(function(arr) {
				if (typeof arr.map === 'function') {
					result = arr.map.call(arr, mapper);
				}
				else {
					result = [];
					for (var i = 0; i < arr.length; i++) {
						result.push(mapper.call(arr, arr[i], i, arr));
					}
				}
			});
			return optional.arr(result);
		},
		'reduce': function(reducer) {
			var reduction;
			this.ifCorrect(function(arr) {
				if (typeof arr.reduce === 'function') {
					reduction = arr.reduce.call(arr, reducer);
				}
				else {
					reduction = arr[0];
					for (var i = 1; i < arr.length; i++) {
						reduction = reducer.call(arr, reduction, arr[i], i, arr);
					}
				}
			});
			return makeOptional(reduction, findOptionalFactor(reduction));
		}, 
		'some': function(predicate) {
			var result;
			this.ifCorrect(function(arr) {
				if (typeof arr.some === 'function') {
					result = arr.some.call(arr, predicate);
				}
				else {
					for (var i = 0; i < arr.length; i++) {
						if (predicate.call(arr, arr[i], i, arr)) {
							result = true;
							return;
						}
					}
					result = false;
				}
			});
			return result;
		}, 
		'every': function(predicate) {
			var result;
			this.ifCorrect(function(arr) {
				if (typeof arr.every === 'function') {
					result = arr.every.call(arr, predicate);
				}
				else {
					for (var i = 0; i < arr.length; i++) {
						if (!predicate.call(arr, arr[i], i, arr)) {
							result = false;
							return;
						}
					}
					result = true;
				}
			});
			return result;
		}, 
		'sort': function(sorter) {
			var sorted;
			this.ifCorrect(function(arr) {
				sorted = arr.sort.call(arr, sorter);
			});
			return optional.arr(sorted);
		}, 
		'forEach': function(consumer) {
			this.ifCorrect(function(arr) {
				if (typeof arr.forEach === 'function') {
				arr.forEach.call(arr, consumer);
				}
				else {
					for (var i = 0; i < arr.length; i++) {
						consumer.call(arr, arr[i], i, arr);
					}
				}
			});
		}, 
		'slice': function(start, end) {
			var slicedArr;
			this.ifCorrect(function(arr) {
				if (start >= 0) {
					slicedArr = arr.slice(start, end);
				}
			});
			return optional.arr(slicedArr);
		}
	};

	CONST_FILE_EXTEND = {
		'ext': function(exts, blackList) {
			return this.filter(function(file) {
				var index = file.name.lastIndexOf('.') + 1;
				var fileExt = optional.str(file.name.substring(index)).map(function(v) {
					return v.toLowerCase();
				}).getOrEmptyString();
				var predicate = function(ext) {
					var cmpExt = optional.str(ext).map(function(v) {
						return v.toLowerCase();
					}).getOrEmptyString();
					return cmpExt === fileExt;
				};

				if (blackList === true) {
					return !optional.arr(exts).some(predicate);
				}
				else {
					if (fileExt.length > 0) {
						return optional.arr(exts).some(predicate);
					}
					else {
						return false;
					}
				}
			});
		}, 
		'limitSize': function(limitSize) {
			return this.filter(function(file) {
				return file.size <= limitSize;
			});
		}
	};

	optionalFactors = {
		'fn': {
			'validate': function(fn) {
				return typeof fn === 'function';
			}, 
			'resolveValue': function(v) {
				return v;
			}, 
			'extend': function(optional) {
				return $.extend(optional, CONST_FN_EXTEND);
			}, 
			'error': function() {
				return new TypeError('value is not a function');
			}
		}, 
		'str': {
			'validate': function(str) {
				return typeof str === 'string';
			}, 
			'resolveValue': function(v) {
				return v;
			}, 
			'extend': function(optional) {
				return $.extend(optional, CONST_STR_EXTEND);
			}, 
			'error': function() {
				return new TypeError('value is not a string');
			}
		}, 
		'arr': {
			'validate': function(arr) {
				return isArrayLike(arr);
			}, 
			'resolveValue': function(v) {
				return [].slice.call(v);
			}, 
			'extend': function(optional) {
				return $.extend(optional, CONST_ARR_EXTEND);
			}, 
			'error': function() {
				return new TypeError('value is not a like array object');
			}
		}, 
		'obj': {
			'validate': function(obj) {
				return obj !== null && typeof obj === 'object';
			}, 
			'resolveValue': function(v) {
				return v;
			}, 
			'extend': function(optional) {
				return $.extend(optional, CONST_OBJ_EXTEND);
			}, 
			'error': function() {
				return new TypeError('value is not valid object');
			}
		}, 
		'bool': {
			'validate': function(bool) {
				return (typeof bool === 'boolean') || 
					(typeof bool === 'string' && (bool === 'true' || bool === 'false'));
			}, 
			'resolveValue': function(v) {
				if (typeof v === 'string') {
					if (v === 'true') {
						return true;
					}
					if (v === 'false') {
						return false;
					}
				}
				else {
					return v;
				}
			}, 
			'extend': function(optional) {
				return optional;
			}, 
			'error': function() {
				return new TypeError('value is not a boolean');
			}
		}, 
		'num': {
			'validate': function(num) {
				return !isNaN(num);
			}, 
			'resolveValue': function(v) {
				if (typeof v === 'number') {
					return v;
				}
				return parseFloat(v);
			}, 
			'extend': function(optional) {
				return optional;
			}, 
			'error': function() {
				return new TypeError('value is not a number');
			}
		}
	};
	
	if (isFileApiSupport()) {
		optionalFactors.file = {
			'validate': function(file) {
				return file instanceof File;
			}, 
			'resolveValue': function(v) {
				return v;
			}, 
			'extend': function(optional) {
				return $.extend(optional, CONST_FILE_EXTEND);
			}, 
			'error': function() {
				return new Error('value is not a instance of File');
			}
		};
	}

	return {
		'fn': function(fn) {
			return makeOptional(fn, optionalFactors['fn']);
		}, 
		'str': function(str) {
			return makeOptional(str, optionalFactors['str']);
		}, 
		'arr': function(arr) {
			return makeOptional(arr, optionalFactors['arr']);
		}, 
		'obj': function(obj) {
			return makeOptional(obj, optionalFactors['obj']);
		}, 
		'bool': function(bool) {
			return makeOptional(bool, optionalFactors['bool']);
		}, 
		'num': function(num) {
			return makeOptional(num, optionalFactors['num']);
		}, 
		'file': function(file) {
			return makeOptional(file, optionalFactors['file']);
		}
	};
})();

/*
	escapeSelector

	타입: function 타입
	설명: 특수문자를 escape 처리하여 jquery 사용 시 오류를 제거
*/
function escapeSelector(selector) {
	if (optional.str(selector).isCorrect()) {
		var escaped = selector.replace(/[\s\!"#\$%&'\(\)\*\+,.\/\:;<=>\?@\[\]\^`\{\|\}\~]/g, '\\$&');
		return escaped;
	}
	else {
		return selector;
	}
}




/*
	selectChain

	타입: function 타입
	설명: 여러 select node 들이 순차적으로 값이 변경되어야 하는 경우 target select node가 변경된 값에 
		  따라 ajax 호출을 통해 영향을 받는 selec node의 option node 들이 변경되는 로직을 구현 할 때 
		  boilerplate한 code들을 정의 하여 손쉽게 구현 할 수 있도록 도와주는 helper class component
	메소드 목록
		- add		: selectInfo 객체를 추가
		- addAll	: 다수의 selectInfo 객체를 추가
		- chaining	: 등록된 selectInfo 목록 정보를 바탕으로 이벤트 연결

	object 명세 목록
		1. [selectInfo 명세]
		- eventTarget: 값이 변경되면 reloadTarget select node가 변경
		- reloadTarget: 영향을 받아서 option node 들이 재 구성되는 select node DOM 객체
		- optionsProvider: select node에서 선택된 값에 해당하는 option node list 를 제공

	예제
		var optionsProvider = function(targetValue) {
			if (targetValue) {
				var options = [];
				... some logic ...
				return options;
			}
			else {
				return '<option value="">선택</option>';
			}
		};
		var selectInfoList = [...some select info list...];
		selectChain().addAll(selectInfoList).chaning();
*/
var selectChain = (function() {

	var CONST_SELECT_INFO = ['eventTarget', 'reloadTarget', 'optionsProvider'];

	function onChange(selectInfo) {
		return function() {
			var reloadTarget = selectInfo.reloadTarget;
			var optionsProvider = selectInfo.optionsProvider;
			var options = optionsProvider.call(this, this.value);
			$(reloadTarget).empty().append(options).trigger('change');
		};
	}

	function selectChain() {

		var __selectInfoList = [];

		return {
			'add': function(pSelectInfo) {
				var selectInfo = optional.obj(pSelectInfo).requireProperty(CONST_SELECT_INFO).get();
				__selectInfoList.push(selectInfo);
				return this;
			}, 
			'addAll': function(selectInfoList) {
				var thisSelectChain = this;
				optional.arr(selectInfoList).notEmpty().forEach(function(selectInfo) {
					thisSelectChain.add(selectInfo);
				});
				return this;
			},
			'chaining': function() {
				for (var i in __selectInfoList) {
					var selectInfo = __selectInfoList[i];
					var eventTarget = selectInfo.eventTarget;
					$(eventTarget).change(onChange(selectInfo));
				}
			}
		};
	}

	return selectChain;

})();

/*
 	alignListIndex
 	
 	타입: function 타입
 	설명: Spring form 의 form control 중 List 객체에 바인딩 되는 항목들에 대한 index 정리
*/
function alignListIndex(targetList, listName, startIndex) {
	var addNumber = 0;
	optional.arr(targetList).slice(startIndex).forEach(function(target) {
		var currentIndex = startIndex + addNumber;
		$(target).find('[name^=' + escapeSelector(listName) + ']').each(function() {
			var name = $(this).attr('name');
			var propertyName = name.substring(name.lastIndexOf('.') + 1);
			var newId = listName + currentIndex + '.' + propertyName;
			var newName = listName + '[' + currentIndex + '].' + propertyName;
			$(this).attr({'id': newId, 'name': newName});
		});
		addNumber++;
	});
}

/*
	ajaxSelectChain

	타입: function 타입
	설명: 여러 select node 들이 순차적으로 값이 변경되어야 하는 경우 target select node가 변경된 값에 
		  따라 ajax 호출을 통해 영향을 받는 selec node의 option node 들이 변경되는 로직을 구현 할 때 
		  boilerplate한 code들을 정의 하여 손쉽게 구현 할 수 있도록 도와주는 helper class component
	메소드 목록
		- add		: ajaxSelectInfo 객체를 추가
		- addAll	: 다수의 ajaxSelectInfo 객체를 추가
		- chaining	: 등록된 ajaxSelectInfo 목록 정보를 바탕으로 이벤트 연결

	object 명세 목록
		[ajaxInfo 명세]
		- url: ajax 요청 url
		- paramName: ajax 요청 parameter 이름
		- data: ajax 요청 추가 데이터 (필수 X)
		- optionsMapper: ajax 요청으로 내려받은 response data를 이용해 option node list를 생성 (필수 X)
		- success: reload 완료 후 실행

	예제
		var ajaxInfo = {
			'url': 'http://ajax.test.com/select/option', 
			'paramName': 'id', 
			'data': {
				'name': 'jacknie',
				'number': 10
			}, 
			'optionsMapper': response => {
				return JSON.parse(response).map(o => '<option value=' + o.value + '>' + o.label + '</option>');
			}
		};

		ajaxSelectChain(ajaxInfo).add({
			'eventTarget': $('#select1').get(0), 
			'defaultOption': '<option value="">선택</option>'
		}).add({
			'eventTarget': $('#select2').get(0), 
			'defaultOption': '<option value="">선택</option>',
			'ajaxInfo': {
				'url': '다른걸로 바꿈'
			}
		}).chaining();
*/
var ajaxSelectChain = (function() {

	var defaultOptionsMapper = function(r) {
		return r;
	};
	
	function getData(ajaxSelectInfo, data) {
		var bind = ajaxSelectInfo;
		while (!!bind) {
			var paramName = bind.paramName;
			var value = $(bind.eventTarget).val();
			data[paramName] = value;
			bind = bind.prev;
		}
		return data;
	}

	function onChange(ajaxSelectInfo, defaultAjaxInfo) {
		var reloadTarget = ajaxSelectInfo.next.eventTarget;
		var defaultOption = ajaxSelectInfo.next.defaultOption || '<option value="">선택</option>';
		var paramName = ajaxSelectInfo.paramName || defaultAjaxInfo.paramName;
		
		return function() {
			var selectValue = optional.str(this.value).getOrEmptyString();
			if (selectValue.length > 0) {
				var url = defaultAjaxInfo.url;
				var data = getData(ajaxSelectInfo, $.extend(true, {}, defaultAjaxInfo.data));
				$(reloadTarget).prop('disabled', true);
				$.get(url, data, function(response) {
					var optionsMapper = optional.fn(defaultAjaxInfo.optionsMapper).get(defaultOptionsMapper);
					var options = optional.str(response).map(optionsMapper).get();
					var cloneDefaultOption = $(defaultOption).clone();
					$(reloadTarget).empty().append(options).prepend(cloneDefaultOption);
					$(cloneDefaultOption).prop('selected', true);
					optional.fn(defaultAjaxInfo.success).call(reloadTarget, cloneDefaultOption);
					$(reloadTarget).prop('disabled', false);
				});
			}
			else {
				var cloneDefaultOption = $(defaultOption).clone();
				$(reloadTarget).empty().prepend(cloneDefaultOption).trigger('change');
			}
		};
	}

	function ajaxSelectChain(defaultAjaxInfo) {
		var __ajaxSelectInfoList = [];
		var __defaultAjaxInfo = optional.obj(defaultAjaxInfo).get({});

		return {
			'add': function(eventTarget, paramName, defaultOption) {
				var ajaxSelectInfo = {
					'eventTarget': eventTarget, 
					'defaultOption': defaultOption, 
					'paramName': paramName
				};
				__ajaxSelectInfoList.push(ajaxSelectInfo);
				return this;
			}, 
			'addAll': function(pAjaxSelectInfoList) {
				var thisAjaxSelectChain = this;
				optional.arr(pAjaxSelectInfoList).notEmpty().forEach(function(ajaxSelectInfo) {
					thisAjaxSelectChain.add(ajaxSelectInfo);
				});
				return this;
			}, 
			'chaining': function() {
				var lastIndex = __ajaxSelectInfoList.length - 1;
				for (var i = 0; i < lastIndex; i++) {
					var ajaxSelectInfo = __ajaxSelectInfoList[i];
					ajaxSelectInfo.prev = __ajaxSelectInfoList[i - 1];
					ajaxSelectInfo.next = __ajaxSelectInfoList[i + 1];
					$(ajaxSelectInfo.eventTarget).change(onChange(ajaxSelectInfo, __defaultAjaxInfo));
				}
			}
		};
	}

	return ajaxSelectChain;

})();

/*
	ajaxChain
	
	타입: jQuery Plugin 타입
	설명: ajaxSelectChain을 쉽게 사용하기 위해 제작
*/
$.fn.ajaxChain = function(ajaxInfo, paramName) {
	
	var ajaxChain = ajaxSelectChain(ajaxInfo).add(this.get(0), paramName);
	
	return {
		'add': function(selector, paramName, defaultOption) {
			ajaxChain.add($(selector).get(0), paramName, defaultOption);
			return this;
		}, 
		'activate': function(selector, defaultOption) {
			ajaxChain.add($(selector).get(0), '', defaultOption).chaining();
		}
	};
};


/*
	maxlength

	타입: jQuery Plugin 타입
	설명: 입력할 수 있는 문자열의 maxlength 설정. 
*/
$.fn.maxlength = function(maxLength, overflowHandler) {

	var __maxLength = optional.num(maxLength).get();

	(function($context) {

		$context.keypress(function(event) {
			var key = event.which;
			if(key >= 33 || key == 13 || key == 32) {
				var length = getLength(this.value);
				if (length > __maxLength) {
					optional.fn(overflowHandler).call(this, event);
					event.preventDefault();
				}
			}
		});

		$context.keyup(function(event) {
			var key = event.which;
			if(key >= 33 || key == 13 || key == 32) {
				var length = getLength(this.value);
				if (length > __maxLength) {
					optional.fn(overflowHandler).call(this, event);
					var value = this.value;
					var newValue = value.substring(0, __maxLength);
					$(this).val(newValue);
				}
			}
		});

	})(this);

	return this;
};

/*
	enhancedSubmit

	타입: jQuery Plugin 타입
	설명: 향상된 submit 이벤트 리스너. 
		  자바스크립트 에러가 발생하면 submit을 중단 시키고 로그
		  done 함수를 boolean 타입의 변수와 함께 실행 시켰을때 boolean 값이 true 면 전송하고 false 면 전송중단.
*/
$.fn.enhancedSubmit = function(eventListener) {
	
	(function($form){
		var breakId;
		
		var done = function(submit, errorMsg) {
			if (submit) {
				$form.off('submit', wrapEventListener).submit();
			}
			else {
				breakId = getUUID();
				var e =  new Error(errorMsg);
				e.name = breakId;
				throw e;
			}
		};
		
		var wrapEventListener = function(event) {
			event.preventDefault();
			try {
				optional.fn(eventListener).call($form.get(0), event, done);
			} catch (e) {
				if (e.name === breakId) {
					breakId = undefined;
				}
				else if (optional.fn(console.error).isCorrect()) {
					console.error(e);
				}
				else {
					console.log(e);
				}
			}
		};
		
		$form.submit(wrapEventListener);
	})(this);
}

/*
	getLength

	타입: function 타입
	설명: 입력된 문자열의 길이 값을 반환, byte 길이 값도 반환 가능
*/
function getLength(string, byteLength) {
	var presentString = optional.str(string).getOrEmptyString();
	if (byteLength && presentString.length > 0) {
		return presentString.replace(/[\0-\x7f]|([0-\u07ff]|(.))/g, "$&$1$2").length;
	}
	else {
		return presentString.length;
	}
}

/*
	previewImage
	
	타입: function 타입
	설명: 입력된 file 타입의 input node DOM 객체를 입력하게 되면 FILE API 지원 유무와 상관없이 
		  image 파일 미리보기
		  
	mataData 객체 명세
		- uploadUrl				: upload service url
		- uploadFileInputName	: upload server 에 전송 될 input name
		- uploadCheckUrl 		: upload 완료 check service url
		- imgSrc				: image 미리보기 주소
		- accessKey				: cache key
*/
var previewImage = (function() {
	
	var __imgLoadIdleTime = 500;
	var __metaDataUrl = '/metaData';
	var __accessKeyHandler = function(accessKey) {};
	
	function previewImage(input, targetImg) {
		if (isFileApiSupport()) {
			if (input.files && input.files[0]) {
				var reader = new FileReader();
				reader.onload = function(e) {
					$(targetImg).attr('src', e.target.result);
				};
				reader.readAsDataURL(input.files[0]);
			}
		}
		else {			
			$.getJSON(__metaDataUrl, function(metaData) {
				
				var uuid = getUUID();
				var iframeContainerId = 'iframeContainer_' + uuid;
				var iframeName = 'iframe_' + uuid;
				var uploadFormId = 'form_' + uuid;
				var uploadUrl = optional.str(metaData.uploadUrl).get();
				var uploadFileInputName = optional.str(metaData.uploadFileInputName).get();
				var uploadCheckUrl = optional.str(metaData.uploadCheckUrl).get();
				var imgSrc = optional.str(metaData.imgSrc).get();
				var accessKey = optional.str(metaData.accessKey).get();
				
				$('body').append([
					'<div id="', iframeContainerId, '" style="display: none;">', 
						'<iframe name="', iframeName, '"></iframe>', 
						'<form id="' + uploadFormId + '" action="', uploadUrl, '" target="', iframeName, '" method="post" enctype="multipart/form-data">', 
							'<input type="hidden" name="accessKey" value="', accessKey, '" />', 
							'<input type="submit" />', 
						'</form>', 
					'<div>'
				].join(''));
				
				var orgInputName = $(input).attr('name');
				$(input).attr('name', uploadFileInputName);
				$('#' + uploadFormId).append(input).submit().submit().submit();
				
				var uploadCheckInterval = setInterval(function() {
					$.get(uploadCheckUrl, function() {
						$(targetImg).attr('src', imgSrc);
						$('#' + iframeContainerId).remove();
						__accessKeyHandler.call(null, accessKey);
						clearInterval(uploadCheckInterval);
					});
				}, __imgLoadIdleTime);
			});
		}
	}
	
	previewImage.setImgLoadIdleTime = function(imgLoadIdleTime) {
		__imgLoadIdleTime = optional.num(imgLoadIdleTime).get();
	}
	
	previewImage.setMetaDataUrl = function(metaDataUrl) {
		__metaDataUrl = optional.str(metaDataUrl).get();
	}
	
	previewImage.setAccessKeyHandler = function(accessKeyHandler) {
		__accessKeyHandler = optional.fn(accessKeyHandler).get();
	}
	
	return previewImage;
	
})();

/*
	pagerBuilder

	타입: function 타입
	설명: 더 보기 버튼 기능을 수행 할수 있는 pager 객체 생성 builder
	예제
		var pager = pagerBuilder().pagination(43, 'page').ifNoNextPage(function() {
			$('#btnMore').remove();	
		}).build();

		$('#btnMore').click(function() {
			pager.nextPage('/list/nextPage').then(function(response) {
				$('#listContainer').append(response);
			}, function(jqXHR, textStatus, errorThrown) {
				console.error(jqXHR, textStatus, errorThrown);
			});
		});
*/
var pagerBuilder = (function() {

	function createPager(builderMemento) {

		var pagination = builderMemento.pagination;
		var hasNextPageHandler = builderMemento.hasNextPageHandler;
		var noNextPageHandler = builderMemento.noNextPageHandler;
		var hasPrevPageHandler = builderMemento.hasPrevPageHandler;
		var noPrevPageHandler = builderMemento.noPrevPageHandler;

		return {
			'loadPage': function(url, page, data) {
				var paramName = pagination.getPageParamName();
				data = optional.obj(data).get({});
				data[paramName] = page;
				var beforePage = pagination.setCurrentpage(page)

				return {
					'then': function(success, reject) {
						$.get(url, data).then(function() {
							optional.fn(success).apply(this, arguments);
							if (beforePage < page) {
								if (!pagination.hasNextPage()) {
									optional.fn(noNextPageHandler).call(this, pagination);
								}
								optional.fn(hasPrevPageHandler).call(this, pagination);
							}
							else {
								if (!pagination.hasPrevPage()) {
									optional.fn(noPrevPageHandler).call(this, pagination);
								}
								optional.fn(hasNextPageHandler).call(this, pagination);
							}
							
						}, function() {
							pagination.setCurrentpage(beforePage);
							optional.fn(reject).apply(this, arguments);
						});
					}
				};
			},
			'nextPage': function(url, data) {
				if (pagination.hasNextPage()) {
					return this.loadPage(url, pagination.nextPage(), data);
				}
				throw new Error('out of page');
			}, 
			'prevPage': function(url, data) {
				if (pagination.hasPrevPage()) {
					return this.loadPage(url, pagination.prevPage(), data);
				}
				throw new Error('out of page');
			},
			'getPagination': function() {
				return $.extend({}, pagination);
			}
		};
	}

	function pagerBuilder() {

		var __pagination, 				// page 매김 처리
			__hasNextPageHandler, 		// 다음 페이지가 있는 경우 실행 되는 handler
			__noNextPageHandler, 		// 다음 페이지가 없는 경우 실행 되는 handler
			__hasPrevPageHandler,		// 이전 페이지가 있는 경우 실행 되는 handler
			__noPrevPageHandler; 		// 이전 페이지가 없는 경우 실행 되는 handler

		function invalidPage(page) {
			return new Error('invalid page[' + page + ']');
		}

		return {
			'pagination': function(totalRecordCount, pageParamName, rowsPerPage, page) {
				var __page = optional.num(page).get(1);
				var __rowsPerPage = optional.num(rowsPerPage).get(10);
				var __totalRecordCount = optional.num(totalRecordCount).get();
				var __totalPageSize = Math.floor(__totalRecordCount / __rowsPerPage) + 1;
				var __pageParamName = optional.str(pageParamName).hasText().get();

				__pagination = {
					'setCurrentpage': function(page) {
						var beforePage = __page;
						__page = optional.num(page).getOrError(invalidPage);
						if (__page > __totalPageSize || __page < 1) {
							__page = beforePage;
							throw invalidPage(__page);
						}
						return beforePage;
					},
					'getCurrentPage': function() {
						return __page;
					}, 
					'getPageParamName': function() {
						return __pageParamName;
					}, 
					'nextPage': function() {
						if (this.hasNextPage()) {
							return __page + 1;
						}
						throw new Error('out of page{totalPageSize: ' + __totalPageSize + ', currentPage: ' + __page + '}');
					}, 
					'hasNextPage': function() {
						return __page < __totalPageSize;
					}, 
					'prevPage': function() {
						if (this.hasPrevPage()) {
							return __page - 1;
						}
						throw new Error('out of page{currentPage: ' + __page + '}');
					}, 
					'hasPrevPage': function() {
						return __page > 1;
					}, 
					'getLastPage': function() {
						return __totalPageSize;
					}, 
					'toString': function() {
						return JSON.stringify({
							'currentPage': __page, 
							'pageParamName': __pageParamName, 
							'rowsPerPage': __rowsPerPage, 
							'totalRecordCount': __totalRecordCount, 
							'totalPageSize': __totalPageSize
						});
					}
				};
				return this;
			},
			'ifNoNextPage': function(noNextPageHandler) {
				__noNextPageHandler = optional.fn(noNextPageHandler).get();
				return this;
			}, 
			'ifHasNextPage': function(hasNextPageHandler) {
				__hasNextPageHandler = optional.fn(hasNextPageHandler).get();
				return this;
			},
			'ifNoPrevPage': function(noPrevPageHandler) {
				__noPrevPageHandler = optional.fn(noPrevPageHandler).get();
				return this;
			}, 
			'ifHasPrevPage': function(hasPrevPageHandler) {
				__hasPrevPageHandler = optional.fn(hasPrevPageHandler).get();
				return this;
			}, 
			'build': function() {
				return createPager({
					'pagination': __pagination,
					'hasNextPageHandler': __hasNextPageHandler,
					'noNextPageHandler': __noNextPageHandler,
					'hasPrevPageHandler': __hasPrevPageHandler,
					'noPrevPageHandler': __noPrevPageHandler
				});
			}
		};
	}

	return pagerBuilder;

})();