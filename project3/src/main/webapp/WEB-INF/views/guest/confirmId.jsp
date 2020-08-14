<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<body onload="confirmIdFocus();">
	<h2>중복확인 페이지</h2>
<form action="${path}confirmId" method="post" name="confirmform"
		onsubmit="confirmIdCheck();">
	<!-- id 중복 -->
	<c:if test="${selectCnt > 0}">
	<table>
		<tr>
			<th colspan="2">
				<span>${id}</span>는 사용할 수 없습니다.
			</th>
		</tr>
		
		<tr>
			<th> 아이디 : </th>
			<td>
				<input class="input" type="text" name="id" maxlength="20"
					style="width:150px" autofocus required>
			</td>
		</tr>
		
		<tr>
			<th colspan="2">
				<input class="inputButton" type="submit" value="확인">
				<input class="inputButton" type="reset" value="취소" onclick="self.close();">
			</th>
		</tr>
	</table>
	</c:if>
	<c:if test="${selectCnt == 0}">
	<table>
		<tr>
			<td>
				<span>${id}</span>는 사용할 수 있습니다.
			</td>
		</tr>
		<tr>
			<th>
				<input class="inputButton" type="button" value="확인" onclick="setId('${id}');">
			</th>
		</tr>		
	</table>
	</c:if>
</form>
</body>
</html>