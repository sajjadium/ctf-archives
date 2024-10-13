<template>
  <div class="landing-page">
    <header class="header">
      <nav class="navbar">
        <div class="logo">Cooking School</div>
        <ul class="nav-links">
          <li><a href="#">Home</a></li>
          <li><a href="#">Courses</a></li>
          <li><a href="#">About Us</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
    </header>

    <section class="hero-section">
      <div class="hero-content">
        <h1>Welcome to Cooking School</h1>
        <p>Learn the art of cooking from our experienced chefs!</p>
        <a href="#" class="cta-button">Explore Courses</a>
      </div>
    </section>

    <section class="about-section">
      <div class="about-content">
        <h2>About Us</h2>
        <p>We are passionate about teaching the art of cooking to aspiring chefs...</p>
        <a href="#" class="cta-button">Learn More</a>
      </div>
    </section>

    <footer class="footer">
      <p>&copy; 2023 Cooking School. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
/* Add your CSS styles here */
.landing-page {
  font-family: Arial, sans-serif;
}

.header {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
}

.nav-links li a {
  text-decoration: none;
  color: #333;
  transition: color 0.3s;
}

.nav-links li a:hover {
  color: #f1592a;
}

.hero-section {
  background-image: url('/hero-bg.jpg');
  background-size: cover;
  color: #fff;
  padding: 100px 0;
  text-align: center;
}

.hero-content h1 {
  font-size: 36px;
  margin-bottom: 20px;
}

.cta-button {
  display: inline-block;
  background-color: #f1592a;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.cta-button:hover {
  background-color: #d93b0a;
}

.about-section {
  background-color: #f9f9f9;
  padding: 80px 0;
  text-align: center;
}

.about-content h2 {
  font-size: 28px;
  margin-bottom: 20px;
}

.footer {
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 20px 0;
}
</style>
