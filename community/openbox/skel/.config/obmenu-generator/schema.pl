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
    {item => ['exo-open --launch TerminalEmulator', 'Terminal', 'terminal']},
    {item => ['exo-open --launch WebBrowser ', 'Web Browser', 'firefox']},
    {item => ['exo-open --launch FileManager', 'File Manager', 'file-manager']},
    {sep => undef},
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
      {begin_cat => ['Openbox', 'openbox']},
        {item => ['lxappearance', 'Settings Editor', 'theme']},
        {item => ['kickshaw', 'Menu Editor', 'openbox']},
        {item => ['obkey', 'Keybind Editor', 'openbox']},
        {item => ['ob-autostart', 'Autostart Editor', 'openbox']},
        {sep => undef},
        {item => ["exo-open ~/.config/openbox/menu.xml", 'Edit menu.xml', 'text-xml']},
        {item => ["exo-open ~/.config/openbox/rc.xml", 'Edit rc.xml', 'text-xml']},
        {item => ["exo-open ~/.config/openbox/autostart", 'Edit autostart', 'text-xml']},
        {sep => undef},
        {item => ['openbox --restart', 'Openbox Restart', 'openbox']},
        {item => ['openbox --reconfigure', 'Openbox Reconfigure', 'openbox']},
      {end_cat => undef},
      {item => ['nitrogen', 'Change Wallpaper', 'nitrogen']},
      {sep => undef},
      {pipe => ['manjaro-compositor', 'Compositor', 'compton']},
      {pipe => ['manjaro-polybar-pipemenu', 'Polybar', 'polybar']},
      {pipe => ['manjaro-conky-pipemenu', 'Conky', 'conky']},
      {pipe => ['manjaro-tint2-pipemenu', 'Tint2', 'tint2']},
      {item => ['rofi-theme-selector', 'Rofi Theme', 'theme']},
      {item => ['manjaro-panel-chooser', 'Panel Chooser', 'panel']},
      {sep => undef},
          {item => ['pavucontrol', 'Pulseaudio Preferences', 'multimedia-volume-control']},
      {item => ['exo-preferred-applications', 'Preferred Applications', 'preferred-applications']},
      {item => ['arandr', 'Screen Layout Editor', 'display']},
    {end_cat => undef},
    {sep => undef},
    {begin_cat => ['Menu Generator', 'menu-editor']},
      {item => ["$editor ~/.config/obmenu-generator/schema.pl", 'Menu Layout', 'text-x-source']},
      {sep  => undef},
      {item => ['obmenu-generator -p', 'Generate a pipe menu', 'menu-editor']},
      {item => ['obmenu-generator -s -c', 'Generate a static menu', 'menu-editor']},
    {end_cat => undef},
    {item => ["switchmenu --static", 'Switch Menu', 'menu-editor']},
    {pipe => ['manjaro-kb-pipemenu', 'Display Keybinds', 'cs-keyboard']},
    {pipe => ['manjaro-help-pipemenu', 'Help and Info', 'info']},
    {sep => undef},
    {item => ['lockscreen -- scrot', 'Lock Screen', 'lock']},
    {item => ['rofr.sh -l', 'Exit Openbox', 'exit']},
    ]
