<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
  <%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<script src="${path}script.js"></script>
<body>
	<!-- 아이디와 비밀번호가 일치 -->
	<c:if test="${selectCnt == 2}">
		<!-- 삭제 에러 -->
		<c:if test="${deleteCnt == 0 }">
			<script type="text/javascript">
				errorAlert(deleteError);
			</script>
		</c:if>
		<!-- 삭제 성공 - 세션삭제, selectCnt= 2(방문환영)로 주고main.jsp로 이동 -->
		<c:if test="${deleteCnt != 0 }">
		<% 
			request.getSession().invalidate();//모든 세션 삭제 
		%>
			<!-- 삭제성공 -->
			<script type="text/javascript">
				alert("탈퇴처리 되었습니다 그동안 이용해주셔서 감사합니다.");
				window.location="main"; 
			</script>	
		</c:if><!-- 삭제성공 -->
	</c:if>	<!-- 아이디와 비밀번호가 일치 -->
	<c:if test="${selectCnt != 2}">
		<script type="text/javascript">
			errorAlert(passwdError);
		</script>
	</c:if>
</body>
</html>