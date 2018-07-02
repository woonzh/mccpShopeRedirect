<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Inventory recon</title>

    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <!--<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">-->
    <link rel='stylesheet prefetch' href='https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/themes/smoothness/jquery-ui.css'>

    <!-- Custom styles for this template -->
    <link href="{{ url_for('static', filename='css/simple-sidebar.css')}}" rel="stylesheet">

</head>

<body onload="onload()">
    <form action="#" id="loading"></form>

    <div id="wrapper">

        <!-- Sidebar -->
        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <li class="sidebar-brand">
                    <a href="">
                        Main Page
                    </a>
                </li>
                <li>
                    <a href="accounts">Accounts</a>
                </li>
                <li>
                    <a href="inventory">Inventory</a>
                </li>
                <li>
                    <a href="">Orders</a>
                </li>
                <li>
                    <a href="">Delivery</a>
                </li>
                <li>
                    <a href="shopee">Shopee</a>
                </li>
            </ul>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <a href="#menu-toggle" class="btn btn-secondary" id="menu-toggle"><b>Toggle Menu</b></a>
                <h1>Shopee</h1>
                <p>Generate Shopee Authentication URL here</code>.</p>
                <p><b>Click on the URL, log in and retrieve the shopid</b></p>
            </div>
            <?php echo "ttt"; ?>
            <p> Shop ID: <?php echo "ttt"; ?></p>
            <form action="#" id="shopee">
              <input type="button" id="shopee" class="submit" value="submit" onclick="shopeeRedirect();">
            </form>

        </div>

        <?php echo "ttt"; ?>
        <!-- /#page-content-wrapper -->

    </div>
    <!-- /#wrapper -->
    <?php echo "ttt"; ?>
    <!-- Bootstrap core JavaScript -->
    <script src="{{ url_for('static', filename='vendor/jquery/jquery.min.js')}}"></script>
    <script src="{{ url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js')}}"></script>
    <script src="{{ url_for('static', filename='js/shopee.js')}}"></script>

    <!-- Menu Toggle Script -->
    <script>
    $("#wrapper").toggleClass("toggled");
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    </script>

</body>

</html>
