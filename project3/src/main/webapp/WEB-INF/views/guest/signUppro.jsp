<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>        
<!DOCTYPE html>
<html>
<body>
	<!-- 회원가입 실패 -->
	<c:if test="${insertCnt == 0}">
		<script type="text/javascript">
			errorAlert(insertError);
		</script>
	</c:if>
	<!-- 회원가입 성공시 -->
	<c:if test="${insertCnt != 0}">
		<script type="text/javascript">
			alert("회원가입 에성공 하였습니다.");
		</script>
		<c:redirect url="main"/>
	</c:if>
</body>
</html>