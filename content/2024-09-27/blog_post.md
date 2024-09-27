Title: Zoom Screen Sharing with Sway (Wayland, NixOS)
Category: Blog
Date: 2024-09-27
Tags: Komputer
Slug: 
Lang: en

I finally got Zoom screen sharing working on Wayland. Since [many people have problems with Zoom screen sharing on
Wayland](https://community.zoom.com/t5/Zoom-Meetings/share-screen-linux-wayland-broken/td-p/184192), here are a few
hints on what did the trick for me.

First, you need to install `xdg-desktop-portal-wlr`[1], which is an `xdg-desktop-portal` backend for wlroots[2].
Basically, you need this because Sway is based on wlroots and `xdg-desktop-portal-wlr` provides a ScreenCast interface to Zoom.
```
$ cat /nix/store/4z1a0hp99c6yga19jb46g50khnhrm0ql-xdg-desktop-portal-wlr-0.7.1/share/xdg-desktop-portal/portals/wlr.portal
[portal]
DBusName=org.freedesktop.impl.portal.desktop.wlr
Interfaces=org.freedesktop.impl.portal.Screenshot;org.freedesktop.impl.portal.ScreenCast;
UseIn=wlroots;sway;Wayfire;river;phosh;Hyprland;
```

Here is the relevant part of my NixOS configuration:
```
xdg.portal = {
  enable = true;
  xdgOpenUsePortal = true;
  wlr.enable = true;
  config = {
    common = {
      default = [ "wlr" ];
    };
    sway = {
      default = [ "wlr" ];
    };
  };
};
```

The `config` part creates the two files `/etc/xdg/xdg-desktop-portal/portals.conf` and
`/etc/xdg/xdg-desktop-portal/sway-portals.conf` with the following identical content:  
```
[preferred]
default=wlr
```

Now, you also get two systemd services, `xdg-desktop-portal.service` and `xdg-desktop-portal-wlr.service`. However,
the `xdg-desktop-portal-wlr.service` unit failed to start with the error `Portal service (wlroots implementation) was
skipped because of an unmet condition check (ConditionEnvironment=WAYLAND_DISPLAY).`. There is a race condition that
starts the unit before the `WAYLAND_DISPLAY` variable is set and Sway hangs when I start it from the TTY via `exec
sway`. I fixed this by adding the following lines to my `~/.config/sway/config`:  
```
exec systemctl --user import-environment WAYLAND_DISPLAY
exec systemctl --user restart xdg-desktop-portal-wlr.service
```

Hope this helps some of you to get Zoom screen sharing working with Sway.

[1] https://github.com/emersion/xdg-desktop-portal-wlr
[2] https://gitlab.freedesktop.org/wlroots/wlroots
