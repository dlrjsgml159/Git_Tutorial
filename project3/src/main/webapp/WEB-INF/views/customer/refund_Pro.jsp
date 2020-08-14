<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>       
<html>
<body>
	<c:if test="${insertCnt == 0}">
		<script type="text/javascript">
			errorAlert(refundError);
		</script>
	</c:if>
	<c:if test="${insertCnt != 0}">
		<script type="text/javascript">
			alert("환불처리 되었습니다.");
			window.location="mypage-orderlist";
		</script>
	</c:if>
</body>
</html>