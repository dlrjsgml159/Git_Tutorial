<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
   <%@ include file="/resources/style/setting.jsp" %>    
<html>
<body>
<h2><center>게시글 수정</center></h2>
<form action="${path}resources/detailView" method="post" name="detailView">
	
	<!-- hidden : submit 일경우 input 태그에 보이지 않는 값을 넘길때 -->
	<input type="hidden" name="num" value="${num}">
	<input type="hidden" name="pageNum" value="${pageNum}">
	
	<table align="center">
		<tr>
			<th colspan="2">
				비밀번호를 입력하세요.!!
			</th>
		</tr>
		
		<tr>
			<th> 비밀번호 </th>
			<td>
				<input class="input" type="password" name="pwd" maxlength="20" placeholder="비밀번호입력" autofocus required>
				
			</td>
		</tr>
		<tr>
			<th colspan="2">
				<input class="input" type="submit" value="확인 ">
				<input class="input" type="reset" value="취소"
					onclick="window.history.back();">
			</th>
		</tr>
	</table>
</form>
</body>
</html>