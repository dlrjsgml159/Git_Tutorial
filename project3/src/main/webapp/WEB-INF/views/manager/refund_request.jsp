<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/refund_request.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
	<script type ="text/javascript">
		function checkAll(){
		      if( $("#th_checkAll").is(':checked') ){
		        $("input[name=checkRow]").prop("checked", true);
		      }else{
		        $("input[name=checkRow]").prop("checked", false);
		      }
		}
	</script>
</head>
<body>
    <header>
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : manager</li>
                <li><a href="${path}logout">로그아웃</a></li>
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
    <contents>
    <form action="" method="post">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
    <input type="hidden" name="REFUND_NOTB_NAME" value="">
    <div align="center">
    	<table class="text1">
    		<tr>
    			<th>환불 상태</th>
    			<th>환불일</th>
    			<th>아이디</th>
    			<th>이미지</th>
    			<th>품명</th>
    			<th>브랜드</th>
    			<th>갯수</th>
    			<th>가격</th>
    		</tr>
    		<c:forEach var="dto" items="${dtos}" >
	    		<tr>
	    			<c:if test="${dto.getREFUND_NOTB_STATE() == 1}">
	    			<td>환불 승인대기중<br><input type="button" value="환불 승인" onclick="window.location='${path}manager/marefund_pro?state=${dto.getREFUND_NOTB_STATE()}&id=${dto.getId()}&notbid=${dto.getREFUND_NOTB_ID()}&notbnum=${dto.getREFUND_NOTB_NUM()}'">
	    			<input type="button" value="환불 거부" onclick="window.location='${path}manager/marefund_pro?state=3&id=${dto.getId()}&notbid=${dto.getREFUND_NOTB_ID()}&notbnum=${dto.getREFUND_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto.getREFUND_NOTB_STATE() == 2}">
	    			<td>환불 승인</td>
	    			</c:if>
	    			<c:if test="${dto.getREFUND_NOTB_STATE() == 3}">
	    			<td>환불 거부</td>
	    			</c:if>
	    			<td>${dto.getREFUND_NOTB_DATE()}</td>
	    			<td>${dto.getId()}</td>
	    			<td><img src="${path}resources/images/${dto.getREFUND_NOTB_IMG()}" width="100" height="100"></td>
	    			<td>${dto.getREFUND_NOTB_NAME()}</td>
	    			<td>${dto.getREFUND_NOTB_BRAND()}</td>
	    			<td>${dto.getREFUND_NOTB_CNT()}</td>
	    			<td><fmt:formatNumber value="${dto.getREFUND_NOTB_PRICE()}" pattern="#,###"/> 원</td>
	    		</tr>
	    		</c:forEach>
    	</table>
    	<table class="paging" style="width:1000px" align="center">
				<tr>
					<th align="center">
						<!-- 게시글이 있으면 -->
						<c:if test="${cnt1 > 0}">
							<!-- 처음[◀◀] / 이전블록[◀] 특수문자 : 한글상태 ㅁ+한자키 -->
							<c:if test="${startPage1 > pageBlock1}">
								<a href="${path}manager/mypage-orderlist">[◀◀]</a>
								<a href="${path}manager/mypage-orderlist?pageNum=${startPage1 - pageBlock1}">[◀]</a>
							</c:if>
							
							<!-- 블록내의 페이지 번호 -->
							<c:forEach var="i" begin="${startPage1}" end="${endPage1}">
								<c:if test="${i == currentPage1}">
								<span><b>[${i}]</b></span>
								</c:if>
								<c:if test="${i != currentPage1}">
									<a href="${path}manager/mypage-orderlist?pageNum=${i}">[${i}]</a>
								</c:if>
							</c:forEach>
							<!-- 다음[▶] / 마지막[▶▶] -->
							<c:if test="${pageCount1 > endPage1}">
								<a href="${path}manager/mypage-orderlist?pageNum=${startPage1 + pageBlock1}">[▶]</a>
								<a href="${path}manager/mypage-orderlist?pageNum=${pageCount1}">[▶▶]</a>
							</c:if>
						</c:if>
					</th>
				</tr>
			</table>
    	</div>
    </form>
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