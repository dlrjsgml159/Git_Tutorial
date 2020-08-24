<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="/resources/setting/setting.jsp" %> 
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
	<link rel="stylesheet" href="${path}css/bootstrap.min.css">
    <link rel="stylesheet" href="${path}css/owl.carousel.min.css">
    <link rel="stylesheet" href="${path}css/magnific-popup.css">
    <link rel="stylesheet" href="${path}css/font-awesome.min.css">
    <link rel="stylesheet" href="${path}css/themify-icons.css">
    <link rel="stylesheet" href="${path}css/nice-select.css">
    <link rel="stylesheet" href="${path}css/flaticon.css">
    <link rel="stylesheet" href="${path}css/gijgo.css">
    <link rel="stylesheet" href="${path}css/animate.css">
    <link rel="stylesheet" href="${path}css/slicknav.css">
    <link rel="stylesheet" href="${path}css/style.css">
</head>
<body>
    <!-- header-start -->
    <header>
        <div class="header-area ">
            <div class="header-top_area">
                <div class="container">
                    <div class="row">
                        <div class="col-xl-6 col-md-6 ">
                            <div class="social_media_links">
                                <a href="#">
                                    <i class="fa fa-linkedin"></i>
                                </a>
                                <a href="#">
                                    <i class="fa fa-facebook"></i>
                                </a>
                                <a href="#">
                                    <i class="fa fa-google-plus"></i>
                                </a>
                            </div>
                        </div>
                        <div class="col-xl-6 col-md-6">
                            <div class="short_contact_list">
                                <ul>
                                    <li><a href="#"> <i class="fa fa-envelope"></i> info@docmed.com</a></li>
                                    <li><a href="#"> <i class="fa fa-phone"></i> 160160</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="sticky-header" class="main-header-area">
                <div class="container">
                    <div class="row align-items-center">
                        <div class="col-xl-3 col-lg-2">
                            <div class="logo">
                                <a href="index.html">
                                    <img src="${path}img/logo.png" alt="">
                                </a>
                            </div>
                        </div>
                        <div class="col-xl-6 col-lg-7">
                            <div class="main-menu  d-none d-lg-block">
                                <nav>
                                    <ul id="navigation">
                                        <li><a class="active" href="index.html">home</a></li>
                                        <li><a href="Department.html">Department</a></li>
                                        <li><a href="#">blog <i class="ti-angle-down"></i></a>
                                            <ul class="submenu">
                                                <li><a href="blog.html">blog</a></li>
                                                <li><a href="single-blog.html">single-blog</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="#">pages <i class="ti-angle-down"></i></a>
                                            <ul class="submenu">
                                                <li><a href="elements.html">elements</a></li>
                                                <li><a href="about.html">about</a></li>
                                            </ul>
                                        </li>
                                        <li><a href="Doctors.html">Doctors</a></li>
                                        <li><a href="contact.html">Contact</a></li>
                                    </ul>
                                </nav>
                            </div>
                        </div>
                        <div class="col-xl-3 col-lg-3 d-none d-lg-block">
                            <div class="Appointment">
                                <div class="book_btn d-none d-lg-block">
                                    <a class="popup-with-form" href="#test-form">Make an Appointment</a>
                                </div>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="mobile_menu d-block d-lg-none"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>
    <!-- header-end -->
    <script src="${path}js/vendor/modernizr-3.5.0.min.js"></script>
    <script src="${path}js/vendor/jquery-1.12.4.min.js"></script>
    <script src="${path}js/popper.min.js"></script>
    <script src="${path}js/bootstrap.min.js"></script>
    <script src="${path}js/owl.carousel.min.js"></script>
    <script src="${path}js/isotope.pkgd.min.js"></script>
    <script src="${path}js/ajax-form.js"></script>
    <script src="${path}js/waypoints.min.js"></script>
    <script src="${path}js/jquery.counterup.min.js"></script>
    <script src="${path}js/imagesloaded.pkgd.min.js"></script>
    <script src="${path}js/scrollIt.js"></script>
    <script src="${path}js/jquery.scrollUp.min.js"></script>
    <script src="${path}js/wow.min.js"></script>
    <script src="${path}js/nice-select.min.js"></script>
    <script src="${path}js/jquery.slicknav.min.js"></script>
    <script src="${path}js/jquery.magnific-popup.min.js"></script>
    <script src="${path}js/plugins.js"></script>
    <script src="${path}js/gijgo.min.js"></script>
    <!--contact js-->
    <script src="${path}js/contact.js"></script>
    <script src="${path}js/jquery.ajaxchimp.min.js"></script>
    <script src="${path}js/jquery.form.js"></script>
    <script src="${path}js/jquery.validate.min.js"></script>
    <script src="${path}js/mail-script.js"></script>

    <script src="${path}js/main.js"></script>
    <script>
        $('#datepicker').datepicker({
            iconsLibrary: 'fontawesome',
            icons: {
                rightIcon: '<span class="fa fa-caret-down"></span>'
            }
        });
        $('#datepicker2').datepicker({
            iconsLibrary: 'fontawesome',
            icons: {
                rightIcon: '<span class="fa fa-caret-down"></span>'
            }

        });
    $(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});
    </script>
</body>
</html>