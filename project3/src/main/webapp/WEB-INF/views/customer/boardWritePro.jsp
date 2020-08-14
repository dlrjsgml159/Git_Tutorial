<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>       
<html>
<body>

	<h2 align="center"> 글쓰기 - 처리페이지 </h2>
	
	<!-- 글쓰기 실패 -->
	<c:if test="${insertCnt == 0}">
		<script type="text/javascript">
			errorAlert(insertError);
		</script>
	</c:if>
	
	<c:if test="${insertCnt != 0}">
		<script type="text/javascript">
			alert("글이작성되었습니다.");
			window.location="board?pageNum=${pageNum}";
		</script>
	</c:if>
</body>
</html>