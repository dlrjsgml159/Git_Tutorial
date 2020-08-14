<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    <%@ include file="/resources/style/setting.jsp" %>    
<html>
<body>
	<h2><center> 글 삭제 </center></h2>
	<!-- 비밀번호 일치 -->
	<c:if test="${selectCnt == 1}">
		<!-- 삭제 실패 -->
		<c:if test="${deleteCnt == 0}">
			<script type="text/javascript">
				errorAlert(deleteError);
			</script>
		</c:if>
		<!-- 삭제  성공-->
		<c:if test="${deleteCnt != 0}">
			<script type="text/javascript">
				alert("글이삭제되었습니다.!!");
				window.location='board?pageNum=${pageNum}';
			</script>
		</c:if>
	</c:if>
	<!-- 비밀번호 불일치 -->
	<c:if test="${selectCnt != 1}">
		<script type="text/javascript">
			errorAlert(pwdError);
		</script>
	</c:if>
</body>
</html>