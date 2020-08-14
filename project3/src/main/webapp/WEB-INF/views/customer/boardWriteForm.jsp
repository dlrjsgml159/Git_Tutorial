<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/boardWriteForm.css">
<meta charset="utf-8" />
</head>
<body>
    <header>
        <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="${path}login" >로그인</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas" >회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" onclick="loginChk();">자유게시판</a></td>
                <td><a href="${path}customer/consulting" onclick="loginChk();">문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if>    
    <!-- 로그인 성공 -->
    <c:if test="${sessionScope.memId != null}">
        <div class="gnb">
            <ul>
				<li style="font-size:15px; color:white;">ID : ${sessionScope.memId}</li>            
                <li><a href="${path}logout" >로그아웃</a></li>
                <li><a href="${path}customer/mypage">내정보</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}aboutas">회사소개</a></td>
                <td><a href="${path}window10" >window10</a></td>
                <td><a href="${path}driver" >driver설치</a></td>
                <td><a href="${path}customer/board" >자유게시판</a></td>
                <td><a href="${path}customer/consulting" >문의사항</a></td>
            </tr>
        </table>    
        </div>
    </c:if> 
    </header>
    <form action="${path}customer/boardWritePro" method="post" name="boardWritePro">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
	<input type="hidden" name="num" value="${num}">
	<input type="hidden" name="pageNum" value="${pageNum}">
	<input type="hidden" name="ref" value="${ref}">
	<input type="hidden" name="ref_step" value="${ref_step}">
	<input type="hidden" name="ref_level" value="${ref_level}">
	<div align="center">
	<fieldset>
	<legend>&nbsp;&nbsp;&nbsp;글작성&nbsp;&nbsp;&nbsp;</legend>
	<table>
		<tr>
			<th> 제목 </th>
			<td>
				<input class="input" type="text" style="outline: none;" name="subject" maxlength="50"
					placeholder="제목을 입력하세요" required>
			</td>
		</tr>
		<tr>
			<th> 작성자 </th>
			<td>
				<input class="input" type="text" style="outline: none;" name="writer" maxlength="20"
					placeholder="작성자를 입력하세요" autofocus required>
			</td>
		</tr>
		<tr>
			<th> 비밀번호 </th>
			<td>
				<input class="input" style="outline: none;" type="password" name="pwd" maxlength="20"
					placeholder="비밀번호를 입력하세요" required>
			</td>
		</tr>
		<tr>
			<td colspan="2">
				<textarea class="input2" rows="10" cols="40" name="content"
					placeholder="글작성란" word-break:break-all></textarea>
			</td>
		</tr>
		<tr>
			<th colspan="2">
				<input class="button" type="submit" value="작성">
				<input class="button" type="reset" value="초기화">
				<input class="button" type="button" value="목록"
					onclick="window.location='${path}customer/board?pageNum=${pageNum}'">
			</th>	
		</tr>
	</table>
	</fieldset>
	</div>
</form>

    <footer>
        <div class="office_adress">
        <pre>
사업자등록번호 : 000-00-00000 
대표이사 : 이건희 
주소 : 서울특별시 O구 OO로 OOO번길
이메일 : gunhee260@gmail.com
		</pre>
		<ul>
			<li></li>
		</ul>
		<pre>
제품이나 사이트 이용에 궁금증을 바로 해결하시려면, 1234-5678 으로 전화하세요.
상담 가능 시간 평일 10:00 - 18:00
        </pre>
        </div>
    </footer>
</body>
</html>