<?php
class Flag
{
    public bool $isflag = false;
    function __construct($ping)
    {
        echo $ping;
    }
    public function get_flag()
    {
        readfile("../flag.txt");
    }
    function __destruct()
    {
        echo "good bye!";
    }
}

if (isset($_GET['a'])) {
    $user_input = unserialize($_GET['a']);
    if ($user_input->isflag == true) {
        $user_input->get_flag();
    }
} else {
    highlight_file(__FILE__);
}