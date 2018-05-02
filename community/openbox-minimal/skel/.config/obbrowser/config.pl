#!/usr/bin/perl

# obbrowser - configuration file
# This file is updated automatically.
# Any additional comment and/or indentation will be lost.

=for comment

|| ICON SETTINGS
    | with_icons       : A true value will make the script to use icons for files and directories.
                         This option may be slow, depending on the configuration of your system.

    | mime_ext_only    : A true value will make the script to get the mimetype by extension only.
                         This will improve the performance, as no content will be read from files.

    | icon_size        : Preferred size for icons. (default: 32)
    | generic_fallback : Try to shorten icon name at '-' characters before looking at inherited themes. (default: 1)
    | force_icon_size  : Always get the icon scaled to the requested size. (default: 0)

|| MENU
    | file_manager     : Command to your file manager for opening files and directories.
    | browse_label     : Label for "Browse here..." action.
    | start_path       : An absolute path from which to start to browse the filesystem.
    | dirs_first       : A true value will make the script to order directories before files.

=cut

our $CONFIG = {
  browse_label     => "Open here...",
  dirs_first       => 1,
  file_manager     => "exo-open --launch FileManager",
  force_icon_size  => 0,
  generic_fallback => 1,
  icon_size        => 32,
  mime_ext_only    => 0,
  start_path       => "$ENV{HOME}",
  VERSION          => 0.08,
  with_icons       => 1,
}
