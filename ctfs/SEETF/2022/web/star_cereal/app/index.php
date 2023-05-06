<?php error_reporting(0); ?>

<!--
Star Cereal page by zeyu2001

TODO:
	1) URGENT - fix login vulnerability by disallowing external logins (done)
	2) Make sure the hackers don't get the flag muahahahaha
-->

<!DOCTYPE html>
<html lang="en">
	<?php include "includes/head.php" ?>
	<body>
		<?php include "includes/nav.php" ?>
		<main>
			<div class="jumbotron landing-head bg-primary text-white">
				<h1 class="display-4 landing-title" align="center">Star Cereal</h1>
				<p class="lead" align="center">The most nutritious cereal to start an astronaut's day.</p>
				<div class="landing-img"></div>
			</div>
			<div class="container">
				<section id="about" class="section">
					<h2 align="center" data-aos="zoom-in-up">About Us</h2>
					<p class="pt-4" data-aos="zoom-in-up"> 
						Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
						Id aliquet lectus proin nibh nisl condimentum id venenatis. Faucibus in ornare quam viverra orci. Ut tellus elementum sagittis vitae et leo duis ut diam. 
						Vitae purus faucibus ornare suspendisse sed. Massa id neque aliquam vestibulum morbi blandit. Rhoncus urna neque viverra justo nec ultrices. 
						Nullam eget felis eget nunc lobortis mattis aliquam faucibus. Cursus metus aliquam eleifend mi in. Felis bibendum ut tristique et egestas quis. Feugiat nisl pretium fusce id velit.
					</p>
					<p class="pt-4" data-aos="zoom-in-up">
						Nunc aliquet bibendum enim facilisis. Sed ullamcorper morbi tincidunt ornare massa eget egestas purus viverra. 
						Euismod lacinia at quis risus sed vulputate. Eu consequat ac felis donec et. Orci eu lobortis elementum nibh tellus molestie nunc. 
						Quisque sagittis purus sit amet. Eu mi bibendum neque egestas congue quisque egestas. Adipiscing elit ut aliquam purus sit amet luctus. 
						Id donec ultrices tincidunt arcu non. Laoreet id donec ultrices tincidunt arcu non. Diam in arcu cursus euismod quis. 
						Augue neque gravida in fermentum. Consequat interdum varius sit amet mattis vulputate enim. Enim tortor at auctor urna nunc id. 
						Risus in hendrerit gravida rutrum quisque non tellus orci ac. Leo in vitae turpis massa sed elementum. Volutpat consequat mauris nunc congue. 
						Adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus.
					</p>
				</section>
				<section id="contact" class="section">
					<h2 align="center" data-aos="zoom-in-up">Contact Us</h2>
					<form action="/" method="post" data-aos="zoom-in-up">
						<div class="form-group">
							<label for="email">Email address</label>
						  	<input type="email" class="form-control" id="email" name="email" aria-describedby="emailHelp" placeholder="Enter email">
						    	<small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
					  	</div>
					  	<div class="form-group">
						    	<label for="query">Your Query</label>
						    	<textarea class="form-control" id="query" name="query" rows="3"></textarea>
					  	</div>
					  	<button type="submit" class="btn btn-primary">Submit</button>
					</form>
				</section>
			</div>
		</main>
	</body>
</html>
