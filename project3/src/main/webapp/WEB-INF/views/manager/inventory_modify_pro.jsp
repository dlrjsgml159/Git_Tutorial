<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>       
<html>
<body>
	<!-- 글쓰기 실패 -->
	<c:if test="${updateCnt == 0}">
		<script type="text/javascript">
			errorAlert(updateError2);
		</script>
	</c:if>
	<!-- 글쓰기 성공 -->
	<c:if test="${updateCnt != 0}">
		<script type="text/javascript">
			alert("수정되었습니다.");
			window.location="inventory_management"; /* ?pageNum=${pageNum} */
		</script>
	</c:if>
</body>
</html>