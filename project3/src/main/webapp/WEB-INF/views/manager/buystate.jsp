<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
    <%@ include file="/resources/style/setting.jsp" %>       
    <link type="text/css" rel="stylesheet" href="${path}resources/style/orderconfirmation.css">
</head>
<body>
 <table class="text5">
	    		<tr>
					<th style="width:10%">
						배송상태
					</th>
					<th style="width:10%">
						제품이미지
					</th>
					<th style="width:20%">
						제품명
					</th>
					<th style="width:10%">
						브랜드
					</th>
					<th style="width:10%">
						수량
					</th>
					<th style="width:10%">
						가격
					</th>
					<th style="width:10%">
						구매자
					</th>
				</tr>
	    		<c:forEach var="dto2" items="${dtos}">
	    		<tr>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 1}">
	    			<td>승인대기중<br><input type="button" value="구매승인" onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getBUYCU_ID()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 2}">
	    			<td>승인완료 배송준비중<br><input type="button" value="배송시작"onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getBUYCU_ID()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 3}">
	    			<td>배송중<br><input type="button" value="배송완료"onclick="window.location='${path}manager/orderconfirmation_pro?state=${dto2.getBUY_NOTB_STATE()}&id=${dto2.getBUYCU_ID()}&notbid=${dto2.getBUY_NOTB_ID()}&notbnum=${dto2.getBUY_NOTB_NUM()}'"></td>
	    			</c:if>
	    			<c:if test="${dto2.getBUY_NOTB_STATE() == 4}">
	    			<td>배송완료</td>
	    			</c:if>
	    			<td><img src="${path}resources/images/${dto2.getBUY_NOTB_IMG()}" width="100" height="100"></td>
	    			<td>${dto2.getBUY_NOTB_NAME()}</td>
	    			<td>${dto2.getBUY_NOTB_BRAND()}</td>
	    			<td>${dto2.getBUY_NOTB_CNT()}</td>
	    			<td><fmt:formatNumber value="${dto2.getBUY_NOTB_PRICE()}" pattern="#,###"/> 원</td>
	    			<td>${dto2.getBUYCU_ID()}</td>
	    		</tr>
	    		</c:forEach>
	    </table>
</body>
</html>