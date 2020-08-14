<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    <%@ include file="/resources/style/setting.jsp" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
</head>
<body>
	<c:if test="${cnt == 1}">
	<form action="${path}pwdChk" method="get" name="email">
		<input type="hidden" name="codes" value="${key}"/>
		<input type="hidden" name="id" value="${id}"/>
		<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
		인증 코드 : <input type="text" name="code">
		<input type="submit" name="확인">
	</form>
	</c:if>
	<c:if test="${cnt == 0}">
		<script type="text/javascript">
			alert("등록되지않은 메일입니다.");
			window.history.back();
		</script>
	</c:if>
	
</body>
</html>