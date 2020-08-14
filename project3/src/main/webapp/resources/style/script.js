var msg_id = "아이디를 입력하세요.!!";
var msg_pwd = "비밀번호를 입력하세요.";
var msg_pwdChk = "비밀번호가 일치하지않습니다.";
var msg_name = "이름을 입력하세요.";
var msg_email1 = "이메일을 입력하세요.";
var msg_email2 = "이메일 형식이올바르지않습니다.";
var msg_confirmId = "중복 확인해주세요";
var msg_hp = "전화번호를 입력하세요!";
var msg_adress = "주소를 바르게 입력해주세요!";
var msg_snadress = "도로명주소를 입력해주세요!";

var insertError = "회원가입에 실패했습니다.\n확인후 다시 시도하세요.!!"
var updateError = "회원정보수정에 실패했습니다.\n확인후 다시 시도하세요.!!";
var deleteError = "회원탈퇴에 실패했습니다.\n확인후 다시 시도하세요.!!"
var passwdError = "입력하신 비밀번호가 일치하지 않습니다.\n확인후 다시 시도하세요";

//재고관리 에러
var updateError2 = "재고수정 실패. 확인후 다시 시도하세요";
var insertError2 = "재고추가 실패. 확인후 다시 시도하세요 ";
var deleteError2 = "재고삭제 실패. 확인후 다시 시도하세요";

//장바구니 에러
var insertError3 = "장바구니추가 실패. 확인후 다시 시도하세요 ";
var deleteError3 = "장바구니삭제 실패. 확인후 다시 시도하세요 ";
//매니저 로그인 에러
var loginErrror = "없는아이디입니다. 확인후 다시 시도하세요 ";

var refundError="환불실패하였습니다. 화인후 다시 시도하세요";

var deleteMemberError="회원 삭제에 실패하였습니다.";
//에러 메시지
function errorAlert(errorMsg){
	alert(errorMsg);
	//이전 페이지로 이동
	window.history.back(); //이전 페이지로 이동
}

//구매에러
var insertError4 = "구매실패 다시시도해주세요";
//회원가입창
function signInCheck(){
	if(!document.signInform.id.value){
		alert(msg_id);
		document.signInform.id.focus();
		return false;
	}
	if(!document.signInform.pwd.value){
		alert(msg_pwd);
		document.signInform.pwd.focus();
		return false;
	}
	if(document.signInform.repwd.value != document.signInform.pwd.value){
		alert(msg_pwdChk);
		document.signInform.repwd.value="";
		document.signInform.repwd.focus();
		return false;
	}
	if(!document.signInform.name.value){
		alert(msg_name);
		document.signInform.name.focus();
		return false;
	}
	if(!document.signInform.hp1.value){
		alert(msg_hp);
		document.signInform.hp1.focus();
		return false;
	}
	if(!document.signInform.hp2.value){
		alert(msg_hp);
		document.signInform.hp2.focus();
		return false;
	}
	if(!document.signInform.hp3.value){
		alert(msg_hp);
		document.signInform.hp3.focus();
		return false;
	}
	if(!document.signInform.address1.value){
		alert(msg_adress);
		document.signInform.address1.focus();
		return false;
	}
	if(!document.signInform.address2.value){
		alert(msg_adress);
		document.signInform.address2.focus();
		return false;
	}
	if(!document.signInform.address3.value){
		alert(msg_adress);
		document.signInform.address3.focus();
		return false;
	}
	//중복확인 버튼을 클릭하지 않는 경우
	//hiddenId : 중복화인 버튼 클릭여부 체크(0:클릭 안함 , 1:클릭함)
	//먼저 <input type ="hidden" name="hiddenId" value="0">
	if(document.signInform.hiddenId.value == "0"){
		alert(msg_confirmId);
		document.signInform.dupChk.focus();
		return false;
	}
	
}
function loginCheck1(){
	if(!document.loginform.id.value){
		alert("아이디를 입력해주세요");
		document.loginform.id.focus();
		return false;
	}
	if(!document.loginform.pwd.value){
		alert("비밀번호를 입력해주세요");
		document.loginform.pwd.focus();
		return false;
	}
}
//중복확인 
function confirmId(){
	//id값 미입력시 
	if(!document.signInform.id.value){
		alert(msg_id);
		document.signInform.id.focus();
		return false;
	}
		var url="confirmId?id=" + document.signInform.id.value;
		window.open(url,"confirmId","menubar=no,width=350,height=200");
}
//이메일 변경 
function selectemailChk(){
	//직접 입력 - email2 값초기화
	if(document.signInform.email3.value == "0"){
		document.signInform.email2.value ="";
	}else{
		//직접입력이 아닌경우 select borx의 값(email3)을 email2의 값으로 설정
		document.signInform.email2.value = document.signInform.email3.value;
	}
}
//opener : window 객체의 open() 메소드로 열린 새창(=중복확인창)에서
//열어준 부모창(=회원가입창)에 접근할 때 사용
//self.close(); 메시지 없이 현재창을 닫을 때사용
function setId(id){
	opener.document.signInform.id.value = id;
	opener.document.signInform.hiddenId.value= 1; //부모쪽에다가
	self.close();// 내창 닫기
}

