<?php

session_start();

function main() {
	if ($_SERVER["REQUEST_METHOD"] == "POST"
			&& $_SERVER["REQUEST_URI"] == "/submit") {
		if (!isset($_SESSION["expiry"])) {
			echo "Invalid session!";
			return;
		}

		if (time() > $_SESSION["expiry"]) {
			echo "You're too slow!";
			return;
		}

		echo $_SESSION["next"]. " " . $_POST["next"] . "\n";
		if (intval($_POST["next"]) != $_SESSION["next"]) {
			echo "Wrong prediction!";
			return;
		}

		echo "FLAG " . getenv("FLAG");
	} else {
		srand(random_int(0, 4294967295));

		$t = time();
		echo strval($t) . "\n";

		echo strval(rand()) . "\n";
		for ($i = 0; $i < 300; $i++) {
			if (($i % 60) == ($t % 60)) {
				echo strval(rand()) . "\n";
			} else {
				rand();
			}
		}

		$_SESSION["next"] = rand();
		$_SESSION["expiry"] = time() + 60;

		echo "Good luck :P";
	}
}

main();

?>

