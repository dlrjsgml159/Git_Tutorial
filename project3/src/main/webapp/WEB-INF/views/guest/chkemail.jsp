<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    <%@ include file="/resources/style/setting.jsp" %>       
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
	<form action="${path}pwdchkemail" method="get" name="emailchk">
	<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
		<input type="text"name="id" maxlength="20" placeholder="아이디">
		<br>
		<input type="text"name="email1" maxlength="10" placeholder="이메일">
	    			 @<input type="text"  name="email2" maxlength="20" placeholder="ex) OOOO.com">
	    			<select name="email3" onchange="selectemailChk();" style="width:100px; height:30px;">
	    				<option value="0">직접입력</option>
	    				<option value="naver.com">네이버</option>
	    				<option value="gmail.com">구글</option>
	    				<option value="nate.com">네이트</option>
	    				<option value="daum.net">다음</option>
	    			</select>
	    			<br>
		<input type="submit" value="확인">
		<input type="button" value="취소" onclick="self.close();">
	</form>
</body>
</html>