//중복확인 아이디 체크
function confirmIdFocus(){
	document.confirmform.id.focus();
}

function confirmIdCheck(){
	if(!document.confirmform.id.value){
		alert(msg_id);
		document.confirmform.id.focus();
		return false;
	}
}

function loginChk(){
	alert("로그인이필요한페이지입니다.");
	window.location="login";
	return false;
}


function nextHp1(){
	if(document.signInform.hp1.value.length >= 3){
		document.signInform.hp2.focus();
	}
}
function nextHp2(){
	if(document.signInform.hp2.value.length >= 4){
		document.signInform.hp3.focus();
	}
}
function nextHp3(){
	if(document.signInform.hp3.value.length >= 4){
		document.signInform.email1.focus();
	}
}
//주소찾기 서비스
function addressSearch(){
    new daum.Postcode({
        oncomplete: function(data) {
            // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분입니다.
            var fullAddr = '';
            var extraAddr = '';
            
            if(data.userSelectedType === 'R'){
            	fullAddr = data.roadAddress;
            }else{
            	fullAddr = data.jibunAddress;
            }
            
            if(data.userSelectedType === 'R'){
            	if(data.bname !== ''){
            		extraAddr += data.bname;
            	}
            	
            	if(data.buildingName !== ''){
            		extraAddr += (extraAddr !== '' ? ',' + data.buildingName : data.buildingName);
            	}
            	fullAddr += (extraAddr !== '' ? '('+ extraAddr +')' : '');
            }
            
            document.getElementById('sample6_postcode').value = data.zonecode;
            document.getElementById('sample6_address').value = fullAddr;
            
            document.getElementById('sample6_address2').focus();
        }
    }).open();
}
function mypageformFocus(){
	document.mypageform.pwd.focus();
}
function mypageformCheck(){
	//비밀번호 재입력 값 다를시 알림
	if(document.mypageform.repwd.value != document.mypageform.pwd.value){
		alert(msg_pwdChk);
		document.mypageform.repwd.value="";
		document.mypageform.repwd.focus();
		return false;
	}
	//이메일 형식 불일치
	if(document.mypageform.email1.value != ""){
		if(!document.mypageform.email2.value && document.mypageform.email3.value == 0){
			alert(msg_email2);
			document.mypageform.email2.focus();
		}
	}
	if(!document.signInform.pwd.value){
		alert(msg_pwd);
		document.signInform.pwd.focus();
		return false;
	}
	if(document.signInform.repwd.value != document.signInform.pwd.value){
		alert(msg_pwdChk);
		document.signInform.repwd.value="";
		document.signInform.repwd.focus();
		return false;
	}
	
}
function nextHp11(){
	if(document.mypageform.hp1.value.length >= 3){
		document.mypageform.hp2.focus();
	}
}
function nextHp22(){
	if(document.mypageform.hp2.value.length >= 4){
		document.mypageform.hp3.focus();
	}
}
function nextHp33(){
	if(document.mypageform.hp3.value.length >= 4){
		document.mypageform.email1.focus();
	}
}
function mypageform_selectemailChk(){
	if(document.mypageform.email3.value == "0"){
		document.mypageform.email2.value ="";
	}else{
		document.mypageform.email2.value = document.mypageform.email3.value;
	}
}
function leaveformCheck(){
	if(!document.leaveform.id.value){
		alert(msg_id);
		document.leaveform.id.focus();
		return false;
	}
	if(!document.leaveform.pwd.value){
		alert(msg_pwd);
		document.leaveform.pwd.focus();
		return false;
	}
}

function mailchk(){
	window.open("chkemail","chkemail","menubar=no,width=350,height=200");
}

function pwdchk(){
	if(document.pwdchk.repwd.value != document.pwdchk.pwd.value){
		alert(msg_pwdChk);
		document.signInform.repwd.value="";
		document.signInform.repwd.focus();
		return false;
	}	
}


