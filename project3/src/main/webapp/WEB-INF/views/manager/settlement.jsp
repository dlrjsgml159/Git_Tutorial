<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/style/setting.jsp" %>    
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<link type="text/css" rel="stylesheet" href="${path}resources/style/settlement.css">
    <meta charset="utf-8" />
    <script type="text/javascript" src="${path}resources/js/jquery-3.5.1.min.js"></script>
	<script type ="text/javascript">
		function logoutChk(){
			alert("로그아웃되었습니다.");
		}
		
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
    <html>
  <head>
  
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
	        <c:forEach var="dto" items="${dtos}">
	          	['${dto.settlement_NOTB_NAME}', ${dto.settlement_NOTB_CNT}],
	        </c:forEach>
        ]);

        // Set chart options
        var options = {'title':'가장 많이팔린 노트북 순위',
                       'width':900,
                       'height':800};

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
      
      google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawStuff);

      function drawStuff() {
        var data = new google.visualization.arrayToDataTable([
          ['Move', 'Percentage'],
          <c:forEach var="dto" items="${dtos}">
          	<c:if test="${dto.settlement_NOTB_PRICE != 0}">
        	['${dto.settlement_NOTB_NAME}', ${dto.settlement_NOTB_PRICE}],
        	</c:if>
      	</c:forEach>
        ]);

        var options = {
          width: 1200,
          legend: { position: 'none' },
          chart: {
            title: '노트북별 총매출',
            subtitle: '노트북별 총매출' },
          axes: {
            x: {
              0: { side: 'top', label: '매출액'} // Top x-axis.
            }
          },
          bar: { groupWidth: "90%" }
        };

        var chart = new google.charts.Bar(document.getElementById('top_x_div'));
        // Convert the Classic options to Material options.
        chart.draw(data, google.charts.Bar.convertOptions(options));
      };
    </script>
  </head>
  <body>
    <!--Div that will hold the pie chart-->
    <div align="center">
    	<table class="set">
    		<tr>
    			<th>총매출</th>
    			<th>총거래수</th>
    		</tr>
    		<tr>
	    		<c:set var="PRICE" value="0"/>
	    		<c:set var="CNT" value="0"/>
		    	<c:forEach var="dto" items="${dtos}">
		    		<c:set var="PRICE" value="${PRICE + dto.settlement_NOTB_PRICE}"/>
		    		<c:set var="CNT" value="${CNT + dto.settlement_NOTB_CNT}"/>
		        </c:forEach>
		        <td><fmt:formatNumber value="${PRICE}" pattern="#,###"/> 원</td>
		        <td>${CNT} 건</td>
	    	</tr>
    	</table>
	    <table class="table">
	    	<tr>	
	    		<td>
	    			<div id="chart_div"></div>
	    		</td>
	    	</tr>
	    	<tr>
	    		<td><div id="top_x_div" style="width: 1000px; height: 600px;"></div></td>
	    	</tr>
	    </table>
    </div>
  </body>
</html>
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