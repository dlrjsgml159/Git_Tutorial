<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>         
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}style/inventory_add.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
</head>
<body>
    <header>
        <div class="gnb">
            <ul>
            	<li style="font-size:15px; color:white;">ID : manager</li>
                <li><a href="logout">로그아웃</a></li>
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
    <form action="${path}manager/inventory_modify_pro" method="post" enctype="multipart/form-data">
    
    <input type="hidden" name="notb_id" value="${dto.notb_id}">
    
    <div class="inventorydiv" align="center">
	    <table class="inventory" >
			<legend>재고수정</legend>
			<tr>
				<th>제품번호</th>
				<td>${dto.notb_id}</td>
			</tr>
			<tr>
				<th>품명</th>
				<td><input class="inventoryinput" type="text" name="notb_name" value="${dto.notb_name}"></td>
			</tr>
			<tr>
				<th>수량</th>
				<td><input class="inventoryinput" type="text" name="notb_cnt" value="${dto.notb_cnt}"></td>
			</tr>
			<tr>
				<th>가격</th>
				<td><input class="inventoryinput" type="text" name="notb_price" value="${dto.notb_price}"></td>
			</tr>
			<tr>
				<th>브랜드</th>
				<td><input class="inventoryinput" type="text" name="notb_brand" value="${dto.notb_brand}"></td>
			</tr>
			<tr>
				<th>상품 이미지</th>
				<td><input type="file" name="file1" value="${dto.notb_img}"></td>
				<th>설명 이미지</th>
				<td><input type="file" name="file2" value="${dto.notb_img_information}"></td>
			</tr>
		</table>
			<input type="submit" value="수정완료">
			<input type="button" value="취소" onclick="window.lacation='inventory_management'">
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