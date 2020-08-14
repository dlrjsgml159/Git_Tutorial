<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>        
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/inventory_management.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
</head>
<body>
    <header>
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : manager</li>
                <li><a href="${path}logout" >로그아웃</a></li>
            </ul>
        </div>
        <div class="lnb" align="center">
        <table>
            <tr>
                <td><a href="${path}manager/inventory_management" >재고관리</a></td>
                <td><a href="${path}manager/orderconfirmation" >주문관리</a></td>
                <td><a href="${path}manager/refund_request" >환불관리</a></td>
                <td><a href="${path}manager/member_management" >회원관리</a></td>
                <td><a href="${path}manager/settlement" >결산</a></td>
            </tr>
        </table>
        </div>
    </header>
    <form method="post">
    <contents>
    <div align="center">
    	<table class="management"style="width:1000px">
			<tr>
				<th colspan="6" align="center" style="height:25px">
					추가목록수 : ${cnt} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				</th>
			</tr>
			<tr>
				<th style="width:15%">번호</th>
				<th style="width:15%">품명</th>
				<th style="width:15%">수량</th>
				<th style="width:15%">가격</th>
				<th style="width:15%">브랜드</th>
				<th style="width:15%">상품이미지</th>
			</tr>
			
			<!-- 게시글이 있으면 -->
			<c:if test="${cnt > 0}">
				<c:forEach var="dto" items="${dtos}">
					<tr>
						<td>
							${number}
							<c:set var="number" value="${number-1}"/>
						</td>
						<td>
							<a href="${path}manager/inventory_add_view?num=${dto.notb_id}&pageNum=${pageNum}&number=${number+1}">${dto.notb_name}</a>
						</td>
						<td>
							${dto.notb_cnt}
						</td>
						<td>
							<fmt:formatNumber value="${dto.notb_price}" pattern="#,###"/> 원
						</td>
						<td>
							${dto.notb_brand}
						</td>
						<td>
							<img src="${path}resources/images/${dto.notb_img}" width="100" height="100">
						</td>
					</tr>
				</c:forEach>
			</c:if>
			<!-- 재고가없으면 -->
			<c:if test="${cnt == 0}">
				<tr>
					<td colspan="6" align="center">
						재고가 없습니다. 재고를 추가 해주세요.!!
					</td>
				</tr>
			</c:if>
		</table>
<!-- 페이지 컨트롤 -->	
		<div align="center">
			<table class="pagenum">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage > pageBlock}">
								<a href="${path}manager/inventory_management">[◀◀]</a>
								<a href="${path}manager/inventory_management?pageNum=${startPage - pageBlock}">[◀]</a>
							</c:if>
							
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage}" end="${endPage}">
								<c:if test="${i == currentPage}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage}">
									<a href="${path}manager/inventory_management?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount > endPage}">
								<a href="${path}manager/inventory_management?pageNum=${startPage + pageBlock}">[▶]</a>
								<a href="${path}manager/inventory_management?pageNum=${pageCount}">[▶▶]</a>
							</c:if>
						</c:if>
					</th>
				</tr>
			</table>
			<input type="button" id="button" value="상품추가" onclick="window.location='inventory_add'">
		</div>
    </div>
    </contents>
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