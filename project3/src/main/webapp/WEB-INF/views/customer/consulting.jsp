<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/consulting.css">
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
    <contents>
    	<div align="center">
    	<table class="text1">
    		<tr>
    			<th colspan="3">자주묻는 질문</th>
    		</tr>
    		<tr>
    			<th>문의사항</th>
    			<th colspan="2" style="width:620px;">내용</th>
    		</tr>
    		<tr>
    			<td ><a href="#" alt="">기타</a></td>
    			<td colspan="2"><a href="#" alt="">협력사 서비스별 문의, 요청 이메일 주소 안내</a></td>
    		</tr>
    		<tr>
    			<td ><a href="#" alt="">주문/결제</a></td>
    			<td colspan="2"><a href="#" alt="">상품 배송은 얼마나 걸리나요?</a></td>
    		</tr>
    		<tr>
    			<td ><a href="#" alt="">주문/결제</a></td>
    			<td colspan="2"><a href="#" alt="">취소 철회 요청은 어떻게 하나요?</a></td>
    		</tr>
    		<tr>
    			<td ><a href="#" alt="">주문/결제</a></td>
    			<td colspan="2"><a href="#" alt="">판매점 연락처, 주소등 판매점 정보는 어디서 확인하나요?</a></td>
    		</tr>
    		<tr>
    			<td ><a href="#" alt="">주문/결제</a></td>
    			<td colspan="2"><a href="#" alt="">주문을 취소하고 싶습니다. 어떻게 하나요?</a></td>
    		</tr>
    	</table>
    	<table class="text2">
    		<tr>
    			<td><a href="#" alt="">이전   </a></td>
    			<td><a href="#" alt="">1 ,   </a></td>
    			<td><a href="#" alt="">2 ,   </a></td>
    			<td><a href="#" alt="">3 ,   </a></td>
    			<td><a href="#" alt="">4 ,   </a></td>
    			<td><a href="#" alt="">5 ,   </a></td>
    			<td><a href="#" alt="">다음   </a></td>
    			<td><a href="문의하기.html" alt=""><input type="button" id="button"value="문의하기"></a></td>
    		</tr>
    	</table>
    	</div>
    </contents>
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