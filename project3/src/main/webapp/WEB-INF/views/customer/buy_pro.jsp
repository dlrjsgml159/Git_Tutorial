<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>    
<html>
<body>
	<c:if test="${insertCnt == 0}">
		<script type="text/javascript">
			errorAlert(insertError4);
		</script>
	</c:if>
	<c:if test="${insertCnt != 0}">
		<script type="text/javascript">
			alert("구매해주셔서 감사합니다.");
			window.location="${path}order";
		</script>
	</c:if>
</body>
</html>