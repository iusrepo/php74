#!/usr/bin/env php
<?php
if ($_SERVER['argc'] < 2) {
	die("Usage {$_SERVER['argv'][0]} /path/to/NEWS\n");
}

$text = file_get_contents($_SERVER['argv'][1]);
if (!$text) {
	die("Can't read {$_SERVER['argv'][1]}\n");
}
$debug = (isset($_SERVER['argv'][2]) && $_SERVER['argv'][2]==-'d');

$text = explode("\n", $text);
$in=false;
foreach ($text as $line) {
	if (preg_match('/(^[0-9]+ .* 20[0-9][0-9])[,]* PHP (.*)$/', $line, $reg)) {
		if ($in) {
			break;
		}
		printf("**PHP version %s** (%s)", $reg[2], $reg[1]);
		$in = true;
		continue;
	} else if (!$in) {
		if ($debug) echo "+ Ignore $line\n";
		continue;
	}
	$line = preg_replace('/(#[0-9])+/', 'php\1', $line);
	if (empty($line)) {
		echo "\n\n";
	} else if (substr($line, 0, 2) == '- ') {
		echo "**" . substr($line, 2) . "**\n";
	} else if (substr($line, 0, 4) == '  . ') {
		echo "\n* " . substr($line, 4);
	} else {
		echo " ".trim($line);
	}
}

