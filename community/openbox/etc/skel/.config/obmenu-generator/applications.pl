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
    ]
