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
	<form action="${path}pwdchange" method="get" name="pwdchk">
	<input type="hidden" name="id" value="${id}"/>
	<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
		<input type="text" name="pwd">
		<input type="text" name="repwd">
		<input type="submit" name="변경완료" onclick="pwdchk();">
	</form>
	</c:if>
	<c:if test="${cnt == 0}">
		<script type="text/javascript">
			alert("코드번호가 틀립니다.");
			window.location("chkemail");
		</script>
	</c:if>
</body>
</html>