# snapd-wait

`snapd-wait` is a small Python3 script that waits for snap autorefresh to complete.
It's primarily intended to be run on boot and is particularly useful when provisioning your system.

For example, if you use a Terraform/Packer provisioner that calls a program installed via snap, 
you'll get miscellaneous failures
saying that program doesn't exist (because snapd is updating it).

## Usage

## What it does
* Delays the next refresh by 6 hours (snapd autorefreshes 4 times a day by default)
* Waits for all changes to finish by calling `snap changes`, essentially using
[this method](https://serverfault.com/a/969379), until every change is marked as `Done`.

## References
* [https://serverfault.com/questions/967674/how-to-wait-for-snapd-auto-refresh-to-complete](https://serverfault.com/questions/967674/how-to-wait-for-snapd-auto-refresh-to-complete)
* [https://popey.com/blog/2021/05/disabling-snap-autorefresh/](https://popey.com/blog/2021/05/disabling-snap-autorefresh/)
