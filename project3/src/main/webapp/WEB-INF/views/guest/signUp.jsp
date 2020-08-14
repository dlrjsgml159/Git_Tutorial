<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>       
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/signUp.css">
<meta charset="utf-8" />
<title>회원가입</title>
<script src="https://t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
</head>
<body>
    <header>
        <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="${path}login" >로그인</a></li>
                <li><a href="${path}order" >주문</a></li>
                <li style="float:left"><a href="${path}main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
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
                <li style="float:left"><a href="${path}main"><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
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
    <form action="${path}signUppro" method="post" name="signInform" onsubmit="return signInCheck();">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
    <input type ="hidden" name="hiddenId" value="0">
    <content>
    <div align="center">
	    <table class="my" >
	    	<tr>
	    		<th colspan="4">회원가입</th>
	    	</tr>
	    	<tr>
	    		<th>*아이디</th> 
	    		<td colspan="3">
		    		<input type="text" id="box" name="id" maxlength="20" placeholder="아이디">
		    		<input type="button" id="button"value="중복체크" onclick="confirmId();">
	    		</td>
	    	</tr>
	    	<tr>
	    		<th>*비밀번호</th>
	    		<td><input type="password" name="pwd" id="box" maxlength="20" placeholder="비밀번호"></td>
	    		<th>*비밀번호 확인</th>
	    		<td><input type="password" name="repwd" id="box" maxlength="20" placeholder="비밀번호 확인"></td>
	    	</tr>
	    	<tr>
	    		<th>*이름</th>
	    		<td colspan="3"><input type="text" name="name"id="box" maxlength="20" placeholder="ex) 홍길동"></td>
	    	</tr>
	    	<tr>
	    		<th>*휴대폰 번호</th>
	    		<td colspan="3">
	    			<input type="text" name="hp1" id="box2" maxlength="3"onkeyup="nextHp1()" > -
	    			<input type="text" name="hp2" id="box3" maxlength="4" onkeyup="nextHp2()"> -
	    			<input type="text" name="hp3" id="box3" maxlength="4" onkeyup="nextHp3()">
	    		</td>
	    	</tr>
	    	<tr>
	    		<th>이메일</th>
	    		<td colspan="3">
	    			<input type="text" id="box" name="email1" maxlength="10" placeholder="이메일">
	    			 @<input type="text" id="box" name="email2" maxlength="20" placeholder="ex) OOOO.com">
	    			<select name="email3" onchange="selectemailChk();" style="width:100px; height:30px;">
	    				<option value="0">직접입력</option>
	    				<option value="naver.com">네이버</option>
	    				<option value="gmail.com">구글</option>
	    				<option value="nate.com">네이트</option>
	    				<option value="daum.net">다음</option>
	    			</select>
	    		</td>
	    	</tr>
	    	<tr>
    			<th>
    				<label id="address"><small>*</small>주소</label>
    			</th>
    			<td colspan="3">
    				<input type="text" name="address1" id="sample6_postcode" placeholder="우편번호" size=6 style="padding:3px;" maxlength="10">
    				<input type="button" id="button4" onclick="addressSearch();" value="주소찾기">
	    			<input type="text" name="address2" id="sample6_address" placeholder="주소" maxlength="45">
	    			<input type="text" name="address3" id="sample6_address2" placeholder="상세주소" size=30 onchange="addinput();" maxlength="45">
	    			<input type="hidden" name="address">
	    		</td>
	    	</tr>
	    </table>
	    <div class="buttoncl">
	    	<div>
		    	<input type="submit" id="button2"value="회원가입">
		    	<input type="reset" id="button3"value="취소" onclick="window.location='main'">
	    	</div>
	    </div>
    </div>
    </content>
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