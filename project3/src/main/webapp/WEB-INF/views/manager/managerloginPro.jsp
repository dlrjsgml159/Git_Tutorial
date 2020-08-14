<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>        
<html>
<body>
	<!-- 로그인 실패 -->
	<c:if test="${selectCnt == 0}">
		<script type="text/javascript">
			errorAlert(loginErrror);
		</script>
	</c:if>
	<!-- 비밀번호 불일치 -->
	<c:if test="${selectCnt == -1}">
		<script type="text/javascript">
			errorAlert(msg_pwdChk);
		</script>
	</c:if>
	<!-- 글쓰기 성공 -->
	<c:if test="${selectCnt == 1}">
		<script type="text/javascript">
			alert("어서오십시오 관리자님.");
			window.location="inventory_management"; /* ?pageNum=${pageNum} */
		</script>
	</c:if>
</body>
</html>