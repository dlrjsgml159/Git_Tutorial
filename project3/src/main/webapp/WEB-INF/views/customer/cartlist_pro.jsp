<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>       
<html>
<body>
	<c:if test="${insertCnt == 0}">
		<script type="text/javascript">
			errorAlert(insertError3);
		</script>	
	</c:if>
	
	<c:if test="${insertCnt != 0}">
		<script type="text/javascript">
			alert("장바구니에 추가되었습니다.");
			window.location="cartlist";
		</script>
	</c:if>
</body>
</html>