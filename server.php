<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('34.66.184.176', 5672, 'admin', 'test');
$channel = $connection->channel();

$channel->queue_declare('hello', false, false, false, false);

echo " [*] Waiting for messages. To exit press CTRL+C\n";

$callback = function ($msg) {
        
	$v = json_decode($msg->body);

	if ($v->{'type'} = "login")
	{
        $email = $v->{'email'};
        $password = $v->{'password'};
        print $email;
        print $password;
	}

	if ($v->{'type'} = "register" && isset($v->{'username'}))
	{
		$email2 = $v->{'email'};
		$username2 = $v->{'username'};
		$password2 = $v->{'password'};
		print $email2;
		print $username2;
		print $password2;

	}
        
};

$channel->basic_consume('hello', '', false, true, false, false, $callback);



while ($channel->is_open()) {
    $channel->wait();
}

$channel->close();
$connection->close();
?>
