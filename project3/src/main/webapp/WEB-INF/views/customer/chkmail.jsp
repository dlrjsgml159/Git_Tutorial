<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<body onload="confirmIdFocus();">
	<h2>중복확인 페이지</h2>
<form action="${path}confirmId" method="post" name="confirmform"
		onsubmit="confirmIdCheck();">
	<!-- id 중복 -->
	<c:if test="${cnt == 0}">
		
	</c:if>
	<c:if test="${cnt != 0}">
	</c:if>
</form>
</body>
</html>