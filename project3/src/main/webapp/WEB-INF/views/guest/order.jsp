<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/order.css">
    <meta charset="utf-8" />
</head>
<body onload="rotate();">
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
                <td><a href="${path}customer/board" onclick="return loginChk();">자유게시판</a></td>
                <td><a href="${path}customer/consulting" onclick="return loginChk();">문의사항</a></td>
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
   	 <div id="content">
	     <div align="center" class="hit_product">
	         <ul>
	         	<c:forEach var="dto" items="${dtos}">
	             	<li>
	             	<a href="productinformation?num=${dto.notb_id}&pageNum=${pageNum}&number=${number+1}">
	             	<img src="${path}resources/images/${dto.notb_img}" width="150" height="150"></a>
	             	<p>${dto.notb_name}<br>${dto.notb_brand}<br><br><fmt:formatNumber value="${dto.notb_price}" pattern="#,###"/> 원</p>
	             	</li>
	             </c:forEach>
	         </ul>
	         <table class="paging" style="width:1000px" align="center">
	<tr>
		<th align="center">
			<c:if test="${cnt > 0}">
				<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
				<c:if test="${startPage > pageBlock}">
					<a href="${path}order">[◀◀]</a>
					<a href="${path}order?pageNum=${startPage - pageBlock}">[◀]</a>
				</c:if>
				<!-- 블록내의 페이지 번호 -->
				<c:forEach var="i" begin="${startPage}" end="${endPage}">
					<c:if test="${i == currentPage}">
					<span><b>[${i}]</b></span>
					</c:if>
					<c:if test="${i != currentPage}">
						<a href="${path}order?pageNum=${i}">[${i}]</a>
					</c:if>
				</c:forEach>
				<!-- 다음[▶] / 마지막[▶▶] -->
				<c:if test="${pageCount > endPage}">
					<a href="${path}order?pageNum=${startPage + pageBlock}">[▶]</a>
					<a href="${path}order?pageNum=${pageCount}">[▶▶]</a>
				</c:if>
			</c:if>
		</th>
	</tr>
</table>
	     </div>
     </div>
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