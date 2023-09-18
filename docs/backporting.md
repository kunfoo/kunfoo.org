# Backporting Fails
Many major Linux distributions (like Red Hat Enterprise Linux, Ubuntu, Debian)
freeze the packaged software versions, when a new major release of the
distribution is created. For example Debian 10 packages the popular Apache
webserver in version 2.4.38, while the current release (31.03.2020) is version
2.4.41. Bugfixes, and therefore also security fixes, must be backported to the
packaged version of the Apache webserver (and all the other packaged software in
the distribution). However, feature updates in newer software versions are not
backported. This is done to guarantee a stable system with minimal changes.

TODO: elaborate more on the issue
* f.e. xscreensaver vs. debian
* security fixes only when CVE issued
  * other bugfixes might have security impact as well

On this site, I will try to collect examplary issues, when backporting failed.

## References
- [Linux kernel: CVE-2017-18344: arbitrary-read vulnerability in the timer subsystem](https://seclists.org/oss-sec/2018/q3/76)
- [Debian - Vulnerable source packages in the stable suite](https://security-tracker.debian.org/tracker/status/release/stable)
