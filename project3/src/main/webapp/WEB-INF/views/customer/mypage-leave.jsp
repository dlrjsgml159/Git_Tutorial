<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/mypage-leave.css">
    <meta charset="utf-8" />
</head>
<body>
    <header>
        <c:if test="${sessionScope.memId == null}">
        <script type="text/javascript">
    		alert("잘못된 접근입니다. 다시로그인하여주십시오!");     
    		window.location="main"
    	 </script>
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
    <form action="${path}customer/mypage-leave-pro" method="post" name="leaveform" onsubmit="return leaveformCheck();">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
    <content>
    <div class="center" align="center">
    	<div class="title">
    		<h2 style="font-size:40px;">회원탈퇴</h2>
    	</div>
    	<div class="titleli">	
    		<ul>
    			<li>홈 > </li>
    			<li>내정보 > </li>
    			<li>회원탈퇴</li>
    		</ul>
	    </div>	
    	<div class="litable">
    	<ul>
    		<li><a href="${path}customer/mypage" class="listyle">정보수정</a></li>
    		<li><a href="${path}customer/mypage-orderlist" class="listyle">주문내역</a></li>
    		<li><a href="${path}customer/refund" class="listyle">환불내역</a></li>
    		<li><a href="${path}customer/cartlist" class="listyle">장바구니</a></li>
    		<li class="hit"><a href="${path}customer/mypage-leave" class="listyle">회원탈퇴</a></li>
    		<li><a href="${path}logout" class="listyle">로그아웃</a></li>
    	</ul>
    	</div>
    	<div class="dividpwd" align="center">
    	<pre style="background:#F2F2F2">
<h2 style="font-size:20px;">회원탈퇴</h2>
아이디와 비밀번호를 확인하고 회원탈퇴 버튼을 누르면 탈퇴가 완료됩니다.
그동안 저희 서비스를 이용하여 주셔서 대단히 감사합니다.
더욱더 개선하여 좋은 서비스와 품질로 보답하겠습니다.
    	</pre>
    	<table class="idpwdtbl">
    		<tr>
    			<td >
    				<input type="text"  name="id" class="idpwd" placeholder="아이디" >
    			</td>
    			<td rowspan="2">
    				<input type="submit" class="idpwd1" value="회원탈퇴">
    			</td>
    		</tr>
    		<tr>
    			<td>
    				<input type="text" name="pwd" class="idpwd" placeholder="패스워드" >
    			</td>
    		</tr>
    	</table>
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