<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    
<%@ include file="/resources/style/setting.jsp" %>    

<html>
<body>
	<h2><center>글수정</center></h2>
	<c:if test="${selectCnt == 0}">
		<script type="text/javascript">
			errorAlert(passwdError);
		</script>
	</c:if>
	<c:if test="${selectCnt != 0}">
		<form action="${path}customer/detailPro" method="post" name="detailPro">
		
		<!-- num, pageNum -->
		<input type="hidden" name="num" value="${num}">
		<input type="hidden" name="pageNum" value="${pageNum}">
		<table align="center">
			<tr>
				<th colspan="2">수정할 정보를 입력하세요.!!</th>
			</tr>
			
			<tr>
				<th style="width:150px">작성자</th>
				<td style="width:150px">${dto.writer}</td>
			</tr>
			<tr>
				<th style="width:150px">글제목</th>
				<td>
					<input class="input" type="text" name="subject" maxlength="50"
						value="${dto.subject}" style="width:270px">
				</td>
			</tr>
			<tr>
				<th>글내용</th>
				<td>
					<textarea class="input" rows="10" cols="40" name="content"
						word-break:break-all> ${dto.content}</textarea>
				</td>
			</tr>
			<tr>
				<th colspan="2">
					<input class="input" type="submit" value="수정">
					<input class="input" type="reset" value="초기화">
					<input class="input" type="button" value="목록보기"
							onclick="window.location='${path}customer/board?pageNum=${pageNum}'">
				</th>
			</tr>
		</table>
		</form>
	</c:if>
</body>
</html>