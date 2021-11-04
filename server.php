<?php

require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('34.66.184.176', 5672, 'admin', 'test');
$channel = $connection->channel();

$channel->queue_declare('hello', false, false, false, false);

echo " [*] Waiting for messages. To exit press CTRL+C\n";

$callback = function ($msg) {
        echo ' [x] Received ', $msg->body, "\n";
        $v = json_decode($msg->body);
        if ($v->{'type'} = "login"){
        $email = $v->{'email'};
        $password = $v->{'password'};
        echo $email;
        echo $password;
	}

	if *$v->{'type'} = "register"){
		$email2 = $v->{'email'};
		$username2 = $v->{'username'};
		$password2 = $v->{'password'};
		echo $email2;
		echo $username2;
		echo $password2;

	}
        
};

$channel->basic_consume('hello', '', false, true, false, false, $callback);



while ($channel->is_open()) {
    $channel->wait();
}

$channel->close();
$connection->close();
?>
