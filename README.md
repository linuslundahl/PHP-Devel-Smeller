# PHP Devel Smeller for Sublime Text 2

Sublime Text 2 plugin that checks PHP files for "smelly" code such as `die;`, `var_dump();`, `print_r();` etc.

This is NOT a syntax checker, use [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) for that.
This is just a check for left behind development code that you usually don't want to commit to a production enviroment.

Installation
------------
	$ git clone git@github.com:linuslundahl/PHP-Devel-Smeller.git ~/Library/Application Support/Sublime Text 2/Packages

Setup
-----

By default the plugin uses the built in Error Message in Sublime for smelly notifications, but you can also use Notification Center for less obtrusive notifications, this requires [Terminal Notifier](https://github.com/alloy/terminal-notifier).

	$ [sudo] gem install terminal-notifier

Then add:

	{
	  "use_notification_center": 1
	}

to `[..]/Packages/User/PhpDevelSmeller.sublime-settings` to enable it.
