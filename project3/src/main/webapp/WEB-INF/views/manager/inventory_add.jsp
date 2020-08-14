<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>         
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/inventory_add.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
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
                <td><a href="inventory_management" >재고관리</a></td>
                <td><a href="orderconfirmation" >주문관리</a></td>
                <td><a href="refund_request" >환불관리</a></td>
                <td><a href="member_management" >회원관리</a></td>
                <td><a href="settlement" >결산</a></td>
            </tr>
        </table>
        </div>
    </header>
    <form action="${path}manager/inventory_add_pro?${_csrf.parameterName}=${_csrf.token}" method="post" enctype="multipart/form-data">
    	<input type ="hidden" name="${_csrf.parameterName}" value="${_csrf.token}">
    <div  align="center">
	    <table class="inventory" >
			<tr>
				<th>품명</th>
				<td><input class="inventoryinput" type="text" name="notb_name"></td>
			</tr>
			<tr>
				<th>수량</th>
				<td><input class="inventoryinput" type="text" name="notb_cnt"></td>
			</tr>
			<tr>
				<th>가격</th>
				<td><input class="inventoryinput" type="text" name="notb_price"></td>
			</tr>
			<tr>
				<th>브랜드</th>
				<td><input class="inventoryinput" type="text" name="notb_brand"></td>
			</tr>
			<tr>
				<th>상품 이미지</th>
				<td><input type="file" name="file1" ></td>
			</tr>
			<tr>
				<th>설명 이미지</th>
				<td><input type="file"  name="file2"></td>
			</tr>
		</table>
			<input type="submit" class="imagebutton" value="추가">
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