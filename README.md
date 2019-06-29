# mysql-shoretel-query-alert-if-phone-changes
Alert if a phone monitored by call recording system changes by querying shoretel mysql db and comparing against known good extensions and mac addresses.

Example: My voice / call recording server requires a static ip / mac address in order to monitor and record phone conversations for target extensions (versadial / adutante). Just ask cron to run this python occasionally to audit and alert if one of the phones gets swapped out so the call recording server can be looked at. Ideally, the call recording software would be smarter than this...but it's not.

Why do this?: We are required by a governing body to record all phone conversations.
