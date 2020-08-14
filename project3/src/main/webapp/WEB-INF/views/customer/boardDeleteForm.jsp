<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
    <%@ include file="/resources/style/setting.jsp" %>    
<html>
<body>

	<h2><center>게시글 삭제</center></h2>
	<form action="${path}customer/boardDeletePro" method="post" name="boardDeletePro">
	
		<input type="hidden" name="num" value="${num}">
		<input type="hidden" name="pageNum" value="${pageNum}">
		
		<table align="center">
			<tr>
				<th colspan="2">
					비밀번호를 입력하세요.!!
				</th>
			</tr>
			<tr>
				<th>비밀번호</th>
				<td>
					<input class="input" type="password" name="pwd" maxlength="20" placeholder="비밀번호입력" autofocus>
				</td>
			</tr>
			<tr>
				<th colspan="2">
					<input class="button" type="submit" value="확인">
					<input class="button" type="reset" value="취소"
						onclick="window.history.back();">
				</th>
			</tr>
		</table>
	</form>
</body>
</html>