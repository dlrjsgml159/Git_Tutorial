<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>     
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link type="text/css" rel="stylesheet" href="${path}resources/style/productinformation.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
	<script type ="text/javascript">
		
	var sell_price;
	var CART_NOTB_CNT;

	function init () {
		sell_price = document.form.sell_price.value;
		CART_NOTB_CNT = document.form.CART_NOTB_CNT.value;
		document.form.CART_NOTB_PRICE.value = sell_price;
		document.form.CART_NOTB_PRICE1.value = numberWithCommas(sell_price);
	}

	function add () {
		hm = document.form.CART_NOTB_CNT;
		var hm1 = parseInt(document.form.CART_NOTB_CNT.value);
		var hm2 = parseInt(document.form.CNT.value);
		console.log(hm2+""+hm.value+""+hm1);
		CART_NOTB_PRICE1 = document.form.CART_NOTB_PRICE1;
		hm.value ++;
		if(hm1 >= hm2) {
			hm.value --;
			alert('수량 안맞음');
			return false;
		} else {
			num = parseInt(hm.value) * sell_price;
			document.form.CART_NOTB_PRICE.value = num;
			CART_NOTB_PRICE1.value = numberWithCommas(num);
			console.log(hm.value);
		}
	}

	function del () {
		hm = document.form.CART_NOTB_CNT;
		sum = document.form.CART_NOTB_PRICE1;
			if (hm.value > 1) {
				hm.value -- ;
				num = parseInt(hm.value) * sell_price;
				 CART_NOTB_PRICE1.value = numberWithCommas(num)
				 document.form.CART_NOTB_PRICE.value = num;
			}
	}

	function numberWithCommas(x) {
	    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}
	
	function formcheck(){
		document.form.action="customer/buy_pro";
		document.form.submit();
	}

	</script>
</head>
<body onload="init();">
    <header>
        <c:if test="${sessionScope.memId == null}">
        <div class="gnb">
            <ul>
                <li><a href="login" >로그인</a></li>
                <li><a href="order" >주문</a></li>
                <li style="float:left"><a href="main" ><img src="${path}resources/images/logo/facebook_cover_photo_1.png"></a></li>
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
    <div align="center">
    <form action="${path}customer/cartlist_pro" name="form" method="post">
    	<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
    	<input type="hidden" name="CART_NOTB_ID" value="${dto.getNotb_id()}">
    	<input type="hidden" name="CU_ID" value="${sessionScope.memId}">
    	<input type="hidden" name="CART_NOTB_NAME" value="${dto.getNotb_name()}">
    	<input type="hidden" name="CART_NOTB_BRAND" value="${dto.getNotb_brand()}">
    	<input type="hidden" name="CART_NOTB_IMG" value="${dto.getNotb_img()}">
    	<input type="hidden" name="CNT" value="${dto.getNotb_cnt()}">
	    <div id="content1" align="center">
	    	<div class="list1" align="center">
	    		<img src="${path}resources/images/${dto.getNotb_img()}" width="400" height="400">
	    	</div>
	    	
	    	<div class="list2" align="center">
	    		<div class="listlab">
		    		<div class="contentname">
		    			<h3>${dto.getNotb_name()}</h3><br><fmt:formatNumber value="${dto.getNotb_price()}" pattern="#,###"/> 원
		    		</div>
	    		</div>
	    		<div style="width:300px;" align="center">
					수량 : <input type=hidden name="sell_price" value="${dto.getNotb_price()}">
					<input type="button" id="count1" value=" - " onclick="del();">
					<input type="text" id="count3" name="CART_NOTB_CNT" value="1" size="3"readonly>
					<input type="button" id="count1" value=" + " onclick="add();">
					<br>
							<input type=hidden name="CART_NOTB_PRICE">
					금액 : <input type="text" name="CART_NOTB_PRICE1" id="count2" size=11 disabled> 원
				</div>
				<table class="buttonclass">
					<tr>
						<c:if test="${sessionScope.memId != null}">
							<th><input type="button" id="button" value="구매하기" onclick="formcheck();"></th>
							<th><input type="submit" id="button1" value="장바구니추가"></th>
						</c:if>
						<c:if test="${sessionScope.memId == null}">
							<th><input type="button" id="button" value="구매하기" onclick="loginChk();"></th>
							<th><input type="button" id="button1" value="장바구니추가" onclick="loginChk();"></th>
						</c:if>
					</tr>
				</table>
			</div>	
		</div>
	</form>
	</div>
	<div id="content">
        <div class="section1">
            <div class="slide_banner"><img src="${path}resources/images/${dto.getNotb_img_information()}"></div>
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