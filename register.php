<?php require_once(__DIR__ . "/partials/nav.php"); 
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('34.66.184.176', 5672, 'admin', 'test');
$channel = $connection->channel();
$channel->queue_declare('hello', false, false, false, false);
$password = $_POST["password"];
$email = $_POST["email"];
$username = $_POST["username"];
$type = "register";
$credential = array("email"=>$email,"password"=> $password, "username"=>$username,"type"=>$type);
$msg = new AMQPMessage(json_encode($credential));
$channel->basic_publish($msg, '', 'hello');
/*
if (isset($_POST["register"])) {
    $email = null;
    $password = null;
    $confirm = null;
    $username = null;
 
    if (isset($_POST["email"])) {
        $email = $_POST["email"];
    }
    if (isset($_POST["password"])) {
        $password = $_POST["password"];
    }
    if (isset($_POST["confirm"])) {
        $confirm = $_POST["confirm"];
    }
    if (isset($_POST["username"])) {
        $username = $_POST["username"];
    }
    $isValid = true;
    //check if passwords match on the server side
    if ($password == $confirm) {
        flash("Passwords match <br>");
    }
    else {
        flash("Passwords don't match<br>");
        $isValid = false;
    }
    if (!isset($email) || !isset($password) || !isset($confirm)) {
        $isValid = false;
    }

    //TODO other validation as desired, remember this is the last line of defense
    if ($isValid) {
        $hash = password_hash($password, PASSWORD_BCRYPT);

        $db = getDB();
        if (isset($db)) {
            //here we'll use placeholders to let PDO map and sanitize our data
            $stmt = $db->prepare("INSERT INTO Users(email, username, password) VALUES(:email,:username, :password)");
            //here's the data map for the parameter to data
            $params = array(":email" => $email, ":username" => $username, ":password" => $hash);
            $r = $stmt->execute($params);
            //let's just see what's returned
            //echo "db returned: " . var_export($r, true);
            $e = $stmt->errorInfo();
            if ($e[0] == "00000") {
                flash("<br>Welcome! You successfully registered, please login.");
            }
            else {
                if ($e[0] == "23000") {//code for duplicate entry
                    flash("<br>Either username or email is already registered, please try again");
                }
                else {
                    flash("uh oh something went wrong: "); // . var_export($e, true);
                }
            }
        }
    }
    else {
        flash("There was a validation issue");
    }
}
//safety measure to prevent php warnings
if (!isset($email)) {
    $email = "";
}
if (!isset($username)) {
    $username = "";
}
 */
?>
<form method="POST">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required value="<?php safer_echo($email); ?>"/>
    <label for="user">Username:</label>
    <input type="text" id="user" name="username" required maxlength="60" value="<?php safer_echo($username); ?>"/>
    <label for="p1">Password:</label>
    <input type="password" id="p1" name="password" required/>
    <label for="p2">Confirm Password:</label>
    <input type="password" id="p2" name="confirm" required/>
    <input type="submit" name="register" value="Register"/>
</form>

