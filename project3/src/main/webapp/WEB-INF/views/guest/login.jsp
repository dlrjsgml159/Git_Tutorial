<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>       
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/login.css">
    <meta charset="utf-8" />
<script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
<script type ="text/javascript">
$(document).ready(function(){
    // 저장된 쿠키값을 가져와서 ID 칸에 넣어준다. 없으면 공백으로 들어감.
    var userInputId = getCookie("userInputId");
    $("input[id='label_id']").val(userInputId); 
     
    if($("input[id='label_id']").val() != ""){ 
       // 그 전에 ID를 저장해서 처음 페이지 로딩 시, 입력 칸에 저장된 ID가 표시된 상태라면,
        $("#remember").attr("checked", true); // ID 저장하기를 체크 상태로 두기.
    }
     
    $("#remember").change(function(){ // 체크박스에 변화가 있다면,
        if($("#remember").is(":checked")){ // ID 저장하기 체크했을 때,
            var userInputId = $("input[id='label_id']").val();
            setCookie("userInputId", userInputId, 7); // 7일 동안 쿠키 보관
        }else{ // ID 저장하기 체크 해제 시,
            deleteCookie("userInputId");
        }
    });
     
    // ID 저장하기를 체크한 상태에서 ID를 입력하는 경우, 이럴 때도 쿠키 저장.
    $("input[id='label_id']").keyup(function(){ // ID 입력 칸에 ID를 입력할 때,
        if($("#remember").is(":checked")){ // ID 저장하기를 체크한 상태라면,
            var userInputId = $("input[id='label_id']").val();
            setCookie("userInputId", userInputId, 7); // 7일 동안 쿠키 보관
        }
    });
 
    //쿠키를 위한 함수 
    function setCookie(cookieName, value, exdays){
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + exdays);
        var cookieValue = escape(value) + ((exdays==null)?"":";expires="+exdate.toGMTString());
        document.cookie = cookieName + "=" + cookieValue;
    }
     
    function deleteCookie(cookieName){
        var expireDate = new Date();
        expireDate.setDate(expireDate.getDate() - 1);
        document.cookie = cookieName + "= " + "; expires=" + expireDate.toGMTString();
    }
     
    function getCookie(cookieName) {
        cookieName = cookieName + '=';
        var cookieData = document.cookie;
        var start = cookieData.indexOf(cookieName);
        var cookieValue = '';
        if(start != -1){
            start += cookieName.length;
            var end = cookieData.indexOf(';', start);
            if(end == -1)end = cookieData.length;
            cookieValue = cookieData.substring(start, end);
        }
        return unescape(cookieValue);
    }
    
});
	
</script>
</head>
<body onload="document.signIn.userID.focus();">
    <header>
        <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="${path}login" >로그인</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="${path}main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas" >회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" onclick="return loginChk();">자유게시판</a></td>
                <td><a href="${path}customer/consulting" onclick="return loginChk();">문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if>    
    <!-- 로그인 성공 -->
    <c:if test="${sessionScope.memId != null}">
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : ${sessionScope.memId}</li>
                <li><a href="${path}logout" >로그아웃</a></li>
                <li><a href="${path}customer/mypage">내정보</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="${path}main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas">회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" >자유게시판</a></td>
                <td><a href="${path}customer/consulting" >문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if> 
    </header>
    <form name="loginform" action="${path}login_check" method="post" onsubmit ="return loginCheck();">
    	<input type ="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
		<fieldset>
			<legend>로그인</legend>
			<table >
				<tr>
					<td align="center"><input type="text" class="idpwd" id="label_id" name="id" width=40px; height=30px; placeholder="아이디" autofocus ></td>
					<td rowspan="2"><input type="submit" class="button" value="로그인 "></td>
				</tr>
				<tr>
					<td align="center"><input type="password" class="idpwd" id="label_pwd" name="pwd" size=40px; placeholder="패스워드" autofocus ></td>
				</tr>
				<tr>
					<td>
						<a href="${path}signUp">회원가입</a>  |  id 저장<input type="checkbox" id="remember" ><a href="#" onclick="mailchk();">비밀번호 찾기</a>
					</td>
				</tr>
			</table>
		</fieldset>
	</form>
    <footer>
        <div class="office_adress">
               <pre>
사업자등록번호 : 000-00-00000 
대표이사 : 이건희 
주소 : 서울특별시 O구 OO로 OOO번길
이메일 : gunhee260@gmail.com
		</pre>
		<ul>
			<li></li>
		</ul>
		<pre>
제품이나 사이트 이용에 궁금증을 바로 해결하시려면, 1234-5678 으로 전화하세요.
상담 가능 시간 평일 10:00 - 18:00
        </pre>
        </div>
    </footer>
</body>
</html>