#!/usr/bin/perl

# obmenu-generator - schema file

=for comment

    item:      add an item inside the menu          {item => ["command", "label", "icon"]},
    cat:       add a category inside the menu       {cat => ["name", "label", "icon"]},
    sep:       horizontal line separator            {sep => undef}, {sep => "label"},
    pipe:      a pipe menu entry                    {pipe => ["command", "label", "icon"]},
    file:      include the content of an XML file   {file => "/path/to/file.xml"},
    raw:       any XML data supported by Openbox    {raw => q(xml data)},
    begin_cat: beginning of a category              {begin_cat => ["name", "icon"]},
    end_cat:   end of a category                    {end_cat => undef},
    obgenmenu: generic menu settings                {obgenmenu => ["label", "icon"]},
    exit:      default "Exit" action                {exit => ["label", "icon"]},

=cut

require "$ENV{HOME}/.config/obmenu-generator/config.pl";

## Text editor
my $editor = $CONFIG->{editor};

our $SCHEMA = [
    # Format:  NAME, LABEL, ICON
    {sep => "Manjaro Openbox"},
    {item => ['alacritty', 'Terminal', 'terminal-emulator']},
    {item => ['xdg-open http:///', 'Web Browser', 'web-browser']},
    {item => ['xdg-open ~/', 'File Manager', 'file-manager']},
    {cat => ['utility', 'Accessories', 'applications-utilities']},
    {cat => ['development', 'Development', 'applications-development']},
    {cat => ['education', 'Education', 'applications-science']},
    {cat => ['game', 'Games', 'applications-games']},
    {cat => ['graphics', 'Graphics', 'applications-graphics']},
    {cat => ['audiovideo', 'Multimedia', 'applications-multimedia']},
    {cat => ['network', 'Network', 'applications-internet']},
    {cat => ['office', 'Office', 'applications-office']},
    {cat => ['other', 'Other', 'applications-other']},
    {cat => ['settings', 'Settings', 'gnome-settings']},
    {cat => ['system', 'System', 'applications-system']},
    {sep => undef},
    {pipe => ['manjaro-places-pipemenu --recent ~/', 'Places', 'folder']},
    {sep => undef},
    {begin_cat => ['Preferences', 'theme']},
      {begin_cat => ['Look and Feel', 'theme']},
        {item => ['lxappearance', 'Gtk Theme', 'theme']},
        {item => ['kvantummanager', 'Kvantum Manager', 'kvantum']},
        {item => ['obconf', 'Openbox Configuration', 'theme']},
        {item => ['rofi-theme-selector', 'Rofi Theme', 'theme']},
        {item => ['nitrogen', 'Wallpaper', 'nitrogen']},
      {end_cat => undef},
      {begin_cat => ['Openbox Settings', 'settings']},
        {item => ['kickshaw', 'Menu Editor', 'openbox']},
        {item => ['obkey', 'Keybind/Shortcut Editor', 'openbox']},
        {item => ['ob-autostart', 'GUI Autostart Editor', 'openbox']},
        {sep => undef},
        {item => ["xdg-open ~/.config/openbox/menu.xml", 'Edit menu.xml', 'text-xml']},
        {item => ["xdg-open ~/.config/openbox/rc.xml", 'Edit rc.xml', 'text-xml']},
        {item => ["xdg-open ~/.config/openbox/autostart", 'Edit autostart', 'text-xml']},
        {sep => undef},
        {item => ['openbox --reconfigure', 'Openbox Reconfigure', 'openbox']},
      {end_cat => undef},
      {pipe => ['manjaro-polybar-pipemenu', 'Polybar', 'gnome-settings']},
      {pipe => ['manjaro-conky-pipemenu', 'Conky', 'gnome-settings']},
      {pipe => ['manjaro-tint2-pipemenu', 'Tint2', 'gnome-settings']},
      {pipe => ['manjaro-compositor', 'Compositor', 'gnome-settings']},
    {end_cat => undef},
    {sep => undef},
    {begin_cat => ['Root menu', 'menu-editor']},
      {item => ['switchmenu --static', 'Switch Menu', 'menu-editor']},
      {item => ["$editor ~/.config/obmenu-generator/schema.pl", 'Menu Layout', 'text-x-source']},
      {item => ['obmenu-generator -p', 'Generate a pipe menu', 'menu-editor']},
      {item => ['obmenu-generator -s -c', 'Generate a static menu', 'menu-editor']},
    {end_cat => undef},
    {sep => undef},
    {item => ['lockscreen -- scrot', 'Lock Screen', 'lock']},
    {item => ['rofr.sh -l', 'Exit Openbox', 'exit']},
]
