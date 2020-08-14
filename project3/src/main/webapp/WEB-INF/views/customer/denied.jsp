<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<%@ include file="/resources/style/setting.jsp" %>    
<meta charset="UTF-8">

<!-- 3초 지나면 해당 url 즉 home으로 이동 -->
<meta http-equiv="refresh" content="3, ${path}">
</head>
<body>
	<p>${errMsg}</p>
</body>
</html>